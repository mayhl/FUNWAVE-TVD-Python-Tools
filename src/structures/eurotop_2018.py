# ------------ COMMENTS 
# Structure type defines set of equations to use & emperical coefficients used
# Additionally, Eurotop guidance uses seaward slope as an additional decision point
# for equation definition 
# Equations are from http://www.overtopping-manual.com/assets/downloads/EurOtop_II_2018_Final_version.pdf


#        From Abi:
#            If there is a foreshore influence: no significant mound is considered,non-
#            impulsive is assumed, and no composite structures are considered.
#           Does not include battered wall types
#            Emergent toe of wall is considered a wall on embankment
#            Cr value is not considered for armored crests. See EurOtop Eq 6.8 for info.
#            Assume no berm influence
#            Assume shore normal wave

# -------------- IMPORT LIBRARIES
import numpy as np

# ---------- DEFINE INFLUENCE FACTORS ---------
# Roughness Influence Factor 
def roughness_influence_factor(structure_material, Hm0):
    ''' Compute roughness influence factor based on structure material.
  
    :param structure_material:         Structure material. Supports 'grass', 'concrete', 'basalt'.
    :type  structure_material:         str
    :param Hm0:           Zeroth momment spectral wave height.
    :type  Hm0:           ndarray
    :param gamma_f:           Roughness influence factor.
    :type  gamma_f:           ndarray
    '''
    # Adjust gamma_f If Needed For Grass 
    if structure_material =='grass':
        # Initialize gamma_f Influence Factor
        gamma_f = 1
        # Correct If Needed 
        if any(Hm0<0.75):
            gamma_f = np.ones(Hm0.size)
            gamma_f[Hm0>0.75] = 1.15*Hm0**0.5

    elif structure_material =='concrete': # Includes concrete, asphalt, concrete blocks
        # Initialize gamma_f Influence Factor
        gamma_f = 1

    elif structure_material =='basalt':
        # Initialize gamma_f Influence Factor
        gamma_f = 0.9

    else:
        print('Unsupported material. Please use grass, concrete or basalt. Assuming concrete material.')
        structure_material = 'concrete'
        gamma_f = 1

    # Return gamma_f 
    return gamma_f

# Wall Influence Factor 
def wall_influence_factor(structure_type, structure_crest_elevation, structure_toe_elevation, water_level):
    ''' Compute wall influence factor for vertical flodwalls.
  
    :param structure_type:         Structure type. Supports 1- levee, 2- rubblemound, 3- flodwalls.
    :type  structure_type:         str
    :param structure_crest_elevation:         Structure crest elevation.
    :type  structure_crest_elevation:         ndarray
    :param structure_toe_elevation:         Structure toe elevation.
    :type  structure_toe_elevation:         ndarray
    :param water_level:           Still water level.
    :type  water_level:           ndarray
    :param gamma_v:           Influence factor for a vertical wall on the slope.
    :type  gamma_v:           ndarray
    :param gamma_star:           Overall influence factor for a storm wall on slope or promenade.
    :type  gamma_star:           ndarray
    '''
    # Compute Structure Freeboard 
    Rc = structure_crest_elevation - water_level
    # Compute Wall Influence Coefficient 
    if structure_type == 3: # vertical, battered or steep walls
        # Compute Wall Height 
        wall_height = structure_crest_elevation - structure_toe_elevation
        # Compute Wall Influence Factor (Gamma_v)
        gamma_v = np.exp(-0.56*wall_height/Rc)
        # Compute gamma_star 
        gamma_star = gamma_v
    elif structure_type == 1 or structure_type == 2: # Levee & Rubblemounds
        # Factor Not Applicable - Set gamma_v as 1
        gamma_v = 1
        # Factor Not Applicable - Set gamma_star as 1
        gamma_star = gamma_v
    else:
        print('Unsupported structure type. Defaulting to levee structure type.')
        gamma_v = 1
        gamma_star = gamma_v
    # return Variables 
    return gamma_v, gamma_star

