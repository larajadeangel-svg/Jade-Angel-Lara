from flask import Flask, jsonify, request, Response

app = Flask(__name__)

students = [
    {"id": 1, "name": "John Doe", "grade": 10, "course": "Computer Science"},
    {"id": 2, "name": "Jane Smith", "grade": 10, "course": "Information Technology"}
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
                background-color: #f7f9fc;
                display: flex;
                justify-content: center;
                align-items: flex-start;
                padding: 40px;
                color: #333;
            }
            .container {
                width: 90%;
                max-width: 900px;
                background: #fff;
                border-radius: 10px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                padding: 20px 30px;
            }
            h2 {
                margin-bottom: 15px;
                font-size: 24px;
                color: #333;
            }
            input[type="text"], input[type="number"] {
                padding: 10px;
                border-radius: 6px;
                border: 1px solid #ccc;
                width: 100%;
                font-size: 14px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }
            th, td {
                padding: 10px;
                text-align: left;
                border-bottom: 1px solid #eee;
            }
            th {
                background: #f4f6f9;
                font-weight: 600;
            }
            button {
                border: none;
                padding: 6px 12px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 14px;
            }
            .edit {
                background-color: #007bff;
                color: white;
            }
            .delete {
                background-color: #dc3545;
                color: white;
            }
            .search-bar {
                display: flex;
                gap: 10px;
                margin-bottom: 10px;
            }
            .search-bar input {
                flex: 1;
            }
            .search-bar button {
                background-color: #007bff;
                color: #fff;
                border: none;
                border-radius: 6px;
                padding: 8px 14px;
            }
            .form-section {
                margin-top: 20px;
            }
            .form-section h3 {
                margin-bottom: 10px;
            }
            .form-group {
                display: flex;
                gap: 10px;
            }
            .form-group input {
                flex: 1;
            }
            .action-btns {
                display: flex;
                gap: 8px;
            }
            .save-btn {
                background-color: #007bff;
                color: white;
                margin-right: 5px;
            }
            .clear-btn {
                background-color: #6c757d;
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Students</h2>
            <div class="search-bar">
                <input type="text" id="search" placeholder="Search name...">
                <button onclick="searchStudent()">Search</button>
                <button onclick="loadStudents()">Refresh</button>
            </div>

            <table id="studentTable">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Grade</th>
                        <th>Course</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>

            <div class="form-section">
                <h3>Add / Edit Student</h3>
                <input type="hidden" id="studentId">
                <input type="text" id="name" placeholder="Full name">
                <div class="form-group">
                    <input type="number" id="grade" placeholder="Grade">
                    <input type="text" id="course" placeholder="Course">
                </div>
                <button class="save-btn" onclick="saveStudent()">Save</button>
                <button class="clear-btn" onclick="clearForm()">Clear</button>
            </div>
        </div>

        <script>
            async function loadStudents() {
                const res = await fetch('/students');
                const data = await res.json();
                renderTable(data);
            }

            async function searchStudent() {
                const name = document.getElementById('search').value.toLowerCase();
                const res = await fetch('/students');
                const data = await res.json();
                const filtered = data.filter(s => s.name.toLowerCase().includes(name));
                renderTable(filtered);
            }

            function renderTable(data) {
                const tbody = document.querySelector('#studentTable tbody');
                tbody.innerHTML = '';
                data.forEach(s => {
                    const row = `<tr>
                        <td>${s.id}</td>
                        <td>${s.name}</td>
                        <td>${s.grade}</td>
                        <td>${s.course}</td>
                        <td class="action-btns">
                            <button class="edit" onclick="editStudent(${s.id})">Edit</button>
                            <button class="delete" onclick="deleteStudent(${s.id})">Delete</button>
                        </td>
                    </tr>`;
                    tbody.innerHTML += row;
                });
            }

            async function saveStudent() {
                const id = document.getElementById('studentId').value;
                const name = document.getElementById('name').value;
                const grade = document.getElementById('grade').value;
                const course = document.getElementById('course').value;

                const method = id ? 'PUT' : 'POST';
                const url = id ? '/students/' + id : '/students';

                const res = await fetch(url, {
                    method,
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({name, grade, course})
                });
                await res.json();
                clearForm();
                loadStudents();
            }

            function editStudent(id) {
                fetch('/students/' + id)
                    .then(res => res.json())
                    .then(s => {
                        document.getElementById('studentId').value = s.id;
                        document.getElementById('name').value = s.name;
                        document.getElementById('grade').value = s.grade;
                        document.getElementById('course').value = s.course;
                    });
            }

            async function deleteStudent(id) {
                if (!confirm('Delete this student?')) return;
                await fetch('/students/' + id, {method: 'DELETE'});
                loadStudents();
            }

            function clearForm() {
                document.getElementById('studentId').value = '';
                document.getElementById('name').value = '';
                document.getElementById('grade').value = '';
                document.getElementById('course').value = '';
            }

            loadStudents();
        </script>
    </body>
    </html>
    """
    return Response(html_content, mimetype="text/html")


@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)


@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student)


@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    new_id = max([s["id"] for s in students], default=0) + 1
    new_student = {
        "id": new_id,
        "name": data.get("name"),
        "grade": data.get("grade"),
        "course": data.get("course")
    }
    students.append(new_student)
    return jsonify(new_student), 201


@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    for s in students:
        if s["id"] == student_id:
            s["name"] = data.get("name", s["name"])
            s["grade"] = data.get("grade", s["grade"])
            s["course"] = data.get("course", s["course"])
            return jsonify(s)
    return jsonify({"error": "Student not found"}), 404


@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students
    students = [s for s in students if s["id"] != student_id]
    return jsonify({"message": "Student deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)
