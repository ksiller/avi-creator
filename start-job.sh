#!/bin/bash

INPUT_DIR=${1}
OUTPUT_DIR=${2}
JOB_INPUT=input.txt

if ! [ -d "${INPUT_DIR}" ]; then
    echo "${INPUT_DIR} does not exist."
    exit 1
fi

# read tif files, extract unique position identifier, and save in input file
for file in ${INPUT_DIR}/*.TIF ; 
    do basename "$file" | awk -F_ '{print$6}'; 
done | sort | uniq > ${JOB_INPUT}

NO_GROUPS=$( < ${JOB_INPUT} wc -l )
echo "Found ${NO_GROUPS} image groups in ${JOB_INPUT}"

# launch job array
sbatch --array=1-${NO_GROUPS} create_avi.slurm ${INPUT_DIR} ${OUTPUT_DIR} ${JOB_INPUT}
