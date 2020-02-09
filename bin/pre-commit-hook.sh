#!/usr/bin/env bash

rm coverage.svg
coverage-badge -o coverage.svg

git add coverage.svg
