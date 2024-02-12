
import ast
import os
from enum import Enum
from types import SimpleNamespace

import numpy as np
import pandas as pd


class Type(Enum):
    STRING  = 1,
    PATH    = 2,
    BOOL    = 3,
    INTEGER = 4,
    FLOAT   = 5,
    ENUM    = 6,
    DENUM   = 7,
    LIST    = 8,
    OBJECT  = 9,
    TEXT    = 10,
    KEY     = 11

def __COL(name, column_type, column_width, is_locked, description):
    return SimpleNamespace(name      = name        , 
                           type      = column_type ,
                           width     = column_width,
                           is_locked = is_locked   , 
                           desc      = description )


INPUT_COLUMNS = [('Name'         , Type.KEY   , 100, False, "FUNWAVE FORTRAN variable name."      ),
                 ('Is Deprecated', Type.BOOL  ,  50, False, "Parameter is no longer in FUNWAVE."         ),
                 ('Python Name'  , Type.STRING, 100, True , "Standardized name for Python toolbox."    ),
                 ('Full Name'    , Type.STRING, 200, False, "Full human-readable name of parameter,"    ),
                 ('Datatype'     , Type.ENUM  ,  80, True , "'Datatype' of parameter:."          ),
                 ('Skill Floor'  , Type.ENUM  ,  80, False, "Skill level required to used parameter: "  ),
                 ('Category'     , Type.LIST  , 300, False, "Category/Categories of parameter."          ),
                 ('Units'        , Type.DENUM ,  30, False, "Optional physical units of parameter."      ),
                 ('Is Required'  , Type.BOOL  ,  30, True , "Is parameter required for FUNWAVE exectution." ),
                 ('Default Value', Type.OBJECT,  80, True , "Optional default value of parameter."      ),
                 ('Mask Type'    , Type.ENUM  ,  80, False, ""      ),
                 ('Mask Values'  , Type.OBJECT, 300, False, ""      ),
                 ('Description'  , Type.TEXT  , 500, False, ""      )]

DEPENDENT_COLUMNS = [('Dependent', Type.KEY   , 100, False, ""),
                     ('Parent'   , Type.STRING, 100, False, ""),
                     ('Value'    , Type.OBJECT, 100, False, "")]

FUN_ENUM_COLUMNS = [('Name'       , Type.KEY  , 100, True , 'FUNWAVE Enum value'),
                    ('Parent'     , Type.DENUM , 100, True , 'Parent FUNWAVE input parameter.'),
                    ('Full Name'  , Type.STRING, 100, False, 'Full human-readable name of parameter.'),
                    ('Description', Type.TEXT  , 500, False, 'Description of value.')]  

UNIT_COLUMNS = [('Name'          , Type.KEY   , 100, False, "Name of units."                        ),
                ('Full Name'     , Type.STRING, 100, False, 'Full human-readable name of parameter.'),
                ('Units'         , Type.STRING, 100, False, "SI units."                             ),
                ('Latex Units'   , Type.STRING, 100, False, "LaTeX markup units."                   ),
                ('US Units'      , Type.STRING, 100, False, "US units."                             ),
                ('US Latex Units', Type.STRING, 100, False, "LaTeX markup units."                   ),
                ('Factor'        , Type.FLOAT , 100, False, "Conversion factor from SI to US units."),
                ('Description'   , Type.TEXT  , 500, False, "Description of units."                 )]

CATEGORY_COLUMNS = [('Name'      , Type.KEY , 100, False, "Name of category value."),
                   ('Description', Type.TEXT, 500, False, "Description of category."      )]


MASKTYPE_COLUMNS = [('Name'       , Type.KEY , 100, False, "Name of mask type."),
                    ('Description', Type.TEXT, 500, False, "Description of mask type.")] 

DATATYPE_COLUMNS = [('Name'       , Type.KEY , 100, False, "Name of datatype."),
                    ('Description', Type.TEXT, 500, False, "Description of datatype.")]

