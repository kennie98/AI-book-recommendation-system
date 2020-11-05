#!/bin/bash

docker build ./ -t service-manager:latest
kubectl delete deployment/service-manager-deployment
kubectl apply -f k8s.yaml