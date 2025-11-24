// pipeline {
//     agent any

//     environment {
//         AWS_REGION = 'ap-south-1'
//         S3_BUCKET = 'aws-assignment-three'
//         STACK_NAME = 'sample-step-function-stack'
//     }

//     stages {

//         stage('Checkout') {
//             steps {
//                 checkout scm
//             }
//         }

//         stage('Package Lambdas') {
//             steps {
//                 bat '''
//                 cd lambdas\\create-ami
//                 powershell -command "Compress-Archive -Path * -DestinationPath ..\\..\\create-ami.zip -Force"

//                 cd ..\\launch-instance
//                 powershell -command "Compress-Archive -Path * -DestinationPath ..\\..\\launch-instance.zip -Force"
//                 '''
//             }
//         }

//         stage('Validate CloudFormation') {
//             steps {
//                 withCredentials([
//                     string(credentialsId: 'aws-jenkins-access', variable: 'AWS_ACCESS_KEY_ID'),
//                     string(credentialsId: 'aws-jenkins-secret', variable: 'AWS_SECRET_ACCESS_KEY')
//                 ]) {
//                     bat """
//                     aws cloudformation validate-template ^
//                         --template-body file://template.yaml ^
//                         --region %AWS_REGION%
//                     """
//                 }
//             }
//         }

//         stage('Upload Artifacts to S3') {
//             steps {
//                 withCredentials([
//                     string(credentialsId: 'aws-jenkins-access', variable: 'AWS_ACCESS_KEY_ID'),
//                     string(credentialsId: 'aws-jenkins-secret', variable: 'AWS_SECRET_ACCESS_KEY')
//                 ]) {
//                     bat """
//                     aws s3 cp create-ami.zip s3://%S3_BUCKET%/lambda/create-ami.zip --region %AWS_REGION%
//                     aws s3 cp launch-instance.zip s3://%S3_BUCKET%/lambda/launch-instance.zip --region %AWS_REGION%
//                     aws s3 cp statemachines\\sample-step-function.json s3://%S3_BUCKET%/statemachines/sample-step-function.json --region %AWS_REGION%
//                     """
//                 }
//             }
//         }

//         stage('Deploy CloudFormation Stack') {
//             steps {
//                 withCredentials([
//                     string(credentialsId: 'aws-jenkins-access', variable: 'AWS_ACCESS_KEY_ID'),
//                     string(credentialsId: 'aws-jenkins-secret', variable: 'AWS_SECRET_ACCESS_KEY')
//                 ]) {
//                     bat """
//                     aws cloudformation deploy ^
//                         --stack-name %STACK_NAME% ^
//                         --template-file template.yaml ^
//                         --capabilities CAPABILITY_NAMED_IAM ^
//                         --parameter-overrides ArtifactBucketName=%S3_BUCKET% ^
//                         --region %AWS_REGION%
//                     """
//                 }
//             }
//         }

//         stage('Trigger Step Function (Optional)') {
//             when {
//                 expression { return params.RUN_STEP_FUNCTION == true }
//             }
//             steps {
//                 withCredentials([
//                     string(credentialsId: 'aws-jenkins-access', variable: 'AWS_ACCESS_KEY_ID'),
//                     string(credentialsId: 'aws-jenkins-secret', variable: 'AWS_SECRET_ACCESS_KEY')
//                 ]) {
//                     bat """
//                     for /f %%i in ('aws cloudformation describe-stacks --stack-name %STACK_NAME% --query "Stacks[0].Outputs[?OutputKey=='StateMachineArn'].OutputValue" --output text --region %AWS_REGION%') do set STEPARN=%%i

//                     aws stepfunctions start-execution ^
//                         --state-machine-arn %STEPARN% ^
//                         --input "{\\"step_function_name\\":\\"jenkins-run\\",\\"step_function_launch_time\\":\\"now\\",\\"existing-instance-id\\":\\"i-xxxxxxxx\\"}" ^
//                         --region %AWS_REGION%
//                     """
//                 }
//             }
//         }
//     }

//     post {
//         success { echo "Pipeline completed successfully." }
//         failure { echo "Pipeline failed!" }
//     }
// }


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

        stage('Validate CloudFormation') {
            steps {
                withCredentials([
                    string(credentialsId: 'aws-jenkins-access', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-jenkins-secret', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    bat """
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

        stage('Trigger Step Function (Optional)') {
            when { expression { return params.RUN_STEP_FUNCTION == true } }
            steps {
                withCredentials([
                    string(credentialsId: 'aws-jenkins-access', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-jenkins-secret', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    bat '''
                    for /f "tokens=*" %%i in ('aws cloudformation describe-stacks --stack-name %STACK_NAME% --query "Stacks[0].Outputs[?OutputKey=='StateMachineArn'].OutputValue" --output text --region %AWS_REGION%') do set STEP_ARN=%%i

                    aws stepfunctions start-execution --state-machine-arn %STEP_ARN% --input "{\\"step_function_name\\":\\"jenkins-run\\",\\"step_function_launch_time\\":\\"now\\",\\"existing-instance-id\\":\\"i-xxxxxxxx\\"}" --region %AWS_REGION%
                    '''
                }
            }
        }
    }

    post {
        success { echo "Pipeline completed successfully." }
        failure { echo "Pipeline failed!" }
    }
}