# Wave obliquity Inlfuence Factor
def wave_obliquity_influence_factor():
    ''' Compute runup and overtoping wave obliquity influence factor.
  
    :param gamma_beta_runup:           Run-up influence factor for oblique wave attack.
    :type  gamma_beta_runup:           ndarray
    :param gamma_beta_overtoping:           Overtoping influence factor for oblique wave attack.
    :type  gamma_beta_overtoping:           ndarray
    '''
    # Wave Obliquity Coefficient
    # Sill not implemented. Not as straight forwaRD.
    # Print Status Message 
    print('Wave obliquity influence factor has not been implemented. Default to 1.')
    # Runup & overtoppping gamma_beta are different
    gamma_beta_runup = 1
    gamma_beta_overtoping = 1
    # Return Values 
    return gamma_beta_runup, gamma_beta_overtoping

# Berm Influence Factor 
def berm_influence_factor():
    ''' Compute berm influence factor.
  
    :param gamma_b:           Berm influence factor.
    :type  gamma_b:           ndarray
    '''
    # Sill not implemented. Not as straight forwaRD.
    # Print Status Message 
    print('Berm influence factor has not been implemented. Default to 1.')
    # Runup & overtoppping gamma_beta are different
    gamma_b = 1
    # Return Values 
    return gamma_b
    
