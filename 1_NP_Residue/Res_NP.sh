#!/bin/bash
#-----------------------------Mail address-----------------------------

#-----------------------------Output files-----------------------------
#SBATCH --output=HPCReport/output_%j.txt
#SBATCH --error=HPCReport/error_output_%j.txt

#-----------------------------Required resources-----------------------
#SBATCH --time=600
#SBATCH --mem=250000

#--------------------Environment, Operations and Job steps-------------
module load python/3.12.0

# Python scripts
# python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Fertilization/1_NP_Residue/1_Cal_Return_Ratio.py
# python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Fertilization/1_NP_Residue/2_Cal_NP_Residue.py
python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Fertilization/1_NP_Residue/3_Cal_NP_Res_Input.py