#!/bin/bash
#-----------------------------Mail address-----------------------------

#-----------------------------Required resources----------------------

#-----------------------------Output files-----------------------------
#SBATCH --output=HPCReport/output_%j.txt
#SBATCH --error=HPCReport/error_output_%j.txt

#-----------------------------Required resources-----------------------
#SBATCH --time=20
#SBATCH --mem=25000

# This code is used to calculate: select certain years from the irrigation data

module load cdo

input_dir="/lustre/nobackup/WUR/ESG/zhou111/WOFOST-withoutNPLimit/CaseStudy_NPInput"
output_dir="/lustre/nobackup/WUR/ESG/zhou111/WOFOST-withoutNPLimit/CaseStudy_NPInput"

StudyAreas=("Rhine" "Yangtze" "LaPlata" "Indus") # "Rhine" "Yangtze" "LaPlata" "Indus"

SelectYears(){
    for studyarea in "${StudyAreas[@]}"; do 
        for file in "$input_dir"/$studyarea/${studyarea}*1980-2020.nc; do
            filename=$(basename "$file")
            output_file="$output_dir/$studyarea/${filename}_cut"
            cdo sellevel,1981/2016 $file $output_file #1981-2016
        done
    done
}

SelectYears