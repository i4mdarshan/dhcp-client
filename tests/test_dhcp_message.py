# test_dhcp_message.py

# Import necessary components from our dhcp_logic package
from dhcp_logic.dhcp_message import DHCPMessage, DHCPDISCOVER, BOOTREQUEST

def run_test():
    """
    Tests the pack and unpack methods of the DHCPMessage class.
    """
    print("--- Starting DHCP Message Serialization/Deserialization Test ---")

    # 1. Create a sample DHCPDISCOVER message
    # Use a dummy MAC address for this test.
    mac_address = "0A:0B:0C:0D:0E:0F"
    print(f"\n[Step 1] Creating a DHCPMessage for MAC: {mac_address}")
    discover_message = DHCPMessage(mac_addr_str=mac_address)

    # Set the options for a DHCPDISCOVER message
    discover_message.options[53] = DHCPDISCOVER # Option 53: DHCP Message Type = DHCPDISCOVER
    discover_message.options[55] = [1, 3, 6, 15] # Option 55: Parameter Request List (Subnet, Router, DNS, Domain Name)
    
    print("Original Message Object (before packing):")
    print(discover_message)
    print("-" * 40)

    # 2. Serialize (pack) the message into bytes
    print("[Step 2] Packing the message into bytes using .pack()...")
    packed_bytes = discover_message.pack()
    print(f"Packed successfully. Total bytes: {len(packed_bytes)}")
    print("-" * 40)

    # 3. Deserialize (unpack) the bytes back into a message object
    print("[Step 3] Unpacking the bytes back into an object using .unpack()...")
    unpacked_message = DHCPMessage.unpack(packed_bytes)
    print("Unpacked Message Object (after unpacking):")
    print(unpacked_message)
    print("-" * 40)

    # 4. Verification
    print("[Step 4] Verifying data integrity...")
    
    # We check that the key fields are identical between the original and unpacked messages.
    # The __repr__ output you selected helps us visually confirm this.
    assert discover_message.xid == unpacked_message.xid, "Verification failed: Transaction ID mismatch!"
    assert discover_message.chaddr == unpacked_message.chaddr, "Verification failed: Client MAC address mismatch!"
    assert unpacked_message.options.get(53) == DHCPDISCOVER, "Verification failed: DHCP Message Type mismatch!"
    assert list(unpacked_message.options.get(55)) == [1, 3, 6, 15], "Verification failed: Parameter Request List mismatch!"
    
    print("\nTest successful! The original and unpacked messages match.")
    print("--- Test Finished ---")


if __name__ == "__main__":
    run_test()
"""

Run Test:

1.  Make sure you are in your `dhcp-client` directory in the terminal.
2.  Run the script with the following command:

    python test_dhcp_message.py
 

You should see output that walks through each step and ends with a "Test successful!" message. This confirms that our `DHCPMessage` class can correctly build and parse a DHCP packet according to the rules.

"""