docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker network rm my-network