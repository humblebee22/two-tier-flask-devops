pipeline {
    agent any

    environment {
        MYSQL_PASSWORD = credentials('mysql-password')
        FLASK_SECRET_KEY = credentials('flask-secret-key')
        MYSQL_USER = credentials('mysql-user')
        MYSQL_DATABASE = credentials('mysql-database')
        MYSQL_HOST = 'jenkins-mysql'
        MYSQL_PORT = '3306'
    }

    stages {
        stage('Fix Docker Socket') {
            steps {
                sh 'sudo chmod 666 /var/run/docker.sock'
            }
        }

        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running automated tests...'
                sh '''
                    . venv/bin/activate
                    python -m pytest tests/test_app.py -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t taskmanager-flask:latest .'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                sh '''
            docker compose down --remove-orphans || true
            docker rm -f taskmanager-mysql taskmanager-flask || true
            MYSQL_PASSWORD=$MYSQL_PASSWORD \
            FLASK_SECRET_KEY=$FLASK_SECRET_KEY \
            MYSQL_USER=$MYSQL_USER \
            MYSQL_DATABASE=$MYSQL_DATABASE \
            MYSQL_HOST=mysql \
            MYSQL_PORT=3306 \
            docker compose up -d
        '''
    }
}

        stage('Verify') {
            steps {
                echo 'Verifying deployment...'
                sh '''
            sleep 15
            FLASK_IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' taskmanager-flask)
            echo "Flask container IP: $FLASK_IP"
            curl -f http://$FLASK_IP:5000/health || exit 1
        '''
    }
}
    }

    post {
        success {
            echo 'Pipeline completed successfully. Application is running.'
        }
        failure {
            echo 'Pipeline failed. Check the logs above for details.'
            sh 'docker compose logs || true'
        }
        always {
            echo 'Cleaning up workspace...'
            sh 'rm -rf venv'
        }
    }
}