#!/bin/bash -e

cd wazuh-docker/single-node
if [ ! -d ./config/wazuh_indexer_ssl_certs ]; then
	docker compose -f generate-indexer-certs.yml run --rm generator
fi

if grep 'MyS3cr37P450r.*-' docker-compose.yml > /dev/null; then
	API_PASSWORD=$(openssl rand -base64 32 | tr '/=+' '*@#')
	sed -i "s/MyS3cr37P450r.*/$API_PASSWORD/g" docker-compose.yml
fi
sed -i "s/DASHBOARD_USERNAME=kibanaserver/DASHBOARD_USERNAME=admin/g" docker-compose.yml
if grep 'DASHBOARD_PASSWORD=kibanaserver' docker-compose.yml > /dev/null; then
	DASHBOARD_PASSWORD=$(openssl rand -base64 32 | tr '/=+' '*@#')
	echo "Admin credentials: admin:$DASHBOARD_PASSWORD"
	sed -i "s/DASHBOARD_PASSWORD=kibanaserver/DASHBOARD_PASSWORD=$DASHBOARD_PASSWORD/g" docker-compose.yml
fi

docker compose up -d
