pipeline {
    agent any
    
    environment {
        DOCKERHUB_USERNAME = "<dockerhub_username>"
        DOCKER_ID = "guillaumednt"
        DOCKERHUB_PASS = credentials('DOCKER_HUB_PASS')
        KUBECONFIG = credentials('config')         
        DOCKER_TAG = "v.${BUILD_ID}.0"
    }
    
    stages {

        stage('Build Docker Images') {
            parallel {
                stage('Build Movie Service') {
                    steps {
                        script {
                            sh '''
                            docker build -t $DOCKER_ID/movie-service:$DOCKER_TAG movie-service/
                            '''
                        }
                    }
                }

                stage('Build Cast Service') {
                    steps {
                        script {
                            sh '''
                            docker build -t $DOCKER_ID/cast-service:$DOCKER_TAG cast-service/
                            '''
                        }
                    }
                }
            }
        }

        stage('Acceptance test') {
            steps {
                script {
                    sh '''
                    docker-compose up -d
                    '''

                }
                script {
                    def url = 'http://localhost:8090/api/v1/movies/'
                    def statusCode = sh(script: "curl -o /dev/null -s -w '%{http_code}' ${url}", returnStdout: true).trim()

                    if (statusCode != '200') {
                        error "HTTP status code is ${statusCode}. Expected 200."
                    } else {
                        echo "HTTP status code is 200. Test passed."
                    }
                script {
                    sh '''
                    docker-compose down 
                    '''
                }
            }
        }

        // stage('Push Docker Images') {
        //     steps {
        //         script {
        //             docker.withRegistry("https://index.docker.io/v1/", DOCKERHUB_CREDENTIALS) {
        //                 sh "docker push ${DOCKERHUB_USERNAME}/movie-service:${IMAGE_TAG}"
        //                 sh "docker push ${DOCKERHUB_USERNAME}/cast-service:${IMAGE_TAG}"
        //             }
        //         }
        //     }
        // }

        // stage('Deploy Movie Database') {
        //     steps {
        //         script {
        //             deployDatabase('movie-db', params.DEPLOY_ENV)
        //         }
        //     }
        // }

        // stage('Deploy Cast Database') {
        //     steps {
        //         script {
        //             deployDatabase('cast-db', params.DEPLOY_ENV)
        //         }
        //     }
        // }

        // stage('Deploy Nginx') {
        //     steps {
        //         script {
        //             deployNginx(params.DEPLOY_ENV)
        //         }
        //     }
        // }

        // stage('Deploy Movie Service to Kubernetes') {
        //     steps {
        //         script {
        //             deployMovieService(params.DEPLOY_ENV)
        //         }
        //     }
        // }

        // stage('Deploy Cast Service to Kubernetes') {
        //     steps {
        //         script {
        //             deployCastService(params.DEPLOY_ENV)
        //         }
        //     }
        // }

        // stage('Manual Approval for Production Deployment') {
        //     when {
        //         branch 'master'
        //         expression { return params.DEPLOY_ENV == 'prod' }
        //     }
        //     steps {
        //         input message: 'Approve Production Deployment?', ok: 'Deploy'
        //         script {
        //             deployMovieService('prod')
        //             deployCastService('prod')
        //             deployDatabase('movie-db', 'prod')
        //             deployDatabase('cast-db', 'prod')
        //             deployNginx('prod')
        //         }
        //     }
        // }
    }

    post {
        always {
            steps {
                script {
                    sh 'docker-compose down'
                }
            }
        }
        success {
            echo "Pipeline terminé avec succès."
        }
        failure {
            echo "Le pipeline a échoué."
        }
    }
}





