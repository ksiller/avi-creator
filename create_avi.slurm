#!/bin/bash
#SBATCH -p standard
#SBATCH -t 00:15:00
#SBATCH -A <your_allocation>
#SBATCH --mem=9G

module purge
module load fiji

INPUTDIR="$1"
OUTPUTDIR="$2"
INPUTFILE="$3"
mkdir -p ${OUTPUTDIR}

# get position identifier from input file
POS=$( sed "${SLURM_ARRAY_TASK_ID}q;d" $INPUTFILE)
echo "Task: ${SLURM_ARRAY_TASK_ID}, ${POS}"

ARGS="inputdir=\"$INPUTDIR\",outputdir=\"$OUTPUTDIR\",pos=\"$POS\""
echo "Setting Fiji script arguments: ${ARGS}"

ImageJ-linux64 --ij2 --mem=9000 --java-home=$JAVA_HOME --headless --run avi-creator.py ${ARGS}