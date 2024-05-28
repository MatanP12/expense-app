def RELEASE_TAG='1.0.0'

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

		stage('Fetch tag from remote repository'){
			steps {
				script{
                    def last_digit = 0
                    echo "Fetching tags from git"
                    sshagent(credentials: ['99336589-4c5e-4b61-af8c-b6fe709d54b0']) {
                        sh """git fetch --tags"""
                    }
                    def git_tags= sh(script: "git tag -l --sort=-v:refname", returnStdout: true).trim()
                    echo "Git tags=${git_tags}"

                    if(git_tags != "") {
                        last_version = git_tags.tokenize("\n")[0]
                        last_digit = last_version.tokenize(".")[2].toInteger()
                        last_digit += 1
                    }
                    new_tag= "${version}.${last_digit}"
                    echo "New tag!===>${new_tag}"
                    RELEASE_TAG = new_tag
                    echo "RELEASE TAG====>${RELEASE_TAG}"
                    echo "BRANCH=========>${BRANCH_NAME}"
				}
			}
		}


        stage('build'){
            steps {
                echo "Here suppose to be a build, but we are using python"
            }
        }        



        stage('Unit tests'){
            steps {
		        sh "./unit_tests/tests.sh"
            }
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
            steps{
                sh """docker tag ${APP_IMAGE_NAME}:latest ${ECR_REGISTRY}:${RELEASE_TAG}"""
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'b4499036-3a99-44a4-a946-9c2ef50b8387']]) {
                    sh """aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY"""
                }
                sh """docker push ${ECR_REGISTRY}:${RELEASE_TAG}"""

            }
		}	

        stage('Add new tag'){
            steps {
                	sshagent(credentials: ['99336589-4c5e-4b61-af8c-b6fe709d54b0']) {
                        sh """git tag ${RELEASE_TAG}"""
                        sh """git push origin ${RELEASE_TAG}"""
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