pipeline {
    agent any
    environment {
        AWS_CREDENTIALS = credentials('jenkins')
    }

    stages {
        stage('Init Terraform') {
            steps {
                script {
                    terraform.init()
                }
            }
        }
        stage('Apply Terraform') {
            steps {
                script {
                    terraform.apply(autoApprove: true)
                }
            }
        }
    }
    post {
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Deployment failed.'
        }
    }
}

