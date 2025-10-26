from flask import Flask, jsonify, request, Response

app = Flask(__name__)

@app.route('/')
def index():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Registered Students</title>
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
                background: #1c1c1c;
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

            .sidebar button.active {
                background: #333;
                color: white;
            }

            /* Main Content */
            .main {
                flex: 1;
                display: flex;
                flex-direction: column;
                background: #111;
                color: #fff;
                border-radius: 20px 0 0 20px;
                margin: 20px;
                padding: 25px 40px;
                box-shadow: 0 0 20px rgba(0,0,0,0.3);
                overflow-y: auto;
            }

            h2 {
                font-weight: 600;
                color: #fff;
            }

            /* Add Student Button */
            #addStudentBtn {
                background: #00bcd4;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                cursor: pointer;
                font-weight: 600;
                font-size: 14px;
                margin-top: 10px;
                width: fit-content;
                transition: 0.3s;
            }

            #addStudentBtn:hover {
                background: #0097a7;
            }

            /* Table */
            table {
                width: 100%;
                margin-top: 25px;
                border-collapse: collapse;
                background: #1e1e1e;
                border-radius: 10px;
                overflow: hidden;
            }

            th, td {
                padding: 14px 16px;
                border-bottom: 1px solid #333;
                text-align: left;
                color: #ddd;
            }

            th {
                background: #222;
                color: #00bcd4;
            }

            tr:hover {
                background: #2a2a2a;
            }

            .action-btn {
                padding: 6px 10px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                color: white;
                margin-right: 5px;
                font-size: 13px;
            }

            .edit-btn {
                background: #4CAF50;
            }

            .delete-btn {
                background: #e53935;
            }

            /* Hidden form (for adding/editing) */
            .card {
                background: #1e1e1e;
                padding: 20px;
                margin-top: 25px;
                border-radius: 12px;
                display: none;
            }

            label {
                display: block;
                margin-bottom: 5px;
                color: #ccc;
            }

            input, select {
                width: 100%;
                padding: 10px;
                margin-bottom: 10px;
                border-radius: 6px;
                border: 1px solid #444;
                background: #111;
                color: white;
            }

            #submitBtn {
                background: #00bcd4;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                cursor: pointer;
                font-weight: 600;
                width: 100%;
            }

            #submitBtn:hover {
                background: #0097a7;
            }
        </style>
    </head>
    <body>
        <div class="sidebar">
            <h2>Student Management System</h2>
            <button class="active">Students</button>
        </div>

        <div class="main">
            <h2>Registered Students</h2>

            <button id="addStudentBtn" onclick="toggleForm()">+ Add Student</button>

            <div class="card" id="studentForm">
                <label>Full Name</label>
                <input id="name" type="text" placeholder="Enter student name">

                <label>Year Level</label>
                <select id="year">
                    <option value="">Select Year Level</option>
                    <option value="1st Year">1st Year</option>
                    <option value="2nd Year">2nd Year</option>
                    <option value="3rd Year">3rd Year</option>
                    <option value="4th Year">4th Year</option>
                </select>

                <label>Course</label>
                <input id="section" type="text" placeholder="e.g., SE, CS, IT">

                <button id="submitBtn" onclick="postStudent()">Add Student</button>
            </div>

            <table id="studentTable">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Year Level</th>
                        <th>Course</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>

        <script>
            const students = [];

            function toggleForm() {
                const form = document.getElementById("studentForm");
                form.style.display = (form.style.display === "block") ? "none" : "block";
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
                    if (data.student) {
                        students.push(data.student);
                        renderTable();
                        document.getElementById("studentForm").style.display = "none";
                        document.getElementById("name").value = "";
                        document.getElementById("year").value = "";
                        document.getElementById("section").value = "";
                    }
                });
            }

            function renderTable() {
                const tbody = document.querySelector("#studentTable tbody");
                tbody.innerHTML = "";
                students.forEach((s, i) => {
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        <td>${s.name}</td>
                        <td>${s["year level"]}</td>
                        <td>${s.course}</td>
                        <td>
                            <button class="action-btn edit-btn" onclick="editStudent(${i})">Edit</button>
                            <button class="action-btn delete-btn" onclick="deleteStudent(${i})">Delete</button>
                        </td>
                    `;
                    tbody.appendChild(row);
                });
            }

            function editStudent(i) {
                alert('Edit function coming soon for: ' + students[i].name);
            }

            function deleteStudent(i) {
                if (confirm('Delete ' + students[i].name + '?')) {
                    students.splice(i, 1);
                    renderTable();
                }
            }
        </script>
    </body>
    </html>
    """
    return Response(html_content, mimetype="text/html")


@app.route('/student', methods=['POST'])
def add_student():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    required = ["name", "year", "section"]
    if not all(field in data and data[field] for field in required):
        return jsonify({"error": "Missing required fields"}), 400
    return jsonify({
        "message": "Student added successfully",
        "student": {
            "name": data["name"],
            "year level": data["year"],
            "course": data["section"]
        }
    }), 201


if __name__ == "__main__":
    app.run(debug=True)
