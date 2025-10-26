from flask import Flask, jsonify, request, Response
import json, os

app = Flask(__name__)

DATA_FILE = "students.json"


# --- Helper Functions ---
def load_students():
    """Load students from JSON file."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_students(students):
    """Save student list to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=4)


# --- Routes ---
@app.route('/')
def index():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Student Management Dashboard</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

            body {
                font-family: 'Poppins', sans-serif;
                background: #f5f6fa;
                margin: 0;
                display: flex;
                height: 100vh;
                overflow: hidden;
            }

            /* Sidebar */
            .sidebar {
                background: #304FFE;
                width: 250px;
                display: flex;
                flex-direction: column;
                color: white;
                padding: 30px 20px;
            }

            .sidebar h2 {
                font-size: 22px;
                text-align: center;
                margin-bottom: 30px;
            }

            .sidebar button {
                background: none;
                border: none;
                color: #dfe3ff;
                text-align: left;
                padding: 12px 15px;
                border-radius: 8px;
                cursor: pointer;
                transition: 0.3s;
                font-size: 15px;
            }

            .sidebar button:hover {
                background: rgba(255, 255, 255, 0.1);
            }

            /* Main Content */
            .main {
                flex: 1;
                display: flex;
                flex-direction: column;
                background: #fff;
                border-radius: 20px 0 0 20px;
                margin: 20px;
                padding: 25px 40px;
                box-shadow: 0 0 20px rgba(0,0,0,0.1);
                overflow-y: auto;
            }

            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .header h2 {
                color: #2c2c2c;
                font-weight: 600;
            }

            .add-btn {
                background: #304FFE;
                color: white;
                padding: 10px 18px;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                transition: 0.3s;
            }

            .add-btn:hover {
                background: #1e36c8;
            }

            /* Form Card */
            .card {
                background: #f8f9ff;
                padding: 20px;
                margin-top: 25px;
                border-radius: 12px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            }

            .form-group {
                margin-bottom: 15px;
            }

            label {
                font-weight: 500;
                display: block;
                margin-bottom: 6px;
                color: #333;
            }

            input, select {
                width: 100%;
                padding: 10px;
                border-radius: 6px;
                border: 1px solid #ccc;
                font-size: 14px;
            }

            #submitBtn {
                margin-top: 10px;
                background: #304FFE;
                color: white;
                padding: 12px 15px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 600;
                width: 100%;
                transition: 0.3s;
            }

            #submitBtn:hover {
                background: #1e36c8;
            }

            .output {
                margin-top: 20px;
                background: #eef1ff;
                padding: 15px;
                border-radius: 8px;
                display: none;
                color: #333;
            }

            /* Table */
            table {
                width: 100%;
                margin-top: 25px;
                border-collapse: collapse;
                background: #fafbff;
                border-radius: 10px;
                overflow: hidden;
            }

            th, td {
                padding: 14px 16px;
                border-bottom: 1px solid #ddd;
                text-align: left;
            }

            th {
                background: #304FFE;
                color: white;
                font-weight: 600;
            }

            tr:hover {
                background: #f2f3ff;
            }

            pre {
                white-space: pre-wrap;
                margin: 0;
            }
        </style>
    </head>
    <body>
        <div class="sidebar">
            <h2>Student Dashboard</h2>
            <button>Dashboard</button>
            <button>Students</button>
            <button>Courses</button>
            <button>Reports</button>
            <button>Settings</button>
        </div>

        <div class="main">
            <div class="header">
                <h2>Student Dashboard</h2>
                <button class="add-btn" onclick="toggleForm()">+ Add Student</button>
            </div>

            <div class="card" id="studentForm" style="display:none;">
                <div class="form-group">
                    <label>Full Name</label>
                    <input id="name" type="text" placeholder="Enter student name">
                </div>

                <div class="form-group">
                    <label>Year Level</label>
                    <select id="year">
                        <option value="">Select Year Level</option>
                        <option value="1st Year">1st Year</option>
                        <option value="2nd Year">2nd Year</option>
                        <option value="3rd Year">3rd Year</option>
                        <option value="4th Year">4th Year</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Course</label>
                    <input id="section" type="text" placeholder="e.g., SE, CS, IT">
                </div>

                <button id="submitBtn" onclick="postStudent()">Submit Student</button>
            </div>

            <table id="studentTable">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Year Level</th>
                        <th>Course</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>

            <div class="output" id="responseBox"></div>
        </div>

        <script>
            function toggleForm() {
                const form = document.getElementById("studentForm");
                form.style.display = form.style.display === "none" ? "block" : "none";
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
                .then(data => {
                    show(data);
                    if (data.student) addToTable(data.student);
                });
            }

            function show(data) {
                const output = document.getElementById("responseBox");
                output.style.display = "block";
                output.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
            }

            function addToTable(student) {
                const tableBody = document.querySelector("#studentTable tbody");
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${student.name}</td>
                    <td>${student["year level"]}</td>
                    <td>${student.course}</td>
                `;
                tableBody.appendChild(row);
            }

            function loadStudents() {
                fetch('/students')
                    .then(res => res.json())
                    .then(data => {
                        const tableBody = document.querySelector("#studentTable tbody");
                        tableBody.innerHTML = "";
                        data.students.forEach(s => addToTable(s));
                    });
            }

            loadStudents();
        </script>
    </body>
    </html>
    """
    return Response(html_content, mimetype="text/html")


@app.route('/student', methods=['POST'])
def add_student():
    students = load_students()
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    required = ["name", "year", "section"]
    if not all(field in data and data[field] for field in required):
        return jsonify({"error": "Missing required fields"}), 400

    student = {
        "name": data["name"],
        "year level": data["year"],
        "course": data["section"]
    }
    students.append(student)
    save_students(students)

    return jsonify({
        "message": "Student added successfully",
        "student": student
    }), 201


@app.route('/students', methods=['GET'])
def get_students():
    return jsonify({"students": load_students()})


if __name__ == "__main__":
    app.run(debug=True)
