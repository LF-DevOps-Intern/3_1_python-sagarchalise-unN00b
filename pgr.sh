#!/bin/bash

show_help(){
    echo -e "usage: $0 url [true|false]\n"
    echo -e "description:\n"
    echo -e "\turl \t\tURL to the remote file\n"
    echo -e "\ttrue|false \tWhether to serve the file after download\n"
}

if [[ $# -eq 0 || "$1" == "-h" ]]; then
    show_help
fi

URL=$1
SERVE_FLAG=$2

if [ "$SERVE_FLAG" = "true" ]; then
    python3 new.py --url=$URL --http_server
fi
