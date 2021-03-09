#!/usr/bin/env bash

# see: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_AWSCLI_Fargate.html

aws ecs register-task-definition --cli-input-json file://fargate1.json
aws ecs register-task-definition --cli-input-json file://fargate2.json

aws ecs list-task-definitions