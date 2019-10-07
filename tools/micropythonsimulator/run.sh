#!/bin/bash

aid="$1"
tid="$2"
be="$3"

if [ -z "$1" ]; then
    echo "Usage: ./run.sh AID TID BE"
    echo "       ./run.sh bash"
    exit 1
fi

if [ -z "$2}" ]; then
    echo "Usage: ./run.sh AID TID BE"
    echo "       ./run.sh bash"
    exit 1
fi

if [[ "x$3" == "x" ]] ; then
    # Do we have a PythingsCloud service running locally?
    DOCKER_PS_LINE=$(docker ps | grep pythingscloud/proxy | grep Up)
    if [[ "x$DOCKER_PS_LINE" != "x" ]] ; then
        PYTHIGSCLOUD_PROXY_ID=$(echo "$DOCKER_PS_LINE" | cut -d' ' -f1)
        PYTHIGSCLOUD_PROXY_IP=$(docker inspect -f "{{ .NetworkSettings.IPAddress }}" $PYTHIGSCLOUD_PROXY_ID)
        echo "Detected local PythingsCloud running, using its proxy IP: $PYTHIGSCLOUD_PROXY_IP"
        be=$PYTHIGSCLOUD_PROXY_IP
    fi
fi



docker run -v $PWD/../../:/opt/PythingsOS -eINTERACTIVE=True -it pythingsos/micropythonsimulator $1 $tid $be



