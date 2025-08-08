#!/bin/bash
set -e

IMAGE_NAME="yourusername/california-housing-app:latest"

if [ "$DEPLOY_TARGET" == "local" ]; then
    echo "Deploying locally..."
    docker stop housing-app || true
    docker rm housing-app || true
    docker run -d --name housing-app -p 5000:5000 $IMAGE_NAME
elif [ "$DEPLOY_TARGET" == "ec2" ]; then
    echo "Deploying to EC2..."
    ssh -o StrictHostKeyChecking=no -i "$EC2_KEY" $EC2_USER@$EC2_HOST \
    "docker stop housing-app || true && \
     docker rm housing-app || true && \
     docker pull $IMAGE_NAME && \
     docker run -d --name housing-app -p 5000:5000 $IMAGE_NAME"
else
    echo "No valid DEPLOY_TARGET provided."
    exit 1
fi