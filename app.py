from flask import Flask, jsonify, request, Response

app = Flask(__name__)

# Temporary in-memory student storage
students = [
    {"id": 1, "name": "John Doe", "year": "1st Year", "course": "SE"},
    {"id": 2, "name": "Jane Smith", "year": "2nd Year", "course": "CS"}
]


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
                background: linear-gradient(135deg, #0d0d0d, #1a1a1a);
                color: #fff;
                display: flex;
                justify-content: center;
                align-items: flex-start;
                min-height: 100vh;
                padding: 40px;
            }
            .container {
                width: 90%;
                max-width: 800px;
                background: #222;
                border-radius: 12px;
                box-shadow: 0 0 25px rgba(255, 255, 255, 0.05);
                padding: 25px;
            }
            h2 {
                text-align: left;
                margin-bottom: 15px;
                color: #f2f2f2;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
                background: #1c1c1c;
                border-radius: 6px;
                overflow: hidden;
            }
            th, td {
                padding: 10px 12px;
                text-align: left;
                border-bottom: 1px solid #333;
            }
            th {
                background: #333;
                font-weight: 600;
                color: #fff;
            }
            tr:hover {
                background: #2a2a2a;
            }
            input, select, button {
                padding: 10px;
                border-radius: 6px;
                border: none;
                font-size: 14px;
                margin: 5px 0;
            }
            input, select {
                background: #333;
                color: #fff;
                width: 100%;
                border: 1px solid #555;
            }
            .actions button {
                background: #444;
                color: #fff;
                margin-right: 5px;
                padding: 6px 12px;
                border-radius: 6px;
                border: none;
                cursor: pointer;
                transition: 0.3s;
            }
            .actions button:hover {
                background: #666;
            }
            .form-section {
                margin-top: 20px;
                border-top: 1px solid #333;
                padding-top: 15px;
            }
            .form-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
            }
            .buttons {
                margin-top: 10px;
                display: flex;
                gap: 10px;
            }
            .save-btn {
                background: #007bff;
            }
            .save-btn:hover {
                background: #0056b3;
            }
            .clear-btn {
                background: #555;
            }
            .clear-btn:hover {
                background: #777;
            }
            .search-area {
                display: flex;
                gap: 10px;
                margin-bottom: 10px;
            }
            .search-area input {
                flex: 1;
            }
            .search-btn, .refresh-btn {
                background: #007bff;
                color: #fff;
                padding: 8px 14px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                transition: 0.3s;
            }
            .refresh-btn {
                background: #555;
            }
            .search-btn:hover {
                background: #0056b3;
            }
            .refresh-btn:hover {
                background: #777;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Students</h2>
            <div class="search-area">
                <input type="text" id="search" placeholder="Search name...">
                <button class="search-btn" onclick="searchStudent()">Search</button>
                <button class="refresh-btn" onclick="loadStudents()">Refresh</button>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Year</th>
                        <th>Course</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody id="studentTable"></tbody>
            </table>

            <div class="form-section">
                <h3>Add / Edit Student</h3>
                <input type="hidden" id="studentId">
                <input type="text" id="name" placeholder="Full name">
                <div class="form-grid">
                    <select id="year">
                        <option value="">Select Year</option>
                        <option value="1st Year">1st Year</option>
                        <option value="2nd Year">2nd Year</option>
                        <option value="3rd Year">3rd Year</option>
                        <option value="4th Year">4th Year</option>
                    </select>
                    <input type="text" id="course" placeholder="Course (e.g., SE, CS, IT)">
                </div>
                <div class="buttons">
                    <button class="save-btn" onclick="saveStudent()">Save</button>
                    <button class="clear-btn" onclick="clearForm()">Clear</button>
                </div>
            </div>
        </div>

        <script>
            let editId = null;

            function loadStudents() {
                fetch('/students')
                    .then(res => res.json())
                    .then(data => {
                        const table = document.getElementById('studentTable');
                        table.innerHTML = '';
                        data.forEach(stu => {
                            table.innerHTML += `
                                <tr>
                                    <td>${stu.id}</td>
                                    <td>${stu.name}</td>
                                    <td>${stu.year}</td>
                                    <td>${stu.course}</td>
                                    <td class='actions'>
                                        <button onclick='editStudent(${stu.id})'>Edit</button>
                                        <button onclick='deleteStudent(${stu.id})'>Delete</button>
                                    </td>
                                </tr>
                            `;
                        });
                    });
            }

            function searchStudent() {
                const name = document.getElementById('search').value.toLowerCase();
                fetch('/students')
                    .then(res => res.json())
                    .then(data => {
                        const filtered = data.filter(s => s.name.toLowerCase().includes(name));
                        const table = document.getElementById('studentTable');
                        table.innerHTML = '';
                        filtered.forEach(stu => {
                            table.innerHTML += `
                                <tr>
                                    <td>${stu.id}</td>
                                    <td>${stu.name}</td>
                                    <td>${stu.year}</td>
                                    <td>${stu.course}</td>
                                    <td class='actions'>
                                        <button onclick='editStudent(${stu.id})'>Edit</button>
                                        <button onclick='deleteStudent(${stu.id})'>Delete</button>
                                    </td>
                                </tr>
                            `;
                        });
                    });
            }

            function saveStudent() {
                const name = document.getElementById('name').value;
                const year = document.getElementById('year').value;
                const course = document.getElementById('course').value;

                if (!name || !year || !course) {
                    alert("Please fill in all fields!");
                    return;
                }

                const method = editId ? "PUT" : "POST";
                const url = editId ? `/students/${editId}` : '/students';

                fetch(url, {
                    method: method,
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ name, year, course })
                })
                .then(res => res.json())
                .then(() => {
                    clearForm();
                    loadStudents();
                });
            }

            function editStudent(id) {
                fetch('/students')
                    .then(res => res.json())
                    .then(data => {
                        const stu = data.find(s => s.id === id);
                        if (stu) {
                            document.getElementById('studentId').value = stu.id;
                            document.getElementById('name').value = stu.name;
                            document.getElementById('year').value = stu.year;
                            document.getElementById('course').value = stu.course;
                            editId = id;
                        }
                    });
            }

            function deleteStudent(id) {
                fetch(`/students/${id}`, { method: "DELETE" })
                    .then(() => loadStudents());
            }

            function clearForm() {
                editId = null;
                document.getElementById('name').value = '';
                document.getElementById('year').value = '';
                document.getElementById('course').value = '';
            }

            window.onload = loadStudents;
        </script>
    </body>
    </html>
    """
    return Response(html_content, mimetype="text/html")


@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)


@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    if not data or not all(k in data for k in ('name', 'year', 'course')):
        return jsonify({"error": "Missing data"}), 400
    new_id = max([s["id"] for s in students], default=0) + 1
    student = {"id": new_id, **data}
    students.append(student)
    return jsonify(student), 201


@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    for s in students:
        if s["id"] == student_id:
            s.update(data)
            return jsonify(s)
    return jsonify({"error": "Student not found"}), 404


@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students
    students = [s for s in students if s["id"] != student_id]
    return jsonify({"message": "Deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)
