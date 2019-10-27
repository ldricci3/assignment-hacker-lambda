#! /usr/bin/env bash

if [[ -e ./build.sh ]]; then
	rm -rf skill_env/
	rm ./lambda.zip
	pip3 install -r requirements.txt -t skill_env
	cp lambda_function.py skill_env/
	cp rds_config.py skill_env/
	cd skill_env
	zip -r lambda.zip *
	mv lambda.zip ../
else
	echo "Error: Enter directory with script before executing."
fi
