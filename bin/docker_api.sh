#!/bin/bash

# USAGE: docker_api.sh DOCKER_HOST=$host:$port $uri | jq .

while [ "$#" -gt 1 ]; do
    eval "$1"
    shift
done
URI=${1?'Required'}
: ${DOCKER_HOST?'Required'}
API_VERSION=${API_VERSION:-v1.35}  # cf. https://docs.docker.com/engine/api/v1.35/

if [[ $(uname) =~ CYGWIN ]]; then
    CERTS_DIR="$(cygpath $USERPROFILE\\.docker\\certs\\$(echo $DOCKER_HOST | tr : _))"
else
    CERTS_DIR="$HOME/.docker/certs/$(echo $DOCKER_HOST | tr : _)"
fi
ca=$CERTS_DIR/ca.pem
cert=$CERTS_DIR/cert.pem
key=$CERTS_DIR/key.pem
curl -v --cacert $ca --cert $cert --key $key https://$DOCKER_HOST/$API_VERSION$URI
