import socket
from .dhcp_message import DHCPMessage, DHCPDISCOVER,DHCPOFFER,DHCPREQUEST,DHCPACK, DHCPNAK

class DHCPClient:
    """Manages the state and network communication for a DHCP Client"""
    def __init__(self, mac_addr_str: str):
        
        self.mac_addr_str = mac_addr_str
        self.socket = None
        self.xid = None
        self.offered_ip=None
        self.server_id=None

        print("Initializing DHCP Client...")
        self._create_and_bind_socket()


    # function responsible to create and open UDP socket connection on port 68
    def _create_and_bind_socket(self):
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
        print(f"\n[D] Sending DHCPDISCOVER (xid: {hex(self.xid)})...")
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

    def send_request():
        pass

    def receive_acknowledgement():
        pass
    # IP orchestrator
