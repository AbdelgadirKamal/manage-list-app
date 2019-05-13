# manage-list-app
A docker container app that pulls data stored in a GIT repo and write it to memcached. 

The data is a list in yaml syntax, see the example below:
  https://github.com/AbdelgadirKamal/testing/blob/master/blacklist.yaml

The files under docker-files directory are used to build the container image using the command:
  - docker build -t manage-list-app .

To run and test the app using docker:
  1. create a test network to connect the app and memcached:
     - docker network create test
     
  2. create and run memcached container:
     - docker run --network=test --name memcached -d memcached
     
  3. create and run the manage-list-app container, use the --env-file option (see env_example):
     - docker run --network=test --env-file=manage-list-env --name manage-list-app -t -d manage-list-app
  
To deploy and test the app in K8s cluster, use manifst files in k8s-deployment folder:

  - kubectl create -f memcached-deploy.yaml
  - kubectl create -f memcached-service.yaml
  - kubectl create -f manage-list-cron.yaml

(the container app "abdelgadirkamal/manage-list-app" is available in dockerhub)
https://cloud.docker.com/repository/registry-1.docker.io/abdelgadirkamal/manage-list-app
