#!/bin/bash

set -a # export all variables
source .env
set +a
python3 manage.py runserver 3000