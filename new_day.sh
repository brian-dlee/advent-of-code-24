#!/bin/bash

set -e

if [[ $# -lt 1 ]]; then
  echo "Provide a day abbreviation" >&2
  exit 1
fi

mkdir "$1"
cp "d0/template.py" "$1/a.py"
