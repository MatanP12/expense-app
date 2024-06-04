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

        stage('build'){
            steps {
                sh "docker-compose build"

            }
        }        

        stage('Unit tests'){
            steps {
		        sh '''#!/bin/bash
                    docker build --tag unit_tests:latest ./unit_tests
                    docker network create test_network
                    docker run -d --rm --name server --network=test_network expense_app-app:latest
                    docker run --rm --name unit_test --network=test_network unit_tests:latest
                    docker network disconnect test_network server
                '''
            }
        }

        stage('E2E tests'){
            steps {
                sh "docker-compose up -d"
		        sh '''#!/bin/bash
                    # Build e2e tests image
                    docker build --tag e2e_tests ./e2e_tests
                    # create a network and connect the proxy server
                    docker network connect test_network expense_app-proxy-1
                    # run the test container
                    docker run --network=test_network --rm --name e2e_test e2e_tests
                    docker network disconnect test_network expense_app-proxy-1
                '''
                sh "docker-compose down"
            }
        }


		stage('Fetch tag from remote repository'){
            when {
                expression {
                    return BRANCH_NAME == "main"
                }
            }            
            steps {
				script{
                    def last_digit = 0
                    echo "Fetching tags from git"
                    sshagent(credentials: ['0c049907-e9ed-49b8-a0ab-496edbf082b9']) {
                        sh """git fetch --tags"""
                    }
                    def git_tags= sh(script: "git tag -l --sort=-v:refname", returnStdout: true).trim()
                    echo "Git tags=${git_tags}"

                    if(git_tags != "") {
                        last_version = git_tags.tokenize("\n")[0]
                        last_version = last_version.tokenize(".")
                        major  = last_version[0].toInteger()
                        minor = last_version[1].toInteger()
                        patch = last_version[2].toInteger()
                        patch = (patch+1)%10
                        if(patch == 0){
                            minor = (minor+1)
                        }
                        RELEASE_TAG="${major}.${minor}.${patch}"
                    }
				}
			}
		}

		stage('Push expense app image to registry'){
            when {
                expression {
                    return BRANCH_NAME == "main"
                }
            }            
            steps{
                sh """docker tag ${APP_IMAGE_NAME}:latest ${ECR_REGISTRY}:${RELEASE_TAG}"""
                // withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'b4499036-3a99-44a4-a946-9c2ef50b8387']]) {
                    sh """aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY"""
                // }
                sh """docker push ${ECR_REGISTRY}:${RELEASE_TAG}"""

            }
		}	

        stage('Upload static files to S3'){
            steps {
                // withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'b4499036-3a99-44a4-a946-9c2ef50b8387']]) {
                    sh "aws s3 --recursive cp src/templates s3://matan-bucket/static"
                    sh "aws s3 --recursive cp nginx/ s3://matan-bucket/nginx"
                // }

            }
        }
        
        stage('Publish tag to Deployment'){
            when {
                expression {
                    return BRANCH_NAME == "main"
                }
            }
            steps {
                sshagent(credentials: ['84a90b8c-8d65-4b26-9197-4cccb29c67a3']) {
                    withCredentials([string(credentialsId:'244629c4-47e5-46fa-ba4a-fa710688d80c', variable: 'repo')]){
                        sh """git clone ${repo}"""
                    }
                    dir('expense-app-gitops') {
                        sh '''
                            sed -i 's/appVersion: [0-9]\\+\\.[0-9]\\+\\.[0-9]\\+/appVersion: '''+RELEASE_TAG+'''/' Chart.yaml 
                            git commit -am "Pipeline Update to version '''+RELEASE_TAG+'''"
                            git push origin main
                        '''                 
                    }
                }
            }        
        }   

        stage('Add new to git tag'){
            when {
                expression {
                    return BRANCH_NAME == "main"
                }
            }
            steps {
                sshagent(credentials: ['0c049907-e9ed-49b8-a0ab-496edbf082b9']) {
                    sh """git tag ${RELEASE_TAG}"""
                    sh """git push origin ${RELEASE_TAG}"""
                }
            }        
        }          

    }

    post {
		always {
            sh 'docker network disconnect test_network expense_app-proxy-1 || true'
            sh 'docker network rm test_network || true'
            sh 'docker-compose down -v || true'
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