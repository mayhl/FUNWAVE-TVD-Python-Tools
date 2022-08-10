# %%
import numpy as np
from numpy.random import randn as randn
import matplotlib.pyplot as plt
import os

# %% [markdown]
#  # Eurotop codes for embankment to vertical walls
#  Based on Matlab code made by Abigail L. Stehno 
#  (translated to Python by Gabriela Salgado)
# ------------------
#  This code's goal is to find the overtopping and runup values of smooth slopes or rubble mounds.
#  This does not include vertical walls or armored structures because the logic for them is 
#  significantly different than with slopes. A seperate function should be written for them. 
# 
# ## Inputs: 
# - Wave/water characteristics (at Structure's Toe):
#     - Hm0             : Zero moment significant wave height                [m]
#     - Tp              : Peak wave period                                   [s]
#     - SWL             : Still Water Level                                  [m]
#     - base            : Structure toe elevation from SWL                   [m]    
# - Structure characteristics:
#     - Rc              : Structure Crest Elevation (Freeboard) from SWL     [m]
#     - slope           : cot(alpha) (also described as delta_x/delta_y)
#     - BermWidth       : Structure Berm Width                               [m]
#     - strucType       : Defines the type of structure (where: 1 = levee, and 2 = rubble mound)
# - Coefficients (Chapter 5 of EurOtop 2018 provides an overview of influence factors):
#     - gamma_f         : Influence of surface friction (See table 5.2 of EurOtop 2018)
#     - gamma_beta_r2p  : Influence of wave direction on runup (equal to 1.0 for wave Dir perpendicular to structure) 
#     - gamma_beta_OT   : Influence of wave direction on overtopping (equal to 1.0 for wave Dir perpendicular to structure)
#     - gamma_star      : Influence of wall on a levee (equal to 1.0 if no wall)
#     - gamma_v         : Influence of wall on a slope (equal to 1.0 if no wall)
#          
# ## Outputs:
# - R2p_final : Runup           [m]
# - q_final   : Overtopping     [m^3/s/m]
# 
#  Does not include berm influence for embankments
#  Does not include foreshore influence for embankments 
# 
# -------------
# ## Assumptions:
# - Wave characteristics are at the toe of the structure
# - Equations are determined by emperical formula derived from experiment.
# - The use of Tm1-0 is used to accomodate complex spectral shapes.
#  
# 
# ### RUNUP:
#  - Thin layers are not considered run-up (i.e. wind driven layers)
#  - Runup height is measured when the thickness is approximately <= 2 cm
# 
# ### OVERTOPPING:
#  - Average overtopping can only be calculated for quasi-stationary wave
#    and water level conditions, so for a time series, each set of 
#    conditions must be calculated individually (not time dependent) 
#  - Eq 5.10 and 5.11 are only true for a freeboard -= 0; if the freeboard
#    is < 0, assume Rc = 0 for the calculation then use the weir eq
#  - Eq 5.18 assumes relatively low freeboard, 0.36 < cota < 2.75, smooth 
#    slopes, and non-breaking
#  - Overflow eq coefficient 0.54 varies with structure type
#  - Additional assumptions of overtopping volumes, velocities, and
#    thicknesses will be added when that code is implemented
# 
# ### INFLUENCE FACTORS:
#  - Found using reference tests or well-known formula for comparison, wave
#    conditions should be identical
#  - Roughness (gamma_f)
#    - Grass has relatively greater hydraulic roughness for thin wave runup
#        depths, gamma_f will be conservative for grass
#    - Small Hm0 may effect roughness for all types of material; however,
#        standard gamma_f will give a conservative result
#  - Oblique Wave Direction (gamma_beta_r2p)
#    - Assume runup and overtopping is equally distributed along the
#        longitudinal axis of a dike (this will decrease for convex curves 
#        and increase for concave curves; however, this is not quatified)
#    - There is limited research for short crested gamma_beta_r2p - only 
#        0 < beta < 80 has been tested
#    - Assume no significant influence of spreading widths for short crested
#        waves
#    - Assume a reduction in Hm0 and Tp for waves over 80 degrees, reducing
#        Hm0 and Tp to zero for angles greater or equal to 110 degrees
#  - Currents are not currently considered; however, current effect
#    definitions were expanded from a limited amount of tests
#  - Berms (gamma_b)
#    - Assume the point of breaking is 1.5 Hm0 below SWL
#    - Limitation of gamma_b = 0.6 corresponds to optimal width of 
#        B = 0.4*Lm10 at SWL
#  - Wave walls (gamma_v and gamma_star)
#    - Submerged foot is limited to slopes between 1:2.5 and 1:3.5 and the
#        foot of the wall is no lower than 1.2Hm0
#    - Wall on top of emerged slope assumes a straight, smooth seaward slope
#        of 1:2 or 1:3 (can also be average slope), valid for 
#        0.01 < sm1-0 < 0.05, breaker parameter between 2.2-4.8, 
#        Rc/Hmo - 0.6, and assumes that other gamma values are valid when
#        wall is present (only tested when gamma_f=gamma_beta=gamma_b= 1)
#    - Smooth dike slope and a storm wall is applicable for h_wall/Rc = 0.08
#        to 1 [ we are assuming all walls are of this nature ] 
# 
#  SCALE EFFECTS AND UNCERTAINTIES
#  - There are such large model uncertainties that no other uncertainties
#    need to be considered if the full standard deviation is added to the
#    coefficients
#  - Frictional scale effects are not significant if gamma_f - 0.9,
#    uncertainties from scale effects for rough slopes is not well defined 
# 