# R2% & OT Gentle Slope Structure Type 1       
def levee_response(application_type, gravity_constant, Tm10, Hm0, water_level, structure_crest_elevation, structure_seaward_slope, gamma_b, gamma_beta_runup, gamma_beta_overtoping, gamma_f, gamma_v, gamma_star):
    ''' Compute levee structure response. Computed responses include wave runup and overtopping. 

    :param application_type:           Response computation context. Supports 1- Mean Value Approach and 2- Design/Assesment Approach.
    :type  application_type:           ndarray
    :param water_level:           Still water level.
    :type  water_level:           ndarray
    :param Hm0:           Zeroth momment spectral wave height.
    :type  Hm0:           ndarray
    :param Tm10:           Zeroth momment spectral wave height.
    :type  Tm10:           ndarray
    :param structure_crest_elevation:         Structure crest elevation.
    :type  structure_crest_elevation:         ndarray
    :param structure_seaward_slope:         Structure seaward slope.
    :type  structure_seaward_slope:         ndarray
    :param gamma_f:           Roughness influence factor.
    :type  gamma_f:           ndarray
    :param gamma_v:           Influence factor for a vertical wall on the slope.
    :type  gamma_v:           ndarray
    :param gamma_star:           Overall influence factor for a storm wall on slope or promenade.
    :type  gamma_star:           ndarray
    :param gamma_beta_runup:           Run-up influence factor for oblique wave attack.
    :type  gamma_beta_runup:           ndarray
    :param gamma_beta_overtoping:           Overtoping influence factor for oblique wave attack.
    :type  gamma_beta_overtoping:           ndarray
    :param gamma_b:           Berm influence factor.
    :type  gamma_b:           ndarray
    '''
    # ----- DEFINE EMPIRICAL COEFFICIENTS -----
    if application_type  == 1: # Mean Value Approach
        # Define Runup Coefficiets
        c1_runup = 1.65 # EurOtop Eq 5.1   
        c2_runup = 1.00 # EurOtop Eq 5.2
        c3_runup = 0.80 # EurOtop Eq 5.6                           
        # Define Overtopping Coefficients 
        c1_ot = 0.023   # EurOtop Eq 5.10
        c2_ot = 2.700   # EurOtop Eq 5.10
        c3_ot = 0.090   # EurOtop Eq 5.11
        c4_ot = 1.500   # EurOtop Eq 5.11
    elif application_type  == 2 : # Design or Assesment Approach
        # Define Runup Coefficiets
        c1_runup = 1.75 # EurOtop Eq 5.4   
        c2_runup = 1.07 # EurOtop Eq 5.5
        c3_runup = 0.86 # EurOtop Eq 5.7                           
        # Define Overtopping Coefficients 
        c1_ot = 0.026   # EurOtop Eq 5.12
        c2_ot = 2.500   # EurOtop Eq 5.12
        c3_ot = 0.1035   # EurOtop Eq 5.13
        c4_ot = 1.35   # EurOtop Eq 5.13

    # ----- COMPUTE ADDITIONAL FIELDS -----
    # Zero Moment Wave Length
    L_m10 = (gravity_constant*Tm10**2)/(2*np.pi)  
    # Wave Steepness
    s_m10 = Hm0/L_m10; 
    # Breaker Parameter
    breaker_m10 = (1/structure_seaward_slope)/np.sqrt(s_m10)  
    # Structure Freeboard
    Rc = structure_crest_elevation - water_level
    # Account For Negative Freeboard (Submergence)
    q_overflow = np.zeros(Rc.size)# Intialize Variables
    Rc_corrt = np.zeros(Rc.size)
    # Assign Corrected q Value (Submerged) -> Rc = 0
    q_overflow[Rc < 0] = 0.54*np.sqrt(gravity_constant*np.abs(Rc[Rc < 0]))
    # Assing Frreboard For Non Submerged Case -> q_overflow = 0
    Rc_corrt[Rc > 0] = Rc[Rc > 0]

    # ----- RENAME INLFUENCE FACTORS FOR SIMPLICITY -----
    # Berm Influence Factor
    g_b = gamma_b  
    # Wave Obliqueness Runup Influence Factor 
    g_beta_r2p = gamma_beta_runup 
    # Wave Obliqueness Overtopping Influence Factor 
    g_beta_ot = gamma_beta_overtoping 
    # Surface Rougness Influence Factor
    g_f = gamma_f 
    # Wall Influence Factor
    g_v = gamma_v 
    # Wall Influence Factor
    g_star = gamma_star 

    # ----- COMPUTE STRUCTURE RESPONSE -----
    if structure_seaward_slope>2: # "(Relatively) Gentle Slope"
        # ----- RUN-UP ----------------
        # Eq. 5.1 Mean Value Approach Wave Run-up:
        R2p_a = Hm0*c1_runup*g_b*g_f*g_beta_r2p*breaker_m10
        # Eq 5.2 With A Maximum Of
        R2p_max = Hm0*c2_runup*g_f*g_beta_r2p*(4-1.5/np.sqrt(g_b*breaker_m10))
        # Initialize Runup Variable 
        R2p = np.zeros(Hm0.size)
        # Negative R2p_max Failsafe
        R2p[R2p_max>0] = np.nanmin([R2p_a[R2p_max>0], R2p_max[R2p_max>0]], axis = 0)
        R2p[R2p_max<=0] = R2p_a[R2p_max<=0]
        
        # ------- OVERTOPPING -----------
        # EurOtop Overtopping Eq 5.10 
        q_a_term_1 = np.sqrt(gravity_constant*Hm0**3)
        q_a_term_2 = (c1_ot/np.sqrt(1/structure_seaward_slope))*g_b*breaker_m10
        q_a_term_3 = np.exp(-(c2_ot*Rc_corrt/breaker_m10/Hm0/g_b/g_f/g_beta_ot/g_v)**1.3)
        q_a = q_a_term_1*q_a_term_2*q_a_term_3
        # with a Minimum of (Eq. 5.11)
        q_max_term_1 = np.sqrt(gravity_constant*Hm0**3)*c3_ot
        q_max_term_2 = np.exp(-(c4_ot*Rc_corrt/(Hm0*g_f*g_beta_ot*g_star))**1.3)
        q_max = q_max_term_1*q_max_term_2
        # Get Minimum
        q = np.nanmin([q_max,q_a], axis = 0)
        # Apply Negative Freeboard Influence Factor (l/s per m ?)
        q = (q_overflow + q)*1000 # meter 2 liter conversion 
    elif structure_seaward_slope<2:
        # Random Uncertainty 
        randn = np.random.randn()

        # EurOtop Runup Eq 5.6
        R2p_a = np.nanmin([Hm0*c3_runup/(1/structure_seaward_slope) + 1.6 , (3*Hm0)], axis = 0)
        R2p = np.nanmax([0,np.nanmax([R2p_a,(1.8*Hm0)], axis = 0)], axis = 0)

        # EurOtop Overtopping eq 5.18- assumes only smooth slopes
        a_a = (0.09 - 0.01*(2-(1/structure_seaward_slope))**2.1)
        a = a_a+(a_a*0.15*randn)
        b_a = np.nanmin([(1.5+0.42*(2-(1/structure_seaward_slope))**1.5),2.35], axis = 0)
        b = b_a+(b_a*0.10*randn)
        q = np.sqrt(gravity_constant*Hm0**3)*a*np.exp(-(b*Rc_corrt/(Hm0*g_beta_ot))**1.3)
        q = (q_overflow + q)*1000 # meter 2 liter conversion 

    # Print Out Results 
    print(['R2%: '+str(R2p)+' ( m )'])
    print(['q: '+str(q)+' ( l/s per m )'])
    return R2p,q

