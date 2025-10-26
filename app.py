from flask import Flask, jsonify, request, Response

app = Flask(__name__)

@app.route('/')
def index():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>Student Management System</title>
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: #111;
            padding: 20px;
            display: flex;
            justify-content: center;
            min-height: 100vh;
            color: #fff;
        }
        .box {
            width: 420px;
            background: #222;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 0 18px rgba(255,255,255,0.05);
        }
        h2 {
            text-align: center;
            color: #e0e0e0;
            margin-bottom: 20px;
        }
        input, button {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border-radius: 6px;
            border: none;
            font-size: 15px;
        }
        input {
            background: #333;
            color: #eee;
            border: 1px solid #444;
        }
        button {
            background: #444;
            color: #fff;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover {
            background: #555;
        }
        .output {
            margin-top: 12px;
            background: #333;
            padding: 12px;
            border-radius: 6px;
            display: none;
            font-size: 14px;
            border: 1px solid #555;
            color: #e0e0e0;
        }
        pre {
            margin: 0;
            white-space: pre-wrap;
        }
    </style>
    </head>
    <body>

    <div class="box">
        <h2>Student Management System</h2>

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
    """
    return Response(html_content, mimetype="text/html")


@app.route('/status')
def status():
    return jsonify({
        "message": "Welcome to my Flask API!",
        "status": "online"
    })


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


@app.route('/student', methods=['POST'])
def add_student():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    required = ["name", "grade", "section"]
    if not all(field in data for field in required):
        return jsonify({"error": "Missing required fields"}), 400

    return jsonify({
        "message": "Student created successfully",
        "student": data
    }), 201


if __name__ == "__main__":
    app.run(debug=True)
