
import sqlite3
from pathlib import Path

# Project folders
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIR / "nids.db"


def get_connection():
    """Open a connection to the NIDS database."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def init_db():
    """Create the database tables if they do not exist."""

    with get_connection() as connection:

        # Store network flows and model predictions
        connection.execute("""
            CREATE TABLE IF NOT EXISTS flows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                source_ip TEXT,
                destination_ip TEXT,
                source_port INTEGER,
                destination_port INTEGER,
                protocol TEXT,
                packet_count INTEGER,
                total_bytes INTEGER,
                duration REAL,
                prediction TEXT NOT NULL,
                confidence REAL
            )
        """)

        # Store alerts associated with suspicious flows
        connection.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                flow_id INTEGER NOT NULL,
                alert_type TEXT NOT NULL,
                severity TEXT NOT NULL DEFAULT 'Medium',
                message TEXT,
                status TEXT NOT NULL DEFAULT 'New',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (flow_id) REFERENCES flows(id)
            )
        """)

        connection.commit()

    print("NIDS database initialized successfully.")
    print(f"Database location: {DATABASE_PATH}")


def save_flow(
    source_ip,
    destination_ip,
    source_port,
    destination_port,
    protocol,
    packet_count,
    total_bytes,
    duration,
    prediction,
    confidence=None,
):
    """Save one analyzed network flow and return its database ID."""

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO flows (
                source_ip, destination_ip,
                source_port, destination_port,
                protocol, packet_count, total_bytes,
                duration, prediction, confidence
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                source_ip,
                destination_ip,
                source_port,
                destination_port,
                protocol,
                packet_count,
                total_bytes,
                duration,
                prediction,
                confidence,
            ),
        )

        return cursor.lastrowid


def save_alert(flow_id, alert_type, severity, message):
    """Save an alert linked to a flow."""

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO alerts (
                flow_id, alert_type, severity, message
            )
            VALUES (?, ?, ?, ?)
            """,
            (flow_id, alert_type, severity, message),
        )

        return cursor.lastrowid


def get_recent_flows(limit=20):
    """Return the most recent network flows."""

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT * FROM flows
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

        return [dict(row) for row in rows]


def get_recent_alerts(limit=20):
    """Return the most recent alerts."""

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT * FROM alerts
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

        return [dict(row) for row in rows]

if __name__ == "__main__":
    init_db()
