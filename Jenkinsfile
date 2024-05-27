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

	stages {

		stage('Package'){
		    steps {
		        echo "Create image"
		        sh "docker compose build"
		    }
		}
		
        stage('E2E tests'){
            steps {
		        echo "Do e2e tests"
                sh "docker compose up"
		        sh "./e2e_tests/tests.sh"
                sh "docker compose down"
            }
        }

		stage('Package Maven'){
            steps {
		        echo "Start Maven package"
		        sh "mvn verify"
            }
		}

        stage('Create terrafrom infrastracture'){
            when {
                expression {
                    return COMMIT_MESSAGE != ''
                }
            }
            steps {
                    sh '''#/bin/bash
                    terraform -chdir=./provision init
                    terraform workspace select default
                    TIME_SINCE_EPOCH=$(date +%s)
                    WORKSPACENAME="ted-search-$TIME_SINCE_EPOCH"
                    terraform -chdir=./provision workspace new ${WORKSPACENAME}
                    terraform -chdir=./provision apply -var-file=values.tfvars -auto-approve
                    '''                       
            }
		}



        stage('E2E tests'){
            when {
                expression {
                    return COMMIT_MESSAGE != ''
                }
            }
            steps {
                sh '''#!/bin/bash
                ip_address=$(terraform -chdir=./provision output -raw instance_ip)
                echo "$ip_address"
                ./e2e_test.sh $ip_address
                '''
            }
        }

	}

	post {
		always {
            sh "terraform -chdir=./provision destroy -var-file=values.tfvars -auto-approve || true"
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