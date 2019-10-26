How to push lambda to AWS

Run "pip3 install -r requirements.txt -t skill_env" in parent directory to install dependencies (only needs to be done once)

Enter into skill_env directory
Delete old lambda_function.py, lambda.zip if needed
Create zip file using command "zip lambda.zip *"
Enter lambda function assignment-hacker in AWS management console, choose upload .zip file and upload lambda.zip
Make sure Handler is "lambda_function.lambda_handler"

