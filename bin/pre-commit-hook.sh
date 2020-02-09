#!/usr/bin/env bash

# update coverage badge
rm coverage.svg
coverage-badge -o coverage.svg
git add coverage.svg

# ensure we commit requirements.txt routinely
pip freeze > requirements.txt
git add requirements.txt
