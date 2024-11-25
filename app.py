from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/troubleshoot', methods=['GET'])
def troubleshoot():
    try:
        # Simulate some processing
        large_array = [i for i in range(1_000_000)]  # Adjust as necessary
        return jsonify({"message": "Troubleshooting function executed successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()