#!/bin/bash
cd /home/ubuntu/hris
source venv/bin/activate

# Kill anything on port 8090
kill $(lsof -ti:8090) 2>/dev/null
sleep 1

python -m uvicorn main:app --host 0.0.0.0 --port 8090 &
echo "Server started with PID $!"
sleep 3

# Check if running
if curl -s http://localhost:8090/docs > /dev/null; then
    echo "✅ Server is running on port 8090"
else
    echo "❌ Server failed to start"
fi
