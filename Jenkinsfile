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

//         stage('Upload Artifacts to S3') {
//             steps {
//                 withCredentials([
//                     string(credentialsId: 'aws-jenkins-access', variable: 'AWS_ACCESS_KEY_ID'),
//                     string(credentialsId: 'aws-jenkins-secret', variable: 'AWS_SECRET_ACCESS_KEY')
//                 ]) {
//                     bat """
//                     aws s3 cp create-ami.zip s3://${S3_BUCKET}/lambda/create-ami.zip --region %AWS_REGION%
//                     aws s3 cp launch-instance.zip s3://${S3_BUCKET}/lambda/launch-instance.zip --region %AWS_REGION%
//                     aws s3 cp statemachines/sample-step-function.json s3://${S3_BUCKET}/statemachines/sample-step-function.json --region %AWS_REGION%
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
//                     --stack-name sample-step-function-stack ^
//                     --template-file template.yaml ^
//                     --capabilities CAPABILITY_NAMED_IAM ^
//                     --parameter-overrides ArtifactBucketName=aws-assignment-three ^
//                     --region ap-south-1

//                     IF %ERRORLEVEL% EQU 255 (
//                         echo "No changes found, continuing pipeline..."
//                     EXIT /B 0
//                 )

//                     """
//                 }
//             }
//         }
//     }

//     post {
//         success {
//             echo "Pipeline completed successfully."
//         }
//         failure {
//             echo "Pipeline failed!"
//         }
//     }
// }



// pipeline {
//     agent any

//     environment {
//         AWS_REGION = "ap-south-1"
//         S3_BUCKET = "aws-assignment-three"
//         STACK_NAME = "sample-step-function-stack"
//     }

//     stages {

//         /* =========================
//            1. CHECKOUT SOURCE CODE
//         ==========================*/
//         stage('Checkout') {
//             steps {
//                 checkout scm
//             }
//         }

//         /* =========================
//            2. PACKAGE LAMBDAS (Windows)
//         ==========================*/
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

//         /* =========================
//            3. VALIDATE CLOUDFORMATION
//         ==========================*/
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

//         /* =========================
//            4. UPLOAD TO S3
//         ==========================*/
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

//         /* =========================
//            5. DEPLOY CLOUDFORMATION
//         ==========================*/
//         stage('Deploy CloudFormation') {
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
//     }

//     post {
//         success {
//             echo "Pipeline completed successfully."
//         }
//         failure {
//             echo "Pipeline failed!"
//         }
//     }
// }


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

//         stage('Load AWS Credentials') {
//             steps {
//                 withCredentials([
//                     string(credentialsId: 'aws-jenkins-access', variable: 'AWS_ACCESS_KEY_ID'),
//                     string(credentialsId: 'aws-jenkins-secret', variable: 'AWS_SECRET_ACCESS_KEY')
//                 ]) {
//                     bat """
//                     echo Using AWS Credentials...
//                     """
//                 }
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

//         stage('Upload Artifacts') {
//             steps {
//                 withCredentials([
//                     string(credentialsId: 'aws-jenkins-access', variable: 'AWS_ACCESS_KEY_ID'),
//                     string(credentialsId: 'aws-jenkins-secret', variable: 'AWS_SECRET_ACCESS_KEY')
//                 ]) {
//                     bat """
//                     aws s3 cp create-ami.zip s3://%S3_BUCKET%/lambda/create-ami.zip --region %AWS_REGION%
//                     aws s3 cp launch-instance.zip s3://%S3_BUCKET%/lambda/launch-instance.zip --region %AWS_REGION%
//                     aws s3 cp statemachines/sample-step-function.json s3://%S3_BUCKET%/statemachines/sample-step-function.json --region %AWS_REGION%
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

//         stage('Trigger Step Function') {
//             steps {
//                 withCredentials([
//                     string(credentialsId: 'aws-jenkins-access', variable: 'AWS_ACCESS_KEY_ID'),
//                     string(credentialsId: 'aws-jenkins-secret', variable: 'AWS_SECRET_ACCESS_KEY')
//                 ]) {
//                     bat """
//                     FOR /F "tokens=* usebackq" %%a in (`aws cloudformation describe-stacks --stack-name %STACK_NAME% --query "Stacks[0].Outputs[?OutputKey=='StateMachineArn'].OutputValue" --output text --region %AWS_REGION%`) do set STEP_ARN=%%a

//                     aws stepfunctions start-execution ^
//                         --state-machine-arn %STEP_ARN% ^
//                         --input "{\\"step_function_name\\":\\"jenkins-run\\", \\"step_function_launch_time\\":\\"now\\", \\"existing-instance-id\\":\\"i-0abcd123\\"}" ^
//                         --region %AWS_REGION%
//                     """
//                 }
//             }
//         }
//     }

//     post {
//         success { echo "Pipeline completed successfully!" }
//         failure { echo "Pipeline failed!" }
//     }
// }




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
                // compress lambda code to zips using powershell Compress-Archive
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
                        --parameter-overrides ArtifactBucketName=%S3_BUCKET% DummyVersion=1 ^
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
