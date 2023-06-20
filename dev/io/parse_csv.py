import ast
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from funwavetvdtools import validation as fv
from funwavetvdtools.io.inputfile import InputFile
from funwavetvdtools.io.parameter import Category, Datatype, Mask
from funwavetvdtools.misc.justifylines import JustifyLines


class FuncMapper():

    """ nested dict mapping output of parsing functions to raw inputs 
    key    - output column name(s), str or list of str, e.g. ko or [ko1, ko2, ...]
             NOTE: It is assumed that the columns names in the raw input exist in 
                   the keys (or in a key that is a list). Keys will not be checked
                   to exist in raw input. 
                   Therefore, keys can be used to create new columns 
    subkeys
        f - function to parse input value, e.g., ki  or [ki1, ki2, ...]
                e.g., ko = f(ki) or ko1, ko2 = cast(ki1, ki2)
        args - additional column names(s) required to parse key column(s)
                e.g. 1 - args = []      : see prev
                e.g. 2 - args = [a]     : ko1, ko2 = f(ki1, ki2, a)
                e.g. 3 - args = [a1, a2]: ko = f(ki, a1, a2)
    """

    def __init__(self):
        self._maps = {}
        self._args = []

    @classmethod
    def get_key(cls, keys):
        return '|'.join(keys) if type(keys) is list else keys

    def key_2_cols(self, key):
        args = key.split('|')
    
        for arg in args:
            if not arg in self._args: 
                raise Exception("Argument '%s' extracted from key '%s' is not in list" % (arg, key))

        return args 


    def append(self, o_args, func, ctype, args=[]):

        if not type(o_args) is list:  o_args = [o_args]
        
        for o_arg in o_args:
            if o_args in self._args: raise Exception("Argument '%s' already in a map." % o_arg)

        key = self.get_key(o_args)
        if key in self._maps: raise Exception("Key '%s' is already in map dict." % key) 

        self._args.extend(o_args)
        self._args.extend(args)
        self._args = sorted(list(np.unique(self._args)))
    
        i_args = o_args.copy()
        i_args.extend(args)
        
        self._maps[key] = {'f': func, 't': ctype, 'i': i_args, 'o': o_args}


    def iterargs(self):
        return iter(self._args)

    def iterkeycols(self):
        return iter([(key, self.key_2_cols(key)) for key in self._maps])

    def _get_subdict(self, args):

        if type(args) is str:
            if args in self._maps: return self._maps[args]

        key = self.get_key(args)
        if not key in self._maps: raise Exception("Key '%s' is not in map dict for args %s." % (key, args))  
        return self._maps[key]

    def get_args(self, key):
        return self._get_subdict(key)['i'] 
        
    def func(self, key):
        return self._get_subdict(key)['f']

    def ctype(self, key):
        return self._get_subdict(key)['t']

    def has_arg(self, arg):
        return arg in self._args

    def iterkeys(self):
        return iter(self._maps)

    def items(self):
        return self._maps.items()


class CSVParser():

    # LARGE value in FUNWAVE
    _LARGE_VALUE = 99999.0
    @classmethod
    def cast_def_val(cls, default_value, datatype):

        default_value = cls.cast_general(default_value)
        if default_value is None: return None

        if datatype in [Datatype.INTEGER, Datatype.FLOAT]:
            if default_value == "LARGE": default_value = cls._LARGE_VALUE 

        return datatype.cast(default_value)

        
    @classmethod
    def cast_dependencies(cls, dependencies, dependencies_values):

        dependencies = cls.cast_general(dependencies)
        if dependencies is None: return None

        dependencies_values = cls.cast_general(dependencies_values)
        t_dep = type(dependencies)


        if t_dep is list: 
            if not len(dependencies) == len(dependencies_values):
                raise Exception("Number of dependecies values do not match number of depedencies")

        else:
            print('eree')
