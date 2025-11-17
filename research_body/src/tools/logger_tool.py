"""
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
THE MEMORY  Logger Tool
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP

ORGAN METAPHOR:
    The Memory records and recalls the organism's experiences.
    Like a biological memory system that stores events for later retrieval,
    the Logger Tool persistently records every mission run, creating
    an audit trail and enabling historical analysis.

PURPOSE:
    " Record mission parameters and timestamps
    " Log pipeline execution steps and outcomes
    " Store metadata (URLs fetched, content sizes, processing times)
    " Enable mission replay and debugging
    " Support historical trend analysis

AGENT vs TOOL:
     NOT an agent  Does not decide what to log or when
     TOOL  Deterministic storage operation

    The Logger Tool:
    - Takes structured data and writes to storage (SQLite/JSON)
    - Does not interpret or analyze logged data
    - Does not make decisions about retention or cleanup
    - Simply records what it's told to record

TEACHING GOALS:
    This module demonstrates:
    1. Persistent state management
    2. Structured logging practices
    3. Database design for mission tracking
    4. Separation of logging from business logic

STORAGE DESIGN:
    " SQLite database: missions.sqlite
    " Tables: missions, tasks, fetch_logs, summaries
    " Indexed by timestamp, mission_id, status
    " Queryable for analytics and debugging

FUTURE EXTENSIONS:
    " Real-time log streaming to UI
    " Log aggregation and alerting
    " Performance metrics and dashboards
    " Automatic anomaly detection
    " Export to external monitoring systems

DEBUGGING NOTES:
    " Ensure database writes don't block pipeline
    " Validate schema on startup
    " Monitor database size and implement rotation
    " Test recovery from database corruption

PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
"""


# ═══════════════════════════════════════════════════════════════════════════
# IMPLEMENTATION — Phase 1 Stub
# ═══════════════════════════════════════════════════════════════════════════

from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
import json
import os


@dataclass
class LogEntry:
    """
    A single log entry for mission tracking.

    Attributes:
        mission_id: Unique mission identifier
        timestamp: When this entry was created
        event_type: Type of event ("mission_start", "fetch_complete", etc.)
        message: Human-readable message
        data: Additional structured data
        level: Log level ("INFO", "WARNING", "ERROR")
    """

    mission_id: str
    event_type: str
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    data: Dict[str, Any] = field(default_factory=dict)
    level: str = "INFO"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "mission_id": self.mission_id,
            "timestamp": self.timestamp.isoformat(),
            "event_type": self.event_type,
            "message": self.message,
            "data": self.data,
            "level": self.level,
        }

    def __repr__(self) -> str:
        return f"LogEntry({self.event_type}, {self.message[:50]}...)"


class MissionLogger:
    """
    Logger for tracking research missions.

    This is a STUB implementation for Phase 1.
    Full SQLite integration comes in Phase 2.

    The logger records all mission activity:
    • When missions start/complete
    • Which URLs were fetched
    • Errors encountered
    • Processing times and metadata

    Teaching Notes:
        This is a deterministic TOOL:
        • Takes events → Stores them persistently
        • No decision-making about what to log
        • Simply records what it's told to record
        • Provides retrieval interface for analysis

        Design patterns:
        - Singleton pattern (one logger per application)
        - Repository pattern (abstract storage layer)
        - Observer pattern (log events as they happen)
    """

    def __init__(self, database_path: str = "data/missions.sqlite"):
        """
        Initialize the mission logger.

        Args:
            database_path: Path to SQLite database
        """
        self.database_path = database_path
        self.in_memory_logs = []  # Phase 1: store in memory

        print(f"[LOGGER STUB] Initialized with database: {database_path}")
        print(f"[LOGGER STUB] Phase 1: Using in-memory storage")

    def log(
        self,
        mission_id: str,
        event_type: str,
        message: str,
        data: Optional[Dict[str, Any]] = None,
        level: str = "INFO",
    ) -> None:
        """
        Log a mission event.

        Args:
            mission_id: Mission identifier
            event_type: Event type (e.g., "fetch_complete", "error")
            message: Human-readable message
            data: Additional structured data
            level: Log level ("DEBUG", "INFO", "WARNING", "ERROR")

        Example:
            logger.log(
                mission_id="abc123",
                event_type="fetch_complete",
                message="Fetched https://example.com",
                data={"url": "https://example.com", "status": 200}
            )
        """
        entry = LogEntry(
            mission_id=mission_id,
            event_type=event_type,
            message=message,
            data=data or {},
            level=level,
        )

        # Phase 1: Store in memory
        self.in_memory_logs.append(entry)

        # Print for visibility
        timestamp = entry.timestamp.strftime("%H:%M:%S")
        print(f"[LOGGER {timestamp}] [{level}] {event_type}: {message}")

        # Phase 2 will write to SQLite database

    def log_mission_start(self, mission_id: str, query: str) -> None:
        """Log the start of a new mission."""
        self.log(
            mission_id=mission_id,
            event_type="mission_start",
            message=f"Mission started: {query}",
            data={"query": query},
        )

    def log_mission_complete(self, mission_id: str, duration: float) -> None:
        """Log successful mission completion."""
        self.log(
            mission_id=mission_id,
            event_type="mission_complete",
            message=f"Mission completed in {duration:.2f}s",
            data={"duration": duration},
        )

    def log_error(self, mission_id: str, error: str, context: Optional[Dict] = None) -> None:
        """Log an error during mission execution."""
        self.log(
            mission_id=mission_id,
            event_type="error",
            message=f"Error: {error}",
            data=context or {},
            level="ERROR",
        )

    def get_mission_logs(self, mission_id: str) -> list:
        """
        Retrieve all logs for a specific mission.

        Args:
            mission_id: Mission to retrieve logs for

        Returns:
            list: List of LogEntry objects
        """
        # Phase 1: Filter in-memory logs
        logs = [log for log in self.in_memory_logs if log.mission_id == mission_id]

        print(f"[LOGGER STUB] Retrieved {len(logs)} logs for mission {mission_id}")

        return logs

    def export_logs_json(self, output_path: str) -> None:
        """
        Export all logs to JSON file.

        Args:
            output_path: Path to output JSON file
        """
        logs_dict = [log.to_dict() for log in self.in_memory_logs]

        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(logs_dict, f, indent=2)

        print(f"[LOGGER STUB] Exported {len(logs_dict)} logs to {output_path}")


