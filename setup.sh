#!/bin/bash

# Create the .streamlit directory if it doesn't exist
mkdir -p ~/.streamlit/

# Create the config.toml file with the necessary configurations
echo -e "[server]\nport=$PORT\nenableCORS=false\nheadless=true" > ~/.streamlit/config.toml

# Any other setup commands...
