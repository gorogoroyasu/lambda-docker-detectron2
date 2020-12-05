docker build -t IMAGE_NAME .

docker run --name lambda --rm -p 9000:8080 \
	  -v ~/.aws-lambda-rie:/aws-lambda \
	    --entrypoint /aws-lambda/aws-lambda-rie \
	      IMAGE_NAME \
	        /usr/local/bin/python -m awslambdaric app.handler




