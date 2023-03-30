#! /bin/sh

# Script to run pytest tests in Github Actions CI
# using github-action-docker-compose-test-run action
# https://github.com/cloudposse/github-action-docker-compose-test-run

python3 -m pytest
