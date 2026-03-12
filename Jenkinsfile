pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                echo 'Code checked out from GitHub!'
                sh 'pwd && ls -la && ls -la backend/'
            }
        }
        stage('Test') {
            steps {
                echo 'Running pytest tests...'
                sh '''
                    BACKEND_PATH=$(pwd)/backend
                    echo "Backend path: $BACKEND_PATH"
                    ls -la $BACKEND_PATH
                    docker run --rm -v $BACKEND_PATH:/app -w /app python:3.11-slim sh -c "ls -la && pip install -r requirements.txt -q && pip install pytest -q && PYTHONPATH=. pytest tests/ -v"
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