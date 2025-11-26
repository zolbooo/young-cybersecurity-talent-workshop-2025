#!/bin/bash -e

cd wazuh-docker/single-node
if [ ! -d ./config/wazuh_indexer_ssl_certs ]; then
	docker compose -f generate-indexer-certs.yml run --rm generator
fi

docker compose up -d