#            if type(dependencies_values) is list: 
            dependencies_values = [dependencies_values]

            dependencies = [dependencies]                

        print(dependencies)
        print(dependencies_values)
        print('=================')
        deps = list(zip(dependencies, dependencies_values))
    
        if not len(deps) == len(dependencies):
            raise Exception("Unknown error, length of tuple list does not match number of depedencies")

        return deps


    @classmethod
    def cast_mask(cls, mask, values, datatype):
    
        mask = cls.cast_general(mask)
        vals = mask
        if mask is None: return Mask.NONE, None
        is_list = type(mask) is list 

        if datatype == Datatype.ENUM:
            if not is_list: raise Exception("Enum vals is not a list. %s" % vals)
            return Mask.RANGE, vals 

        if datatype in [Datatype.INTEGER, Datatype.FLOAT]:
            if is_list                    : return Mask.RANGE            , vals
            if mask == 'Positive Definite': return Mask.POSITIVE_DEFINITE, None
            if mask == 'Positive'         : return Mask.POSITIVE         , None

        if datatype in [Datatype.STRING, Datatype.OUT_FLAG, Datatype.FLAG]:
            if not mask is None: raise Exception('Only Mask.NONE allowed for Datatype.%s.' % mask)
            return Mask.NONE, None

        raise NotImplementedError("No validator defined for %s and vals %s." % (datatype, mask))
        

    @classmethod
    def cast_general(cls, val):


        if val is None: return None
        if CSVParser.is_list(val):
            #val = ast.literal_eval(val) 
            #print(type(val), val)
            #return val
            return list(ast.literal_eval(val))
       
        if not type(val) is str: return val
        lval = val.lower()
        if lval == 'none' : return None
        if lval == 'yes'  : return True
        if lval == 'no'   : return False
        if lval == 'true' : return True
        if lval == 'false': return False
        if lval == 't'    : return True
        if lval == 'n'    : return True

        return val

    @classmethod
    def is_list(cls, val):
        
        v_type = type(val)

        if v_type is list: return True

        # Assume all not strings can not be parse to list
        if not v_type is str: return False

        if not ('[' in val and ']' in val): return False

        return True


    @classmethod
    def get_datatype(cls, name):
        
        _map={
            'Flag'       : Datatype.FLAG    ,
            'Integer'    : Datatype.INTEGER ,
            'List'       : Datatype.ENUM    ,
            'Boolean'    : Datatype.BOOL    ,
            'Float'      : Datatype.FLOAT   ,
            'Path'       : Datatype.PATH    ,
            'String'     : Datatype.STRING  ,
            'Output Flag': Datatype.OUT_FLAG,
            'Enum'       : Datatype.ENUM
        }

        if not name in _map:
            raise Exception("Can not map datatype '%s'." % name)

        return _map[name]

    @classmethod
    def _get_category(cls, name):

        _map = {
            'Main'                   : Category.GENERAL       ,
            'Output'                 : Category.OUTPUT        ,
            'Statistics'             : Category.STATISTICS    ,
            'Grid'                   : Category.GRID          ,
            'Parallel'               : Category.PARALLEL      ,
            'Bathymetry'             : Category.BATHYMETRY    ,
            'Time'                   : Category.TIME          ,
            'Hot Start'              : Category.HOT_START     ,
            'Wave Maker'             : Category.WAVE_MAKER    ,
            'Sponge Layer'           : Category.SPONGE_LAYER  ,
            'Obstacle and Breakwater': Category.OBS_AND_BRKWTR,
            'Physics'                : Category.PHYSICS       ,
            'Numerics'               : Category.NUMERICS      ,
            'Stations'               : Category.STATIONS      ,
            'Wave Breaking'          : Category.BREAKING      ,
            'Periodic'               : Category.PERIODIC      ,
            'Central'                : Category.CENTRAL       , 
            'Spherical'              : Category.SPHERICAL     ,
            'Vessel'                 : Category.VESSEL             ,
            'Deep Draft'             : Category.DEEP_DRAFT         ,
            'Sediment'               : Category.SEDIMENT           ,
            'Boundary Conditions'    : Category.BOUNDARY_CONDITIONS,
            'Morphology'             : Category.MORPHOLOGY 
        }

        if not name in _map:
            raise Exception("Can not map category '%s'." % name)

        return _map[name]


    @classmethod
    def get_category(cls, names):

        if CSVParser.is_list(names): 
            names = ast.literal_eval(names)
            return tuple([CSVParser._get_category(n) for n in names])
        else:
            return CSVParser._get_category(names)
                    


    def __init__(self, fpath):

        df = pd.read_csv(fpath)
        df = CSVParser._parse_data(df)
        df = CSVParser._sort_increasing_depedencies(df)
        self._df = df

    @property 
    def parameters(self):
        return self._df['name'].values


    def iterdict(self):
        return [row.to_dict() for _, row in self._df.iterrows()]

            

    @classmethod
    def _sort_increasing_depedencies(cls, df): 
    
        sort_idxs = []
        def is_deps_defined(deps):

            if deps is None: return True 

            if not deps is None:

                for name in [n for n, _ in deps]:
                        if name not in parameters: return False

            return True

        df_orig = df
        df = df_orig.copy()
        max_steps = 10

        sort_idxs = []
        parameters = []

        for s in range(1, max_steps+1):

            add_indices = []
            for i, row in df.iterrows():
                if is_deps_defined(row['dependencies']):
                    add_indices.append(i)
                    parameters.append(row['name'])

            if len(add_indices) < 1: continue 

            sort_idxs.extend(add_indices)
            df = df.drop(index=add_indices)
            df = df.reset_index(drop=True)
            if len(df) == 0: break

        # Saftey checks    
        if s == max_steps:
            raise Exception("Max steps reached, parameter csv not processed correctly.")

        if not len(df_orig) == len(sort_idxs):
            raise Exception("Length of sort indices does not match length of Dataframe.") 
        # Sorting original Dataframe 
        df = df_orig
        sort = 'Sort'
        df[sort] = None
        for i, si in enumerate(sort_idxs): df.loc[si, sort] = i
        df = df.sort_values(by=sort)
        df = df.drop(columns=sort)
        return df.reset_index(drop=True)

    @classmethod
    def get_cols_func_mapper(cls):

        m = FuncMapper()
        m.append('name'               , str                  , object              )
        m.append('is_deprecated'      , Datatype.BOOL.cast   , bool                )
        m.append('full_name'          , str                  , str                 )
        m.append('fortran_name'       , str                  , str                 )
        m.append('datatype'           , cls.get_datatype     , object              )
        m.append('is_essential'       , Datatype.BOOL.cast   , bool                )
        m.append('category'           , cls.get_category     , object              )
        m.append('units'              , str                  , str                 )
        m.append('is_required'        , Datatype.BOOL.cast   , bool                )
        m.append('default_value'      , cls.cast_def_val     , object, ['datatype'])
        m.append(['mask', 'values']   , cls.cast_mask        , object, ['datatype'])
        m.append('dependencies'       , cls.cast_dependencies, object, ['dependencies_values'])
