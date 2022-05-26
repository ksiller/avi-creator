#!/bin/bash

INPUT_DIR=${1}
JOB_INPUT=input.txt

if ! [ -d "${INPUT_DIR}" ]; then
    echo "${INPUT_DIR} does not exist."
    exit 1
fi

for file in ${INPUT_DIR}/*.TIF ; 
    do basename "$file" | awk -F_ '{print$6}'; 
done | sort | uniq > ${JOB_INPUT}

NO_GROUPS=$( < ${JOB_INPUT} wc -l )
echo "Found ${NO_GROUPS} image groups in ${JOB_INPUT}"
