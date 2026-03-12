pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                echo 'Code checked out from GitHub!'
                sh 'find . -name "requirements.txt"'
            }
        }
        stage('Test') {
            steps {
                echo 'Running pytest tests...'
                sh '''
                    docker run --rm -v $(pwd)/backend:/app -w /app python:3.11-slim sh -c "ls -la /app && pip install -r /app/requirements.txt -q && pip install pytest -q && PYTHONPATH=/app pytest tests/ -v"
                '''
            }
        }
        stage('Build') {
            steps {
                echo 'Building Docker images...'
                sh 'docker-compose -f docker/docker-compose.yml build'
            }
        }
    }
}