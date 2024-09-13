# Configuring Database and Cloud

## Configuring Database

To create a database on render and creating a environment file, follow the given steps

1. Visit the [website](https://render.com/) and create an account or sign in. 
2. Next, choose a new service as PostgreSQL to create a new database service. 
3. Give an appropriate name to the database and the instance name.
4. Select <b>Free</b> option in the Instance type and hit <b>Create Database</b> button at the bottom.

A new empty PostgreSQL database service will then be created. You can view all the services on your Render Dashboard.
> **Note** <br>
> The PostgreSQL database service will remain free on render only upto 3 months.

## Configuring Cloud

To create cloud locally using LocalStack, follow the steps given below

1. Install Docker on your machine.
2. Pull and run LocalStack in Docker: ```docker run --rm -it -p 4566:4566 -p 4510-4559:4510-4559 localstack/localstack```
3. Install AWS on your machine
4. Run: ```aws configure```
5. Setup the required credentials
6. Once LocalStack is running, you can create an S3 bucket with the AWS CLI: ```aws --endpoint-url=http://localhost:4566 s3 mb s3://my-pii-bucket```
7. Now, you can upload your files to bucket using: ```aws --endpoint-url=http://localhost:4566 s3 cp /path/to/your/file.txt s3://my-pii-bucket/```

