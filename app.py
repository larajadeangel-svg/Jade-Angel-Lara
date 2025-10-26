from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# UI Route
@app.route('/')
def index():
    return render_template("index.html")

# Status Endpoint
@app.route('/status')
def status():
    return jsonify({
        "message": "Welcome to my Flask API!",
        "status": "online"
    })

# GET Student Data
@app.route('/student', methods=['GET'])
def get_student():
    name = request.args.get('name', 'Your Name')
    grade = request.args.get('grade', 10)
    section = request.args.get('section', 'Zechariah')

    return jsonify({
        "name": name,
        "grade": grade,
        "section": section
    })

# POST Student Creation
@app.route('/student', methods=['POST'])
def add_student():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    required_fields = ["name", "grade", "section"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    return jsonify({
        "message": "Student created successfully",
        "student": data
    }), 201


if __name__ == '__main__':
    app.run()
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Student API Interface</title>
<style>
    body {
        font-family: Arial, sans-serif;
        background: #eee;
        padding: 20px;
        display: flex;
        justify-content: center;
        min-height: 100vh;
    }
    .box {
        width: 420px;
        background: #fff;
        border-radius: 10px;
        padding: 25px;
        box-shadow: 0 0 12px rgba(0,0,0,0.1);
    }
    h2 {
        text-align: center;
        color: #222;
    }
    input, button {
        width: 100%;
        padding: 10px;
        margin: 8px 0;
        border-radius: 6px;
        border: 1px solid #ccc;
        font-size: 15px;
    }
    button {
        background: #007bff;
        color: #fff;
        border: none;
        cursor: pointer;
        font-weight: bold;
    }
    button:hover {
        background: #0056b3;
    }
    .output {
        margin-top: 12px;
        background: #eaf3ff;
        padding: 12px;
        border-radius: 6px;
        display: none;
        font-size: 14px;
    }
</style>
</head>
<body>

<div class="box">
    <h2>Student API</h2>

    <input id="name" type="text" placeholder="Student Name">
    <input id="grade" type="number" placeholder="Grade Level">
    <input id="section" type="text" placeholder="Section">

    <button onclick="getStudent()">GET Student</button>
    <button onclick="postStudent()">POST Student</button>

    <div class="output" id="responseBox"></div>
</div>

<script>
function getStudent() {
    const name = document.getElementById("name").value;
    const grade = document.getElementById("grade").value;
    const section = document.getElementById("section").value;

    fetch(`/student?name=${name}&grade=${grade}&section=${section}`)
        .then(res => res.json())
        .then(data => show(data));
}

function postStudent() {
    const body = {
        name: document.getElementById("name").value,
        grade: document.getElementById("grade").value,
        section: document.getElementById("section").value
    };

    fetch('/student', {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(body)
    })
        .then(res => res.json())
        .then(data => show(data));
}

function show(data) {
    const output = document.getElementById("responseBox");
    output.style.display = "block";
    output.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
}
</script>

</body>
</html>
