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
                background: linear-gradient(135deg, #141414, #1e1e1e);
                margin: 0;
                padding: 20px;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                color: #fff;
            }
            .box {
                width: 400px;
                background: #222;
                border-radius: 12px;
                padding: 25px;
                box-shadow: 0 0 25px rgba(255, 255, 255, 0.05);
            }
            h2 {
                text-align: center;
                color: #f2f2f2;
                margin-bottom: 20px;
            }
            input, select, button {
                width: 100%;
                padding: 12px;
                margin: 10px 0;
                border-radius: 6px;
                border: none;
                font-size: 15px;
            }
            input, select {
                background: #333;
                color: #e6e6e6;
                border: 1px solid #474747;
            }
            button {
                background: #007bff;
                color: #fff;
                cursor: pointer;
                font-weight: bold;
                transition: 0.3s;
            }
            button:hover {
                background: #0056b3;
            }
            .output {
                margin-top: 15px;
                background: #1f1f1f;
                padding: 14px;
                border-radius: 6px;
                display: none;
                font-size: 14px;
                border: 1px solid #555;
                color: #ddd;
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

            <select id="year">
                <option value="">Select Year Level</option>
                <option value="1st Year">1st Year</option>
                <option value="2nd Year">2nd Year</option>
                <option value="3rd Year">3rd Year</option>
                <option value="4th Year">4th Year</option>
            </select>

            <input id="section" type="text" placeholder="Section (e.g., SE, CS)">

            <button onclick="getStudent()">GET Student</button>
            <button onclick="postStudent()">POST Student</button>

            <div class="output" id="responseBox"></div>
        </div>

        <script>
            function getStudent() {
                const name = document.getElementById("name").value;
                const year = document.getElementById("year").value;
                const section = document.getElementById("section").value;

                fetch(`/student?name=${name}&year=${year}&section=${section}`)
                    .then(res => res.json())
                    .then(data => show(data));
            }

            function postStudent() {
                const body = {
                    name: document.getElementById("name").value,
                    year: document.getElementById("year").value,
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
        "message": "Student Management API is running successfully",
        "status": "online"
    })


@app.route('/student', methods=['GET'])
def get_student():
    name = request.args.get('name', 'Unknown Student')
    year = request.args.get('year', 'Not Provided')
    section = request.args.get('section', 'Unassigned')

    return jsonify({
        "student": {
            "name": name,
            "year level": year,
            "section": section
        }
    })


@app.route('/student', methods=['POST'])
def add_student():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    required = ["name", "year", "section"]
    if not all(field in data and data[field] for field in required):
        return jsonify({"error": "Missing required fields (name, year, section)"}), 400

    return jsonify({
        "message": "Student added successfully",
        "student": {
            "name": data["name"],
            "year level": data["year"],
            "section": data["section"]
        }
    }), 201


if __name__ == "__main__":
    app.run(debug=True)
