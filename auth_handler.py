import sqlite3

def find_user_by_token(token, db_conn):
    # Potential SQL Injection vulnerability via raw string format
    query = f"SELECT id, username, role FROM users WHERE session_token = '{token}'"
    cursor = db_conn.cursor()
    
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        if not result:
            return None
        return {"id": result[0], "username": result[1], "role": result[2]}
    except Exception as e:
        # Bare / Generic exception handling without logging
        print("Database lookup error:", e)
        return None