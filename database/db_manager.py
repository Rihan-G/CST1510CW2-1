import sqlite3
import bcrypt
from typing import Optional, Dict, List, Any

class DatabaseManager:
    def __init__(self, db_path: str = "intelligence_platform.db"):
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        return sqlite3.connect(self.db_path, timeout=30)

    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create tables
        tables = [
            '''CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',
            '''CREATE TABLE IF NOT EXISTS cyber_incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                threat_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                resolved_at TIMESTAMP,
                resolution_time_hours REAL,
                assigned_to TEXT
            )''',
            '''CREATE TABLE IF NOT EXISTS datasets_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                source_department TEXT NOT NULL,
                size_mb REAL NOT NULL,
                row_count INTEGER NOT NULL,
                column_count INTEGER NOT NULL,
                quality_score REAL,
                last_accessed TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                sensitivity TEXT
            )''',
            '''CREATE TABLE IF NOT EXISTS it_tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL,
                assigned_to TEXT NOT NULL,
                current_stage TEXT NOT NULL,
                priority TEXT DEFAULT 'Medium',
                created_at TIMESTAMP NOT NULL,
                resolved_at TIMESTAMP,
                time_in_stage_hours REAL,
                category TEXT
            )'''
        ]
        
        for table_sql in tables:
            cursor.execute(table_sql)
        
        # Insert default users
        default_users = [
            ("admin", bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), "admin"),
            ("cyber", bcrypt.hashpw("cyber123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), "cybersecurity"), 
            ("data", bcrypt.hashpw("data123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), "data_science"),
            ("it", bcrypt.hashpw("it123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), "it_operations")
        ]
        
        for username, hashed_pw, role in default_users:
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
            if cursor.fetchone()[0] == 0:
                cursor.execute(
                    "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                    (username, hashed_pw, role)
                )
        
        conn.commit()
        conn.close()

    def create_user(self, username: str, password_hash: str, role: str) -> bool:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash, role)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT username, password_hash, role FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            if user:
                return {'username': user[0], 'password_hash': user[1], 'role': user[2]}
            return None
        finally:
            conn.close()

    def get_cyber_incidents(self) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cyber_incidents ORDER BY created_at DESC")
        incidents = cursor.fetchall()
        conn.close()
        return [{
            'id': row[0], 'title': row[1], 'description': row[2], 'threat_type': row[3],
            'severity': row[4], 'status': row[5], 'created_at': row[6], 'resolved_at': row[7],
            'resolution_time_hours': row[8], 'assigned_to': row[9]
        } for row in incidents]

    def get_all_datasets(self) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM datasets_metadata ORDER BY created_at DESC")
        datasets = cursor.fetchall()
        conn.close()
        return [{
            'id': row[0], 'name': row[1], 'source_department': row[2], 'size_mb': row[3],
            'row_count': row[4], 'column_count': row[5], 'quality_score': row[6],
            'last_accessed': row[7], 'created_at': row[8], 'sensitivity': row[9]
        } for row in datasets]

    def get_all_it_tickets(self) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM it_tickets ORDER BY created_at DESC")
        tickets = cursor.fetchall()
        conn.close()
        return [{
            'id': row[0], 'title': row[1], 'description': row[2], 'status': row[3],
            'assigned_to': row[4], 'current_stage': row[5], 'priority': row[6],
            'created_at': row[7], 'resolved_at': row[8], 'time_in_stage_hours': row[9], 'category': row[10]
        } for row in tickets]

    def create_cyber_incident(self, data: Dict[str, Any]) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cyber_incidents 
            (title, description, threat_type, severity, status, created_at, resolved_at, resolution_time_hours, assigned_to)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['title'], data['description'], data['threat_type'],
            data['severity'], data['status'], data['created_at'], 
            data.get('resolved_at'), data.get('resolution_time_hours'),
            data.get('assigned_to')
        ))
        incident_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return incident_id

    def create_dataset(self, data: Dict[str, Any]) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO datasets_metadata 
            (name, source_department, size_mb, row_count, column_count, quality_score, last_accessed, created_at, sensitivity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'], data['source_department'], data['size_mb'], data['row_count'],
            data['column_count'], data.get('quality_score'), data.get('last_accessed'),
            data.get('created_at'), data.get('sensitivity')
        ))
        dataset_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return dataset_id

    def create_it_ticket(self, data: Dict[str, Any]) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO it_tickets 
            (title, description, status, assigned_to, current_stage, priority, created_at, resolved_at, time_in_stage_hours, category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['title'], data['description'], data['status'], data['assigned_to'],
            data['current_stage'], data.get('priority', 'Medium'), data['created_at'],
            data.get('resolved_at'), data.get('time_in_stage_hours'), data.get('category')
        ))
        ticket_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return ticket_id

    def update_ticket_status(self, ticket_id: int, status: str, current_stage: str) -> bool:
        """Update the status and stage of an IT ticket."""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE it_tickets 
                SET status = ?, current_stage = ?, 
                    resolved_at = CASE WHEN ? = 'Resolved' OR ? = 'Closed' THEN CURRENT_TIMESTAMP ELSE resolved_at END
                WHERE id = ?
            ''', (status, current_stage, status, status, ticket_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating ticket status: {e}")
            return False
        finally:
            conn.close()

    def update_dataset_quality(self, dataset_id: int, quality_score: float) -> bool:
        """Update the quality score of a dataset."""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE datasets_metadata 
                SET quality_score = ?, last_accessed = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (quality_score, dataset_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating dataset quality: {e}")
            return False
        finally:
            conn.close()

    def update_incident_status(self, incident_id: int, status: str) -> bool:
        """Update the status of a security incident."""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE cyber_incidents 
                SET status = ?, 
                    resolved_at = CASE WHEN ? = 'Resolved' THEN CURRENT_TIMESTAMP ELSE resolved_at END,
                    resolution_time_hours = CASE 
                        WHEN ? = 'Resolved' AND resolution_time_hours IS NULL 
                        THEN (julianday(CURRENT_TIMESTAMP) - julianday(created_at)) * 24 
                        ELSE resolution_time_hours 
                    END
                WHERE id = ?
            ''', (status, status, status, incident_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating incident status: {e}")
            return False
        finally:
            conn.close()

    def delete_it_ticket(self, ticket_id: int) -> bool:
        """Delete an IT ticket."""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM it_tickets WHERE id = ?', (ticket_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting ticket: {e}")
            return False
        finally:
            conn.close()

    def delete_dataset(self, dataset_id: int) -> bool:
        """Delete a dataset."""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM datasets_metadata WHERE id = ?', (dataset_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting dataset: {e}")
            return False
        finally:
            conn.close()

    def delete_incident(self, incident_id: int) -> bool:
        """Delete a security incident."""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM cyber_incidents WHERE id = ?', (incident_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting incident: {e}")
            return False
        finally:
            conn.close()

    def get_statistics(self) -> Dict[str, Any]:
        """Get platform statistics."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # User count
        cursor.execute("SELECT COUNT(*) FROM users")
        stats['user_count'] = cursor.fetchone()[0]
        
        # Incident stats
        cursor.execute("SELECT COUNT(*) FROM cyber_incidents")
        stats['total_incidents'] = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM cyber_incidents WHERE status = 'Open'")
        stats['open_incidents'] = cursor.fetchone()[0]
        
        # Dataset stats
        cursor.execute("SELECT COUNT(*) FROM datasets_metadata")
        stats['total_datasets'] = cursor.fetchone()[0]
        cursor.execute("SELECT COALESCE(AVG(quality_score), 0) FROM datasets_metadata")
        stats['avg_quality'] = cursor.fetchone()[0]
        
        # Ticket stats
        cursor.execute("SELECT COUNT(*) FROM it_tickets")
        stats['total_tickets'] = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM it_tickets WHERE status = 'Open'")
        stats['open_tickets'] = cursor.fetchone()[0]
        
        conn.close()
        return stats