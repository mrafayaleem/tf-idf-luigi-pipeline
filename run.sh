#!/bin/bash

PWD=$PWD

echo "${PWD}"

if [ $# != 1 ]; then
  echo "Error: expecting exactly one argument (documents.txt), received [$#]: '$@'"
  exit
fi

pip install -r code/requirements.txt

FULLPATH="${PWD}/${1}"

echo "Full path for the documents file is ${FULLPATH}"
echo "Cleaning previous runs..."
./clean.sh
echo "Will execute tasks in --local-scheduler mode so web server won't be accessible"
#luigid &

PYTHONPATH="${PWD}"/code luigi --module pipeline.tasks TfIdfSimilarityPipeline --inputpath "${FULLPATH}" --outputpath "${PWD}" --local-scheduler
