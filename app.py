from flask import Flask, jsonify, render_template
import datetime
import os
import requests

app = Flask(__name__)

COMMIT_HASH = os.getenv('COMMIT_HASH', 'local-dev')
DEPLOY_TIME = datetime.datetime.now().isoformat()

def check_docker_hub():
    """Check if Docker Hub is accessible and the image exists"""
    try:
        response = requests.get("https://hub.docker.com/v2/repositories/devpai/cicd-demo/", timeout=5)
        if response.status_code == 200:
            return "healthy"
        else:
            return "degraded"
    except requests.exceptions.RequestException:
        return "degraded"

def check_github_actions():
    """Check if GitHub API is accessible"""
    try:
        response = requests.get("https://api.github.com/repos/Devpai21/CiCd-demo/commits", timeout=5)
        if response.status_code == 200:
            return "healthy"
        else:
            return "degraded"
    except requests.exceptions.RequestException:
        return "degraded"

def check_api_server():
    """Check if this API server is responding"""
    return "healthy"

# List of services with real status checks
services = [
    {"name": "API Server", "status": check_api_server(), "type": "backend"},
    {"name": "Docker Hub Registry", "status": check_docker_hub(), "type": "container registry"},
    {"name": "GitHub Actions CI/CD", "status": check_github_actions(), "type": "pipeline"},
]

@app.route('/')
def home():
    return render_template('index.html', 
                         commit_hash=COMMIT_HASH, 
                         deploy_time=DEPLOY_TIME,
                         services=services)

@app.route('/api/status')
def api_status():
    # Refresh statuses on API call
    return jsonify({
        "status": "operational",
        "commit": COMMIT_HASH,
        "deployed_at": DEPLOY_TIME,
        "services": [
            {"name": "API Server", "status": check_api_server()},
            {"name": "Docker Hub Registry", "status": check_docker_hub()},
            {"name": "GitHub Actions CI/CD", "status": check_github_actions()},
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)