# Global logger instance (singleton pattern)
_logger_instance: Optional[MissionLogger] = None


def get_logger(database_path: str = "data/missions.sqlite") -> MissionLogger:
    """
    Get the global logger instance (singleton).

    Args:
        database_path: Path to database (only used on first call)

    Returns:
        MissionLogger: The global logger instance

    Teaching Notes:
        Singleton pattern ensures only one logger exists:
        • Prevents duplicate log entries
        • Centralizes logging configuration
        • Simplifies access across modules

        Usage:
            from tools.logger_tool import get_logger
            logger = get_logger()
            logger.log(...)
    """
    global _logger_instance

    if _logger_instance is None:
        _logger_instance = MissionLogger(database_path)

    return _logger_instance


# ═══════════════════════════════════════════════════════════════════════════
# FUTURE IMPLEMENTATION NOTES (Phase 2)
# ═══════════════════════════════════════════════════════════════════════════

"""
Phase 2 Implementation Plan:

1. Create SQLite database schema:
   CREATE TABLE missions (
       mission_id TEXT PRIMARY KEY,
       query TEXT NOT NULL,
       started_at TIMESTAMP,
       completed_at TIMESTAMP,
       status TEXT,
       error TEXT
   );

   CREATE TABLE events (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       mission_id TEXT NOT NULL,
       timestamp TIMESTAMP,
       event_type TEXT,
       message TEXT,
       data JSON,
       level TEXT,
       FOREIGN KEY (mission_id) REFERENCES missions(mission_id)
   );

   CREATE INDEX idx_mission_id ON events(mission_id);
   CREATE INDEX idx_timestamp ON events(timestamp);

2. Initialize database on startup:
   import sqlite3
   conn = sqlite3.connect(database_path)
   conn.execute(CREATE_TABLE_SQL)
   conn.commit()

3. Implement log() with SQLite:
   def log(self, mission_id, event_type, message, data=None, level="INFO"):
       conn = sqlite3.connect(self.database_path)
       conn.execute(
           "INSERT INTO events (mission_id, event_type, message, data, level) VALUES (?, ?, ?, ?, ?)",
           (mission_id, event_type, message, json.dumps(data), level)
       )
       conn.commit()
       conn.close()

4. Query and analytics:
   • Get all missions: SELECT * FROM missions ORDER BY started_at DESC
   • Get failed missions: SELECT * FROM missions WHERE status = 'failed'
   • Average duration: SELECT AVG(completed_at - started_at) FROM missions
   • Error rate: SELECT COUNT(*) / total WHERE status = 'failed'

5. Advanced features:
   • Real-time log streaming (websockets for UI)
   • Log rotation (archive old missions)
   • Structured logging (proper levels, formatters)
   • Integration with standard Python logging module
   • Export to external monitoring (Prometheus, Grafana)

6. Connection pooling:
   • Don't open/close connection for every log
   • Use connection pool or context manager
   • Handle concurrent writes safely

Example Phase 2 implementation:
    import sqlite3
    from contextlib import contextmanager

    class MissionLogger:
        def __init__(self, database_path):
            self.database_path = database_path
            self._init_database()

        def _init_database(self):
            with self._get_connection() as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS events (
                        id INTEGER PRIMARY KEY,
                        mission_id TEXT,
                        timestamp TEXT,
                        event_type TEXT,
                        message TEXT,
                        data TEXT,
                        level TEXT
                    )
                ''')

        @contextmanager
        def _get_connection(self):
            conn = sqlite3.connect(self.database_path)
            try:
                yield conn
                conn.commit()
            finally:
                conn.close()

        def log(self, mission_id, event_type, message, data=None, level="INFO"):
            with self._get_connection() as conn:
                conn.execute(
                    "INSERT INTO events VALUES (NULL, ?, ?, ?, ?, ?, ?)",
                    (mission_id, datetime.now().isoformat(),
                     event_type, message, json.dumps(data), level)
                )
"""
