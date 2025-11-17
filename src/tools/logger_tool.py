"""
THE MEMORY — LOGGER TOOL
=========================

ORGAN METAPHOR:
---------------
The Logger is the MEMORY of the research organism.
It records every mission, every fetch, every summary,
creating a complete audit trail and historical archive.

AGENT vs TOOL:
--------------
This is a TOOL because it:
  • Performs deterministic logging operations
  • Does not decide WHAT to log or WHY, only HOW to log it
  • Has no autonomous decision-making capability
  • Simply records data as instructed

RESPONSIBILITIES:
-----------------
  1. Initialize SQLite database for mission history
  2. Record mission metadata (start time, mission type, sources)
  3. Log all fetch operations (URL, status, timestamp)
  4. Store summaries and outputs
  5. Provide query interface for historical data

TEACHING NOTES:
---------------
The Logger TOOL is purely mechanical. It writes everything to a database
in a structured format. It does not interpret the data or make decisions
about what's important — it just preserves everything for later analysis.

FUTURE EXTENSIONS:
------------------
  • Advanced querying and filtering
  • Dashboard visualizations of historical data
  • Anomaly detection (unusual mission patterns)
  • Export to CSV, JSON, or other formats

DEBUGGING TIPS:
---------------
  • Verify database schema matches data structure
  • Monitor database size and implement archival strategies
  • Test query performance with large datasets
"""

import sqlite3
import json
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path


# Database path
DB_PATH = Path(__file__).parent.parent.parent / "data" / "missions.sqlite"


