#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Create config.toml with proper content
echo -e "[server]\nport=\nenableCORS=false\nheadless=true" > config.toml

# Any other setup commands...
