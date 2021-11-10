#!/bin/bash

show_help(){
    echo -ne "usage: $0 url [true|false]\n"
    echo -ne "description:\n"
    echo -ne "\turl \t\tURL to the remote file\n"
    echo -ne "\ttrue|false \tWhether to serve the file after download\n"
}

if [[ $# -eq 0 || "$1" == "-h" ]]; then
    show_help
fi

URL=$1
SERVE_FLAG=$2

if [ "$SERVE_FLAG" = "true" ]; then
    python3 new.py --url=$URL --http_server
fi
