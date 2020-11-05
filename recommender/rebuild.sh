#!/bin/bash

docker build ./ -t ai-recommender-server:latest
kubectl delete deployment/ai-recommender-deployment
kubectl apply -f k8s.yaml