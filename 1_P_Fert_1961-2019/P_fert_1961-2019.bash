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
# python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Fertilization/1_P_Fert_1961-2019/1_Cal_P_InorgFert_Amount.py
# python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Fertilization/1_P_Fert_1961-2019/2_Form_Trans_tiff2nc.py
# python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Fertilization/1_P_Fert_1961-2019/3_Res_Trans_Upscale_P_05d.py
python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Fertilization/1_P_Fert_1961-2019/4_Cal_HA.py