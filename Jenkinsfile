#!/usr/bin/env groovy

node {
    stage("Environment Setup") {
        echo "Grab Code"
        checkout scm

        echo "Remove Old Run Data"
        sh "rm -r *test-results.xml || exit 0"

        if (!fileExists("tests/system/config.ini")) {
            echo "Copy System Tests' Configuration File"
            withCredentials([file(
                    credentialsId: "lets-do-dns-system-test-config",
                    variable: "SYSTEM_TEST_CONFIG")]) {
                sh "cp $SYSTEM_TEST_CONFIG tests/system/config.ini"
            }
        }

        echo "Create Python 2.7 Build Environment"
        python_build = docker.build("python:2.7.ldd", "-f jenkins/Dockerfile.py27 .")
    }

    stage("Build Python Artifacts") {
        python_build.inside {
            echo "Remove Old Artifacts"
            sh "rm dist/* || exit 0"

            echo "Create Source Artifact"
            sh "python setup.py sdist"

            echo "Create Wheel Artifact"
            sh "python setup.py bdist_wheel"
        }
    }

    stage("Run Python Test Suite") {
        parallel py27: {
            echo "Create Python 2.7 Environment"
            python_27 = docker.build("python:2.7.ldd", "-f jenkins/Dockerfile.py27 .")

            python_27.inside {
                echo "Install Wheel Artifact"
                sh "pip install dist/*.whl"

                echo "Run py.test Test Suite"
                try {
                    sh "py.test --pylama --junit-xml py27-test-results.xml --junit-prefix py27"
                }
                finally {
                    junit "py27-test-results.xml"
                }
            }
        }, py36: {
            echo "Create Python 3.6 Environment"
            python_36 = docker.build("python:3.6.ldd", "-f jenkins/Dockerfile.py36 .")

            python_36.inside {
                echo "Install Wheel Artifact"
                sh "pip install dist/*.whl"

                echo "Run py.test Test Suite"
                xmlFile = "py36-test-results.xml"
                try {
                    sh "py.test --pylama --junit-xml py36-test-results.xml --junit-prefix py36"
                }
                finally {
                    junit "py36-test-results.xml"
                }
            }
        }, certbot: {
            echo "Create certbot/lets-do-dns Environment"
            certbot = docker.build("lets-do-dns", ".")

            certbot.inside {
                withCredentials([string(credentialsId: 'DO_APIKEY', variable: 'DO_APIKEY'),
                                 string(credentialsId: 'DO_DOMAIN', variable: 'DO_DOMAIN'),
                                 string(credentialsId: 'CERTBOT_EMAIL', variable: 'CERTBOT_EMAIL')]) {
                    withEnv(["DO_APIKEY = $DO_APIKEY", "DO_DOMAIN = $DO_DOMAIN"]) {
                        sh """\
certbot certonly --manual\
    --manual-auth-hook lets-do-dns --manual-cleanup-hook lets-do-dns\
    --preferred-challenges dns -d test.$DO_DOMAIN --test-cert --manual-public-ip-logging-ok\
    --non-interactive --agree-tos --email $CERTBOT_EMAIL"""
                    }
                }
            }
        }
    }

    stage("Archive Python Artifacts") {
        archiveArtifacts artifacts: "dist/*",
                fingerprint: true,
                onlyIfSuccessful: true
    }
}
