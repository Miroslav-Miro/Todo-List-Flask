import sqlite3 

def connect_db():
    conn = sqlite3.connect('my_todo_database.db')
    cursor = conn.cursor()
    return conn, cursor

def create_table():
    conn, cursor = connect_db()
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       task_name TEXT NOT NULL,
                       completed INTEGER DEFAULT 0)''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
    finally:
        conn.close()

def add_task(task_name):
    conn, cursor = connect_db()
    try:
        cursor.execute('''INSERT INTO tasks (task_name) VALUES (?)''', (task_name,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error adding task: {e}")
    finally:
        conn.close()

def get_tasks():
    conn, cursor = connect_db()
    try:
        cursor.execute('''SELECT * FROM tasks''')
        tasks = cursor.fetchall()
        return tasks
    except sqlite3.Error as e:
        print(f"Error fetching tasks: {e}")
        return []
    finally:
        conn.close()

def complete_task(task_id):
    conn, cursor = connect_db()
    try:
        cursor.execute('''UPDATE tasks SET completed = 1 WHERE id = ?''', (task_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error completing task: {e}")
    finally:
        conn.close()
        
        
def undo_task(task_id):
    conn, cursor = connect_db()
    try:
        cursor.execute('''UPDATE tasks SET completed = 0 WHERE id = ?''', (task_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error undoing task completion: {e}")
    finally:
        conn.close()


def delete_task(task_id):
    conn, cursor = connect_db()
    try:
        cursor.execute('''DELETE FROM tasks WHERE id = ?''', (task_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error deleting task: {e}")
    finally:
        conn.close()

def delete_all_tasks():
    conn, cursor = connect_db()
    try:
        cursor.execute('''DELETE FROM tasks''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error deleting all tasks: {e}")
    finally:
        conn.close()

def delete_amount_tasks(amount):
    conn, cursor = connect_db()
    try:
        cursor.execute("SELECT id FROM tasks ORDER BY id ASC LIMIT ?", (amount,))
        task_ids = cursor.fetchall()

        task_ids = [task[0] for task in task_ids]

        if task_ids:
            cursor.execute(f"DELETE FROM tasks WHERE id IN ({','.join('?' * len(task_ids))})", task_ids)

        conn.commit()
    except sqlite3.Error as e:
        print(f"Error deleting tasks: {e}")
    finally:
        conn.close()

def get_task_by_id(task_id):
    conn, cursor = connect_db()
    try:
        cursor.execute('''SELECT * FROM tasks WHERE id = ?''', (task_id,))
        task = cursor.fetchone()
        return task  # Returns None if task not found
    except sqlite3.Error as e:
        print(f"Error fetching task by ID: {e}")
        return None
    finally:
        conn.close()

if __name__ == '__main__':
    create_table()

    add_task('Buy groceries')
    add_task('Walk the dog')

    print("Tasks:", get_tasks())

    complete_task(1)

    tasks = get_tasks()
    if len(tasks) > 10:
        delete_amount_tasks(5)

    # delete_all_tasks()
    print("Updated Tasks:", get_tasks())
