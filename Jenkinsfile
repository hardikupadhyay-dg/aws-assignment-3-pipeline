pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'
        S3_BUCKET = 'aws-assignment-three'
        STACK_NAME = 'sample-step-function-stack'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Package Lambdas') {
            steps {
            bat '''
            cd lambdas\\create-ami
            powershell -command "Compress-Archive -Path * -DestinationPath ..\\..\\create-ami.zip -Force"

            cd ..\\launch-instance
            powershell -command "Compress-Archive -Path * -DestinationPath ..\\..\\launch-instance.zip -Force"
            '''
        }
    }
}

        stage('Validate CloudFormation') {
            steps {
                withAWS(credentials: 'aws-creds', region: "${AWS_REGION}") {
                    bat """
                    aws cloudformation validate-template \
                        --template-body file://template.yaml
                    """
                }
            }
        }

        stage('Upload Artifacts to S3') {
            steps {
                withAWS(credentials: 'aws-creds', region: "${AWS_REGION}") {
                    bat """
                    aws s3 cp create-ami.zip s3://${S3_BUCKET}/lambda/create-ami.zip
                    aws s3 cp launch-instance.zip s3://${S3_BUCKET}/lambda/launch-instance.zip
                    aws s3 cp statemachines/sample-step-function.json s3://${S3_BUCKET}/statemachines/sample-step-function.json
                    """
                }
            }
        }

        stage('Deploy CloudFormation Stack') {
            steps {
                withAWS(credentials: 'aws-creds', region: "${AWS_REGION}") {
                    bat """
                    aws cloudformation deploy \
                        --stack-name ${STACK_NAME} \
                        --template-file template.yaml \
                        --capabilities CAPABILITY_NAMED_IAM \
                        --parameter-overrides ArtifactBucketName=${S3_BUCKET}
                    """
                }
            }
        }

        stage('Trigger Step Function (Optional)') {
            when { expression { return params.RUN_STEP_FUNCTION == true } }
            steps {
                withAWS(credentials: 'aws-creds', region: "${AWS_REGION}") {
                    bat '''
                    STEP_ARN=$(aws cloudformation describe-stacks \
                        --stack-name ${STACK_NAME} \
                        --query "Stacks[0].Outputs[?OutputKey=='StateMachineArn'].OutputValue" \
                        --output text)

                    aws stepfunctions start-execution \
                        --state-machine-arn $STEP_ARN \
                        --input '{"step_function_name":"jenkins-run","step_function_launch_time":"now","existing-instance-id":"i-xxxxxxxx"}'
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully."
        }
        failure {
            echo "Pipeline failed!"
        }
    }
}
