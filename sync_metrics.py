import sys
import subprocess
import pymysql

def get_system_metrics():
    # Dynamically extract real active process count from the VM terminal
    cmd = "ps -ef | wc -l"
    processes = int(subprocess.check_output(cmd, shell=True).decode().strip())
    return processes

def insert_metrics(hostname, os_dist, processes):
    try:
        # Connect as the restricted non-sudo analyst user
        connection = pymysql.connect(
            host='localhost',
            user='ds_analyst',
            password='AnalystPass123!',
            database='lab_analytics'
        )
        with connection.cursor() as cursor:
            # 1. Resolve the node ID for this specific host
            cursor.execute("SELECT node_id FROM server_nodes WHERE hostname = %s", (hostname,))
            result = cursor.fetchone()
            if not result:
                print(f"Error: Hostname {hostname} not found in lookup table.")
                return
            
            node_id = result[0]
            
            # 2. Insert active process count and simulated idle parameters into logs
            sql = """INSERT INTO performance_logs (node_id, cpu_idle_pct, ram_used_mb, active_processes) 
                     VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (node_id, 99.10, 250, processes))
            connection.commit()
            print(f"[SUCCESS] Committed logs for {hostname} ({os_dist}). Active processes recorded: {processes}")
            
    except Exception as e:
        print(f"[FAILURE] Database operation failed: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python sync_metrics.py <hostname> <os_distribution>")
        sys.exit(1)
        
    current_host = sys.argv[1]
    current_os = sys.argv[2]
    
    active_proc = get_system_metrics()
    insert_metrics(current_host, current_os, active_proc)

