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
                    docker run --rm -e DATABASE_URL=sqlite:///test.db gps-test sh -c "pip install pytest -q && PYTHONPATH=. pytest tests/test_api.py::TestHealth::test_health_check tests/test_api.py::TestRootEndpoint::test_root tests/test_api.py::TestCapitals::test_get_nonexistent_capital -v"
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