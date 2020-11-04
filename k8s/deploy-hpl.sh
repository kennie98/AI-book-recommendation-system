#!/bin/bash

PRJ_DIR=$HOME/dev/AI_Book_Recommendation_System/
source ./helper.sh

echo ""
print_info "> Rebuild all docker images"
echo ""
#. $PRJ_DIR/recommender/local-build.sh --build
cd $PRJ_DIR/manager
docker build ./ -t manager_service-manager:latest

echo ""
echo ""
print_header "-- deploy on Minikube --"
echo ""
echo ""
if ! command -v minikube version &> /dev/null
then
  echo "Minikube not installed, start to install"
  curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb
  sudo dpkg -i minikube_latest_amd64.deb
  # need conntrack & socat
else
  print_info "> restart Minikube"
  echo ""
  minikube stop
  minikube delete
fi

sudo sysctl fs.protected_regular=0
sudo minikube start --driver=none
sudo mv /home/$USER/.kube /home/$USER/.minikube $HOME
sudo chown -R $USER /home/$USER/.kube /home/$USER/.minikube

minikube addons list
echo ""
print_info "> Minikube status"
echo ""
minikube status

echo ""
print_info "> Create hpl namespace"
echo ""
kubectl create namespace hpl

echo ""
print_info "> Apply kubernetes system config files"
echo ""
kubectl apply -f $PRJ_DIR/k8s/env-configmap.yaml


echo ""
print_info "> Apply kubernetes config for all microservices"
echo ""
kubectl apply -f $PRJ_DIR/recommender/k8s.yaml
kubectl apply -f $PRJ_DIR/manager/k8s.yaml

echo ""
print_info "> Set current namespace to hpl"
echo ""
# set default namespace to mlo-dev
kubectl config set-context --current --namespace=hpl

## waiting for the web pod to be ready
#echo ""
#print_info "> Waiting for all the pods to be ready..."
#echo ""
#kubectl wait --for=condition=ready pod --all --timeout=3000s
#
#echo ""
#print_info "> Forwarding web service port ..."
#echo ""
## expose web service
## should setup proper ingress instead of port forwarding
#kubectl port-forward deployment/web-deployment 3000 &
