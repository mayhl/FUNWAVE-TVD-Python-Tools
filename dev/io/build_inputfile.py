import ast

import pandas as pd

from funwavetvdtools.misc.justifylines import JustifyLines


def write(line, tabs=0):

    spacing = ''.join(['   ']*tabs)
    fmt_line = '%s%s\n' % (spacing, line)
    fh.write(fmt_line)


_d_map={
    'Flag'   : 'FLAG'   ,    
    'Integer': 'INTEGER',
    'List'   : 'ENUM'   ,
    'Boolean': 'BOOL'   ,
    'Float'  : 'FLOAT'  ,
    'Path'   : 'PATH'    
} 
_c_map={
    'Grid'      : 'GRID'      ,
    'Parallel'  : 'PARALLEL'  ,
    'Bathymetry': 'BATHYMETRY',
    'Time'      : 'TIME'      ,
    'Hot Start' : 'HOT_START' ,
    'Wave Maker': 'WAVE_MAKER',
    'Sponge Boundary Layer': 'ERR', 
    'Obstacle and Breakwater': 'ERR',
    'Physics'   : 'PHYSICS',
    'Numerics'  : 'NUMERICS',
    'Stations'  : 'STATIONS',
    'Wave Breaking'  : 'ERR',
    'Boundary Conditions': 'ERR'
}

_v_map={
    'Datatype.INTEGER': {
        'Positive Definite': 'convert_pos_def_int', 
    },
    'Datatype.ENUM': {

    }
}

def get_validator(row, datatype):


    vals = row['Values']

    if vals is None: return "Mask.NONE"

    if datatype == 'Datatype.ENUM':
        if not type(vals) is list: raise Exception("Enum vals is not a list")
        return "Mask.RANGE"

    if datatype == 'Datatype.INTEGER':

        if type(vals) is list: return "Mask.RANGE"
        if vals == 'Positive Definite': return "Mask.POSITIVE_DEFINITE"
        if vals == 'Positive': return 'Mask.POSITIVE'

    if datatype == 'Datatype.FLOAT':

        if type(vals) is list: return "Mask.RANGE"
        if vals == 'Positive Definite': return "Mask.POSITIVE_DEFINITE"
        if vals == 'Positive': return 'Mask.POSITIVE'

    raise NotImplementedError("No validator defined for %s and vals %s." % (datatype, vals))


def get_dependencies(row):

    deps = row['Requires']

    if deps is None: return 'None'


    nd = len(deps) if type(deps) is list else 1
    

    values = row['Required Value']

    if values == "Positive Definite": values = "Mask.POSITIVE_DEFINITE"
    if type(values) is list:
        nv = len(values) if type(values[0]) is list else 1
    else:
        nv = 1


    nv = len(values) if type(values) is list else 1 

    if not type(values) is list: values = [values]

    if type(deps) is list:
        if not nd == nv:
            print(deps)
            print(values)
            raise Exception("Dependencies lengths do not match - nd: %d | nv: %d" % (nd, nv))
    
    if not type(deps) is list: deps = [deps]

    lst = [('self._%s' % dep, val) for dep, val in zip(deps, values)]   

    def format(val):
        if type(val) is str:
            if "Mask." in val: return '%s' % val
            return "'%s'" % val
        else:
            return "%s" % val

    lst = [("'%s'" % dep, format(val)) for dep, val in zip(deps, values)] 
    
    words = ["(%s, %s)" % (p, v) for p, v in lst]      
    line = "[%s]" % ', '.join(words) 
    return line

def get_default_value(row):

    default_value = row['Default Value']
    
    if default_value is None: return 'None'
    if default_value == 'LARGE': return '999999'
    
    if type(default_value) is str: return "'%s'" % default_value

    return "%s" % default_value


def add_parameter(row):

    c_name = 'Category'
    d_name = 'Datatype'

    name="'%s'" % row['Name']
    fullname="'%s'" % row['Full Name']    
    datatype = "%s.%s" % (d_name, _d_map[row['Datatype']])
    category = "%s.%s" % (c_name, _c_map[row['Category']])
    is_required = "True" if row['Is Required'] == 'Yes' else 'False'

    description = "'%s'" % row['Description']

    validator = get_validator(row, datatype) 

    vals = row['Values']
    values = "%s" % str(row['Values']) if type(vals) is list else 'None'
 

    default_value = get_default_value(row)


    dependencies = get_dependencies(row)

    
    start = "self._%s = Parameter(...)" % row['Name']

    'self._%s' % row['Name']
    s2 = " = Parameter("


    inputs = [name, fullname, datatype, category, is_required, description, validator, values, default_value, dependencies]

    names = ['name', 'fullname', 'datatype', 'category', 'is_required', 'description', 'mask', 'values', 'default_value', 'dependencies']

    tabs = 3

    jlines = JustifyLines(['l']*2, seperators=' = ')

    for inp, name in zip(inputs, names):
        jlines.append([name, inp])

    tabs = 2
    def_lines.append(('self._%s = Parameter(' % row['Name'], tabs))
    tabs = 3


    lines = jlines.to_formatted_lines()
    for i in range(len(lines)-1):  lines[i] += ","
    def_lines.extend([(line, tabs) for line in lines])
 
    tabs = 2
    def_lines.append((')', tabs))

    #for inp in inputs[:-1]:
    #    def_lines.append((inp +",", tabs))

    #inp = inputs[-1]
    #def_lines.append((inp +")", tabs))


