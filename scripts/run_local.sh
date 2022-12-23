#!/bin/bash

scripts/run_aux_scripts.py
zola --config local.config.toml serve --drafts
