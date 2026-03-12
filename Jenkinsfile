pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                echo 'Code checked out from GitHub!'
            }
        }
        stage('Test') {
            steps {
                echo 'Running pytest tests...'
                sh '''
                    docker run --rm \
                        -v $(pwd)/backend:/app \
                        -w /app \
                        python:3.11-slim \
                        sh -c "pip install -r requirements.txt -q && pip install pytest -q && PYTHONPATH=. pytest tests/ -v"
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