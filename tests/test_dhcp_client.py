from dhcp_logic.dhcp_client import DHCPClient

def run_test():
    print("--- Testing Socket Creation ---")
    client = DHCPClient(mac_addr_str="AA:BB:CC:DD:EE:FF")
    if client.socket:
        print("Test successful: Socket was created and bound.")
        client.close()
    else:
        print("Test failed: Socket could not be created or bound.")

if __name__ == "__main__":
    run_test()

# Make sure you are running this test with sudo privilleges as the it will be required to bind port

"""

Run Test:

1.  Make sure you are in your `dhcp-client` directory in the terminal.
2.  Run the script with the following command:

    sudo python -m tests.test_dhcp_client
 

You should see output that walks through each step and ends with a "Test successful!" message. This confirms that our `DHCPClient` class can correctly create a socket connection and bind to port 68.

"""