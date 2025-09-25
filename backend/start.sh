#!/bin/bash
# Install Python dependencies
pip install -r requirements.txt

# Launch FastAPI with Uvicorn
uvicorn main:app --host 0.0.0.0 --port 5000
