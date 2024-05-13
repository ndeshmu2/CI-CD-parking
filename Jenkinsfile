pipeline {
    agent any

    environment {
        AWS_CREDENTIALS = credentials('jenkins')
    }

    stages {
        stage('Init Terraform') {
            steps {
                dir('terraform') {  // Ensure you are in the right directory
                    script {
                        terraform.init()
                    }
                }
            }
        }
        stage('Apply Terraform') {
            steps {
                dir('terraform') {  // Ensure you are in the right directory
                    script {
                        terraform.apply(autoApprove: true)
                    }
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
