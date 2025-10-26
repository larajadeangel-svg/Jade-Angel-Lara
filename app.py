from flask import Flask, jsonify, request, Response

app = Flask(__name__)

# Temporary in-memory data store
students = []

@app.route('/')
def index():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Student Management Dashboard</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body {
                font-family: 'Poppins', sans-serif;
                background: #f4f6fb;
                display: flex;
                height: 100vh;
                overflow: hidden;
            }
            .sidebar {
                width: 220px;
                background: #2b47ff;
                color: #fff;
                display: flex;
                flex-direction: column;
                align-items: start;
                padding: 30px 20px;
            }
            .sidebar h2 {
                margin-bottom: 40px;
                font-size: 20px;
                font-weight: 600;
            }
            .sidebar button {
                width: 100%;
                background: #3c5bff;
                color: #fff;
                border: none;
                padding: 12px;
                border-radius: 8px;
                font-size: 15px;
                margin-bottom: 10px;
                text-align: left;
                cursor: pointer;
                transition: 0.3s;
            }
            .sidebar button:hover {
                background: #1f35d6;
            }
            .content {
                flex: 1;
                padding: 30px 50px;
                overflow-y: auto;
            }
            h1 {
                color: #333;
                margin-bottom: 20px;
            }
            .add-btn {
                background: #2b47ff;
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                border: none;
                font-weight: bold;
                cursor: pointer;
                margin-bottom: 25px;
                transition: 0.3s;
            }
            .add-btn:hover {
                background: #1f35d6;
            }
            .student-card {
                background: white;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 15px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .student-info {
                display: flex;
                flex-direction: column;
                gap: 5px;
            }
            .actions button {
                background: none;
                border: none;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
                cursor: pointer;
                transition: 0.3s;
            }
            .edit {
                color: #2b47ff;
            }
            .edit:hover {
                background: rgba(43,71,255,0.1);
            }
            .delete {
                color: #ff3b3b;
            }
            .delete:hover {
                background: rgba(255,59,59,0.1);
            }
        </style>
    </head>
    <body>
        <div class="sidebar">
            <h2>Dashboard</h2>
            <button>Students</button>
        </div>

        <div class="content">
            <h1>Registered Students</h1>
            <button class="add-btn" onclick="addStudent()">Add Student</button>
            <div id="studentsList"></div>
        </div>

        <script>
            function loadStudents() {
                fetch('/students')
                .then(res => res.json())
                .then(data => {
                    const container = document.getElementById('studentsList');
                    container.innerHTML = '';
                    data.forEach((s, index) => {
                        container.innerHTML += `
                            <div class='student-card'>
                                <div class='student-info'>
                                    <strong>${s.name}</strong>
                                    <span>Course: ${s.course}</span>
                                    <span>Year Level: ${s.year}</span>
                                </div>
                                <div class='actions'>
                                    <button class='edit' onclick='editStudent(${index})'>Edit</button>
                                    <button class='delete' onclick='deleteStudent(${index})'>Delete</button>
                                </div>
                            </div>
                        `;
                    });
                });
            }

            function addStudent() {
                const name = prompt("Enter student name:");
                const course = prompt("Enter course (e.g., BSIT, BSE, etc.):");
                const year = prompt("Enter year level (e.g., 1st Year):");

                if (name && course && year) {
                    fetch('/students', {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({name, course, year})
                    }).then(() => loadStudents());
                }
            }

            function editStudent(index) {
                const newName = prompt("Enter new name:");
                const newCourse = prompt("Enter new course:");
                const newYear = prompt("Enter new year level:");
                fetch(`/students/${index}`, {
                    method: "PUT",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({name: newName, course: newCourse, year: newYear})
                }).then(() => loadStudents());
            }

            function deleteStudent(index) {
                if (confirm("Are you sure you want to delete this student?")) {
                    fetch(`/students/${index}`, { method: "DELETE" })
                    .then(() => loadStudents());
                }
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


@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    students.append(data)
    return jsonify({"message": "Student added successfully"}), 201


@app.route('/students/<int:index>', methods=['PUT'])
def edit_student(index):
    if 0 <= index < len(students):
        data = request.get_json()
        students[index] = data
        return jsonify({"message": "Student updated"}), 200
    return jsonify({"error": "Student not found"}), 404


@app.route('/students/<int:index>', methods=['DELETE'])
def delete_student(index):
    if 0 <= index < len(students):
        students.pop(index)
        return jsonify({"message": "Student deleted"}), 200
    return jsonify({"error": "Student not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
