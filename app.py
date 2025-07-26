from flask import Flask, render_template, jsonify, request
from dhcp_logic.dhcp_client import DHCPClient
import netifaces
import threading
import uuid


app = Flask(__name__)

# use redis caching on production for in-memory storage
dhcp_tasks = {}

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/get-mac-address")
def get_mac_address():

    try:
        default_gateway = netifaces.gateways()['default'][netifaces.AF_INET]
        interface_name = default_gateway[1]

        mac_address = netifaces.ifaddresses(interface_name)[netifaces.AF_LINK][0]['addr']
        return jsonify(success=True,mac_address=mac_address)
    
    except Exception as ex:
        print(f"Could not auto-detect MAC address: {ex}")
        return jsonify(success=False,error=str(ex))

def run_dhcp_process(client):
    client.request_ip_address()

@app.route('/start-dhcp', methods=['POST'])
def start_dhcp():

    data = request.get_json()
    mac_address = data.get('mac_address')
    if not mac_address:
        return jsonify(success=False, message="MAC address is required.")

    task_id = str(uuid.uuid4())
    client = DHCPClient(mac_addr_str=mac_address)
    
    # If socket binding failed, report error immediately.
    if client.state.startswith("ERROR"):
        return jsonify(success=False, message=client.state)

    dhcp_tasks[task_id] = client
    
    thread = threading.Thread(target=run_dhcp_process, args=(client,))
    thread.start()
    
    return jsonify(success=True, task_id=task_id)

# Endpoint for the frontend to poll for status updates.
@app.route('/status/<task_id>')
def status(task_id):
    client = dhcp_tasks.get(task_id)
    if not client:
        return jsonify(status="NOT_FOUND")
        
    return jsonify(
        status=client.state,
        assigned_ip=client.assigned_ip,
        server_id=client.server_id
    )

@app.route('/release-ip', methods=['POST'])
def release_ip():
    data = request.get_json()
    mac_address = data.get('mac_address')
    ip_to_release = data.get('ip_address')
    server_id = data.get('server_id')

    if not all([mac_address, ip_to_release, server_id]):
        return jsonify(success=False, message="Missing required data for release.")

    try:
        client = DHCPClient(mac_addr_str=mac_address)
        if client.socket:
            client.release_ip_address(ip_to_release, server_id)
            return jsonify(success=True, message=f"Release message sent for {ip_to_release}.")
        else:
            return jsonify(success=False, message="Could not create socket for release.")
    except Exception as ex:
        return jsonify(success=False, message=f"An error occurred during release: {ex}")
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