# %%
def Eurotop_r2p_q(input_dict): 
    
    base = input_dict['base']
    Hm0 = input_dict['Hm0']
    Tp = input_dict['Tp']
    SWL = input_dict['SWL']
    Rc = input_dict['Rc']
    slope = input_dict['slope']
    BermWidth = input_dict['BermWidth']
    strucType = input_dict['strucType']
    gamma_f= input_dict['gamma_f']
    gamma_beta_r2p = input_dict['gamma_beta_r2p']
    gamma_beta_OT= input_dict['gamma_beta_OT']
    gamma_star = input_dict['gamma_star']
    gamma_v = input_dict['gamma_v']
    

    # Do not calculate structure response if no storm forcing                
    if Hm0<=0 or Tp<=0 or SWL<=-100 or np.isnan(Hm0)==True or np.isnan(Tp)==True or np.isnan(SWL)==True: 
        q_final = float("nan") 
        R2p_final = float("nan")
    else:

        ## Define variables
        g = 9.80665                            # gravitational acceleration
        T_m10 = Tp/1.1                         # neg zero moment period tm_1,0
        L_m10 = g*T_m10**2 /(2*np.pi)              # Zero moment wave length
        s_m10 = Hm0/L_m10                      # Wave steepness
        breaker_m10 = (1/slope)/np.sqrt(s_m10)    # Breaker parameter

        # Assume no berm!
        gamma_b = 1

        ## Negative freeboard influence
        # EurOtop Eq 5.20
        if Rc <= 0 :
            q_overflow = 0.54 * np.sqrt(g*abs(Rc)**3)
            Rc_corrt = 0 # need to calculate q with Rc = 0 for negative freeboards
        else: 
            q_overflow = 0
            Rc_corrt = Rc


        ## Runup and overtopping loop
        if slope > 0.1 and  strucType==1:  # slope cota > 1 ->  (levee)
            print('      Calculating Levee Overtopping and Runup...')
            # Embankment coefficients
            runup_coeff1 = 1.65 # EurOtop Eq 5.1   
            runup_coeff2 = 1.00 # EurOtop Eq 5.2
            runup_coeff3 = 0.80 # EurOtop Eq 5.6                           

            OT_coeff1 = 0.026 #0.023   # EurOtop Eq 5.10
            OT_coeff2 = 2.5 #2.700   # EurOtop Eq 5.10
            OT_coeff3 = 0.1035 #0.090   # EurOtop Eq 5.11
            OT_coeff4 = 1.35 #1.500   # EurOtop Eq 5.11

            if slope > 2:
                # EurOtop Runup Eq 5.1 and 5.2 
                R2p_a = Hm0*runup_coeff1*gamma_b*gamma_f*gamma_beta_r2p*breaker_m10
                R2p_max = Hm0*runup_coeff2*gamma_f*gamma_beta_r2p*(4-1.5/np.sqrt(gamma_b*breaker_m10))
                if R2p_max > 0: 
                    R2p = np.minimum(R2p_a,R2p_max)
                else:
                    R2p = R2p_a

               
                # EurOtop Overtopping Eq 5.10 and 5.11
                q_a_1 = np.sqrt(g*Hm0**3)*OT_coeff1/np.sqrt(1/slope)*gamma_b*breaker_m10
                q_a_2 = np.exp(-(OT_coeff2*Rc_corrt/breaker_m10/Hm0/gamma_b/gamma_f/gamma_beta_OT/gamma_v)**1.3)
                q_a = q_a_1*q_a_2
                
                q_max_1 = np.sqrt(g*Hm0**3)*OT_coeff3
                q_max_2 = np.exp(-(OT_coeff4*Rc_corrt/OT_coeff4*Rc_corrt/Hm0/gamma_f/gamma_beta_OT/gamma_star)**1.3)
                q_max = q_max_1*q_max_2
                
                q = np.minimum(q_a,q_max)

                del R2p_a, R2p_max, q_a, q_max

            else: # cota between 1:2 and 1:1 - embankment to vertical wall
                # EurOtop Runup Eq 5.6
                R2p_a = np.minimum(Hm0*runup_coeff3/(1/slope) + 1.6 , (3*Hm0))
                R2p = np.maximum(0,np.maximum(R2p_a,(1.8*Hm0)))

                # EurOtop Overtopping eq 5.18- assumes only smooth slopes
                a_a = (0.09 - 0.01*(2-(1/slope))**2.1)
                a = a_a #+(a_a*0.15*randn())
                b_a = np.minimum((1.5+0.42*(2-(1/slope))**1.5),2.35)
                b = b_a #+(b_a*0.10*randn())
                
                q = np.sqrt(g*Hm0**3)*a*np.exp(-(b*Rc_corrt/Hm0/gamma_beta_OT)**1.3) 
                                
                del R2p_a, a_a, a, b_a, b


        elif slope > 0.1 and  strucType==2: # rubble mound 
            print('      Calculating Rubble Mound Overtopping and Runup...')
            # Embankment coefficients
            runup_coeff1 = 1.65 # EurOtop Eq 6.1   
            runup_coeff2 = 1.00 # EurOtop Eq 6.1                  

            OT_coeff3 = 0.090   # EurOtop Eq 6.5
            OT_coeff4 = 1.500   # EurOtop Eq 6.5

            # gamma_f modifications
            # May need to include a switch for user to turn on/off
            if breaker_m10 > 1.8 and breaker_m10 < 10: # EurOtop Eq. 6.1
                gamma_f_surge = gamma_f + (breaker_m10-1.8)*(1-gamma_f)/8.2 
            else:
                gamma_f_surge = gamma_f 


            # For overtopping, if there is a berm gamma_f is changed to gamma_BB in the
            # equations- assume hardly and partly reshaping berm breakwaters

            # Will also take care of instances where structure has steep slopes
            if slope < 2: # Accounts for eq 6.5 - gamma_f
                gamma_f_orBB = 1 
            elif BermWidth > 0: # EurOtop Eq 6.11 - gamma_f is not used for berm structures
                gamma_f_orBB = np.maximum(0.6, 0.68-4.1*s_m10-0.05*BermWidth/Hm0) # Max influence is 0.6
            elif breaker_m10 > 5 and breaker_m10 < 10: # EurOtop Eq. 6.7 - gamma_f
                gamma_f_orBB = gamma_f + (breaker_m10-5)*(1-gamma_f)/5 
            else:
                gamma_f_orBB = 1 


            # EurOtop Runup Eq 6.1
            ### maximum Ru2#/Hm0 = 3 for impermeable and 2.0 for permeable

            R2p_a = Hm0*runup_coeff1*gamma_b*gamma_f_surge*gamma_beta_r2p*breaker_m10
            R2p_max = Hm0*runup_coeff2*gamma_f_surge*gamma_beta_r2p*(4-1.5/np.sqrt(gamma_b*breaker_m10))
            if R2p_max > 0: 
                R2p = np.minimum(R2p_a,R2p_max)
            else:
                R2p = R2p_a

            q = np.sqrt(g*Hm0**3)*OT_coeff3*np.exp(-(OT_coeff4*Rc_corrt/Hm0/gamma_f_orBB/gamma_beta_OT)**1.3)


    q_final = q + q_overflow 
    R2p_final = R2p

    return R2p_final,q_final
  

# %%
## Case Study 8.2 – St. Peter Ording – grass covered dike

input_dict = {'base' : 3.00,
'Hm0' : 1.93,
'Tp' : 4.5*1.1,
'SWL' : 6.0,
'Rc' : 1.38,
'slope' : 8,
'strucType' : 1,
'gamma_f' : 1.0,
'gamma_beta_r2p' : 1.0,
'gamma_beta_OT' : 1.0,
'gamma_star' : 1.0,
'gamma_v' : 1.0,
'BermWidth' : 3.50}

[R2p_final, q_final] = Eurotop_r2p_q(input_dict)

print('R2p_final:',R2p_final,',   q_final:',q_final)

# %%



