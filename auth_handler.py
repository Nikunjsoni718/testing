"""Authentication handler module with secure parameterized database queries and structured logging."""

import logging
import sqlite3
from typing import Any, Dict, Optional

# Structured logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def find_user_by_token(token: str, db_conn: sqlite3.Connection) -> Optional[Dict[str, Any]]:
    """
    Safely retrieves user details by session token using parameterized SQL queries
    to mitigate SQL injection vulnerabilities.
    """
    if not token or not isinstance(token, str):
        logger.warning("Authentication failed: Invalid or empty token supplied.")
        return None

    # Secure parameterized query prevents SQL injection
    query = "SELECT id, username, role FROM users WHERE session_token = ?"

    try:
        cursor = db_conn.cursor()
        cursor.execute(query, (token,))
        result = cursor.fetchone()

        if not result:
            logger.info("Authentication lookup: No matching active session token found.")
            return None

        return {
            "id": result[0],
            "username": result[1],
            "role": result[2],
        }
    except sqlite3.Error as err:
        logger.error("Database query execution failed during authentication: %s", err)
        return None
