from dhcp_logic.dhcp_client import DHCPClient

def test_socket_creation():
    print("--- Testing Socket Creation ---")
    client = DHCPClient(mac_addr_str="AA:BB:CC:DD:EE:FF")
    if client.socket:
        print("Test successful: Socket was created and bound.")
        client.close()
    else:
        print("Test failed: Socket could not be created or bound.")
    print("--- Done ---")

def test_discover_and_offer():
    print("--- Testing Discover and Offer methods ---")
    YOUR_MAC_ADDRESS = "AA:BB:CC:DD:EE:FF"
    
    print("--- Starting DHCP Discover/Offer Test ---")
    print(f"Attempting to get an IP offer for MAC: {YOUR_MAC_ADDRESS}")
    print("NOTE: This script must be run with administrator/root privileges (e.g., `sudo`)")
    
    client = DHCPClient(mac_addr_str=YOUR_MAC_ADDRESS)
    
    # Execute only the first two steps of D-O-R-A
    client.send_discover()
    if client.receive_offer():
        print("\n --- Discover/Offer Test Successful ---")
        print(f"    Successfully received an offer for IP: {client.offered_ip}")
    else:
        print("\n --- Discover/Offer Test Failed --- ")
        print("    Could not get a valid offer from the DHCP server.")
        
    client.close()
    print("--- Done ---")

def run_tests():
    
    test_socket_creation()
    test_discover_and_offer()

    

if __name__ == "__main__":
    run_tests()

# Make sure you are running this test with sudo privilleges as the it will be required to bind port

"""

Run Test:

1.  Make sure you are in your `dhcp-client` directory in the terminal.
2.  Run the script with the following command:

    sudo python -m tests.test_dhcp_client
 

You should see output that walks through each step and ends with a "Test successful!" message. This confirms that our `DHCPClient` class can correctly create a socket connection and bind to port 68.

"""