## Configuration

# Environments to setup.
ENVS+=python
ENVS+=arduino

## Targets
# Do nothing.
.PHONY: null
null:
	@$(error No Default Target).

ARTIFACT_PTR=$(wildcard artifacts/*.txt)
ARTIFACT_FILES=$(patsubst %.txt,%,${ARTIFACT_PTR})

.PHONY: artifacts
artifacts: ${ARTIFACT_FILES}
	tar -xzvf ${@}/linuxcan.tar.gz -C ${@}
	cd "${@}" && unzip "Ginkgo_USB-I2C&SPI&CAN_API_v2.0.3.5.zip"
	cd "${@}" && unzip pycanlib.zip

.PHONY: ${ARTIFACT_FILES}
${ARTIFACT_FILES}:
	curl --silent --location --output "${@}" "$(shell cat "${@}.txt")"

#.PHONY: env
#env: 
#	git submodule foreach "${MAKE} env"

# Toolchain Includes
include .mk_inc/env.mk
