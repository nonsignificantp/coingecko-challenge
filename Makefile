all: tidy deploy

tools:
	nvm install --lts
	npm install -g \
		serverless \
		serverless-python-requirements

tidy:
	isort app/ tests/
	black app/ tests/

deploy:
	serverless deploy --stage sandbox