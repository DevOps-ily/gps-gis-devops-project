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
                    docker build -t gps-test -f Dockerfile .
                    docker run --rm -e DATABASE_URL=sqlite:///test.db gps-test sh -c "pip install pytest -q && PYTHONPATH=. pytest tests/ -v --ignore=tests/test_connection.py"
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