#    jl_params.append([
#        s1, s2, name, fullname, datatype, category, is_required, description,
#        validator, values, default_value, dependencies, ")"])

    parameters[(row['Name'])] = row['Description']

def write_getter_setter(name, desc):

    sg_lines.append((""                            , 0))
    sg_lines.append(("@property"                   , 1))
    sg_lines.append(("def %s(self):" % name        , 1))
    sg_lines.append(('"""%s"""' % desc             , 2))
    sg_lines.append(("return self._%s.value" % name, 2))
    sg_lines.append((""                            , 0))
    sg_lines.append(("@%s.setter" % name           , 1))
    sg_lines.append(("def %s(self, val):" % name   , 1))
    sg_lines.append(("self._%s.value = val" % name , 2))


def get_formated_slots(d=6):

    sep = ', '
    jlines = JustifyLines(['l']*d, seperators=sep)
    params = [name for name in parameters]
    for s in range(0, len(params), d):
    
        e = s + d
        p = params[s:e]
        n = len(p)
        if n < d: p.extend(['']*(d-n))
        p = ["'%s'" % i for i in p]
        jlines.append(p) 
        
    lines = jlines.to_formatted_lines()

    for i in range(len(lines)-1): lines[i] += sep
   
    line = lines[-1]
    line, *_ = line.split(sep + "''")
    lines[-1] = line.ljust(len(lines[0])) + "])"
    return lines

def write_header():

    write("from funwavetvdtools.io.inputfileinterface import InputFileInterface")
    write("from funwavetvdtools.io.parameter import Category, Datatype, Mask, Parameter")
#    write("import funwavetvdtools.validation as fv")
#    write("from functools import Partial")
    write("")
    write("class InputFile(InputFileInterface):")
    write("")
    tabs = 1
    write("__slots__ = InputFileInterface.get_slots([", tabs)
 
    tabs = 2

    for line in get_formated_slots(): write(line, tabs)
    [name for name in parameters]
    write("")

    tabs = 1
    write('"""', tabs)
    write('Input File Class', tabs)
    write( 'Auto generated on ', tabs) 
    write('"""', tabs)

    write("def __init__(self, **values):", tabs)
    tabs = 2 
    write("super().__init__(**values)", tabs)
    tabs = 0
    write("", tabs)
    tabs = 1
    write('def __add_parameters__(self):', tabs)

    
if __name__ == "__main__":

    csv_fpath ='input_parameters.csv'
    py_fpath = 'inputfile.py'
    df = pd.read_csv(csv_fpath)

    na = 13

    seps = [', ']*(na-1)
    seps[0] = seps[1] = seps[-1] = ''
    justs = ['l']*na
    justs[1] = 'r'
    jl_params = JustifyLines(justs, seps)



    def_lines = []
    sg_lines = []

    parameters = {}


    # Light preprocessing
    df = df.where(pd.notnull(df), None)
    df = df.replace(['none', 'None'], None)
    df = df.replace(['True', 'TRUE'], 'True')
    df = df.replace(['False', 'FALSE'], 'False')

    # Casting entries containing [ character as literal Python lists
    for i, row in df.iterrows():
    
        for key in row.keys():        
            if row[key] is None: continue
            if not '[' in row[key]: continue

            try: 
                row[key] = ast.literal_eval(row[key])
            except Exception:
                print(row)
                print("Key: %s" % key)
                print("Value: %s" % row[key])
                raise Exception("FAIL CONVERT")

    # Filter parameters by none to most dependinces 
    max_steps = 10
    for step in range(1, max_steps+1):
    
        add_indices = []
        for index, row in df.iterrows():
            
            # Only adding parameters with depedencies that have already be added
            is_add = True
            if not row['Requires'] is None:
            
                if not type(row['Requires']) is list:
                    if not row['Requires'] in parameters.keys(): is_add = False
                else:
                    for val in row['Requires']:
                        if not val in parameters.keys():
                            is_add = False
                            break
                                
            if is_add: add_indices.append(index)
                    
        if len(add_indices) > 0:         
            for i in add_indices: add_parameter(df.iloc[i])    
            df = df.drop(add_indices)
            df = df.reset_index(drop=True)
            
        if len(df) == 0: break
        
    # Saftey check    
    if step == max_steps:
        for index, row in df.iterrows(): print(row)
        raise Exception("Max steps reached, parameter csv not processed correctly.")


    # Constructing parameterlist.py file
    with open(py_fpath, 'w+') as fh:
 
        write_header()

        #for line in jl_params.to_formatted_lines(): write(line, tabs=2)

        for line, tabs in def_lines: write(line, tabs=tabs)
        for name in parameters:
            write_getter_setter(name, parameters[name]) 

        for line, tabs in sg_lines: write(line, tabs)
                    
