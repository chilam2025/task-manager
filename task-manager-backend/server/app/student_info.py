from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'Welcome to the Mock API Suite',
        'status': 'running'
    })

@app.route('/api/student')
def get_student():
    student_id = request.args.get('id', '0')
    mock_students = {
        '12345': {'name': 'Alice Johnson', 'course': 'Data Science', 'year': 3, 'gpa': 3.8},
        '67890': {'name': 'Bob Smith', 'course': 'AI Engineering', 'year': 2, 'gpa': 3.6}
    }

    if student_id in mock_students:
        return jsonify({
            'id': student_id,
            **mock_students[student_id]
        })
    else:
        return jsonify({'error': 'Student not found'}), 404


@app.route('/api/students/count')
def student_count():
    total_students = 2  # mock value
    return jsonify({
        'total_students': total_students
    })


if __name__ == '__main__':
    app.run(debug=True, port=6050)
