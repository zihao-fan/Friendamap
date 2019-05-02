docker network create my-network
docker build -t webserver ./webserver
docker build -t my-mysql ./my-mysql
docker run -d -p 3306:3306 --network my-network --name my-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw my-mysql
sleep 15
docker run -d -p 5000:5000 --network my-network --name webserver -e FLASK_APP=webserver.py webserver