from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

categories = []
category_id_counter = 1

# -------------------------------
# Helper Functions
# -------------------------------
def find_task(task_id):
    return next((t for t in tasks if t['id'] == task_id), None)

def find_category(cat_id):
    return next((c for c in categories if c['id'] == cat_id), None)

def validate_date_format(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None


# -------------------------------
# Category Management (Part 1)
# -------------------------------
@app.route("/api/categories", methods=["POST"])
def add_category():
    global category_id_counter
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Category name required"}), 400

    category = {"id": category_id_counter, "name": data["name"]}
    categories.append(category)
    category_id_counter += 1
    return jsonify(category), 201

@app.route("/api/categories", methods=["GET"])
def get_categories():
    return jsonify(categories), 200

@app.route("/api/categories/<int:cat_id>", methods=["DELETE"])
def delete_category(cat_id):
    category = find_category(cat_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404
    categories.remove(category)
    return jsonify({"message": "Category deleted"})


# -------------------------------
# Task Management
# -------------------------------
tasks = []
task_id_counter = 1

# ------------------ POST: Add a new task ------------------
@app.route("/api/tasks", methods=["POST"])
def add_task():
    global task_id_counter
    data = request.json
    title = data.get("title")
    if not title:
        return jsonify({"error": "Task title required"}), 400

    # Validate date
    due_date = data.get("due_date")
    if due_date and not validate_date_format(due_date):
        return jsonify({"error": "Invalid date format (YYYY-MM-DD)"}), 400

    # Validate category
    cat_id = data.get("category_id")
    if cat_id and not find_category(cat_id):
        return jsonify({"error": "Category not found"}), 404

    # Validate priority
    priority = data.get("priority", "medium").lower()
    if priority not in ["low", "medium", "high"]:
        return jsonify({"error": "Invalid priority"}), 400

    task = {
        "id": task_id_counter,
        "title": title,
        "completed": False,
        "category_id": cat_id,
        "due_date": due_date,
        "priority": priority
    }
    tasks.append(task)
    task_id_counter += 1
    return jsonify(task), 201

# ------------------ GET: Retrieve tasks ------------------
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    cat_filter = request.args.get("category_id")
    filtered = tasks
    if cat_filter:
        filtered = [t for t in tasks if str(t.get("category_id")) == cat_filter]
    return jsonify(filtered), 200



# -------------------------------
# Overdue Tasks (Part 2)
# -------------------------------
@app.route("/api/tasks/overdue", methods=["GET"])
def get_overdue_tasks():
    now = datetime.now()
    overdue = []
    for t in tasks:
        if t["due_date"]:
            due = validate_date_format(t["due_date"])
            if due and due < now and not t["completed"]:
                overdue.append(t)
    return jsonify(overdue)


# -------------------------------
# Statistics (Part 3)
# -------------------------------
@app.route("/api/tasks/stats", methods=["GET"])
def get_stats():
    total = len(tasks)
    completed = len([t for t in tasks if t["completed"]])
    pending = len([t for t in tasks if not t["completed"]])
    now = datetime.now()
    overdue = len([
        t for t in tasks
        if t["due_date"] and validate_date_format(t["due_date"]) and
        validate_date_format(t["due_date"]) < now and not t["completed"]
    ])
    return jsonify({
        "total_tasks": total,
        "completed": completed,
        "pending": pending,
        "overdue": overdue
    })


if __name__ == "__main__":
    app.run(debug=True)
