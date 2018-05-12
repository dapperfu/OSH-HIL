# Config

## Targets
# Do nothing.
.PHONY: null
null:
	@$(error No Default Target).

ARTIFACT_PTR=$(wildcard artifacts/*.txt)
ARTIFACT_FILES=$(patsubst %.txt,%,${ARTIFACT_PTR})

.PHONY: artifacts
artifacts: ${ARTIFACT_FILES}

.PHONY: ${ARTIFACT_FILES}
${ARTIFACT_FILES}:
	curl --silent --location --output "${@}" "$(shell cat "${@}.txt")"

# Toolchain Includes
include .mk_inc/env.mk