SKILLLVL_COLUMNS = [('Name'       , Type.KEY    , 100, True , "Name of skill level."      ),
                    ('Level'      , Type.INTEGER,  30, True , "Numerical level of skill." ),
                    ('Description', Type.TEXT   , 500, False, "Description of skil level.")] 


def __CREATE_DICT(COLUMNS):
    return {c.lower().replace(' ','_'): __COL(c, *x) for c, *x in COLUMNS}

INPUT_COLUMNS     = __CREATE_DICT(INPUT_COLUMNS    )
DEPENDENT_COLUMNS = __CREATE_DICT(DEPENDENT_COLUMNS)
FUN_ENUM_COLUMNS  = __CREATE_DICT(FUN_ENUM_COLUMNS )
UNIT_COLUMNS      = __CREATE_DICT(UNIT_COLUMNS     )
CATEGORY_COLUMNS  = __CREATE_DICT(CATEGORY_COLUMNS )
DATATYPE_COLUMNS  = __CREATE_DICT(DATATYPE_COLUMNS )
SKILLLVL_COLUMNS  = __CREATE_DICT(SKILLLVL_COLUMNS )
MASKTYPE_COLUMNS  = __CREATE_DICT(MASKTYPE_COLUMNS )


#ENUM_VALUES = {'datatype'   : [ 'Flag', 'Float', 'Integer', 'Enum', 'Boolean', 'String', 'Path'],
#               'mask_type'  : [ 'None', 'Positive Definite', 'Positive', 'Range'],
#               'skill_floor': [ 'Beginner', 'Intermediate', 'Advanced', 'Hidden']}

#ENUM_VALUES['skill_floor'] = [(n, "[%d] %s" % (i+1, n)) for i, n in enumerate(ENUM_VALUES['skill_floor'])]

FILTER_COLUMNS = ['datatype', 'skill_floor', 'category', 'is_required', 'is_deprecated']

FFILTER_COLUMNS = ['parent']

class Parameter:

    @property
    def attrs(self): return self._columns

    def __init__(self, **kwargs):

        for k, v in kwargs.items(): setattr(self, k, v)
        self._columns = list(kwargs.keys())




class Parameters:


    def _read_csv(self, fpath):

        df = pd.read_csv(fpath)
        for c in df.columns:
            df.loc[pd.isnull(df[c]), c] = None
        return df

    def __init__(self, dpath=""):

        par_fpath = os.path.join(dpath, 'list.csv')
        par_df = self._read_csv(par_fpath)

        for k, c in INPUT_COLUMNS.items():
            if c.type is Type.LIST:
                par_df[c.name] = par_df[c.name].apply(ast.literal_eval)

        self._par_df = par_df 
 
        dep_fpath = os.path.join(dpath, 'dependencies.csv')
        self._dep_df = self._read_csv(dep_fpath)

        cat_fpath = os.path.join(dpath, 'categories.csv')
        self._cat_df = self._read_csv(cat_fpath)

        units_fpath = os.path.join(dpath, 'units.csv')
        self._units_df = self._read_csv(units_fpath)

        fenums_fpath = os.path.join(dpath, 'funwave_enums.csv')
        self._fenums_df = self._read_csv(fenums_fpath)

        mask_fpath = os.path.join(dpath, 'mask_types.csv')
        self._mask_df = self._read_csv(mask_fpath)

        skill_fpath = os.path.join(dpath, 'skill_lvls.csv')
        self._skill_df = self._read_csv(skill_fpath)

        data_fpath = os.path.join(dpath, 'datatypes.csv')
        self._data_df = self._read_csv(data_fpath)

        df = self._dep_df


        
        #def get_depth(dependent, depth=1):



        parents = np.unique(df['Parent'].values)


        def get_depth(df, name, depth=1):
            idx = df['Dependent'] == name
            df2 = df[idx]
            n = len(df2)
            if n == 0: return depth

            if n > 1: raise Exception()
           
            depth+=1
            name = df2.iloc[0]['Parent']

            return get_depth(df, name, depth)






        np.max([get_depth(df, p) for p in parents])
   

