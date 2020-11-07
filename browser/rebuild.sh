#!/bin/bash
docker rmi $(docker images | grep "^<none>" | awk '{ print $3 }')
docker rmi -f hpl-browser:latest
docker build ./ -t hpl-browser:latest
kubectl delete deployment/hpl-browser-deployment
kubectl apply -f k8s.yaml