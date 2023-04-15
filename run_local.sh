#!/bin/bash

# zola serve overwrites config.base_url
zola --config local.config.toml serve --drafts -i 0.0.0.0 -u /
