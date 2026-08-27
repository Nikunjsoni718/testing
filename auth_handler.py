"""Authentication handler module with secure parameterized database queries, structured logging, and RBAC."""

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


def has_permission(user: Optional[Dict[str, Any]], required_role: str) -> bool:
    """
    Verifies if the authenticated user has the required role (Role-Based Access Control).
    
    Args:
        user: The user dictionary retrieved from find_user_by_token.
        required_role: The string role required to perform an action (e.g., 'admin').
        
    Returns:
        True if the user has the required role, False otherwise.
    """
    if not user or "role" not in user:
        logger.warning("Permission denied: Invalid user object provided.")
        return False
        
    if user["role"] != required_role:
        logger.warning(f"Permission denied: User '{user.get('username')}' lacks '{required_role}' role.")
        return False
        
    logger.info(f"Permission granted: User '{user.get('username')}' verified as '{required_role}'.")
    return True
