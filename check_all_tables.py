import sqlite3

def check_database_schema():
    try:
        # Connect to the backend database
        conn = sqlite3.connect('curagenie-backend/curagenie.db')
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("All tables in backend database:")
        for table in tables:
            table_name = table[0]
            print(f"\n📋 Table: {table_name}")
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            print("  Columns:")
            for col in columns:
                print(f"    - {col[1]} ({col[2]}) {'NOT NULL' if col[3] else 'NULL'} {'PK' if col[5] else ''}")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  Records: {count}")
            
            # Show a few sample records if any exist
            if count > 0 and count <= 5:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                rows = cursor.fetchall()
                if rows:
                    print("  Sample data:")
                    for row in rows:
                        print(f"    {row}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_database_schema()
