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
                    cd backend
                    pip3 install -r requirements.txt --quiet --break-system-packages
                    pip3 install pytest --quiet --break-system-packages
                    PYTHONPATH=. pytest tests/ -v
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