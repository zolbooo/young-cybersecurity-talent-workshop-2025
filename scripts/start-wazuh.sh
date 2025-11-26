#!/bin/bash -e

pushd $(pwd)
if [ -d services ]; then
	cd services
fi
cd wazuh

if [ ! -d ./config/wazuh_indexer_ssl_certs ]; then
	docker compose -f generate-indexer-certs.yml run --rm generator
fi
docker compose up -d

popd
if [ -d services ]; then
	cd services
fi
cd wazuh-agent
docker compose up -d