# OT Structure Type 3
def vertical_wall_response(application_type, gravity_constant, Hm0, water_level, structure_crest_elevation, structure_toe_elevation, gamma_beta_overtoping):
    ''' Compute vertical wall structure response. Computed responses include overtopping. 

    :param application_type:           Response computation context. Supports 1- Mean Value Approach and 2- Design/Assesment Approach.
    :type  application_type:           ndarray
    :param water_level:           Still water level.
    :type  water_level:           ndarray
    :param Hm0:           Zeroth momment spectral wave height.
    :type  Hm0:           ndarray
    :param structure_crest_elevation:         Structure crest elevation.
    :type  structure_crest_elevation:         ndarray
    :param structure_toe_elevation:         Structure toe elevation.
    :type  structure_toe_elevation:         ndarray
    :param gamma_beta_overtoping:           Overtoping influence factor for oblique wave attack.
    :type  gamma_beta_overtoping:           ndarray
    '''
    # ----- DEFINE EMPIRICAL COEFFICIENTS -----
    if application_type  == 1: # Mean Value Approach
        # Vertical wall coefficients
        c1_wall_ot = 0.047 # EurOtop Eq 7.1
        c2_wall_ot = 2.350 # EurOtop Eq 7.1
        c3_wall_ot = 0.050 # EurOtop Eq 7.5
        c4_wall_ot = 2.780 # EurOtop Eq 7.5
        c5_wall_ot = 0.011 # EurOtop Eq 7.7 and 7.15
        c6_wall_ot = 0.0014 # EurOtop Eq 7.8 and 7.14 
    elif application_type  == 2 : # Design or Assesment Approach
        # Vertical wall coefficients (Needs To be Changed)
        c1_wall_ot = 0.047 # EurOtop Eq 7.1
        c2_wall_ot = 2.350 # EurOtop Eq 7.1
        c3_wall_ot = 0.050 # EurOtop Eq 7.5
        c4_wall_ot = 2.780 # EurOtop Eq 7.5
        c5_wall_ot = 0.011 # EurOtop Eq 7.7 and 7.15
        c6_wall_ot = 0.0014 # EurOtop Eq 7.8 and 7.14  

    # ----- COMPUTE ADDITIONAL FIELDS -----
    # Structure Freeboard
    Rc = structure_crest_elevation - water_level
    # Account For Negative Freeboard (Submergence)
    if Rc < 0:
        q_overflow = 0.54*np.sqrt(gravity_constant*np.abs(Rc))
        Rc_corrt = 0
    else:
        q_overflow = 0
        Rc_corrt = Rc
    # Sumberged depth of wall
    w_depth=-structure_toe_elevation + water_level;     

    # ----- RENAME INLFUENCE FACTORS FOR SIMPLICITY -----
    # Wave Obliqueness Overtopping Influence Factor 
    g_beta_ot = gamma_beta_overtoping 

    # ----- COMPUTE STRUCTURE RESPONSE -----
    if w_depth/Hm0 > 4:  # no foreshore influence
        # EurOtop Overtopping Eq 7.1
        q = np.sqrt(gravity_constant*Hm0**3)*c1_wall_ot*np.exp(-((c2_wall_ot/g_beta_ot)*Rc_corrt/Hm0)**1.3)     
    else: # foreshore influence
        q = np.sqrt(gravity_constant*Hm0**3)*c3_wall_ot*np.exp(-(c4_wall_ot/g_beta_ot)*Rc_corrt/Hm0)     

    q = (q + q_overflow)*1000 # meter 2 liter conversion

    # Print Out Results 
    print(['q: '+str(q)+' ( l/s per m )'])






