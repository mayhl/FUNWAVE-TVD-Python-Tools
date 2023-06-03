from funwavetvdtools.io.inputfileinterface import InputFileInterface
from funwavetvdtools.io.parameter import Category, Datatype, Mask, Parameter


class InputFile(InputFileInterface):

   __slots__ = InputFileInterface.get_slots([
      'ZALPHA'          , 'PARALLEL'      , 'nGlob'               , 'mGlob'             , 'CARTESIAN'                , 'DEPTH_TYPE'        , 
      'BATHY_CORRECTION', 'WaterLevel'    , 'TOTAL_TIME'          , 'PLOT_START_TIME'   , 'PLOT_INTV'                , 'SCREEN_INTV'       , 
      'INI_UVZ'         , 'WAVEMAKER'     , 'DIRECT_SPONGE'       , 'DIFFUSION_SPONGE'  , 'FRICTION_SPONGE'          , 'OBSTACLE_FILE'     , 
      'BREAKWATER_FILE' , 'DISPERSION'    , 'Gamma1'              , 'FRICTION_MATRIX'   , 'Time_Scheme'              , 'CONSTRUCTION'      , 
      'HIGH_ORDER'      , 'CFL'           , 'FIXED_DT'            , 'FroudeCap'         , 'MinDepth'                 , 'MinDepthFrc'       , 
      'OUT_Time'        , 'NumberStations', 'ROLLER_EFFECT'       , 'VISCOSITY_BREAKING', 'SHOW_BREAKING'            , 'WAVEMAKER_Cbrk'    , 
      'WAVEMAKER_VIS'   , 'PX'            , 'PY'                  , 'DX'                , 'DY'                       , 'StretchGrid'       , 
      'DEPTH_FILE'      , 'DEPTH_FLAT'    , 'SLP'                 , 'Xslp'              , 'BED_DEFORMATION'          , 'ETA_FILE'          , 
      'U_FILE'          , 'V_FILE'        , 'MASK_FILE'           , 'HotStartTime'      , 'OutputStartNumber'        , 'AMP'               , 
      'DEP'             , 'LAGTIME'       , 'NumWaveComp'         , 'PeakPeriod'        , 'Xc_WK'                    , 'Yc_WK'             , 
      'DEP_WK'          , 'Time_ramp'     , 'Delta_WK'            , 'Ywidth_WK'         , 'SolitaryPositiveDirection', 'XWAVEMARKER'       , 
      'x1_Nwave'        , 'x2_Nwave'      , 'a0_Nwave'            , 'gamma_Nwave'       , 'dep_Nwave'                , 'Xc'                , 
      'Yc'              , 'WID'           , 'Tperiod'             , 'AMP_WK'            , 'Theta_WK'                 , 'alpha_c'           , 
      'EqualEnergy'     , 'WAVE_DATA_TYPE', 'DepthWaveMaker'      , 'ETA_LIMITER'       , 'WaveMakerCd'              , 'PERODIC'           , 
      'Csp'             , 'CDsponge'      , 'Sponge_west_width'   , 'Sponge_east_width' , 'Sponge_south_width'       , 'Sponge_north_width', 
      'R_sponge'        , 'A_sponge'      , 'BreakWaterAbsorbCoef', 'Gamma2'            , 'Beta_ref'                 , 'Gamma3'            , 
      'FRICTION_FILE'   , 'Cd'            , 'ArrTimeMin'          , 'PLOT_INTV_STATION' , 'StationOutputBuffer'      , 'STATIONS_FILE'     , 
      'SWE_ETA_DEP'     , 'Cbrk1'         , 'Cbrk2'               , 'visbrk'            , 'WAVEMAKER_visbrk'         , 'DX_FILE'           , 
      'DY_FILE'         , 'CORIOLIS_FILE' , 'Lon_West'            , 'Lat_South'         , 'Dphi'                     , 'Dtheta'            , 
      'WaveCompFile'    , 'FreqPeak'      , 'FreqMin'             , 'FreqMax'           , 'Hmo'                      , 'Nfreq'             , 
      'Ntheta'          , 'ThetaPeak'     , 'Sigma_Theta'         , 'WidthWaveMaker'    , 'R_sponge_wavemaker'       , 'A_sponge_wavemaker', 
      'CrestLimit'      , 'TroughLimit'                                                                                                      ])

   """
   Input File Class
   Auto generated on 
   """
   def __init__(self, **values):
      super().__init__(**values)

   def __add_parameters__(self):
      self._ZALPHA = Parameter(
         name          = 'ZALPHA'     ,
         fullname      = 'ZALPHA'     ,
         datatype      = Datatype.FLAG,
         category      = Category.GRID,
         is_required   = False        ,
         description   = 'None'       ,
         mask          = Mask.NONE    ,
         values        = None         ,
         default_value = 'False'      ,
         dependencies  = None         
      )
      self._PARALLEL = Parameter(
         name          = 'PARALLEL'                                                  ,
         fullname      = 'Parallel'                                                  ,
         datatype      = Datatype.FLAG                                               ,
         category      = Category.PARALLEL                                           ,
         is_required   = False                                                       ,
         description   = 'FORTRAN compile flag for turning on parallel computations.',
         mask          = Mask.NONE                                                   ,
         values        = None                                                        ,
         default_value = 'False'                                                     ,
         dependencies  = None                                                        
      )
      self._nGlob = Parameter(
         name          = 'nGlob'                          ,
         fullname      = 'nGlob'                          ,
         datatype      = Datatype.INTEGER                 ,
         category      = Category.GRID                    ,
         is_required   = True                             ,
         description   = 'Number of points in x direction',
         mask          = Mask.POSITIVE_DEFINITE           ,
         values        = None                             ,
         default_value = None                             ,
         dependencies  = None                             
      )
      self._mGlob = Parameter(
         name          = 'mGlob'                          ,
         fullname      = 'mGlob'                          ,
         datatype      = Datatype.INTEGER                 ,
         category      = Category.GRID                    ,
         is_required   = True                             ,
         description   = 'Number of points in y direction',
         mask          = Mask.POSITIVE_DEFINITE           ,
         values        = None                             ,
         default_value = None                             ,
         dependencies  = None                             
      )
      self._CARTESIAN = Parameter(
         name          = 'CARTESIAN'                                                                              ,
         fullname      = 'Cartesian'                                                                              ,
         datatype      = Datatype.FLAG                                                                            ,
         category      = Category.GRID                                                                            ,
         is_required   = True                                                                                     ,
         description   = 'FORTRAN compile flag for switch between cartesian coordinates and spherical coordinates',
         mask          = Mask.NONE                                                                                ,
         values        = None                                                                                     ,
         default_value = 'True'                                                                                   ,
         dependencies  = None                                                                                     
      )
      self._DEPTH_TYPE = Parameter(
         name          = 'DEPTH_TYPE'                   ,
         fullname      = 'DEPTH_TYPE'                   ,
         datatype      = Datatype.ENUM                  ,
         category      = Category.BATHYMETRY            ,
         is_required   = False                          ,
         description   = 'Bathymetry/Depth type to use.',
         mask          = Mask.RANGE                     ,
         values        = ['FLAT', 'DATA', 'SLOPE']      ,
         default_value = 'FLAT'                         ,
         dependencies  = None                           
      )
      self._BATHY_CORRECTION = Parameter(
         name          = 'BATHY_CORRECTION'                                                           ,
         fullname      = 'BATHY_CORRECTION'                                                           ,
         datatype      = Datatype.BOOL                                                                ,
         category      = Category.BATHYMETRY                                                          ,
         is_required   = False                                                                        ,
         description   = 'Flag to using built in interative local smoothing scheme to bathymetry data',
         mask          = Mask.NONE                                                                    ,
         values        = None                                                                         ,
         default_value = 'False'                                                                      ,
         dependencies  = None                                                                         
      )
      self._WaterLevel = Parameter(
         name          = 'WaterLevel'                                                                       ,
         fullname      = 'WaterLevel'                                                                       ,
         datatype      = Datatype.FLOAT                                                                     ,
         category      = Category.BATHYMETRY                                                                ,
         is_required   = False                                                                              ,
         description   = 'Additional water level to add/substract from still water level in bathymetry data',
         mask          = Mask.NONE                                                                          ,
         values        = None                                                                               ,
         default_value = '0'                                                                                ,
         dependencies  = None                                                                               
      )
      self._TOTAL_TIME = Parameter(
         name          = 'TOTAL_TIME'                   ,
         fullname      = 'TOTAL_TIME'                   ,
         datatype      = Datatype.FLOAT                 ,
         category      = Category.TIME                  ,
         is_required   = True                           ,
         description   = 'Total simulation time for run',
         mask          = Mask.POSITIVE_DEFINITE         ,
         values        = None                           ,
         default_value = None                           ,
         dependencies  = None                           
      )
      self._PLOT_START_TIME = Parameter(
         name          = 'PLOT_START_TIME'                              ,
         fullname      = 'PLOT_START_TIME'                              ,
         datatype      = Datatype.FLOAT                                 ,
         category      = Category.TIME                                  ,
         is_required   = False                                          ,
         description   = 'Optional offset for initial start time of run',
         mask          = Mask.POSITIVE                                  ,
         values        = None                                           ,
         default_value = '0'                                            ,
         dependencies  = None                                           
      )
      self._PLOT_INTV = Parameter(
         name          = 'PLOT_INTV'                                           ,
         fullname      = 'PLOT_INTV'                                           ,
         datatype      = Datatype.FLOAT                                        ,
         category      = Category.TIME                                         ,
         is_required   = False                                                 ,
         description   = 'Time interval between wrtiting 2D field data to file',
         mask          = Mask.POSITIVE_DEFINITE                                ,
         values        = None                                                  ,
         default_value = '1'                                                   ,
         dependencies  = None                                                  
      )
      self._SCREEN_INTV = Parameter(
         name          = 'SCREEN_INTV'                                             ,
         fullname      = 'SCREEN_INTV'                                             ,
         datatype      = Datatype.FLOAT                                            ,
         category      = Category.TIME                                             ,
         is_required   = False                                                     ,
         description   = 'Time interval between summary updates in log file output',
         mask          = Mask.POSITIVE_DEFINITE                                    ,
         values        = None                                                      ,
         default_value = '1'                                                       ,
         dependencies  = None                                                      
      )
      self._INI_UVZ = Parameter(
         name          = 'INI_UVZ'                                                                                                          ,
         fullname      = 'INI_UVZ'                                                                                                          ,
         datatype      = Datatype.BOOL                                                                                                      ,
         category      = Category.HOT_START                                                                                                 ,
         is_required   = False                                                                                                              ,
         description   = 'Flag for using hot start mode. Allows specifiying initial free surface height (eta) and velocities (u, v) for run',
         mask          = Mask.NONE                                                                                                          ,
         values        = None                                                                                                               ,
         default_value = 'False'                                                                                                            ,
         dependencies  = None                                                                                                               
      )
      self._WAVEMAKER = Parameter(
         name          = 'WAVEMAKER'                                                                                                                                                                       ,
         fullname      = 'WAVEMAKER'                                                                                                                                                                       ,
         datatype      = Datatype.ENUM                                                                                                                                                                     ,
         category      = Category.WAVE_MAKER                                                                                                                                                               ,
         is_required   = False                                                                                                                                                                             ,
         description   = 'Wave maker type to use in simulation'                                                                                                                                            ,
         mask          = Mask.RANGE                                                                                                                                                                        ,
         values        = ['LEF_SOL', 'WK_TIME', 'INI_SOL', 'N_WAVE', 'INI_REC', 'INI_GAU', 'INI_DIP', 'WK_REG', 'WK_IRR', 'TMA_1D', 'JON_1D', 'JON_2D', 'WK_NEW_DATA2D', 'WK_DATA2D', 'ABS', 'LEFT_BC_IRR'],
         default_value = None                                                                                                                                                                              ,
         dependencies  = None                                                                                                                                                                              
      )
      self._DIRECT_SPONGE = Parameter(
         name          = 'DIRECT_SPONGE',
         fullname      = 'DIRECT_SPONGE',
         datatype      = Datatype.BOOL  ,
         category      = Category.ERR   ,
         is_required   = False          ,
         description   = 'None'         ,
         mask          = Mask.NONE      ,
         values        = None           ,
         default_value = 'False'        ,
         dependencies  = None           
      )
      self._DIFFUSION_SPONGE = Parameter(
         name          = 'DIFFUSION_SPONGE',
         fullname      = 'DIFFUSION_SPONGE',
         datatype      = Datatype.BOOL     ,
         category      = Category.ERR      ,
         is_required   = False             ,
         description   = 'None'            ,
         mask          = Mask.NONE         ,
         values        = None              ,
         default_value = 'False'           ,
         dependencies  = None              
      )
      self._FRICTION_SPONGE = Parameter(
         name          = 'FRICTION_SPONGE',
         fullname      = 'FRICTION_SPONGE',
         datatype      = Datatype.BOOL    ,
         category      = Category.ERR     ,
         is_required   = False            ,
         description   = 'None'           ,
         mask          = Mask.NONE        ,
         values        = None             ,
         default_value = 'False'          ,
         dependencies  = None             
      )
      self._OBSTACLE_FILE = Parameter(
         name          = 'OBSTACLE_FILE',
         fullname      = 'OBSTACLE_FILE',
         datatype      = Datatype.PATH  ,
         category      = Category.ERR   ,
         is_required   = False          ,
         description   = 'None'         ,
         mask          = Mask.NONE      ,
         values        = None           ,
         default_value = None           ,
         dependencies  = None           
      )
      self._BREAKWATER_FILE = Parameter(
         name          = 'BREAKWATER_FILE',
         fullname      = 'BREAKWATER_FILE',
         datatype      = Datatype.PATH    ,
         category      = Category.ERR     ,
         is_required   = False            ,
         description   = 'None'           ,
         mask          = Mask.NONE        ,
         values        = None             ,
         default_value = None             ,
         dependencies  = None             
      )
      self._DISPERSION = Parameter(
         name          = 'DISPERSION'    ,
         fullname      = 'DISPERSION'    ,
         datatype      = Datatype.BOOL   ,
         category      = Category.PHYSICS,
         is_required   = False           ,
         description   = 'None'          ,
         mask          = Mask.NONE       ,
         values        = None            ,
         default_value = 'True'          ,
         dependencies  = None            
      )
      self._Gamma1 = Parameter(
         name          = 'Gamma1'        ,
         fullname      = 'Gamma1'        ,
         datatype      = Datatype.FLOAT  ,
         category      = Category.PHYSICS,
         is_required   = False           ,
         description   = 'None'          ,
         mask          = Mask.POSITIVE   ,
         values        = None            ,
         default_value = '1'             ,
         dependencies  = None            
      )
      self._FRICTION_MATRIX = Parameter(
         name          = 'FRICTION_MATRIX',
         fullname      = 'FRICTION_MATRIX',
         datatype      = Datatype.BOOL    ,
         category      = Category.PHYSICS ,
         is_required   = False            ,
         description   = 'None'           ,
         mask          = Mask.NONE        ,
         values        = None             ,
         default_value = 'False'          ,
         dependencies  = None             
      )
      self._Time_Scheme = Parameter(
         name          = 'Time_Scheme'                         ,
         fullname      = 'Time_Scheme'                         ,
         datatype      = Datatype.ENUM                         ,
         category      = Category.NUMERICS                     ,
         is_required   = False                                 ,
         description   = 'None'                                ,
         mask          = Mask.RANGE                            ,
         values        = ['Runge_Kutta', 'Predictor_Corrector'],
         default_value = 'Runge_Kutta'                         ,
         dependencies  = None                                  
      )
      self._CONSTRUCTION = Parameter(
         name          = 'CONSTRUCTION'   ,
         fullname      = 'CONSTRUCTION'   ,
         datatype      = Datatype.ENUM    ,
         category      = Category.NUMERICS,
         is_required   = False            ,
         description   = 'None'           ,
         mask          = Mask.RANGE       ,
         values        = ['HLLC']         ,
         default_value = 'HLLC'           ,
         dependencies  = None             
      )
      self._HIGH_ORDER = Parameter(
         name          = 'HIGH_ORDER'       ,
         fullname      = 'HIGH_ORDER'       ,
         datatype      = Datatype.ENUM      ,
         category      = Category.NUMERICS  ,
         is_required   = False              ,
         description   = 'None'             ,
         mask          = Mask.RANGE         ,
         values        = ['FOURTH', 'THIRD'],
         default_value = 'FOURTH'           ,
         dependencies  = None               
      )
      self._CFL = Parameter(
         name          = 'CFL'                 ,
         fullname      = 'CFL'                 ,
         datatype      = Datatype.FLOAT        ,
         category      = Category.NUMERICS     ,
         is_required   = False                 ,
         description   = 'None'                ,
         mask          = Mask.POSITIVE_DEFINITE,
         values        = None                  ,
         default_value = '0.5'                 ,
         dependencies  = None                  
      )
      self._FIXED_DT = Parameter(
         name          = 'FIXED_DT'       ,
         fullname      = 'FIXED_DT'       ,
         datatype      = Datatype.BOOL    ,
         category      = Category.NUMERICS,
         is_required   = False            ,
         description   = 'None'           ,
         mask          = Mask.NONE        ,
         values        = None             ,
         default_value = 'False'          ,
         dependencies  = None             
      )
      self._FroudeCap = Parameter(
         name          = 'FroudeCap'           ,
         fullname      = 'FroudeCap'           ,
         datatype      = Datatype.FLOAT        ,
         category      = Category.NUMERICS     ,
         is_required   = False                 ,
         description   = 'None'                ,
         mask          = Mask.POSITIVE_DEFINITE,
         values        = None                  ,
         default_value = '3'                   ,
         dependencies  = None                  
      )
      self._MinDepth = Parameter(
         name          = 'MinDepth'            ,
         fullname      = 'MinDepth'            ,
         datatype      = Datatype.FLOAT        ,
         category      = Category.NUMERICS     ,
         is_required   = False                 ,
         description   = 'None'                ,
         mask          = Mask.POSITIVE_DEFINITE,
         values        = None                  ,
         default_value = '0.1'                 ,
         dependencies  = None                  
      )
      self._MinDepthFrc = Parameter(
         name          = 'MinDepthFrc'         ,
         fullname      = 'MinDepthFrc'         ,
         datatype      = Datatype.FLOAT        ,
         category      = Category.NUMERICS     ,
         is_required   = False                 ,
         description   = 'None'                ,
         mask          = Mask.POSITIVE_DEFINITE,
         values        = None                  ,
         default_value = '0.1'                 ,
         dependencies  = None                  
      )
      self._OUT_Time = Parameter(
         name          = 'OUT_Time'       ,
         fullname      = 'OUT_Time'       ,
         datatype      = Datatype.BOOL    ,
         category      = Category.NUMERICS,
         is_required   = False            ,
         description   = 'None'           ,
         mask          = Mask.NONE        ,
         values        = None             ,
         default_value = 'False'          ,
         dependencies  = None             
      )
      self._NumberStations = Parameter(
         name          = 'NumberStations' ,
         fullname      = 'NumberStations' ,
         datatype      = Datatype.INTEGER ,
         category      = Category.STATIONS,
         is_required   = False            ,
         description   = 'None'           ,
         mask          = Mask.POSITIVE    ,
         values        = None             ,
         default_value = '0'              ,
         dependencies  = None             
      )
      self._ROLLER_EFFECT = Parameter(
         name          = 'ROLLER_EFFECT',
         fullname      = 'ROLLER_EFFECT',
         datatype      = Datatype.BOOL  ,
         category      = Category.ERR   ,
         is_required   = False          ,
         description   = 'None'         ,
         mask          = Mask.NONE      ,
         values        = None           ,
         default_value = 'False'        ,
         dependencies  = None           
      )
      self._VISCOSITY_BREAKING = Parameter(
         name          = 'VISCOSITY_BREAKING',
         fullname      = 'VISCOSITY_BREAKING',
         datatype      = Datatype.BOOL       ,
         category      = Category.ERR        ,
         is_required   = False               ,
         description   = 'None'              ,
         mask          = Mask.NONE           ,
         values        = None                ,
         default_value = 'True'              ,
         dependencies  = None                
      )
      self._SHOW_BREAKING = Parameter(
         name          = 'SHOW_BREAKING',
         fullname      = 'SHOW_BREAKING',
         datatype      = Datatype.BOOL  ,
         category      = Category.ERR   ,
         is_required   = False          ,
         description   = 'None'         ,
         mask          = Mask.NONE      ,
         values        = None           ,
         default_value = 'True'         ,
         dependencies  = None           
      )
      self._WAVEMAKER_Cbrk = Parameter(
         name          = 'WAVEMAKER_Cbrk',
         fullname      = 'WAVEMAKER_Cbrk',
         datatype      = Datatype.FLOAT  ,
         category      = Category.ERR    ,
         is_required   = False           ,
         description   = 'None'          ,
         mask          = Mask.NONE       ,
         values        = None            ,
         default_value = '1'             ,
         dependencies  = None            
      )
      self._WAVEMAKER_VIS = Parameter(
         name          = 'WAVEMAKER_VIS',
         fullname      = 'WAVEMAKER_VIS',
         datatype      = Datatype.BOOL  ,
         category      = Category.ERR   ,
         is_required   = False          ,
         description   = 'None'         ,
         mask          = Mask.NONE      ,
         values        = None           ,
         default_value = 'False'        ,
         dependencies  = None           
      )
      self._PX = Parameter(
         name          = 'PX'                                                     ,
         fullname      = 'Parallel'                                               ,
         datatype      = Datatype.INTEGER                                         ,
         category      = Category.PARALLEL                                        ,
         is_required   = False                                                    ,
         description   = 'Number for parallel cores/threads to use in x direction',
         mask          = Mask.POSITIVE_DEFINITE                                   ,
         values        = None                                                     ,
         default_value = '1'                                                      ,
         dependencies  = [('PARALLEL', 'True')]                                   
      )
      self._PY = Parameter(
         name          = 'PY'                                                     ,
         fullname      = 'Parallel'                                               ,
         datatype      = Datatype.INTEGER                                         ,
         category      = Category.PARALLEL                                        ,
         is_required   = False                                                    ,
         description   = 'Number for parallel cores/threads to use in y direction',
         mask          = Mask.POSITIVE_DEFINITE                                   ,
         values        = None                                                     ,
         default_value = '1'                                                      ,
         dependencies  = [('PARALLEL', 'True')]                                   
      )
      self._DX = Parameter(
         name          = 'DX'                                   ,
         fullname      = 'DX'                                   ,
         datatype      = Datatype.FLOAT                         ,
         category      = Category.GRID                          ,
         is_required   = True                                   ,
         description   = 'Spatial resolution in the x direction',
         mask          = Mask.POSITIVE_DEFINITE                 ,
         values        = None                                   ,
         default_value = None                                   ,
         dependencies  = [('CARTESIAN', 'True')]                
      )
      self._DY = Parameter(
         name          = 'DY'                                   ,
         fullname      = 'DY'                                   ,
         datatype      = Datatype.FLOAT                         ,
         category      = Category.GRID                          ,
         is_required   = True                                   ,
         description   = 'Spatial resolution in the y direction',
         mask          = Mask.POSITIVE_DEFINITE                 ,
         values        = None                                   ,
         default_value = None                                   ,
         dependencies  = [('CARTESIAN', 'True')]                
      )
      self._StretchGrid = Parameter(
         name          = 'StretchGrid'                                       ,
         fullname      = 'StretchGrid'                                       ,
         datatype      = Datatype.BOOL                                       ,
         category      = Category.GRID                                       ,
         is_required   = False                                               ,
         description   = 'Flag for using a grid varying grid point spacing. ',
         mask          = Mask.NONE                                           ,
         values        = None                                                ,
         default_value = 'False'                                             ,
         dependencies  = [('CARTESIAN', 'False')]                            
      )
      self._DEPTH_FILE = Parameter(
         name          = 'DEPTH_FILE'                                                                                                      ,
         fullname      = 'DEPTH_FILE'                                                                                                      ,
         datatype      = Datatype.PATH                                                                                                     ,
         category      = Category.BATHYMETRY                                                                                               ,
         is_required   = True                                                                                                              ,
         description   = 'Path to text file of still water level depth at each grid point. Note, positive values denote below water level.',
         mask          = Mask.NONE                                                                                                         ,
         values        = None                                                                                                              ,
         default_value = None                                                                                                              ,
         dependencies  = [('DEPTH_TYPE', 'DATA')]                                                                                          
      )
      self._DEPTH_FLAT = Parameter(
         name          = 'DEPTH_FLAT'                                                                          ,
         fullname      = 'DEPTH_FLAT'                                                                          ,
         datatype      = Datatype.FLOAT                                                                        ,
         category      = Category.BATHYMETRY                                                                   ,
         is_required   = False                                                                                 ,
         description   = 'Depth of flat region in bathymetry. Note, positive values denote below water level. ',
         mask          = Mask.POSITIVE_DEFINITE                                                                ,
         values        = None                                                                                  ,
         default_value = '10'                                                                                  ,
         dependencies  = [('DEPTH_TYPE', 'FLAT')]                                                              
      )
      self._SLP = Parameter(
         name          = 'SLP'                    ,
         fullname      = 'SLP'                    ,
         datatype      = Datatype.FLOAT           ,
         category      = Category.BATHYMETRY      ,
         is_required   = False                    ,
         description   = 'Slope of beach'         ,
         mask          = Mask.NONE                ,
         values        = None                     ,
         default_value = '0.1'                    ,
         dependencies  = [('DEPTH_TYPE', 'SLOPE')]
      )
      self._Xslp = Parameter(
         name          = 'Xslp'                                                         ,
         fullname      = 'Xlsp'                                                         ,
         datatype      = Datatype.FLOAT                                                 ,
         category      = Category.BATHYMETRY                                            ,
         is_required   = False                                                          ,
         description   = 'x location to transition between flat depth and slope region.',
         mask          = Mask.POSITIVE                                                  ,
         values        = None                                                           ,
         default_value = '0'                                                            ,
         dependencies  = [('DEPTH_TYPE', 'SLOPE')]                                      
      )
      self._BED_DEFORMATION = Parameter(
         name          = 'BED_DEFORMATION'    ,
         fullname      = 'BED_DEFORMATION'    ,
         datatype      = Datatype.BOOL        ,
         category      = Category.HOT_START   ,
         is_required   = False                ,
         description   = 'DEPRECATED?'        ,
         mask          = Mask.NONE            ,
         values        = None                 ,
         default_value = 'False'              ,
         dependencies  = [('INI_UVZ', 'True')]
      )
      self._ETA_FILE = Parameter(
         name          = 'ETA_FILE'                                                                  ,
         fullname      = 'ETA_FILE'                                                                  ,
         datatype      = Datatype.PATH                                                               ,
         category      = Category.HOT_START                                                          ,
         is_required   = True                                                                        ,
         description   = 'Path to initial free surface height at grid points  to initialize run with',
         mask          = Mask.NONE                                                                   ,
         values        = None                                                                        ,
         default_value = None                                                                        ,
         dependencies  = [('INI_UVZ', 'True')]                                                       
      )
      self._U_FILE = Parameter(
         name          = 'U_FILE'                                                                                 ,
         fullname      = 'U_FILE'                                                                                 ,
         datatype      = Datatype.PATH                                                                            ,
         category      = Category.HOT_START                                                                       ,
         is_required   = False                                                                                    ,
         description   = 'Optional path to initial x-direction velocities, u, at grid points  for hot start mode.',
         mask          = Mask.NONE                                                                                ,
         values        = None                                                                                     ,
         default_value = None                                                                                     ,
         dependencies  = [('INI_UVZ', 'True')]                                                                    
      )
      self._V_FILE = Parameter(
         name          = 'V_FILE'                                                                                 ,
         fullname      = 'V_FILE'                                                                                 ,
         datatype      = Datatype.PATH                                                                            ,
         category      = Category.HOT_START                                                                       ,
         is_required   = False                                                                                    ,
         description   = 'Optional path to initial y-direction velocities, v, at grid points  for hot start mode.',
         mask          = Mask.NONE                                                                                ,
         values        = None                                                                                     ,
         default_value = None                                                                                     ,
         dependencies  = [('INI_UVZ', 'True')]                                                                    
      )
      self._MASK_FILE = Parameter(
         name          = 'MASK_FILE'          ,
         fullname      = 'MASK_FILE'          ,
         datatype      = Datatype.PATH        ,
         category      = Category.HOT_START   ,
         is_required   = False                ,
         description   = 'DEPRECATED?'        ,
         mask          = Mask.NONE            ,
         values        = None                 ,
         default_value = None                 ,
         dependencies  = [('INI_UVZ', 'True')]
      )
      self._HotStartTime = Parameter(
         name          = 'HotStartTime'                                           ,
         fullname      = 'HotStartTime'                                           ,
         datatype      = Datatype.FLOAT                                           ,
         category      = Category.HOT_START                                       ,
         is_required   = False                                                    ,
         description   = 'Optional offset for initial start time of hot start run',
         mask          = Mask.POSITIVE                                            ,
         values        = None                                                     ,
         default_value = '0'                                                      ,
         dependencies  = [('INI_UVZ', 'True')]                                    
      )
      self._OutputStartNumber = Parameter(
         name          = 'OutputStartNumber'                                                         ,
         fullname      = 'OutputStartNumber'                                                         ,
         datatype      = Datatype.INTEGER                                                            ,
         category      = Category.HOT_START                                                          ,
         is_required   = False                                                                       ,
         description   = 'Optional offset number for field data file output numbers in hot start run',
         mask          = Mask.POSITIVE                                                               ,
         values        = None                                                                        ,
         default_value = '1'                                                                         ,
         dependencies  = [('INI_UVZ', 'True')]                                                       
      )
      self._AMP = Parameter(
         name          = 'AMP'                      ,
         fullname      = 'AMP'                      ,
         datatype      = Datatype.FLOAT             ,
         category      = Category.WAVE_MAKER        ,
         is_required   = True                       ,
         description   = 'None'                     ,
         mask          = Mask.POSITIVE_DEFINITE     ,
         values        = None                       ,
         default_value = None                       ,
         dependencies  = [('WAVEMAKER', 'LEFT_SOL')]
      )
      self._DEP = Parameter(
         name          = 'DEP'                      ,
         fullname      = 'DEP'                      ,
         datatype      = Datatype.FLOAT             ,
         category      = Category.WAVE_MAKER        ,
         is_required   = True                       ,
         description   = 'None'                     ,
         mask          = Mask.POSITIVE_DEFINITE     ,
         values        = None                       ,
         default_value = None                       ,
         dependencies  = [('WAVEMAKER', 'LEFT_SOL')]
      )
      self._LAGTIME = Parameter(
         name          = 'LAGTIME'                  ,
         fullname      = 'LAGTIME'                  ,
         datatype      = Datatype.FLOAT             ,
         category      = Category.WAVE_MAKER        ,
         is_required   = False                      ,
         description   = 'None'                     ,
         mask          = Mask.POSITIVE              ,
         values        = None                       ,
         default_value = '0'                        ,
         dependencies  = [('WAVEMAKER', 'LEFT_SOL')]
      )
      self._NumWaveComp = Parameter(
         name          = 'NumWaveComp'             ,
         fullname      = 'NumWaveComp'             ,
         datatype      = Datatype.INTEGER          ,
         category      = Category.WAVE_MAKER       ,
         is_required   = True                      ,
         description   = 'None'                    ,
         mask          = Mask.POSITIVE             ,
         values        = None                      ,
         default_value = None                      ,
         dependencies  = [('WAVEMAKER', 'WK_TIME')]
      )
      self._PeakPeriod = Parameter(
         name          = 'PeakPeriod'              ,
         fullname      = 'PeakPeriod'              ,
         datatype      = Datatype.FLOAT            ,
         category      = Category.WAVE_MAKER       ,
         is_required   = True                      ,
         description   = 'None'                    ,
         mask          = Mask.POSITIVE             ,
         values        = None                      ,
         default_value = None                      ,
         dependencies  = [('WAVEMAKER', 'WK_TIME')]
      )
      self._Xc_WK = Parameter(
         name          = 'Xc_WK'                   ,
         fullname      = 'Xc_WK'                   ,
         datatype      = Datatype.FLOAT            ,
         category      = Category.WAVE_MAKER       ,
         is_required   = True                      ,
         description   = 'None'                    ,
         mask          = Mask.POSITIVE             ,
         values        = None                      ,
         default_value = None                      ,
         dependencies  = [('WAVEMAKER', 'WK_TIME')]
      )
      self._Yc_WK = Parameter(
         name          = 'Yc_WK'                   ,
         fullname      = 'Yc_WK'                   ,
         datatype      = Datatype.FLOAT            ,
         category      = Category.WAVE_MAKER       ,
         is_required   = False                     ,
         description   = 'None'                    ,
         mask          = Mask.POSITIVE             ,
         values        = None                      ,
         default_value = '0'                       ,
         dependencies  = [('WAVEMAKER', 'WK_TIME')]
      )
      self._DEP_WK = Parameter(
         name          = 'DEP_WK'                  ,
         fullname      = 'DEP_WK'                  ,
         datatype      = Datatype.FLOAT            ,
         category      = Category.WAVE_MAKER       ,
         is_required   = True                      ,
         description   = 'None'                    ,
         mask          = Mask.POSITIVE             ,
         values        = None                      ,
         default_value = '0'                       ,
         dependencies  = [('WAVEMAKER', 'WK_TIME')]
      )
      self._Time_ramp = Parameter(
         name          = 'Time_ramp'               ,
         fullname      = 'Time_ramp'               ,
         datatype      = Datatype.FLOAT            ,
         category      = Category.WAVE_MAKER       ,
         is_required   = False                     ,
         description   = 'None'                    ,
         mask          = Mask.POSITIVE             ,
         values        = None                      ,
         default_value = '0'                       ,
         dependencies  = [('WAVEMAKER', 'WK_TIME')]
      )
      self._Delta_WK = Parameter(
         name          = 'Delta_WK'                ,
         fullname      = 'Delta_WK'                ,
         datatype      = Datatype.FLOAT            ,
         category      = Category.WAVE_MAKER       ,
         is_required   = False                     ,
         description   = 'None'                    ,
         mask          = Mask.POSITIVE_DEFINITE    ,
         values        = None                      ,
         default_value = '0.5'                     ,
         dependencies  = [('WAVEMAKER', 'WK_TIME')]
      )
      self._Ywidth_WK = Parameter(
         name          = 'Ywidth_WK'               ,
         fullname      = 'Ywidth_WK'               ,
         datatype      = Datatype.FLOAT            ,
         category      = Category.WAVE_MAKER       ,
         is_required   = False                     ,
         description   = 'None'                    ,
         mask          = Mask.POSITIVE             ,
         values        = None                      ,
         default_value = 999999                    ,
         dependencies  = [('WAVEMAKER', 'WK_TIME')]
      )
      self._SolitaryPositiveDirection = Parameter(
         name          = 'SolitaryPositiveDirection',
         fullname      = 'SolitaryPositiveDirection',
         datatype      = Datatype.BOOL              ,
         category      = Category.WAVE_MAKER        ,
         is_required   = False                      ,
         description   = 'None'                     ,
         mask          = Mask.NONE                  ,
         values        = None                       ,
         default_value = 'True'                     ,
         dependencies  = [('WAVEMAKER', 'INI_SOL')] 
      )
      self._XWAVEMARKER = Parameter(
         name          = 'XWAVEMARKER'             ,
         fullname      = 'XWAVEMAKER'              ,
         datatype      = Datatype.FLOAT            ,
         category      = Category.WAVE_MAKER       ,
         is_required   = True                      ,
         description   = 'None'                    ,
         mask          = Mask.POSITIVE             ,
         values        = None                      ,
         default_value = None                      ,
         dependencies  = [('WAVEMAKER', 'INI_SOL')]
      )
      self._x1_Nwave = Parameter(
         name          = 'x1_Nwave'               ,
         fullname      = 'x1_Nwave'               ,
         datatype      = Datatype.FLOAT           ,
         category      = Category.WAVE_MAKER      ,
         is_required   = True                     ,
         description   = 'None'                   ,
         mask          = Mask.POSITIVE            ,
         values        = None                     ,
         default_value = None                     ,
         dependencies  = [('WAVEMAKER', 'N_WAVE')]
      )
      self._x2_Nwave = Parameter(
         name          = 'x2_Nwave'               ,
         fullname      = 'x2_Nwave'               ,
         datatype      = Datatype.FLOAT           ,
         category      = Category.WAVE_MAKER      ,
         is_required   = True                     ,
         description   = 'None'                   ,
         mask          = Mask.POSITIVE            ,
         values        = None                     ,
         default_value = None                     ,
         dependencies  = [('WAVEMAKER', 'N_WAVE')]
      )
      self._a0_Nwave = Parameter(
         name          = 'a0_Nwave'               ,
         fullname      = 'a0_Nwave'               ,
         datatype      = Datatype.FLOAT           ,
         category      = Category.WAVE_MAKER      ,
         is_required   = True                     ,
         description   = 'None'                   ,
         mask          = Mask.POSITIVE            ,
         values        = None                     ,
         default_value = None                     ,
         dependencies  = [('WAVEMAKER', 'N_WAVE')]
      )
      self._gamma_Nwave = Parameter(
         name          = 'gamma_Nwave'            ,
         fullname      = 'gamma_Nwave'            ,
         datatype      = Datatype.FLOAT           ,
         category      = Category.WAVE_MAKER      ,
         is_required   = True                     ,
         description   = 'None'                   ,
         mask          = Mask.POSITIVE            ,
         values        = None                     ,
         default_value = None                     ,
         dependencies  = [('WAVEMAKER', 'N_WAVE')]
      )
      self._dep_Nwave = Parameter(
         name          = 'dep_Nwave'              ,
         fullname      = 'dep_Nwave'              ,
         datatype      = Datatype.FLOAT           ,
         category      = Category.WAVE_MAKER      ,
         is_required   = True                     ,
         description   = 'None'                   ,
         mask          = Mask.POSITIVE_DEFINITE   ,
         values        = None                     ,
         default_value = None                     ,
         dependencies  = [('WAVEMAKER', 'N_WAVE')]
      )
      self._Xc = Parameter(
         name          = 'Xc'                      ,
         fullname      = 'Xc'                      ,
         datatype      = Datatype.FLOAT            ,
         category      = Category.WAVE_MAKER       ,
         is_required   = True                      ,
         description   = 'None'                    ,
         mask          = Mask.POSITIVE             ,
         values        = None                      ,
         default_value = None                      ,
         dependencies  = [('WAVEMAKER', 'INI_REC')]
      )
      self._Yc = Parameter(
         name          = 'Yc'                      ,
         fullname      = 'Yc'                      ,
         datatype      = Datatype.FLOAT            ,
         category      = Category.WAVE_MAKER       ,
         is_required   = False                     ,
         description   = 'None'                    ,
         mask          = Mask.POSITIVE             ,
         values        = None                      ,
         default_value = '0'                       ,
         dependencies  = [('WAVEMAKER', 'INI_REC')]
      )
      self._WID = Parameter(
         name          = 'WID'                     ,
         fullname      = 'WID'                     ,
         datatype      = Datatype.FLOAT            ,
         category      = Category.WAVE_MAKER       ,
         is_required   = True                      ,
         description   = 'None'                    ,
         mask          = Mask.NONE                 ,
         values        = None                      ,
         default_value = None                      ,
         dependencies  = [('WAVEMAKER', 'INI_REC')]
      )
      self._Tperiod = Parameter(
         name          = 'Tperiod'                ,
         fullname      = 'Tperiod'                ,
         datatype      = Datatype.FLOAT           ,
         category      = Category.WAVE_MAKER      ,
         is_required   = True                     ,
         description   = 'None'                   ,
         mask          = Mask.POSITIVE_DEFINITE   ,
         values        = None                     ,
         default_value = None                     ,
         dependencies  = [('WAVEMAKER', 'WK_REG')]
      )
      self._AMP_WK = Parameter(
         name          = 'AMP_WK'                 ,
         fullname      = 'AMP_WK'                 ,
         datatype      = Datatype.FLOAT           ,
         category      = Category.WAVE_MAKER      ,
         is_required   = True                     ,
         description   = 'None'                   ,
         mask          = Mask.POSITIVE_DEFINITE   ,
         values        = None                     ,
         default_value = None                     ,
         dependencies  = [('WAVEMAKER', 'WK_REG')]
      )
      self._Theta_WK = Parameter(
         name          = 'Theta_WK'               ,
         fullname      = 'Theta_WK'               ,
         datatype      = Datatype.FLOAT           ,
         category      = Category.WAVE_MAKER      ,
         is_required   = False                    ,
         description   = 'None'                   ,
         mask          = Mask.NONE                ,
         values        = None                     ,
         default_value = '0'                      ,
         dependencies  = [('WAVEMAKER', 'WK_REG')]
      )
      self._alpha_c = Parameter(
         name          = 'alpha_c'                    ,
         fullname      = 'alpha_c'                    ,
         datatype      = Datatype.FLOAT               ,
         category      = Category.WAVE_MAKER          ,
         is_required   = False                        ,
         description   = 'None'                       ,
         mask          = Mask.POSITIVE                ,
         values        = None                         ,
         default_value = '0'                          ,
         dependencies  = [('WAVEMAKER', 'WK_NEW_IRR')]
      )
      self._EqualEnergy = Parameter(
         name          = 'EqualEnergy'            ,
         fullname      = 'EqualEnergy'            ,
         datatype      = Datatype.BOOL            ,
         category      = Category.WAVE_MAKER      ,
         is_required   = False                    ,
         description   = 'None'                   ,
         mask          = Mask.NONE                ,
         values        = None                     ,
         default_value = 'False'                  ,
         dependencies  = [('WAVEMAKER', 'WK_IRR')]
      )
      self._WAVE_DATA_TYPE = Parameter(
         name          = 'WAVE_DATA_TYPE'                             ,
         fullname      = 'WAVE_DATA_TYPE'                             ,
         datatype      = Datatype.ENUM                                ,
         category      = Category.WAVE_MAKER                          ,
         is_required   = False                                        ,
         description   = 'None'                                       ,
         mask          = Mask.RANGE                                   ,
         values        = ['ABS', 'DATA', 'TMA_1D', 'JON_1D', 'JON_2D'],
         default_value = None                                         ,
         dependencies  = [('WAVEMAKER', 'ABS')]                       
      )
      self._DepthWaveMaker = Parameter(
         name          = 'DepthWaveMaker'      ,
         fullname      = 'DepthWaveMaker'      ,
         datatype      = Datatype.FLOAT        ,
         category      = Category.WAVE_MAKER   ,
         is_required   = False                 ,
         description   = 'None'                ,
         mask          = Mask.POSITIVE_DEFINITE,
         values        = None                  ,
         default_value = None                  ,
         dependencies  = [('WAVEMAKER', 'ABS')]
      )
      self._ETA_LIMITER = Parameter(
         name          = 'ETA_LIMITER'             ,
         fullname      = 'ETA_LIMITER'             ,
         datatype      = Datatype.BOOL             ,
         category      = Category.WAVE_MAKER       ,
         is_required   = False                     ,
         description   = 'None'                    ,
         mask          = Mask.NONE                 ,
         values        = None                      ,
         default_value = 'False'                   ,
         dependencies  = [('WAVEMAKER', 'LEF_SOL')]
      )
      self._WaveMakerCd = Parameter(
         name          = 'WaveMakerCd'             ,
         fullname      = 'WaveMakerCd'             ,
         datatype      = Datatype.FLOAT            ,
         category      = Category.WAVE_MAKER       ,
         is_required   = False                     ,
         description   = 'None'                    ,
         mask          = Mask.NONE                 ,
         values        = None                      ,
         default_value = None                      ,
         dependencies  = [('WAVEMAKER', 'LEF_SOL')]
      )
      self._PERODIC = Parameter(
         name          = 'PERODIC'              ,
         fullname      = 'PERODIC'              ,
         datatype      = Datatype.BOOL          ,
         category      = Category.ERR           ,
         is_required   = False                  ,
         description   = 'None'                 ,
         mask          = Mask.NONE              ,
         values        = None                   ,
         default_value = 'False'                ,
         dependencies  = [('CARTESIAN', 'True')]
      )
      self._Csp = Parameter(
         name          = 'Csp'                         ,
         fullname      = 'Csp'                         ,
         datatype      = Datatype.FLOAT                ,
         category      = Category.ERR                  ,
         is_required   = False                         ,
         description   = 'None'                        ,
         mask          = Mask.POSITIVE_DEFINITE        ,
         values        = None                          ,
         default_value = '0.1'                         ,
         dependencies  = [('DIFFUSION_SPONGE', 'True')]
      )
      self._CDsponge = Parameter(
         name          = 'CDsponge'                   ,
         fullname      = 'CDsponge'                   ,
         datatype      = Datatype.FLOAT               ,
         category      = Category.ERR                 ,
         is_required   = False                        ,
         description   = 'None'                       ,
         mask          = Mask.POSITIVE_DEFINITE       ,
         values        = None                         ,
         default_value = '5'                          ,
         dependencies  = [('FRICTION_SPONGE', 'True')]
      )
      self._Sponge_west_width = Parameter(
         name          = 'Sponge_west_width'                                                             ,
         fullname      = 'Sponge_west_width'                                                             ,
         datatype      = Datatype.FLOAT                                                                  ,
         category      = Category.ERR                                                                    ,
         is_required   = False                                                                           ,
         description   = 'None'                                                                          ,
         mask          = Mask.POSITIVE                                                                   ,
         values        = None                                                                            ,
         default_value = '0'                                                                             ,
         dependencies  = [('DIRECT_SPONGE', True), ('DIFFUSION_SPONGE', True), ('FRICTION_SPONGE', True)]
      )
      self._Sponge_east_width = Parameter(
         name          = 'Sponge_east_width'                                                             ,
         fullname      = 'Sponge_east_width'                                                             ,
         datatype      = Datatype.FLOAT                                                                  ,
         category      = Category.ERR                                                                    ,
         is_required   = False                                                                           ,
         description   = 'None'                                                                          ,
         mask          = Mask.POSITIVE                                                                   ,
         values        = None                                                                            ,
         default_value = '0'                                                                             ,
         dependencies  = [('DIRECT_SPONGE', True), ('DIFFUSION_SPONGE', True), ('FRICTION_SPONGE', True)]
      )
      self._Sponge_south_width = Parameter(
         name          = 'Sponge_south_width'                                                            ,
         fullname      = 'Sponge_south_width'                                                            ,
         datatype      = Datatype.FLOAT                                                                  ,
         category      = Category.ERR                                                                    ,
         is_required   = False                                                                           ,
         description   = 'None'                                                                          ,
         mask          = Mask.POSITIVE                                                                   ,
         values        = None                                                                            ,
         default_value = '0'                                                                             ,
         dependencies  = [('DIRECT_SPONGE', True), ('DIFFUSION_SPONGE', True), ('FRICTION_SPONGE', True)]
      )
      self._Sponge_north_width = Parameter(
         name          = 'Sponge_north_width'                                                            ,
         fullname      = 'Sponge_north_width'                                                            ,
         datatype      = Datatype.FLOAT                                                                  ,
         category      = Category.ERR                                                                    ,
         is_required   = False                                                                           ,
         description   = 'None'                                                                          ,
         mask          = Mask.POSITIVE                                                                   ,
         values        = None                                                                            ,
         default_value = '0'                                                                             ,
         dependencies  = [('DIRECT_SPONGE', True), ('DIFFUSION_SPONGE', True), ('FRICTION_SPONGE', True)]
      )
      self._R_sponge = Parameter(
         name          = 'R_sponge'                                                                      ,
         fullname      = 'R_sponge'                                                                      ,
         datatype      = Datatype.FLOAT                                                                  ,
         category      = Category.ERR                                                                    ,
         is_required   = False                                                                           ,
         description   = 'None'                                                                          ,
         mask          = Mask.POSITIVE_DEFINITE                                                          ,
         values        = None                                                                            ,
         default_value = '0.85'                                                                          ,
         dependencies  = [('DIRECT_SPONGE', True), ('DIFFUSION_SPONGE', True), ('FRICTION_SPONGE', True)]
      )
      self._A_sponge = Parameter(
         name          = 'A_sponge'                                                                      ,
         fullname      = 'A_sponge'                                                                      ,
         datatype      = Datatype.FLOAT                                                                  ,
         category      = Category.ERR                                                                    ,
         is_required   = False                                                                           ,
         description   = 'None'                                                                          ,
         mask          = Mask.POSITIVE_DEFINITE                                                          ,
         values        = None                                                                            ,
         default_value = '5'                                                                             ,
         dependencies  = [('DIRECT_SPONGE', True), ('DIFFUSION_SPONGE', True), ('FRICTION_SPONGE', True)]
      )
      self._BreakWaterAbsorbCoef = Parameter(
         name          = 'BreakWaterAbsorbCoef'          ,
         fullname      = 'BreakWaterAbsorbCoef'          ,
         datatype      = Datatype.FLOAT                  ,
         category      = Category.ERR                    ,
         is_required   = False                           ,
         description   = 'None'                          ,
         mask          = Mask.NONE                       ,
         values        = None                            ,
         default_value = '10'                            ,
         dependencies  = [('BREAKWATER_FILE', 'Defined')]
      )
      self._Gamma2 = Parameter(
         name          = 'Gamma2'               ,
         fullname      = 'Gamma2'               ,
         datatype      = Datatype.FLOAT         ,
         category      = Category.PHYSICS       ,
         is_required   = False                  ,
         description   = 'None'                 ,
         mask          = Mask.POSITIVE          ,
         values        = None                   ,
         default_value = '1'                    ,
         dependencies  = [('CARTESIAN', 'True')]
      )
      self._Beta_ref = Parameter(
         name          = 'Beta_ref'                             ,
         fullname      = 'Beta_ref'                             ,
         datatype      = Datatype.FLOAT                         ,
         category      = Category.PHYSICS                       ,
         is_required   = False                                  ,
         description   = 'None'                                 ,
         mask          = Mask.NONE                              ,
         values        = None                                   ,
         default_value = '-0.531'                               ,
         dependencies  = [('CARTESIAN', True), ('ZALPHA', True)]
      )
      self._Gamma3 = Parameter(
         name          = 'Gamma3'               ,
         fullname      = 'Gamma3'               ,
         datatype      = Datatype.FLOAT         ,
         category      = Category.PHYSICS       ,
         is_required   = False                  ,
         description   = 'None'                 ,
         mask          = Mask.POSITIVE          ,
         values        = None                   ,
         default_value = '1'                    ,
         dependencies  = [('CARTESIAN', 'True')]
      )
      self._FRICTION_FILE = Parameter(
         name          = 'FRICTION_FILE'              ,
         fullname      = 'FRICTION_FILE'              ,
         datatype      = Datatype.PATH                ,
         category      = Category.PHYSICS             ,
         is_required   = True                         ,
         description   = 'None'                       ,
         mask          = Mask.NONE                    ,
         values        = None                         ,
         default_value = None                         ,
         dependencies  = [('FRICTION_MATRIX', 'True')]
      )
      self._Cd = Parameter(
         name          = 'Cd'                          ,
         fullname      = 'Cd'                          ,
         datatype      = Datatype.FLOAT                ,
         category      = Category.PHYSICS              ,
         is_required   = False                         ,
         description   = 'None'                        ,
         mask          = Mask.POSITIVE                 ,
         values        = None                          ,
         default_value = '0'                           ,
         dependencies  = [('FRICTION_MATRIX', 'False')]
      )
      self._ArrTimeMin = Parameter(
         name          = 'ArrTimeMin'          ,
         fullname      = 'ArrTimeMin'          ,
         datatype      = Datatype.FLOAT        ,
         category      = Category.NUMERICS     ,
         is_required   = False                 ,
         description   = 'None'                ,
         mask          = Mask.NONE             ,
         values        = None                  ,
         default_value = '0.001'               ,
         dependencies  = [('OUT_Time', 'True')]
      )
      self._PLOT_INTV_STATION = Parameter(
         name          = 'PLOT_INTV_STATION'                         ,
         fullname      = 'PLOT_INTV_STATION'                         ,
         datatype      = Datatype.FLOAT                              ,
         category      = Category.STATIONS                           ,
         is_required   = False                                       ,
         description   = 'None'                                      ,
         mask          = Mask.POSITIVE_DEFINITE                      ,
         values        = None                                        ,
         default_value = '1'                                         ,
         dependencies  = [('NumberStations', Mask.POSITIVE_DEFINITE)]
      )
      self._StationOutputBuffer = Parameter(
         name          = 'StationOutputBuffer'                       ,
         fullname      = 'StationOutputBuffer'                       ,
         datatype      = Datatype.INTEGER                            ,
         category      = Category.STATIONS                           ,
         is_required   = False                                       ,
         description   = 'None'                                      ,
         mask          = Mask.POSITIVE_DEFINITE                      ,
         values        = None                                        ,
         default_value = '1000'                                      ,
         dependencies  = [('NumberStations', Mask.POSITIVE_DEFINITE)]
      )
      self._STATIONS_FILE = Parameter(
         name          = 'STATIONS_FILE'                             ,
         fullname      = 'STATIONS_FILE'                             ,
         datatype      = Datatype.PATH                               ,
         category      = Category.STATIONS                           ,
         is_required   = True                                        ,
         description   = 'None'                                      ,
         mask          = Mask.NONE                                   ,
         values        = None                                        ,
         default_value = None                                        ,
         dependencies  = [('NumberStations', Mask.POSITIVE_DEFINITE)]
      )
      self._SWE_ETA_DEP = Parameter(
         name          = 'SWE_ETA_DEP'                    ,
         fullname      = 'SWE_ETA_DEP'                    ,
         datatype      = Datatype.FLOAT                   ,
         category      = Category.ERR                     ,
         is_required   = False                            ,
         description   = 'None'                           ,
         mask          = Mask.NONE                        ,
         values        = None                             ,
         default_value = '0.8'                            ,
         dependencies  = [('VISCOSITY_BREAKING', 'False')]
      )
      self._Cbrk1 = Parameter(
         name          = 'Cbrk1'                    ,
         fullname      = 'Cbrk1'                    ,
         datatype      = Datatype.FLOAT             ,
         category      = Category.ERR               ,
         is_required   = False                      ,
         description   = 'None'                     ,
         mask          = Mask.NONE                  ,
         values        = None                       ,
         default_value = '0.45'                     ,
         dependencies  = [('SHOW_BREAKING', 'True')]
      )
      self._Cbrk2 = Parameter(
         name          = 'Cbrk2'                    ,
         fullname      = 'Cbrk2'                    ,
         datatype      = Datatype.FLOAT             ,
         category      = Category.ERR               ,
         is_required   = False                      ,
         description   = 'None'                     ,
         mask          = Mask.NONE                  ,
         values        = None                       ,
         default_value = '0.35'                     ,
         dependencies  = [('SHOW_BREAKING', 'True')]
      )
      self._visbrk = Parameter(
         name          = 'visbrk'                   ,
         fullname      = 'visbrk'                   ,
         datatype      = Datatype.FLOAT             ,
         category      = Category.ERR               ,
         is_required   = True                       ,
         description   = 'None'                     ,
         mask          = Mask.NONE                  ,
         values        = None                       ,
         default_value = None                       ,
         dependencies  = [('WAVEMAKER_VIS', 'True')]
      )
      self._WAVEMAKER_visbrk = Parameter(
         name          = 'WAVEMAKER_visbrk'         ,
         fullname      = 'WAVEMAKER_visbrk'         ,
         datatype      = Datatype.FLOAT             ,
         category      = Category.ERR               ,
         is_required   = True                       ,
         description   = 'None'                     ,
         mask          = Mask.NONE                  ,
         values        = None                       ,
         default_value = None                       ,
         dependencies  = [('WAVEMAKER_VIS', 'True')]
      )
      self._DX_FILE = Parameter(
         name          = 'DX_FILE'                                           ,
         fullname      = 'DX FILE'                                           ,
         datatype      = Datatype.PATH                                       ,
         category      = Category.GRID                                       ,
         is_required   = True                                                ,
         description   = 'Path to text file of spacing between x grid points',
         mask          = Mask.NONE                                           ,
         values        = None                                                ,
         default_value = None                                                ,
         dependencies  = [('StretchGrid', 'True')]                           
      )
      self._DY_FILE = Parameter(
         name          = 'DY_FILE'                                           ,
         fullname      = 'DY_FILE'                                           ,
         datatype      = Datatype.PATH                                       ,
         category      = Category.GRID                                       ,
         is_required   = True                                                ,
         description   = 'Path to text file of spacing between y grid points',
         mask          = Mask.NONE                                           ,
         values        = None                                                ,
         default_value = None                                                ,
         dependencies  = [('StretchGrid', 'True')]                           
      )
      self._CORIOLIS_FILE = Parameter(
         name          = 'CORIOLIS_FILE'                                               ,
         fullname      = 'CORIOLIS_FILE'                                               ,
         datatype      = Datatype.PATH                                                 ,
         category      = Category.GRID                                                 ,
         is_required   = True                                                          ,
         description   = 'Path to text file of Coriolis parameters at each grid point.',
         mask          = Mask.NONE                                                     ,
         values        = None                                                          ,
         default_value = None                                                          ,
         dependencies  = [('StretchGrid', 'False')]                                    
      )
      self._Lon_West = Parameter(
         name          = 'Lon_West'                              ,
         fullname      = 'Lon_West'                              ,
         datatype      = Datatype.FLOAT                          ,
         category      = Category.GRID                           ,
         is_required   = True                                    ,
         description   = 'Longitude of west boundary in degrees ',
         mask          = Mask.RANGE                              ,
         values        = [-180, 180]                             ,
         default_value = None                                    ,
         dependencies  = [('StretchGrid', 'True')]               
      )
      self._Lat_South = Parameter(
         name          = 'Lat_South'                             ,
         fullname      = 'Lat_South'                             ,
         datatype      = Datatype.FLOAT                          ,
         category      = Category.GRID                           ,
         is_required   = True                                    ,
         description   = 'Latitude of south boundary in degrees.',
         mask          = Mask.RANGE                              ,
         values        = [-180, 180]                             ,
         default_value = None                                    ,
         dependencies  = [('StretchGrid', 'True')]               
      )
      self._Dphi = Parameter(
         name          = 'Dphi'                                                  ,
         fullname      = 'Dphi'                                                  ,
         datatype      = Datatype.FLOAT                                          ,
         category      = Category.GRID                                           ,
         is_required   = True                                                    ,
         description   = 'Spatial resolution in degree in the logitude direction',
         mask          = Mask.POSITIVE_DEFINITE                                  ,
         values        = None                                                    ,
         default_value = None                                                    ,
         dependencies  = [('StretchGrid', 'True')]                               
      )
      self._Dtheta = Parameter(
         name          = 'Dtheta'                                                ,
         fullname      = 'Dtheta'                                                ,
         datatype      = Datatype.FLOAT                                          ,
         category      = Category.GRID                                           ,
         is_required   = True                                                    ,
         description   = 'Spatial resolution in degree in the latitude direction',
         mask          = Mask.POSITIVE_DEFINITE                                  ,
         values        = None                                                    ,
         default_value = None                                                    ,
         dependencies  = [('StretchGrid', 'True')]                               
      )
      self._WaveCompFile = Parameter(
         name          = 'WaveCompFile'                                                                        ,
         fullname      = 'WaveCompFile'                                                                        ,
         datatype      = Datatype.PATH                                                                         ,
         category      = Category.WAVE_MAKER                                                                   ,
         is_required   = True                                                                                  ,
         description   = 'None'                                                                                ,
         mask          = Mask.NONE                                                                             ,
         values        = None                                                                                  ,
         default_value = None                                                                                  ,
         dependencies  = [('WAVEMAKER', ['WK_TIME', 'WK_NEW_DATA2D', 'WK_DATA2D']), ('WAVE_DATA_TYPE', 'DATA')]
      )
      self._FreqPeak = Parameter(
         name          = 'FreqPeak'                                                                                                                           ,
         fullname      = 'FreqPeak'                                                                                                                           ,
         datatype      = Datatype.FLOAT                                                                                                                       ,
         category      = Category.WAVE_MAKER                                                                                                                  ,
         is_required   = True                                                                                                                                 ,
         description   = 'None'                                                                                                                               ,
         mask          = Mask.POSITIVE_DEFINITE                                                                                                               ,
         values        = None                                                                                                                                 ,
         default_value = None                                                                                                                                 ,
         dependencies  = [('WAVEMAKER', ['WK_IRR', 'TMA_1D', 'JON_1D', 'JON_2D', 'WK_NEW_IRR']), ('WAVE_DATA_TYPE', ['WK_IRR', 'TMA_1D', 'JON_1D', 'JON_2D'])]
      )
      self._FreqMin = Parameter(
         name          = 'FreqMin'                                                                                                                            ,
         fullname      = 'FreqMin'                                                                                                                            ,
         datatype      = Datatype.FLOAT                                                                                                                       ,
         category      = Category.WAVE_MAKER                                                                                                                  ,
         is_required   = True                                                                                                                                 ,
         description   = 'None'                                                                                                                               ,
         mask          = Mask.POSITIVE_DEFINITE                                                                                                               ,
         values        = None                                                                                                                                 ,
         default_value = None                                                                                                                                 ,
         dependencies  = [('WAVEMAKER', ['WK_IRR', 'TMA_1D', 'JON_1D', 'JON_2D', 'WK_NEW_IRR']), ('WAVE_DATA_TYPE', ['WK_IRR', 'TMA_1D', 'JON_1D', 'JON_2D'])]
      )
      self._FreqMax = Parameter(
         name          = 'FreqMax'                                                                                                                            ,
         fullname      = 'FreqMax'                                                                                                                            ,
         datatype      = Datatype.FLOAT                                                                                                                       ,
         category      = Category.WAVE_MAKER                                                                                                                  ,
         is_required   = True                                                                                                                                 ,
         description   = 'None'                                                                                                                               ,
         mask          = Mask.POSITIVE_DEFINITE                                                                                                               ,
         values        = None                                                                                                                                 ,
         default_value = None                                                                                                                                 ,
         dependencies  = [('WAVEMAKER', ['WK_IRR', 'TMA_1D', 'JON_1D', 'JON_2D', 'WK_NEW_IRR']), ('WAVE_DATA_TYPE', ['WK_IRR', 'TMA_1D', 'JON_1D', 'JON_2D'])]
      )
      self._Hmo = Parameter(
         name          = 'Hmo'                                                                                                                                ,
         fullname      = 'Hmo'                                                                                                                                ,
         datatype      = Datatype.FLOAT                                                                                                                       ,
         category      = Category.WAVE_MAKER                                                                                                                  ,
         is_required   = True                                                                                                                                 ,
         description   = 'None'                                                                                                                               ,
         mask          = Mask.POSITIVE_DEFINITE                                                                                                               ,
         values        = None                                                                                                                                 ,
         default_value = None                                                                                                                                 ,
         dependencies  = [('WAVEMAKER', ['WK_IRR', 'TMA_1D', 'JON_1D', 'JON_2D', 'WK_NEW_IRR']), ('WAVE_DATA_TYPE', ['WK_IRR', 'TMA_1D', 'JON_1D', 'JON_2D'])]
      )
      self._Nfreq = Parameter(
         name          = 'Nfreq'                                                                                                                              ,
         fullname      = 'Nfreq'                                                                                                                              ,
         datatype      = Datatype.INTEGER                                                                                                                     ,
         category      = Category.WAVE_MAKER                                                                                                                  ,
         is_required   = False                                                                                                                                ,
         description   = 'None'                                                                                                                               ,
         mask          = Mask.POSITIVE_DEFINITE                                                                                                               ,
         values        = None                                                                                                                                 ,
         default_value = '45'                                                                                                                                 ,
         dependencies  = [('WAVEMAKER', ['WK_IRR', 'TMA_1D', 'JON_1D', 'JON_2D', 'WK_NEW_IRR']), ('WAVE_DATA_TYPE', ['WK_IRR', 'TMA_1D', 'JON_1D', 'JON_2D'])]
      )
      self._Ntheta = Parameter(
         name          = 'Ntheta'                                                                                     ,
         fullname      = 'Ntheta'                                                                                     ,
         datatype      = Datatype.INTEGER                                                                             ,
         category      = Category.WAVE_MAKER                                                                          ,
         is_required   = False                                                                                        ,
         description   = 'None'                                                                                       ,
         mask          = Mask.POSITIVE_DEFINITE                                                                       ,
         values        = None                                                                                         ,
         default_value = '24'                                                                                         ,
         dependencies  = [('WAVEMAKER', ['WK_IRR', 'JON_2D', 'WK_NEW_IRR']), ('WAVE_DATA_TYPE', ['WK_IRR', 'JON_2D'])]
      )
      self._ThetaPeak = Parameter(
         name          = 'ThetaPeak'                                                                                  ,
         fullname      = 'ThetaPeak'                                                                                  ,
         datatype      = Datatype.FLOAT                                                                               ,
         category      = Category.WAVE_MAKER                                                                          ,
         is_required   = False                                                                                        ,
         description   = 'None'                                                                                       ,
         mask          = Mask.NONE                                                                                    ,
         values        = None                                                                                         ,
         default_value = '0'                                                                                          ,
         dependencies  = [('WAVEMAKER', ['WK_IRR', 'JON_2D', 'WK_NEW_IRR']), ('WAVE_DATA_TYPE', ['WK_IRR', 'JON_2D'])]
      )
      self._Sigma_Theta = Parameter(
         name          = 'Sigma_Theta'                                                                                ,
         fullname      = 'Sigma_Theta'                                                                                ,
         datatype      = Datatype.FLOAT                                                                               ,
         category      = Category.WAVE_MAKER                                                                          ,
         is_required   = False                                                                                        ,
         description   = 'None'                                                                                       ,
         mask          = Mask.POSITIVE_DEFINITE                                                                       ,
         values        = None                                                                                         ,
         default_value = '10'                                                                                         ,
         dependencies  = [('WAVEMAKER', ['WK_IRR', 'JON_2D', 'WK_NEW_IRR']), ('WAVE_DATA_TYPE', ['WK_IRR', 'JON_2D'])]
      )
      self._WidthWaveMaker = Parameter(
         name          = 'WidthWaveMaker'           ,
         fullname      = 'WidthWaveMaker'           ,
         datatype      = Datatype.FLOAT             ,
         category      = Category.WAVE_MAKER        ,
         is_required   = True                       ,
         description   = 'None'                     ,
         mask          = Mask.POSITIVE_DEFINITE     ,
         values        = None                       ,
         default_value = None                       ,
         dependencies  = [('WAVE_DATA_TYPE', 'ABS')]
      )
      self._R_sponge_wavemaker = Parameter(
         name          = 'R_sponge_wavemaker'       ,
         fullname      = 'R_sponge_wavemaker'       ,
         datatype      = Datatype.FLOAT             ,
         category      = Category.WAVE_MAKER        ,
         is_required   = True                       ,
         description   = 'None'                     ,
         mask          = Mask.POSITIVE_DEFINITE     ,
         values        = None                       ,
         default_value = None                       ,
         dependencies  = [('WAVE_DATA_TYPE', 'ABS')]
      )
      self._A_sponge_wavemaker = Parameter(
         name          = 'A_sponge_wavemaker'       ,
         fullname      = 'A_sponge_wavemaker'       ,
         datatype      = Datatype.FLOAT             ,
         category      = Category.WAVE_MAKER        ,
         is_required   = True                       ,
         description   = 'None'                     ,
         mask          = Mask.POSITIVE_DEFINITE     ,
         values        = None                       ,
         default_value = None                       ,
         dependencies  = [('WAVE_DATA_TYPE', 'ABS')]
      )
      self._CrestLimit = Parameter(
         name          = 'CrestLimit'             ,
         fullname      = 'CrestLimit'             ,
         datatype      = Datatype.FLOAT           ,
         category      = Category.WAVE_MAKER      ,
         is_required   = True                     ,
         description   = 'None'                   ,
         mask          = Mask.POSITIVE_DEFINITE   ,
         values        = None                     ,
         default_value = None                     ,
         dependencies  = [('ETA_LIMITER', 'True')]
      )
      self._TroughLimit = Parameter(
         name          = 'TroughLimit'            ,
         fullname      = 'TroughLimit'            ,
         datatype      = Datatype.FLOAT           ,
         category      = Category.WAVE_MAKER      ,
         is_required   = True                     ,
         description   = 'None'                   ,
         mask          = Mask.POSITIVE_DEFINITE   ,
         values        = None                     ,
         default_value = None                     ,
         dependencies  = [('ETA_LIMITER', 'True')]
      )

   @property
   def ZALPHA(self):
      """None"""
      return self._ZALPHA.value

   @ZALPHA.setter
   def ZALPHA(self, val):
      self._ZALPHA.value = val

   @property
   def PARALLEL(self):
      """FORTRAN compile flag for turning on parallel computations."""
      return self._PARALLEL.value

   @PARALLEL.setter
   def PARALLEL(self, val):
      self._PARALLEL.value = val

   @property
   def nGlob(self):
      """Number of points in x direction"""
      return self._nGlob.value

   @nGlob.setter
   def nGlob(self, val):
      self._nGlob.value = val

   @property
   def mGlob(self):
      """Number of points in y direction"""
      return self._mGlob.value

   @mGlob.setter
   def mGlob(self, val):
      self._mGlob.value = val

   @property
   def CARTESIAN(self):
      """FORTRAN compile flag for switch between cartesian coordinates and spherical coordinates"""
      return self._CARTESIAN.value

   @CARTESIAN.setter
   def CARTESIAN(self, val):
      self._CARTESIAN.value = val

   @property
   def DEPTH_TYPE(self):
      """Bathymetry/Depth type to use."""
      return self._DEPTH_TYPE.value

   @DEPTH_TYPE.setter
   def DEPTH_TYPE(self, val):
      self._DEPTH_TYPE.value = val

   @property
   def BATHY_CORRECTION(self):
      """Flag to using built in interative local smoothing scheme to bathymetry data"""
      return self._BATHY_CORRECTION.value

   @BATHY_CORRECTION.setter
   def BATHY_CORRECTION(self, val):
      self._BATHY_CORRECTION.value = val

   @property
   def WaterLevel(self):
      """Additional water level to add/substract from still water level in bathymetry data"""
      return self._WaterLevel.value

   @WaterLevel.setter
   def WaterLevel(self, val):
      self._WaterLevel.value = val

   @property
   def TOTAL_TIME(self):
      """Total simulation time for run"""
      return self._TOTAL_TIME.value

   @TOTAL_TIME.setter
   def TOTAL_TIME(self, val):
      self._TOTAL_TIME.value = val

   @property
   def PLOT_START_TIME(self):
      """Optional offset for initial start time of run"""
      return self._PLOT_START_TIME.value

   @PLOT_START_TIME.setter
   def PLOT_START_TIME(self, val):
      self._PLOT_START_TIME.value = val

   @property
   def PLOT_INTV(self):
      """Time interval between wrtiting 2D field data to file"""
      return self._PLOT_INTV.value

   @PLOT_INTV.setter
   def PLOT_INTV(self, val):
      self._PLOT_INTV.value = val

   @property
   def SCREEN_INTV(self):
      """Time interval between summary updates in log file output"""
      return self._SCREEN_INTV.value

   @SCREEN_INTV.setter
   def SCREEN_INTV(self, val):
      self._SCREEN_INTV.value = val

   @property
   def INI_UVZ(self):
      """Flag for using hot start mode. Allows specifiying initial free surface height (eta) and velocities (u, v) for run"""
      return self._INI_UVZ.value

   @INI_UVZ.setter
   def INI_UVZ(self, val):
      self._INI_UVZ.value = val

   @property
   def WAVEMAKER(self):
      """Wave maker type to use in simulation"""
      return self._WAVEMAKER.value

   @WAVEMAKER.setter
   def WAVEMAKER(self, val):
      self._WAVEMAKER.value = val

   @property
   def DIRECT_SPONGE(self):
      """None"""
      return self._DIRECT_SPONGE.value

   @DIRECT_SPONGE.setter
   def DIRECT_SPONGE(self, val):
      self._DIRECT_SPONGE.value = val

   @property
   def DIFFUSION_SPONGE(self):
      """None"""
      return self._DIFFUSION_SPONGE.value

   @DIFFUSION_SPONGE.setter
   def DIFFUSION_SPONGE(self, val):
      self._DIFFUSION_SPONGE.value = val

   @property
   def FRICTION_SPONGE(self):
      """None"""
      return self._FRICTION_SPONGE.value

   @FRICTION_SPONGE.setter
   def FRICTION_SPONGE(self, val):
      self._FRICTION_SPONGE.value = val

   @property
   def OBSTACLE_FILE(self):
      """None"""
      return self._OBSTACLE_FILE.value

   @OBSTACLE_FILE.setter
   def OBSTACLE_FILE(self, val):
      self._OBSTACLE_FILE.value = val

   @property
   def BREAKWATER_FILE(self):
      """None"""
      return self._BREAKWATER_FILE.value

   @BREAKWATER_FILE.setter
   def BREAKWATER_FILE(self, val):
      self._BREAKWATER_FILE.value = val

   @property
   def DISPERSION(self):
      """None"""
      return self._DISPERSION.value

   @DISPERSION.setter
   def DISPERSION(self, val):
      self._DISPERSION.value = val

   @property
   def Gamma1(self):
      """None"""
      return self._Gamma1.value

   @Gamma1.setter
   def Gamma1(self, val):
      self._Gamma1.value = val

   @property
   def FRICTION_MATRIX(self):
      """None"""
      return self._FRICTION_MATRIX.value

   @FRICTION_MATRIX.setter
   def FRICTION_MATRIX(self, val):
      self._FRICTION_MATRIX.value = val

   @property
   def Time_Scheme(self):
      """None"""
      return self._Time_Scheme.value

   @Time_Scheme.setter
   def Time_Scheme(self, val):
      self._Time_Scheme.value = val

   @property
   def CONSTRUCTION(self):
      """None"""
      return self._CONSTRUCTION.value

   @CONSTRUCTION.setter
   def CONSTRUCTION(self, val):
      self._CONSTRUCTION.value = val

   @property
   def HIGH_ORDER(self):
      """None"""
      return self._HIGH_ORDER.value

   @HIGH_ORDER.setter
   def HIGH_ORDER(self, val):
      self._HIGH_ORDER.value = val

   @property
   def CFL(self):
      """None"""
      return self._CFL.value

   @CFL.setter
   def CFL(self, val):
      self._CFL.value = val

   @property
   def FIXED_DT(self):
      """None"""
      return self._FIXED_DT.value

   @FIXED_DT.setter
   def FIXED_DT(self, val):
      self._FIXED_DT.value = val

   @property
   def FroudeCap(self):
      """None"""
      return self._FroudeCap.value

   @FroudeCap.setter
   def FroudeCap(self, val):
      self._FroudeCap.value = val

   @property
   def MinDepth(self):
      """None"""
      return self._MinDepth.value

   @MinDepth.setter
   def MinDepth(self, val):
      self._MinDepth.value = val

   @property
   def MinDepthFrc(self):
      """None"""
      return self._MinDepthFrc.value

   @MinDepthFrc.setter
   def MinDepthFrc(self, val):
      self._MinDepthFrc.value = val

   @property
   def OUT_Time(self):
      """None"""
      return self._OUT_Time.value

   @OUT_Time.setter
   def OUT_Time(self, val):
      self._OUT_Time.value = val

   @property
   def NumberStations(self):
      """None"""
      return self._NumberStations.value

   @NumberStations.setter
   def NumberStations(self, val):
      self._NumberStations.value = val

   @property
   def ROLLER_EFFECT(self):
      """None"""
      return self._ROLLER_EFFECT.value

   @ROLLER_EFFECT.setter
   def ROLLER_EFFECT(self, val):
      self._ROLLER_EFFECT.value = val

   @property
   def VISCOSITY_BREAKING(self):
      """None"""
      return self._VISCOSITY_BREAKING.value

   @VISCOSITY_BREAKING.setter
   def VISCOSITY_BREAKING(self, val):
      self._VISCOSITY_BREAKING.value = val

   @property
   def SHOW_BREAKING(self):
      """None"""
      return self._SHOW_BREAKING.value

   @SHOW_BREAKING.setter
   def SHOW_BREAKING(self, val):
      self._SHOW_BREAKING.value = val

   @property
   def WAVEMAKER_Cbrk(self):
      """None"""
      return self._WAVEMAKER_Cbrk.value

   @WAVEMAKER_Cbrk.setter
   def WAVEMAKER_Cbrk(self, val):
      self._WAVEMAKER_Cbrk.value = val

   @property
   def WAVEMAKER_VIS(self):
      """None"""
      return self._WAVEMAKER_VIS.value

   @WAVEMAKER_VIS.setter
   def WAVEMAKER_VIS(self, val):
      self._WAVEMAKER_VIS.value = val

   @property
   def PX(self):
      """Number for parallel cores/threads to use in x direction"""
      return self._PX.value

   @PX.setter
   def PX(self, val):
      self._PX.value = val

   @property
   def PY(self):
      """Number for parallel cores/threads to use in y direction"""
      return self._PY.value

   @PY.setter
   def PY(self, val):
      self._PY.value = val

   @property
   def DX(self):
      """Spatial resolution in the x direction"""
      return self._DX.value

   @DX.setter
   def DX(self, val):
      self._DX.value = val

   @property
   def DY(self):
      """Spatial resolution in the y direction"""
      return self._DY.value

   @DY.setter
   def DY(self, val):
      self._DY.value = val

   @property
   def StretchGrid(self):
      """Flag for using a grid varying grid point spacing. """
      return self._StretchGrid.value

   @StretchGrid.setter
   def StretchGrid(self, val):
      self._StretchGrid.value = val

   @property
   def DEPTH_FILE(self):
      """Path to text file of still water level depth at each grid point. Note, positive values denote below water level."""
      return self._DEPTH_FILE.value

   @DEPTH_FILE.setter
   def DEPTH_FILE(self, val):
      self._DEPTH_FILE.value = val

   @property
   def DEPTH_FLAT(self):
      """Depth of flat region in bathymetry. Note, positive values denote below water level. """
      return self._DEPTH_FLAT.value

   @DEPTH_FLAT.setter
   def DEPTH_FLAT(self, val):
      self._DEPTH_FLAT.value = val

   @property
   def SLP(self):
      """Slope of beach"""
      return self._SLP.value

   @SLP.setter
   def SLP(self, val):
      self._SLP.value = val

   @property
   def Xslp(self):
      """x location to transition between flat depth and slope region."""
      return self._Xslp.value

   @Xslp.setter
   def Xslp(self, val):
      self._Xslp.value = val

   @property
   def BED_DEFORMATION(self):
      """DEPRECATED?"""
      return self._BED_DEFORMATION.value

   @BED_DEFORMATION.setter
   def BED_DEFORMATION(self, val):
      self._BED_DEFORMATION.value = val

   @property
   def ETA_FILE(self):
      """Path to initial free surface height at grid points  to initialize run with"""
      return self._ETA_FILE.value

   @ETA_FILE.setter
   def ETA_FILE(self, val):
      self._ETA_FILE.value = val

   @property
   def U_FILE(self):
      """Optional path to initial x-direction velocities, u, at grid points  for hot start mode."""
      return self._U_FILE.value

   @U_FILE.setter
   def U_FILE(self, val):
      self._U_FILE.value = val

   @property
   def V_FILE(self):
      """Optional path to initial y-direction velocities, v, at grid points  for hot start mode."""
      return self._V_FILE.value

   @V_FILE.setter
   def V_FILE(self, val):
      self._V_FILE.value = val

   @property
   def MASK_FILE(self):
      """DEPRECATED?"""
      return self._MASK_FILE.value

   @MASK_FILE.setter
   def MASK_FILE(self, val):
      self._MASK_FILE.value = val

   @property
   def HotStartTime(self):
      """Optional offset for initial start time of hot start run"""
      return self._HotStartTime.value

   @HotStartTime.setter
   def HotStartTime(self, val):
      self._HotStartTime.value = val

   @property
   def OutputStartNumber(self):
      """Optional offset number for field data file output numbers in hot start run"""
      return self._OutputStartNumber.value

   @OutputStartNumber.setter
   def OutputStartNumber(self, val):
      self._OutputStartNumber.value = val

   @property
   def AMP(self):
      """None"""
      return self._AMP.value

   @AMP.setter
   def AMP(self, val):
      self._AMP.value = val

   @property
   def DEP(self):
      """None"""
      return self._DEP.value

   @DEP.setter
   def DEP(self, val):
      self._DEP.value = val

   @property
   def LAGTIME(self):
      """None"""
      return self._LAGTIME.value

   @LAGTIME.setter
   def LAGTIME(self, val):
      self._LAGTIME.value = val

   @property
   def NumWaveComp(self):
      """None"""
      return self._NumWaveComp.value

   @NumWaveComp.setter
   def NumWaveComp(self, val):
      self._NumWaveComp.value = val

   @property
   def PeakPeriod(self):
      """None"""
      return self._PeakPeriod.value

   @PeakPeriod.setter
   def PeakPeriod(self, val):
      self._PeakPeriod.value = val

   @property
   def Xc_WK(self):
      """None"""
      return self._Xc_WK.value

   @Xc_WK.setter
   def Xc_WK(self, val):
      self._Xc_WK.value = val

   @property
   def Yc_WK(self):
      """None"""
      return self._Yc_WK.value

   @Yc_WK.setter
   def Yc_WK(self, val):
      self._Yc_WK.value = val

   @property
   def DEP_WK(self):
      """None"""
      return self._DEP_WK.value

   @DEP_WK.setter
   def DEP_WK(self, val):
      self._DEP_WK.value = val

   @property
   def Time_ramp(self):
      """None"""
      return self._Time_ramp.value

   @Time_ramp.setter
   def Time_ramp(self, val):
      self._Time_ramp.value = val

   @property
   def Delta_WK(self):
      """None"""
      return self._Delta_WK.value

   @Delta_WK.setter
   def Delta_WK(self, val):
      self._Delta_WK.value = val

   @property
   def Ywidth_WK(self):
      """None"""
      return self._Ywidth_WK.value

   @Ywidth_WK.setter
   def Ywidth_WK(self, val):
      self._Ywidth_WK.value = val

   @property
   def SolitaryPositiveDirection(self):
      """None"""
      return self._SolitaryPositiveDirection.value

   @SolitaryPositiveDirection.setter
   def SolitaryPositiveDirection(self, val):
      self._SolitaryPositiveDirection.value = val

   @property
   def XWAVEMARKER(self):
      """None"""
      return self._XWAVEMARKER.value

   @XWAVEMARKER.setter
   def XWAVEMARKER(self, val):
      self._XWAVEMARKER.value = val

   @property
   def x1_Nwave(self):
      """None"""
      return self._x1_Nwave.value

   @x1_Nwave.setter
   def x1_Nwave(self, val):
      self._x1_Nwave.value = val

   @property
   def x2_Nwave(self):
      """None"""
      return self._x2_Nwave.value

   @x2_Nwave.setter
   def x2_Nwave(self, val):
      self._x2_Nwave.value = val

   @property
   def a0_Nwave(self):
      """None"""
      return self._a0_Nwave.value

   @a0_Nwave.setter
   def a0_Nwave(self, val):
      self._a0_Nwave.value = val

   @property
   def gamma_Nwave(self):
      """None"""
      return self._gamma_Nwave.value

   @gamma_Nwave.setter
   def gamma_Nwave(self, val):
      self._gamma_Nwave.value = val

   @property
   def dep_Nwave(self):
      """None"""
      return self._dep_Nwave.value

   @dep_Nwave.setter
   def dep_Nwave(self, val):
      self._dep_Nwave.value = val

   @property
   def Xc(self):
      """None"""
      return self._Xc.value

   @Xc.setter
   def Xc(self, val):
      self._Xc.value = val

   @property
   def Yc(self):
      """None"""
      return self._Yc.value

   @Yc.setter
   def Yc(self, val):
      self._Yc.value = val

   @property
   def WID(self):
      """None"""
      return self._WID.value

   @WID.setter
   def WID(self, val):
      self._WID.value = val

   @property
   def Tperiod(self):
      """None"""
      return self._Tperiod.value

   @Tperiod.setter
   def Tperiod(self, val):
      self._Tperiod.value = val

   @property
   def AMP_WK(self):
      """None"""
      return self._AMP_WK.value

   @AMP_WK.setter
   def AMP_WK(self, val):
      self._AMP_WK.value = val

   @property
   def Theta_WK(self):
      """None"""
      return self._Theta_WK.value

   @Theta_WK.setter
   def Theta_WK(self, val):
      self._Theta_WK.value = val

   @property
   def alpha_c(self):
      """None"""
      return self._alpha_c.value

   @alpha_c.setter
   def alpha_c(self, val):
      self._alpha_c.value = val

   @property
   def EqualEnergy(self):
      """None"""
      return self._EqualEnergy.value

   @EqualEnergy.setter
   def EqualEnergy(self, val):
      self._EqualEnergy.value = val

   @property
   def WAVE_DATA_TYPE(self):
      """None"""
      return self._WAVE_DATA_TYPE.value

   @WAVE_DATA_TYPE.setter
   def WAVE_DATA_TYPE(self, val):
      self._WAVE_DATA_TYPE.value = val

   @property
   def DepthWaveMaker(self):
      """None"""
      return self._DepthWaveMaker.value

   @DepthWaveMaker.setter
   def DepthWaveMaker(self, val):
      self._DepthWaveMaker.value = val

   @property
   def ETA_LIMITER(self):
      """None"""
      return self._ETA_LIMITER.value

   @ETA_LIMITER.setter
   def ETA_LIMITER(self, val):
      self._ETA_LIMITER.value = val

   @property
   def WaveMakerCd(self):
      """None"""
      return self._WaveMakerCd.value

   @WaveMakerCd.setter
   def WaveMakerCd(self, val):
      self._WaveMakerCd.value = val

   @property
   def PERODIC(self):
      """None"""
      return self._PERODIC.value

   @PERODIC.setter
   def PERODIC(self, val):
      self._PERODIC.value = val

   @property
   def Csp(self):
      """None"""
      return self._Csp.value

   @Csp.setter
   def Csp(self, val):
      self._Csp.value = val

   @property
   def CDsponge(self):
      """None"""
      return self._CDsponge.value

   @CDsponge.setter
   def CDsponge(self, val):
      self._CDsponge.value = val

   @property
   def Sponge_west_width(self):
      """None"""
      return self._Sponge_west_width.value

   @Sponge_west_width.setter
   def Sponge_west_width(self, val):
      self._Sponge_west_width.value = val

   @property
   def Sponge_east_width(self):
      """None"""
      return self._Sponge_east_width.value

   @Sponge_east_width.setter
   def Sponge_east_width(self, val):
      self._Sponge_east_width.value = val

   @property
   def Sponge_south_width(self):
      """None"""
      return self._Sponge_south_width.value

   @Sponge_south_width.setter
   def Sponge_south_width(self, val):
      self._Sponge_south_width.value = val

   @property
   def Sponge_north_width(self):
      """None"""
      return self._Sponge_north_width.value

   @Sponge_north_width.setter
   def Sponge_north_width(self, val):
      self._Sponge_north_width.value = val

   @property
   def R_sponge(self):
      """None"""
      return self._R_sponge.value

   @R_sponge.setter
   def R_sponge(self, val):
      self._R_sponge.value = val

   @property
   def A_sponge(self):
      """None"""
      return self._A_sponge.value

   @A_sponge.setter
   def A_sponge(self, val):
      self._A_sponge.value = val

   @property
   def BreakWaterAbsorbCoef(self):
      """None"""
      return self._BreakWaterAbsorbCoef.value

   @BreakWaterAbsorbCoef.setter
   def BreakWaterAbsorbCoef(self, val):
      self._BreakWaterAbsorbCoef.value = val

   @property
   def Gamma2(self):
      """None"""
      return self._Gamma2.value

   @Gamma2.setter
   def Gamma2(self, val):
      self._Gamma2.value = val

   @property
   def Beta_ref(self):
      """None"""
      return self._Beta_ref.value

   @Beta_ref.setter
   def Beta_ref(self, val):
      self._Beta_ref.value = val

   @property
   def Gamma3(self):
      """None"""
      return self._Gamma3.value

   @Gamma3.setter
   def Gamma3(self, val):
      self._Gamma3.value = val

   @property
   def FRICTION_FILE(self):
      """None"""
      return self._FRICTION_FILE.value

   @FRICTION_FILE.setter
   def FRICTION_FILE(self, val):
      self._FRICTION_FILE.value = val

   @property
   def Cd(self):
      """None"""
      return self._Cd.value

   @Cd.setter
   def Cd(self, val):
      self._Cd.value = val

   @property
   def ArrTimeMin(self):
      """None"""
      return self._ArrTimeMin.value

   @ArrTimeMin.setter
   def ArrTimeMin(self, val):
      self._ArrTimeMin.value = val

   @property
   def PLOT_INTV_STATION(self):
      """None"""
      return self._PLOT_INTV_STATION.value

   @PLOT_INTV_STATION.setter
   def PLOT_INTV_STATION(self, val):
      self._PLOT_INTV_STATION.value = val

   @property
   def StationOutputBuffer(self):
      """None"""
      return self._StationOutputBuffer.value

   @StationOutputBuffer.setter
   def StationOutputBuffer(self, val):
      self._StationOutputBuffer.value = val

   @property
   def STATIONS_FILE(self):
      """None"""
      return self._STATIONS_FILE.value

   @STATIONS_FILE.setter
   def STATIONS_FILE(self, val):
      self._STATIONS_FILE.value = val

   @property
   def SWE_ETA_DEP(self):
      """None"""
      return self._SWE_ETA_DEP.value

   @SWE_ETA_DEP.setter
   def SWE_ETA_DEP(self, val):
      self._SWE_ETA_DEP.value = val

   @property
   def Cbrk1(self):
      """None"""
      return self._Cbrk1.value

   @Cbrk1.setter
   def Cbrk1(self, val):
      self._Cbrk1.value = val

   @property
   def Cbrk2(self):
      """None"""
      return self._Cbrk2.value

   @Cbrk2.setter
   def Cbrk2(self, val):
      self._Cbrk2.value = val

   @property
   def visbrk(self):
      """None"""
      return self._visbrk.value

   @visbrk.setter
   def visbrk(self, val):
      self._visbrk.value = val

   @property
   def WAVEMAKER_visbrk(self):
      """None"""
      return self._WAVEMAKER_visbrk.value

   @WAVEMAKER_visbrk.setter
   def WAVEMAKER_visbrk(self, val):
      self._WAVEMAKER_visbrk.value = val

   @property
   def DX_FILE(self):
      """Path to text file of spacing between x grid points"""
      return self._DX_FILE.value

   @DX_FILE.setter
   def DX_FILE(self, val):
      self._DX_FILE.value = val

   @property
   def DY_FILE(self):
      """Path to text file of spacing between y grid points"""
      return self._DY_FILE.value

   @DY_FILE.setter
   def DY_FILE(self, val):
      self._DY_FILE.value = val

   @property
   def CORIOLIS_FILE(self):
      """Path to text file of Coriolis parameters at each grid point."""
      return self._CORIOLIS_FILE.value

   @CORIOLIS_FILE.setter
   def CORIOLIS_FILE(self, val):
      self._CORIOLIS_FILE.value = val

   @property
   def Lon_West(self):
      """Longitude of west boundary in degrees """
      return self._Lon_West.value

   @Lon_West.setter
   def Lon_West(self, val):
      self._Lon_West.value = val

   @property
   def Lat_South(self):
      """Latitude of south boundary in degrees."""
      return self._Lat_South.value

   @Lat_South.setter
   def Lat_South(self, val):
      self._Lat_South.value = val

   @property
   def Dphi(self):
      """Spatial resolution in degree in the logitude direction"""
      return self._Dphi.value

   @Dphi.setter
   def Dphi(self, val):
      self._Dphi.value = val

   @property
   def Dtheta(self):
      """Spatial resolution in degree in the latitude direction"""
      return self._Dtheta.value

   @Dtheta.setter
   def Dtheta(self, val):
      self._Dtheta.value = val

   @property
   def WaveCompFile(self):
      """None"""
      return self._WaveCompFile.value

   @WaveCompFile.setter
   def WaveCompFile(self, val):
      self._WaveCompFile.value = val

   @property
   def FreqPeak(self):
      """None"""
      return self._FreqPeak.value

   @FreqPeak.setter
   def FreqPeak(self, val):
      self._FreqPeak.value = val

   @property
   def FreqMin(self):
      """None"""
      return self._FreqMin.value

   @FreqMin.setter
   def FreqMin(self, val):
      self._FreqMin.value = val

   @property
   def FreqMax(self):
      """None"""
      return self._FreqMax.value

   @FreqMax.setter
   def FreqMax(self, val):
      self._FreqMax.value = val

   @property
   def Hmo(self):
      """None"""
      return self._Hmo.value

   @Hmo.setter
   def Hmo(self, val):
      self._Hmo.value = val

   @property
   def Nfreq(self):
      """None"""
      return self._Nfreq.value

   @Nfreq.setter
   def Nfreq(self, val):
      self._Nfreq.value = val

   @property
   def Ntheta(self):
      """None"""
      return self._Ntheta.value

   @Ntheta.setter
   def Ntheta(self, val):
      self._Ntheta.value = val

   @property
   def ThetaPeak(self):
      """None"""
      return self._ThetaPeak.value

   @ThetaPeak.setter
   def ThetaPeak(self, val):
      self._ThetaPeak.value = val

   @property
   def Sigma_Theta(self):
      """None"""
      return self._Sigma_Theta.value

   @Sigma_Theta.setter
   def Sigma_Theta(self, val):
      self._Sigma_Theta.value = val

   @property
   def WidthWaveMaker(self):
      """None"""
      return self._WidthWaveMaker.value

   @WidthWaveMaker.setter
   def WidthWaveMaker(self, val):
      self._WidthWaveMaker.value = val

   @property
   def R_sponge_wavemaker(self):
      """None"""
      return self._R_sponge_wavemaker.value

   @R_sponge_wavemaker.setter
   def R_sponge_wavemaker(self, val):
      self._R_sponge_wavemaker.value = val

   @property
   def A_sponge_wavemaker(self):
      """None"""
      return self._A_sponge_wavemaker.value

   @A_sponge_wavemaker.setter
   def A_sponge_wavemaker(self, val):
      self._A_sponge_wavemaker.value = val

   @property
   def CrestLimit(self):
      """None"""
      return self._CrestLimit.value

   @CrestLimit.setter
   def CrestLimit(self, val):
      self._CrestLimit.value = val

   @property
   def TroughLimit(self):
      """None"""
      return self._TroughLimit.value

   @TroughLimit.setter
   def TroughLimit(self, val):
      self._TroughLimit.value = val
