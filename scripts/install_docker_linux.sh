#!/bin/bash

echo '====> updating local ppas'
sudo apt-get update
sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(. /etc/os-release; echo "$UBUNTU_CODENAME") stable"

echo '====> catting repo list for verification'
cat /etc/apt/sources.list.d/additional-repositories.list 

echo '====> installing docker'
sudo apt-get update
sudo apt-get -y  install docker-ce docker-compose

echo '====> setting up docker user'
sudo usermod -aG docker $USER
docker run --rm -it  --name test alpine:latest /bin/sh

echo '====> restart your computer or at least sign out and in again to use docker'
