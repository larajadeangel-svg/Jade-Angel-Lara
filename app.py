from flask import Flask, jsonify, request

app = Flask(__name__)

# Root Endpoint
@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to my Flask API!",
        "status": "running"
    })

# GET Example with Query Parameters
@app.route('/student', methods=['GET'])
def get_student():
    # Optional dynamic query: /student?name=John&grade=11&section=A
    name = request.args.get('name', 'Your Name')
    grade = request.args.get('grade', 10)
    section = request.args.get('section', 'Zechariah')

    return jsonify({
        "name": name,
        "grade": grade,
        "section": section
    })

# POST Example for Adding New Student Data
@app.route('/student', methods=['POST'])
def add_student():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    required_fields = ["name", "grade", "section"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required student fields"}), 400

    return jsonify({
        "message": "Student added successfully",
        "student": data
    }), 201


if __name__ == '__main__':
    app.run(debug=True)
