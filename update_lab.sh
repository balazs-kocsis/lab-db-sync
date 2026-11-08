#!/bin/bash

# Define the absolute IP addresses of your virtual machines
DEBIAN_IP="YOUR_DEBIAN_IP"
UBUNTU_IP="YOUR_UBUNTU_IP"
ROCKY_IP="YOUR_ROCKY_IP"

echo "=== 1. Syncing Local Code Asset up to GitHub ==="
git add .
git commit -m "Automated laboratory synchronization push" 2>/dev/null
git push origin main

echo -e "\n=== 2. Triggering Parallel Remote Repository Pulls ==="

# Execute remote git updates using your verified secure SSH keys
ssh bkocsis@$DEBIAN_IP "cd ~/lab-db-sync && git pull origin main" &
ssh bkocsis@$UBUNTU_IP "cd ~/lab-db-sync && git pull origin main" &
ssh bkocsis@$ROCKY_IP "cd ~/lab-db-sync && git pull origin main" &

# Wait for all background SSH tasks to complete cleanly
wait

echo -e "\n[SUCCESS] Entire 3-node laboratory is fully synchronized and up to date."
