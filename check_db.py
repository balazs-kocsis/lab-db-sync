import pymysql

try:
    # Connect to the local database workspace as the analyst user
    connection = pymysql.connect(
        host='localhost',
        user='ds_analyst',
        password='AnalystPass123!',
        database='lab_analytics'
    )
    with connection.cursor() as cursor:
        # Count the total telemetry records logged in the database
        cursor.execute("SELECT COUNT(*) FROM performance_logs")
        total_records = cursor.fetchone()[0]
        
        print(f"=== Database Integrity Check ===")
        print(f"[ONLINE] Connected to lab_analytics successfully.")
        print(f"[DATA] Total telemetry logs recorded across the lab: {total_records}")
        
except Exception as e:
    print(f"[ERROR] Could not query database: {e}")
finally:
    if 'connection' in locals():
        connection.close()

