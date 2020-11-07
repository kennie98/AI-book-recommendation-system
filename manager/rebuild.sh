#!/bin/bash

docker build ./ -t hpl-service-manager:latest
kubectl delete deployment/hpl-service-manager-deployment
kubectl apply -f k8s.yaml