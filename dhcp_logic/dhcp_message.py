import random
import socket
import struct


# DHCP message OP codes

# Used to specify if the request is message or reply
BOOTREQUEST=1
BOOTREPLY=2

# DHCP message Type codes

DHCPDISCOVER=1
DHCPOFFER=2
DHCPREQUEST=3
DHCPDECLINE=4
DHCPACK=5
DHCPNAK=6
DHCPRELEASE=7
DHCPINFORM=8


class DHCPMessage:
    
    """This class will be used to build and parse a DHCPMessage according to RFC 2131."""

    def __init__(self, mac_addr_str: str = "00:00:00:00:00:00"):
        
        self.op = BOOTREQUEST

        self.htype = 1 # hardware address type

        self.hlen = 6 # hardware address length

        self.hops = 0 # hops used by relay agents

        self.xid = random.randint(0,0xFFFFFFFF) # Tx ID a 32 bit integer number to match requests with replies

        self.secs = 0

        self.flags = 0

        self.ciaddr = '0.0.0.0' # client IP address 

        self.yiaddr = '0.0.0.0' # own IP address

        self.siaddr = '0.0.0.0' # IP address of the next server

        self.giaddr = '0.0.0.0' # Relay agent IP address
        
        # client hardware address
        self.chaddr_str = mac_addr_str
        self.chaddr = self._mac_str_to_bytes(mac_addr_str)

        self.sname = b'\x00' * 64 # server hostname

        self.file = b'\x00' * 128 # boot file name

        self.magic_cookie = b'\x63\x82\x53\x63' # identify the start of the DHCP options field

        self.options = {} # optional params


    def _mac_str_to_bytes(self, mac_str: str) -> bytes:
        """ Converts MAC address string to bytes, padding to 16 bytes for chaddr field.  """
        mac_bytes = bytes.fromhex(mac_str.replace(':', ''))
        return mac_bytes.ljust(16, b'\x00')
    
    def _mac_bytes_to_str(self, mac_bytes: bytes) -> str:
        """Converts raw MAC address bytes (first 6 bytes of chaddr) to a string."""
        return ':'.join(f'{b:02x}' for b in mac_bytes[:6])
    
    def _pack_options(self) -> bytes:
        """ Packs the options dictionary into a bytes string. """

        packed_options = bytearray()
        if 53 in self.options: # dhcp message type
            packed_options.extend([53,1,self.options[53]])
        if 55 in self.options: # parameter request list
            params = self.options[55]
            packed_options.extend([55,len(params)])
            packed_options.extend(params)
        if 50 in self.options: # requested IP address
            packed_options.extend([50,4])
            packed_options.extend(socket.inet_aton(self.options[50]))
        if 54 in self.options:
            packed_options.extend([54,4])
            packed_options.extend(socket.inet_aton(self.options[54]))
        packed_options.append(255) # end option
        return bytes(packed_options)

    def pack(self) -> bytes:
        """ Packs the DHCPMessage Object into a bytes object for network transmission """
        packet = struct.pack('!BBBBIHH',
                             self.op, self.htype, self.hlen, self.hops,
                             self.xid, self.secs, self.flags)
        packet += socket.inet_aton(self.ciaddr)
        packet += socket.inet_aton(self.yiaddr)
        packet += socket.inet_aton(self.siaddr)
        packet += socket.inet_aton(self.giaddr)
        packet += self.chaddr
        packet += self.sname
        packet += self.file
        packet += self.magic_cookie
        packet += self._pack_options()
        return packet
    
    @staticmethod
    def _parse_options(options_bytes: str) -> dict:
        """Parses the raw options bytes into a dictionary"""
        options = {}
        i = 0
        while i < len(options_bytes):
            option_code = options_bytes[i]
            if option_code == 255: # end option
                break

            if option_code == 0:
                i += 1
                continue

            option_len = options_bytes[i+1]
            option_val_start = i + 2
            option_val_end = option_val_start + option_len
            option_value = options_bytes[option_val_start:option_val_end]
            if option_code in [50, 54]: # IP Address
                 options[option_code] = socket.inet_ntoa(option_value)
            elif option_code == 53: # DHCP Message Type
                options[option_code] = struct.unpack('!B', option_value)[0]
            else: # Other options as raw bytes
                options[option_code] = option_value
            
            i = option_val_end
        return options
    
    @staticmethod
    def unpack(packet: bytes) -> 'DHCPMessage':
        """
        Unpacks a bytes object from a network response into a DHCPMessage object.
        """
        # Unpack the fixed-size part of the packet
        fixed_part = packet[:236]
        (op, htype, hlen, hops, xid, secs, flags,
         ciaddr_raw, yiaddr_raw, siaddr_raw, giaddr_raw,
         chaddr, sname, file) = struct.unpack('!BBBBIHH4s4s4s4s16s64s128s', fixed_part)

        # Create a message object to hold the data
        msg = DHCPMessage()
        msg.op = op
        msg.htype = htype
        msg.hlen = hlen
        msg.hops = hops
        msg.xid = xid
        msg.secs = secs
        msg.flags = flags
        msg.ciaddr = socket.inet_ntoa(ciaddr_raw)
        msg.yiaddr = socket.inet_ntoa(yiaddr_raw)
        msg.siaddr = socket.inet_ntoa(siaddr_raw)
        msg.giaddr = socket.inet_ntoa(giaddr_raw)
        msg.chaddr = chaddr
        msg.chaddr_str = msg._mac_bytes_to_str(chaddr)
        msg.sname = sname
        msg.file = file

        # The rest of the packet contains the magic cookie and options
        magic_cookie_and_options = packet[236:]
        msg.magic_cookie = magic_cookie_and_options[:4]
        
        if msg.magic_cookie == b'\x63\x82\x53\x63':
            msg.options = DHCPMessage._parse_options(magic_cookie_and_options[4:])

        return msg

    def __repr__(self):
        return (f"DHCPMessage(xid={hex(self.xid)}, op={self.op}, "
                f"chaddr='{self.chaddr_str}', yiaddr='{self.yiaddr}', "
                f"options={self.options})")

        	
    
   
        
