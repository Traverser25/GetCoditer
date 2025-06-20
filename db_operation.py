import sqlite3
from typing import List, Optional


class SQLiteHandler:
    def __init__(self, db_path: str = "candidates.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        """
        Create the candidates table if it doesn't exist already.
        """
        query = """
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT,
            score INTEGER,
            location TEXT,
            relocate TEXT,
            job_type TEXT,
            notice_period TEXT,
            experience_years REAL,
            cv_link TEXT,
            blurb TEXT,
            tech_stack TEXT
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def insert_candidate(self, data: dict):
        """
        Insert a structured candidate dictionary into the database.
        """
        query = """
        INSERT INTO candidates (
            author, score, location, relocate, job_type,
            notice_period, experience_years, cv_link,
            blurb, tech_stack
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        techs = ",".join(data.get("tech_stack", []))
        values = (
            data.get("author"),
            data.get("score", 0),
            data.get("location", ""),
            data.get("willing_to_relocate", ""),
            data.get("type", ""),
            data.get("notice_period", ""),
            data.get("experience_years", 0.0),
            data.get("cv_link", ""),
            data.get("blurb", ""),
            techs
        )
        self.conn.execute(query, values)
        self.conn.commit()

    def filter_candidates(
        self,
        techs: Optional[List[str]] = None,
        locations: Optional[List[str]] = None,
        min_yoe: float = 0.0
    ) -> List[dict]:
        """
        Filter candidates based on:
        - techs: All keywords must be present (AND)
        - locations: Any keyword can match (OR)
        - min_yoe: Minimum years of experience
        """
        query = "SELECT * FROM candidates WHERE experience_years >= ?"
        args = [min_yoe]

        # Tech stack filters (AND match)
        if techs:
            for tech in techs:
                query += " AND tech_stack LIKE ?"
                args.append(f"%{tech}%")

        # Location filters (OR match)
        if locations:
            loc_clauses = []
            for loc in locations:
                loc_clauses.append("location LIKE ?")
                args.append(f"%{loc}%")
            if loc_clauses:
                query += " AND (" + " OR ".join(loc_clauses) + ")"

        rows = self.conn.execute(query, tuple(args)).fetchall()
        return [self._row_to_dict(row) for row in rows]

    def search_by_author(self, name: str) -> List[dict]:
        """
        Search candidates by author name (partial match).
        """
        query = "SELECT * FROM candidates WHERE author LIKE ?"
        rows = self.conn.execute(query, (f"%{name}%",)).fetchall()
        return [self._row_to_dict(row) for row in rows]

    def get_all(self) -> List[dict]:
        """
        Fetch all candidate entries from the database.
        """
        query = "SELECT * FROM candidates"
        rows = self.conn.execute(query).fetchall()
        return [self._row_to_dict(row) for row in rows]

    def _row_to_dict(self, row: tuple) -> dict:
        """
        Convert a DB row tuple to a dictionary.
        """
        return {
            "id": row[0],
            "author": row[1],
            "score": row[2],
            "location": row[3],
            "relocate": row[4],
            "type": row[5],
            "notice_period": row[6],
            "experience_years": row[7],
            "cv_link": row[8],
            "blurb": row[9],
            "tech_stack": row[10].split(",") if row[10] else []
        }

    def close(self):
        """
        Close the SQLite database connection.
        """
        self.conn.close()
