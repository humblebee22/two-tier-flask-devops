from app.db import get_db_connection


def get_all_tasks():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
    tasks = cursor.fetchall()
    cursor.close()
    connection.close()
    return tasks


def get_task_by_id(task_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cursor.fetchone()
    cursor.close()
    connection.close()
    return task


def create_task(title, description):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, description) VALUES (%s, %s)",
        (title, description),
    )
    connection.commit()
    new_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return new_id


def update_task(task_id, title, description, status):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        """UPDATE tasks
           SET title = %s, description = %s, status = %s
           WHERE id = %s""",
        (title, description, status, task_id),
    )
    connection.commit()
    affected = cursor.rowcount
    cursor.close()
    connection.close()
    return affected > 0


def delete_task(task_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    connection.commit()
    affected = cursor.rowcount
    cursor.close()
    connection.close()
    return affected > 0
