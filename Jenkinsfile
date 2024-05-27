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


        stage('Publish'){
            steps {
                sh '''#!/bin/bash

                
                
                '''
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