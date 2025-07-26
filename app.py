from flask import Flask, render_template, jsonify, request
from dhcp_logic.dhcp_client import DHCPClient
import netifaces

app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

