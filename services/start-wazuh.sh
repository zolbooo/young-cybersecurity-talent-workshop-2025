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
if grep '<WAZUH_MANAGER_IP>' docker-compose.yml; then
		sed -i "s/<WAZUH_MANAGER_IP>/host.docker.internal/g" docker-compose.yml
		yq -y -i '
      .services[] |= (
        .extra_hosts = (.extra_hosts // []) |
        (if (.extra_hosts | index("host.docker.internal:host-gateway"))
          then .
          else (.extra_hosts += ["host.docker.internal:host-gateway"])
        end)
      )
    ' docker-compose.yml
fi
docker compose up -d
