from flask import Flask, render_template, jsonify, request
from dhcp_logic.dhcp_client import DHCPClient
import netifaces

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

