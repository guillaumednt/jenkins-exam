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
                            sleep 6
                            '''
                        }
                    }
                }

                stage('Build Cast Service') {
                    steps {
                        script {
                            sh '''
                            docker build -t $DOCKER_ID/cast-service:$DOCKER_TAG cast-service/
                            sleep 6
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
                    helm upgrade --install cast-service-db helm-charts/cast-service-db/ --namespace test
                    helm upgrade --install movie-service-db helm-charts/movie-service-db/ --namespace test
                    sleep 5
                    helm upgrade --install cast-service-fastapi helm-charts/movie-service-fastapi/ --namespace test --set image.tag=v.${BUILD_ID}.0
                    helm upgrade --install movie-service-fastapi helm-charts/movie-service-fastapi/ --namespace test --set image.tag=v.${BUILD_ID}.0
                    sleep 5 
                    helm upgrade --install nginx helm-charts/nginx/ --namespace test
                    NODE_PORT=$(kubectl get svc nginx-service -o jsonpath='{.spec.ports[0].nodePort}')
                    curl http://localhost:$NODEPORT/api/v1/movies
                    curl http://localhost:$NODEPORT/api/v1/casts
                    helm uninstall nginx
                    helm uninstall cast-service-fastapi
                    helm uninstall movie-service-fastapi
                    helm uninstall cast-service-db
                    helm uninstall movie-service-db
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
        success {
            echo "Pipeline terminé avec succès."
        }
        failure {
            echo "Le pipeline a échoué."
        }
    }
}

// // Fonction pour déployer les bases de données
// def deployDatabase(dbName, env) {
//     sh """
//         helm upgrade --install ${dbName} helm-charts/${dbName} \\
//             --namespace=${env} --kubeconfig=${KUBECONFIG_CREDENTIALS}
//     """
// }





