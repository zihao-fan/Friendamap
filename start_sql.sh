docker build -t my-mysql ./my-mysql
docker run -d -p 3306:3306 --name my-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw my-mysql