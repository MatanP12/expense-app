def COMMIT_MESSAGE=""

pipeline {
	agent any
	options {
		timestamps()
		timeout(time:10, unit:'MINUTES')
		buildDiscarder(logRotator(
			numToKeepStr: '4',
			daysToKeepStr:'3',
			artifactNumToKeepStr:'10'))
	}


    environment {
        ECR_REGISTRY="644435390668.dkr.ecr.ap-south-1.amazonaws.com/matan-protfolio"
        AWS_DEFAULT_REGION="ap-south-1"
        APP_IMAGE_NAME="expense_app-app"
    }


	stages {

        stage('build'){
            sh '''
                pip install -f requirments.py
            '''
        }        

        stage('Unit tests'){
            echo "Here are tests that suppose to run in pytests, I don't want to create another Dockerfile for pytests"
        }

		stage('Package'){
		    steps {
		        echo "Create image"
		        sh '''
                    docker-compose build
                    '''
		    }
		}
		
        stage('E2E tests'){
            steps {
		        echo "Do e2e tests"
                sh '''
                    docker-compose up -d
                '''
		        sh "./e2e_tests/tests.sh"
                sh "docker-compose down"
            }
        }


		stage('Push expense app image to registry'){
            when { expression { env.BRANCH_NAME == 'main' } }
                steps{
					sh """docker tag ${APP_IMAGE_NAME}:latest ${ECR_REGISTRY}:latest"""
				    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'b4499036-3a99-44a4-a946-9c2ef50b8387']]) {
                        sh """aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY"""
                    }
		        	sh """docker push ${ECR_REGISTRY}:latest"""

    		    }
		    }	
    }

	post {
		always {
            cleanWs()
		}
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed'
        }
	}
}