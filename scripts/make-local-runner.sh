#!/bin/bash

# Create a folder
mkdir actions-runner && cd actions-runner
# Download the latest runner package
curl -O -L https://github.com/actions/runner/releases/download/v2.275.1/actions-runner-linux-x64-2.275.1.tar.gz
# Extract the installer
tar xzf ./actions-runner-linux-x64-2.275.1.tar.gz

