------------------ Code description --------------
The code of this folder is used to calculate global inorganic N input
1. Cal_fer_InorganicN.py: Extract Urea N application rate and other inorganic N application rate
2. Res_Trans_N_Inorganic_Upscale05d.py: Upscale N inorganic input from 5 arc minute to 0.5 degree
   2.1 Calculate the urea N input, other inorganic N input, and total inorganic N input (Urea + Other) [kg] for each pixel at 5 arc minute (harvest area * N fertilization rate)
   2.2 Sum up the urea N input, other inorganic N input, and total inorganic N input (Urea + Other) [kg] to 0.5 degree resolution
   2.3 Divide the N inorganic input amount at 0.5 degree resolution by harvest area at each pixel [kg/ha harvest area]