#!/bin/bash

python -m gunicorn -w $1 "main:server"
