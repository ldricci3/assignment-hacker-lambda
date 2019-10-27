if [[ -e ./build.sh ]]; then
	rm -rf skill_env/
	pip3 install -r requirements.txt -t skill_env
	cp lambda_function.py skill_env/
	cp rds_config.py skill_env/
	zip -r lambda.zip skill_env/*
else
	echo "Error: Enter directory with script before executing."
fi
