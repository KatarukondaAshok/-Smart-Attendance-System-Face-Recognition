#!/bin/bash
set -e

echo "===== Starting FastAPI backend on 127.0.0.1:8000 ====="
uvicorn backend.app:app --host 127.0.0.1 --port 8000 --log-level info &

echo "===== Waiting for backend to become ready ====="
READY=0
for i in $(seq 1 60); do
    if curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/ 2>/dev/null | grep -q "200"; then
        echo "Backend is up (after ${i}s)."
        READY=1
        break
    fi
    sleep 1
done

if [ "$READY" -ne 1 ]; then
    echo "WARNING: backend did not respond within 60s. Starting frontend anyway"
    echo "so you can still see the error in the Streamlit UI / container logs."
fi

echo "===== Starting Streamlit frontend on 0.0.0.0:7860 ====="
exec streamlit run frontend/kiosk.py \
    --server.port 7860 \
    --server.address 0.0.0.0 \
    --server.headless true \
    --browser.gatherUsageStats false
