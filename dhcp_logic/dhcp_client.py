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
