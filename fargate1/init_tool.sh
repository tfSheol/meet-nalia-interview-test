#!/usr/bin/env bash

value=$(awk -F "=" '/$1/ {print $2}' config.ini)
echo $value