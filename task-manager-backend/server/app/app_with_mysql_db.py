from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# -----------------------------
# Database Configuration (MySQL)
# -----------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:passw0rd@localhost:3308/app_db?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ============================================================
# PART 1: USER MODEL
# ============================================================

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship: one user has many tasks
    tasks = db.relationship("Task", backref="user", cascade="all, delete-orphan")


# TASK MODEL WITH user_id FOREIGN KEY (Part 3)
class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Linking task → user
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


# Create tables
with app.app_context():
    db.create_all()


# ============================================================
# PART 2: USER CRUD ENDPOINTS
# ============================================================

# CREATE USER
@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.json

    if "username" not in data or "email" not in data:
        return jsonify({"error": "username and email required"}), 400

    new_user = User(username=data["username"], email=data["email"])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created", "user_id": new_user.id}), 201


# LISTING ALL USERS
@app.route("/api/users", methods=["GET"])
def list_users():
    users = User.query.all()
    output = []

    for u in users:
        output.append({
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "created_at": u.created_at
        })

    return jsonify(output), 200


# GET SINGLE USER
@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at
    }), 200


# UPDATE USER
@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json

    if "username" in data:
        user.username = data["username"]
    if "email" in data:
        user.email = data["email"]

    db.session.commit()
    return jsonify({"message": "User updated"}), 200


# DELETE USER
@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted"}), 200


# ============================================================
# PART 3: LINK TASKS TO USERS
# ============================================================

# CREATE TASK WITH user_id
@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.json

    if "title" not in data or "user_id" not in data:
        return jsonify({"error": "title and user_id required"}), 400

    # Ensure user exists
    user = User.query.get(data["user_id"])
    if not user:
        return jsonify({"error": "User does not exist"}), 404

    new_task = Task(title=data["title"], user_id=data["user_id"])
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"message": "Task created", "task_id": new_task.id}), 201


# GET ALL TASKS OF A USER
@app.route("/api/users/<int:user_id>/tasks", methods=["GET"])
def get_user_tasks(user_id):
    user = User.query.get_or_404(user_id)
    tasks = Task.query.filter_by(user_id=user.id).all()

    output = []
    for t in tasks:
        output.append({
            "id": t.id,
            "title": t.title,
            "created_at": t.created_at
        })

    return jsonify({"user_id": user.id, "tasks": output}), 200


# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
