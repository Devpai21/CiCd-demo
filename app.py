from flask import Flask, jsonify, render_template
import datetime
import os
import json

app = Flask(__name__)

# Get commit hash from environment variable (set in pipeline)
COMMIT_HASH = os.getenv('COMMIT_HASH', 'local-dev')
DEPLOY_TIME = datetime.datetime.now().isoformat()

# List of services to monitor
services = [
    {"name": "API Server", "status": "healthy", "type": "backend"},
    {"name": "Database", "status": "healthy", "type": "data"},
    {"name": "Kubernetes Cluster", "status": "healthy", "type": "infrastructure"},
    {"name": "Docker Hub Registry", "status": "healthy", "type": "external"},
]

@app.route('/')
def home():
    return render_template('index.html', 
                         commit_hash=COMMIT_HASH, 
                         deploy_time=DEPLOY_TIME,
                         services=services)

@app.route('/api/status')
def api_status():
    return jsonify({
        "status": "operational",
        "commit": COMMIT_HASH,
        "deployed_at": DEPLOY_TIME,
        "services": services,
        "uptime_percentage": 99.95
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)