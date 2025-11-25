pipeline {
    agent any

    parameters {
        string(name: 'INSTANCE_ID', defaultValue: 'i-007a79f121e7465ad', description: 'EC2 Instance ID for AMI creation')
    }

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
                powershell -Command "Compress-Archive -Path * -DestinationPath ..\\..\\create-ami.zip -Force"

                cd ..\\launch-instance
                powershell -Command "Compress-Archive -Path * -DestinationPath ..\\..\\launch-instance.zip -Force"
                '''
            }
        }

        stage('Validate CloudFormation') {
            steps {
                withCredentials([
                    string(credentialsId: 'aws-jenkins-access', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-jenkins-secret', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    bat """
                    set AWS_REGION=%AWS_REGION%
                    set AWS_ACCESS_KEY_ID=%AWS_ACCESS_KEY_ID%
                    set AWS_SECRET_ACCESS_KEY=%AWS_SECRET_ACCESS_KEY%

                    aws cloudformation validate-template --template-body file://template.yaml --region %AWS_REGION%
                    """
                }
            }
        }

        stage('Upload Artifacts to S3') {
            steps {
                withCredentials([
                    string(credentialsId: 'aws-jenkins-access', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-jenkins-secret', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    bat """
                    set AWS_REGION=%AWS_REGION%
                    set AWS_ACCESS_KEY_ID=%AWS_ACCESS_KEY_ID%
                    set AWS_SECRET_ACCESS_KEY=%AWS_SECRET_ACCESS_KEY%

                    aws s3 cp create-ami.zip s3://%S3_BUCKET%/lambda/create-ami.zip --region %AWS_REGION%
                    aws s3 cp launch-instance.zip s3://%S3_BUCKET%/lambda/launch-instance.zip --region %AWS_REGION%
                    aws s3 cp statemachines/sample-step-function.json s3://%S3_BUCKET%/statemachines/sample-step-function.json --region %AWS_REGION%
                    """
                }
            }
        }

        stage('Deploy CloudFormation Stack') {
            steps {
                withCredentials([
                    string(credentialsId: 'aws-jenkins-access', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-jenkins-secret', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    bat """
                    set AWS_REGION=%AWS_REGION%
                    set AWS_ACCESS_KEY_ID=%AWS_ACCESS_KEY_ID%
                    set AWS_SECRET_ACCESS_KEY=%AWS_SECRET_ACCESS_KEY%

                    aws cloudformation deploy ^
                        --stack-name %STACK_NAME% ^
                        --template-file template.yaml ^
                        --capabilities CAPABILITY_NAMED_IAM ^
                        --parameter-overrides ArtifactBucketName=%S3_BUCKET% ^
                        --region %AWS_REGION%
                    """
                }
            }
        }

        stage('Trigger Step Function') {
            steps {
                withCredentials([
                    string(credentialsId: 'aws-jenkins-access', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-jenkins-secret', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    bat """
                    set AWS_REGION=%AWS_REGION%
                    set AWS_ACCESS_KEY_ID=%AWS_ACCESS_KEY_ID%
                    set AWS_SECRET_ACCESS_KEY=%AWS_SECRET_ACCESS_KEY%

                    FOR /F "tokens=* USEBACKQ" %%A IN (`aws cloudformation describe-stacks --stack-name %STACK_NAME% --query "Stacks[0].Outputs[?OutputKey=='StateMachineArn'].OutputValue" --output text --region %AWS_REGION%`) DO SET STEP_ARN=%%A

                    echo Found Step Function ARN: %STEP_ARN%

                    aws stepfunctions start-execution ^
                        --state-machine-arn %STEP_ARN% ^
                        --input "{ \\"step_function_name\\": \\"jenkins-run\\", \\"step_function_launch_time\\": \\"now\\", \\"existing-instance-id\\": \\"${params.INSTANCE_ID}\\" }" ^
                        --region %AWS_REGION%
                    """
                }
            }
        }
    }

    post {
        success { echo 'Pipeline finished SUCCESS' }
        failure { echo 'Pipeline finished FAILURE' }
    }
}
