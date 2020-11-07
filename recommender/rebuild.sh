#!/bin/bash

docker build ./ -t hpl-ai-recommender-server:latest
kubectl delete deployment/hpl-ai-recommender-deployment
kubectl apply -f k8s.yaml