#!/usr/bin/with-contenv bashio

bashio::log.info "Starting Brain Graph server on port 8099..."
exec python3 /server.py
