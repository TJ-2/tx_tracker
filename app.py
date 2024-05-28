
from flask import Flask, jsonify, request
from script import *

app = Flask(__name__)


@app.route('/')
def index():
    return "Transaction Tracker API"

@app.route('/api', methods=['GET'])
def get_fuse_user_info():
    tx_hash = request.args.get('tx')
    try:
        timestamp, tx_info = fetch_tx(tx_hash)
        return jsonify({"timestamp": timestamp, "tx_info": tx_info }), 200
    except Exception as e:
        print(f"Error checking data: {str(e)}")
        return jsonify({"result": {"isValid": False}}), 200 
    

if __name__ == "__main__":
    app.run(debug=True)
    