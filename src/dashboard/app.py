from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        "system": "Adaptive Human Risk Engine (AHRE)",
        "status": "Operational",
        "version": "1.0.0"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
