from flask import Blueprint, request, jsonify
from app.models import (
    get_all_tasks,
    get_task_by_id,
    create_task,
    update_task,
    delete_task,
)

bp = Blueprint("tasks", __name__)


@bp.route("/tasks", methods=["GET"])
def list_tasks():
    tasks = get_all_tasks()
    return jsonify(tasks), 200


@bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = get_task_by_id(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task), 200


@bp.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json(silent=True)
    if not data or not data.get("title"):
        return jsonify({"error": "Field 'title' is required"}), 400

    title = data["title"]
    description = data.get("description", "")
    new_id = create_task(title, description)
    return jsonify({"id": new_id, "title": title, "description": description}), 201


@bp.route("/tasks/<int:task_id>", methods=["PUT"])
def edit_task(task_id):
    data = request.get_json(silent=True)
    if not data or not data.get("title"):
        return jsonify({"error": "Field 'title' is required"}), 400

    title = data["title"]
    description = data.get("description", "")
    status = data.get("status", "pending")

    success = update_task(task_id, title, description, status)
    if not success:
        return jsonify({"error": "Task not found"}), 404
    return (
        jsonify(
            {
                "id": task_id,
                "title": title,
                "description": description,
                "status": status,
            }
        ),
        200,
    )


@bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def remove_task(task_id):
    success = delete_task(task_id)
    if not success:
        return jsonify({"error": "Task not found"}), 404
    return "", 204
