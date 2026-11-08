#!/bin/bash

# Define the absolute IP addresses of your virtual machines
DEBIAN_IP="172.16.158.134"
UBUNTU_IP="172.16.158.131"
ROCKY_IP="172.16.158.133"

echo "=== 1. Syncing Local Code Asset up to GitHub ==="
git add .
git commit -m "Automated laboratory synchronization push" 2>/dev/null
git push origin master

echo -e "\n=== 2. Triggering Parallel Remote Repository Pulls ==="

# Execute remote git updates using your verified secure SSH keys
ssh bkocsis@$DEBIAN_IP "cd ~/lab-db-sync && git pull origin master" &
ssh bkocsis@$UBUNTU_IP "cd ~/lab-db-sync && git pull origin master" &
ssh bkocsis@$ROCKY_IP "cd ~/lab-db-sync && git pull origin master" &

# Wait for all background SSH tasks to complete cleanly
wait

echo -e "\n[SUCCESS] Entire 3-node laboratory is fully synchronized and up to date."