#        m.append('dependencies_values', cls.cast_general  ,  object              )
        m.append('description'        , str               ,  object              )
            # Deprecated
       # m.append('subcategory'   , str    ,  str )

        return m

    @classmethod
    def _parse_data(cls, raw_df):

        #print(raw_df['Dependencies'].values)
        df = raw_df.copy()

        # Light preprocessing
        df = df.where(pd.notnull(df), None)
        df = df.replace(['none', 'None'], None)
        df = df.replace(['true', 'True', 'TRUE'], True)
        df = df.replace(['false', 'False', 'FALSE'], False)

        # Renaming columns to lower case with spaces replace by '_' 
        cols_rename = {name: name.lower().replace(' ', '_') for name in df.columns}
        df = df.rename(columns=cols_rename)

        fv.check_unique_list(df['name'].values, "df['name']")

        # Checking column map and table columns match
#        cols = df.columns
#        col_map = cls.get_col_dict()
#        for col in cols:
#            if not col in col_map: 
#                raise Exception("Column '%s' is not in map." % col)
#
#            for n in ['cast', 'type', 'args']:
#                if n not in col_map[col]:
#                    raise Exception("Subkey '%s' does not exists in map key '%s'" % (n, col)) 



        cols = df.columns
        col_map = cls.get_cols_func_mapper()

        for col in cols:
            if not col_map.has_arg(col): raise Exception("Column '%s' is not in map." % col)
    
        for arg in col_map.iterargs():
            if not arg in cols: df[arg] = None
 
        for key, o_args in col_map.iterkeycols():
            i_args = col_map.get_args(key)
            
            vals = df[i_args].apply(lambda x: col_map.func(key)(*x), axis=1)

            # HACK: For single o_arg with func return list 
            vals = [vals] if len(o_args) == 1 else list(zip(*vals))
            
            for o_arg, val in zip(o_args, vals): df[o_arg] = val

        del_cols = ['dependencies_values']
        df = df.drop(columns=del_cols)
        

        return df


if __name__ == "__main__":

    csv_fpath ='input_parameters.csv'
    parser = CSVParser(csv_fpath)
    print(parser._df.dtypes)
