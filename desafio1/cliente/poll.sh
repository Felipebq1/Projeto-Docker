#!/bin/sh

set -eu

TARGET_URL="${TARGET_URL:-http://web:8080/health}"
POLL_INTERVAL="${POLL_INTERVAL:-5}"

log() {
    printf '[%s] %s\n' "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" "$1"
}

while true; do
    log "Enviando requisição para ${TARGET_URL}"

    RESPONSE=$(curl --silent --show-error --write-out " HTTP_STATUS:%{http_code}" "${TARGET_URL}" || true)
    STATUS=$(printf "%s" "$RESPONSE" | sed -n 's/.*HTTP_STATUS://p')
    BODY=$(printf "%s" "$RESPONSE" | sed 's/ HTTP_STATUS:.*//')

    if [ -n "${STATUS}" ]; then
        log "Resposta recebida (status ${STATUS}): ${BODY}"
    else
        log "Falha ao conectar ao servidor: ${BODY}"
    fi

    sleep "${POLL_INTERVAL}"
done