class LoggerTool:
    """
    THE MEMORY — Deterministic Mission Logging Tool
    ================================================

    This class encapsulates all database logging operations.
    It's a TOOL because it has NO autonomous decision-making.

    TOOL CHARACTERISTICS:
    ---------------------
      • Records data exactly as provided
      • No judgment about what's important
      • Deterministic: same data → same log entry
      • Returns confirmation without interpretation

    WHY NOT AN AGENT:
    -----------------
    The Logger doesn't decide:
      - What is worth logging
      - How to organize or categorize data
      - When to archive or delete old data
      - What patterns or anomalies exist

    It just logs. Period.

    TEACHING NOTE:
    --------------
    This is a fully functional SQLite logger demonstrating
    persistent state management and structured data storage.
    """

    def __init__(self, db_path: Optional[Path] = None, debug: bool = False):
        """
        Initialize the Logger Tool.

        Args:
            db_path: Path to SQLite database (uses default if None)
            debug: Enable detailed logging output
        """
        self.db_path = db_path or DB_PATH
        self.debug = debug
        self._ensure_database()

    def _ensure_database(self):
        """Ensure database and tables exist."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create missions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS missions (
                mission_id TEXT PRIMARY KEY,
                topic TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                completed_at TIMESTAMP,
                source_count INTEGER,
                summary_count INTEGER,
                metadata TEXT
            )
        ''')

        # Create fetches table (tracks individual URL fetches)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fetches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mission_id TEXT NOT NULL,
                url TEXT NOT NULL,
                status_code INTEGER,
                fetch_time REAL,
                timestamp TIMESTAMP NOT NULL,
                FOREIGN KEY (mission_id) REFERENCES missions (mission_id)
            )
        ''')

        # Create summaries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mission_id TEXT NOT NULL,
                summary_text TEXT NOT NULL,
                style TEXT,
                word_count INTEGER,
                quality_score REAL,
                timestamp TIMESTAMP NOT NULL,
                FOREIGN KEY (mission_id) REFERENCES missions (mission_id)
            )
        ''')

        # Create indexes for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_missions_timestamp ON missions(created_at)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_fetches_mission ON fetches(mission_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_summaries_mission ON summaries(mission_id)')

        conn.commit()
        conn.close()

    def log_mission(self, mission_data: Dict) -> str:
        """
        Log a mission to the database.

        Args:
            mission_data: Dictionary containing:
                - mission_id: Unique identifier
                - topic: Research topic
                - status: Mission status (pending, in_progress, completed, failed)
                - source_count: Number of sources
                - summary_count: Number of summaries
                - metadata: Additional JSON metadata

        Returns:
            Mission ID of the logged mission

        Example:
            >>> logger = LoggerTool()
            >>> mission_id = logger.log_mission({
            >>>     "mission_id": "m_001",
            >>>     "topic": "Wildfire AI",
            >>>     "status": "completed",
            >>>     "source_count": 5
            >>> })
        """
        mission_id = mission_data.get('mission_id', '')
        topic = mission_data.get('topic', '')
        status = mission_data.get('status', 'pending')
        source_count = mission_data.get('source_count', 0)
        summary_count = mission_data.get('summary_count', 0)
        metadata = json.dumps(mission_data.get('metadata', {}))
        created_at = mission_data.get('created_at', datetime.now())
        completed_at = mission_data.get('completed_at')

        if self.debug:
            print(f"\n[LOGGER TOOL] Logging mission: {mission_id}")
            print(f"[LOGGER TOOL] Topic: {topic}")
            print(f"[LOGGER TOOL] Status: {status}")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO missions
            (mission_id, topic, status, created_at, completed_at, source_count, summary_count, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (mission_id, topic, status, created_at, completed_at, source_count, summary_count, metadata))

        conn.commit()
        conn.close()

        if self.debug:
            print(f"[LOGGER TOOL] ✓ Mission logged successfully")

        return mission_id

    def log_fetch(self, mission_id: str, url: str, status_code: int, fetch_time: float):
        """Log a URL fetch operation."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO fetches (mission_id, url, status_code, fetch_time, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (mission_id, url, status_code, fetch_time, datetime.now()))

        conn.commit()
        conn.close()

    def log_summary(self, mission_id: str, summary_data: Dict):
        """Log a generated summary."""
        summary_text = summary_data.get('summary', '')
        style = summary_data.get('style', 'unknown')
        word_count = summary_data.get('word_count', 0)
        quality_score = summary_data.get('score', 0.0)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO summaries (mission_id, summary_text, style, word_count, quality_score, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (mission_id, summary_text, style, word_count, quality_score, datetime.now()))

        conn.commit()
        conn.close()

    def get_mission_history(self, limit: int = 10) -> List[Dict]:
        """Retrieve recent mission history."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM missions
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_mission_by_id(self, mission_id: str) -> Optional[Dict]:
        """Retrieve a specific mission by ID."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM missions WHERE mission_id = ?', (mission_id,))
        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    def get_mission_stats(self) -> Dict:
        """Get overall statistics about all missions."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM missions')
        total_missions = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM missions WHERE status = "completed"')
        completed_missions = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM fetches')
        total_fetches = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM summaries')
        total_summaries = cursor.fetchone()[0]

        conn.close()

        return {
            'total_missions': total_missions,
            'completed_missions': completed_missions,
            'success_rate': completed_missions / total_missions if total_missions > 0 else 0.0,
            'total_fetches': total_fetches,
            'total_summaries': total_summaries
        }

    def get_all_missions(self) -> List[Dict]:
        """
        Get all missions with full metadata and summaries.

        PHASE 5 ENHANCEMENT:
        --------------------
        Returns complete mission data for trend analysis.
        Used by TrendAnalyzer for cross-mission insights.

        Returns:
            List of all missions with parsed metadata
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM missions ORDER BY created_at DESC')
        rows = cursor.fetchall()

        missions = []
        for row in rows:
            mission = dict(row)
            # Parse JSON metadata
            if mission['metadata']:
                try:
                    mission['metadata'] = json.loads(mission['metadata'])
                except:
                    mission['metadata'] = {}

            missions.append(mission)

        conn.close()
        return missions

    def get_mission_with_summaries(self, mission_id: str) -> Optional[Dict]:
        """
        Get mission with all associated summaries.

        PHASE 5 ENHANCEMENT:
        --------------------
        Returns mission data enriched with summaries for analysis.

        Args:
            mission_id: Mission identifier

        Returns:
            Dict with mission data and summaries array
        """
        mission = self.get_mission_by_id(mission_id)
        if not mission:
            return None

        # Get summaries
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM summaries
            WHERE mission_id = ?
            ORDER BY timestamp
        ''', (mission_id,))

        summary_rows = cursor.fetchall()
        conn.close()

        mission['summaries'] = [dict(row) for row in summary_rows]

        # Parse metadata
        if mission['metadata']:
            try:
                mission['metadata'] = json.loads(mission['metadata'])
            except:
                mission['metadata'] = {}

        return mission


# Convenience functions for simple one-off logging
def init_database() -> bool:
    """Initialize the database (creates tables if needed)."""
    logger = LoggerTool()
    return True


def log_mission(mission_data: Dict) -> str:
    """Simple convenience function for logging a mission."""
    logger = LoggerTool()
    return logger.log_mission(mission_data)


def get_mission_history(limit: int = 10) -> List[Dict]:
    """Simple convenience function for retrieving mission history."""
    logger = LoggerTool()
    return logger.get_mission_history(limit)
