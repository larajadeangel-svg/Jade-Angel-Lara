from flask import Flask, Response

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
                align-items: center;
            }

            .sidebar h2 {
                font-size: 22px;
                text-align: center;
                margin-bottom: 30px;
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
        </div>

        <div class="main">
            <h2>Register Students</h2>

            <button id="addStudentBtn" onclick="toggleForm()">Add Student</button>

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
                <select id="section">
                    <option value="">Select Course</option>
                    <option value="BSIT">BSIT</option>
                    <option value="BSED">BSED</option>
                    <option value="BEED">BEED</option>
                    <option value="BSOA">BSOA</option>
                    <option value="BSHM">BSHM</option>
                    <option value="BSA">BSA</option>
                </select>
                
                <button id="submitBtn" onclick="saveStudent()">Save Student</button>
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
            let students = JSON.parse(localStorage.getItem("students")) || [];
            let editingIndex = -1;

            function toggleForm() {
                const form = document.getElementById("studentForm");
                form.style.display = (form.style.display === "block") ? "none" : "block";
                editingIndex = -1;
                document.getElementById("submitBtn").innerText = "Add Student";
                document.getElementById("name").value = "";
                document.getElementById("year").value = "";
                document.getElementById("section").value = "";
            }

            function saveStudent() {
                const name = document.getElementById("name").value.trim();
                const year = document.getElementById("year").value;
                const section = document.getElementById("section").value;

                if (!name || !year || !section) {
                    alert("Please fill out all fields");
                    return;
                }

                const student = { name, "year level": year, course: section };

                if (editingIndex === -1) {
                    students.push(student);
                } else {
                    students[editingIndex] = student;
                }

                localStorage.setItem("students", JSON.stringify(students));
                renderTable();
                toggleForm();
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
                const s = students[i];
                document.getElementById("name").value = s.name;
                document.getElementById("year").value = s["year level"];
                document.getElementById("section").value = s.course;
                document.getElementById("studentForm").style.display = "block";
                document.getElementById("submitBtn").innerText = "Update Student";
                editingIndex = i;
            }

            function deleteStudent(i) {
                if (confirm('Delete ' + students[i].name + '?')) {
                    students.splice(i, 1);
                    localStorage.setItem("students", JSON.stringify(students));
                    renderTable();
                }
            }

            // Render students from localStorage on page load
            window.onload = renderTable;
        </script>
    </body>
    </html>
    """
    return Response(html_content, mimetype="text/html")


if __name__ == "__main__":
    app.run(debug=True)
