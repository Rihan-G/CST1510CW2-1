"""
Database Seeder - Run this script to populate the database with sample data.
Executes the seed_data.sql file to insert 160+ sample records.
"""

import sqlite3
import os

def seed_database():
    """Seed the database by executing the SQL file."""
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sql_file = os.path.join(script_dir, 'seed_data.sql')
    db_path = os.path.join(os.path.dirname(script_dir), 'intelligence_platform.db')
    
    print("🌱 Seeding database with sample data...")
    print(f"   Database: {db_path}")
    print(f"   SQL File: {sql_file}")
    
    if not os.path.exists(sql_file):
        print(f"❌ Error: SQL file not found at {sql_file}")
        return False
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Read and execute SQL file
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Execute the SQL script
        cursor.executescript(sql_script)
        
        # Commit changes
        conn.commit()
        
        # Get counts
        cursor.execute("SELECT COUNT(*) FROM cyber_incidents")
        cyber_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM it_tickets")
        ticket_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM datasets_metadata")
        dataset_count = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"\n✅ Successfully seeded database!")
        print(f"   - {cyber_count} cyber security incidents")
        print(f"   - {ticket_count} IT tickets")
        print(f"   - {dataset_count} datasets")
        print(f"   - Total: {cyber_count + ticket_count + dataset_count} records")
        
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = seed_database()
    exit(0 if success else 1)

