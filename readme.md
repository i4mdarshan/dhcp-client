## DHCP Client Project Plan

This plan outlines the tasks required to build a functional DHCP client with a user-friendly interface.

### Phase 1: Core DHCP Logic (Backend)

The goal of this phase is to handle the fundamental DHCP protocol interactions.

- [x] **Task 1.1: Project Setup**
  - Create a new project directory.
  - Set up a Python virtual environment.
  - Install necessary libraries (e.g., `flask` for the future UI).
- [x] **Task 1.2: DHCP Message Structure (RFC 2131)**
  - Define a Python class or data structure to represent a DHCP message.
  - Include fields for `Op`, `Htype`, `Hlen`, `Xid` (Transaction ID), `CIAddr`, `YIAddr`, `SIAddr`, `GIAddr`, `CHAddr` (MAC Address), and `Options`.
- [x] **Task 1.3: DHCP Message Serialization**
  - Create a function that takes a DHCP message object (from Task 1.2) and converts it into a `bytes` object formatted for UDP transmission.
  - Pay close attention to data types, byte order (network byte order - big-endian), and field sizes.
- [x] **Task 1.4: DHCP Message Deserialization**
  - Create a function that takes a `bytes` object (received from a DHCP server) and parses it into a DHCP message object.
  - This is the reverse of serialization.
- [x] **Task 1.5: UDP Socket Communication**
  - Write the code to create a UDP socket.
  - Configure the socket to send broadcast messages (`SO_BROADCAST`).
  - Bind the socket to listen for responses on the correct port (client port 68).

- [ ] **Task 1.6: Implement the D-O-R-A Flow**
  - **Discover:** Construct and serialize a `DHCPDISCOVER` message. Broadcast it using the UDP socket.
  - **Offer:** Listen for an incoming `DHCPOFFER` message from a server. Deserialize and validate it.
  - **Request:** Construct and serialize a `DHCPREQUEST` message using information from the offer. Broadcast it.
  - **Acknowledge:** Listen for a `DHCPACK` message to confirm the IP address lease.

### Phase 2: User Interface (Frontend)

The goal of this phase is to build an interface to control the client and display results.

- [ ] **Task 2.1: Basic Web Server**
- [ ] **Task 2.2: UI Controls and Display**
- [ ] **Task 2.3: API Endpoints**

### Phase 3: Integration and Refinement

- [ ] **Task 3.1: Real-time Updates**
- [ ] **Task 3.2: Handling Other Message Types**
- [ ] **Task 3.3: Error Handling & Edge Case**
