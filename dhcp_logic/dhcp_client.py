import socket
import sys
from .dhcp_message import DHCPMessage, DHCPDISCOVER,DHCPOFFER,DHCPREQUEST,DHCPACK, DHCPNAK

class DHCPClient:
    """Manages the state and network communication for a DHCP Client"""
    def __init__(self, mac_addr_str: str):
        
        self.mac_addr_str = mac_addr_str
        self.socket = None
        self.xid = None
        self.offered_ip = None
        self.server_id = None
        self.assigned_ip = None

        print("Initializing DHCP Client...")
        self._create_and_bind_socket()


    # function responsible to create and open UDP socket connection on port 68
    def _create_and_bind_socket(self):

        # close any old socket connection before creating new one
        if self.socket:
            self.close()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.settimeout(10)

        try:
            self.socket.bind(('', 68))
            print("Socket created and bound successfully to ('', 68).")
        except OSError as e:
            print(f"--- SOCKET BINDING ERROR ---")
            print(f"Error: {e}")
            print("Could not bind to port 68. This usually means another process is using it,")
            print("or you don't have sufficient privileges.")
            print("On Linux/macOS, try running the script with 'sudo'.")
            print("----------------------------")
            self.socket.close()
            self.socket = None

            # exit if no socket is found
            sys.exit(1)

    def close(self):
        if self.socket:
            self.socket.close()
            self.socket = None
            print("Socket closed.")

    # DORA functions for the client
    def send_discover(self):

        # check if socket is present
        if not self.socket: return

        discover_msg = DHCPMessage(self.mac_addr_str)
        self.xid = discover_msg.xid
        discover_msg.options[53]= DHCPDISCOVER
        """
            1 -> Subnet Mask
            3 -> Router
            6 -> DNS Server
            15 -> Domain Name
        """
        discover_msg.options[55] = [1,3,6,15] 
        packed_discover = discover_msg.pack()
        print(f"[D] Sending DHCPDISCOVER (xid: {hex(self.xid)})...")
        self.socket.sendto(packed_discover, ('<broadcast>', 67))
        return

    def receive_offer(self):

        # check if socket is present
        if not self.socket: return False
        
        print("[O] Waiting for DHCPOFFER...")
        try:
            # get packets and address from the socket
            packet, addr = self.socket.recvfrom(1024)
            offer_msg = DHCPMessage().unpack(packet)

            # validate the offer
            if offer_msg.xid == self.xid and offer_msg.options.get(53) == DHCPOFFER:

                # store offered ip and server id
                self.offered_ip = offer_msg.yiaddr
                self.server_id = offer_msg.options.get(54)

                print(f"[O] Received DHCPOFFER from {addr[0]} ({self.server_id})")
                print(f"    Offered IP: {self.offered_ip}")
                return True
            else:
                print("[!] Received non-matching packet. Ignoring.")
                return False

        except socket.timeout:
            print("[!] Socket timedout waiting for DHCPOFFER.")
            return False

        return True

    def send_request(self):
        
        # check if the socket is available and an ip is offered
        if not self.socket or not self.offered_ip: return

        # build dhcp msg
        request_msg = DHCPMessage(self.mac_addr_str)
        request_msg.xid = self.xid
        request_msg.options[53] = DHCPREQUEST
        request_msg.options[50] = self.offered_ip
        request_msg.options[54] = self.server_id

        packed_request = request_msg.pack()


        print(f"\n[R] Sending DHCPREQUEST for {self.offered_ip}...")
        # broadcast the dhcp message on port 67
        self.socket.sendto(packed_request, ('<broadcast>', 67)) 

    def receive_acknowledgement(self):
        
        if not self.socket: return False

        print("[A] Waiting for DHCPACK/DHCPNAK...")

        try:

            packet, addr = self.socket.recvfrom(1024)
            ack_msg = DHCPMessage.unpack(packet)

            if ack_msg.xid == self.xid:
                
                msg_type = ack_msg.options.get(53)
                if msg_type == DHCPACK:
                    self.assigned_ip = ack_msg.yiaddr
                    print(f"[A] Received DHCPACK from {addr[0]}")
                    print(f"    IP Address {self.assigned_ip} is now leased.")
                    return True
                elif msg_type == DHCPNAK:
                    print(f"[!] Received DHCPNAK from {addr[0]}. Offer declined.")
                    return False
            else:
                print("[!] Received non-matching packet. Ignoring.")
                return False

        except socket.timeout:
            print("[!] Socket timed out waiting for DHCPACK/NAK.")
            return False

    # IP orchestrator
    def request_ip_address(self):
        """ Execute the full D-O-R-A sequence. """
        if not self.socket: return None

        self.send_discover()
        if self.receive_offer():
            self.send_request()
            if self.receive_acknowledgement():
                print(f"--- IP Acquisition Successful ---")
                print(f"    Assigned IP: {self.assigned_ip}")
                self.close()
                return self.assigned_ip
            
        print("--- IP Acquisition Failed ---")
        self.close()
        return None
