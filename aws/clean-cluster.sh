#!/usr/bin/env bash

aws ecs delete-service --cluster fargate-cluster --service fargate-service --force
aws ecs delete-cluster --cluster fargate-cluster