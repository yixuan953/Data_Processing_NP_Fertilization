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

# Python scripts: Calculate the residue N, P input based on wofost simulated N, P amount
# python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Fertilization/1_NP_Residue/1_Cal_Return_Ratio.py
# python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Fertilization/1_NP_Residue/2_Cal_NP_Residue.py
# python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Fertilization/1_NP_Residue/3_Cal_NP_Res_Input.py

# Calculate the residue N input based on: Adalibieke, W., Cui, X., Cai, H., You, L., Zhou, F. (2023). Global crop-specific nitrogen fertilization dataset in 1961-2020. 
# Data download: National Tibetan Plateau / Third Pole Environment Data Center. https://doi.org/10.11888/Terre.tpdc.300446. https://cstr.cn/18406.11.Terre.tpdc.300446.
# python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Fertilization/1_NP_Residue/4_Cal_fert_ResidueN.py
python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Fertilization/1_NP_Residue/5_Res_Trans_N_Residue_Upscale05d.py