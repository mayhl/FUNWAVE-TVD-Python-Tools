import ast
from datetime import datetime, timezone

import numpy as np
import pandas as pd
from parse_csv import CSVParser

from funwavetvdtools.io.parameter import Category, Datatype
from funwavetvdtools.misc.justifylines import JustifyLines


class PythonWriter():

    _tab_str = ''.join([' ']*3)
  
    def __init__(self, fpath):

        self._fpath = fpath
        self._fh = open(fpath, 'w')
        self._n = 0
        self._tab = ''

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name == '_n': self._tab = ''.join([PythonWriter._tab_str]*self._n)

    def __close__(self):
        self._fh.close()

    def newline(self):
        self._write("")
        
    def indent(self):
        self._n += 1

    def unindent(self):
        if self._n == 0: raise Exception("Writer is aleady at zero indents.")
        self._n -= 1

    def reset_indent(self):
        self._n = 0
         
    def _write(self, line):
        self._fh.write( self._tab + line + "\n")
            

    def write(self, line):
        self._write(line)

    def comment(self, line):
        line = "# " + line
        self._write(line)
    

def get_formated_slots(parameters, d=5):
    
    sep = ', '   
    jlines = JustifyLines(['l']*d, seperators=sep)
    params = sorted([name for name in parameters])
    for s in range(0, len(params), d):
    
        e = s + d            
        p = params[s:e]
        n = len(p)           
        if n < d: p.extend(['']*(d-n))
        p = ["'%s'" % i for i in p]
        jlines.append(p) 
    
    lines = jlines.to_formatted_lines()

    lines[-1] = lines[-1].replace(", ''", "   ")
    for i in range(len(lines)-1): lines[i] += sep
    
    line = lines[-1]
    line, *_ = line.split(sep + "''")
    #lines[-1] = line.ljust(len(lines[0])) + "])"
    return lines

def write_header(fh, parameters):

    fh.write("from funwavetvdtools.io.inputfileinterface import InputFileInterface")
    fh.write("from funwavetvdtools.io.parameter import Category, Datatype, Mask, Parameter")
    fh.newline()

    fh.write("class InputFile(InputFileInterface):")
    fh.newline()

    fh.indent()

    dt_stamp = datetime.now(timezone.utc).strftime("%Y/%m/%d %H:%M:%S %Z")
    fh.write("__doc__ = InputFileInterface._get_doc_string('%s')" % dt_stamp)
    fh.newline()

    fh.write("# NOTE: __slots__ appearing before doc string caused issues in Sphinx")
    fh.write("__slots__ = InputFileInterface._get_slots([")

    fh.indent()
    for line in get_formated_slots(parameters): fh.write(line)
    fh.unindent()
    fh.write("])")

    fh.newline()

    fh.write("def __init__(self, **values):")
    fh.indent() 
    fh.write("super().__init__(**values)")
    fh.unindent()
    fh.newline()
    fh.write('def __add_parameters__(self):')
    fh.reset_indent()
    

def write_para_init(fh, pdict):

    def format_val2(val):
        
        return ("'%s'" if type(val) is str else "%s") % val

    def format_val(val):


        tval = type(val)

        print("TEST:", val, tval)
        if tval is list:
            return "[%s]" % ', '.join([format_val(v) for v in val])

        if tval is tuple:
            return "(%s)" % ', '.join([format_val(v) for v in val])

        return ("'%s'" if tval is str else "%s") % val

    fh.write('self._%s = Parameter(' % pdict['name'])
    fh.indent()
    jlines = JustifyLines(['l']*2, seperators=' = ')
    for name, value in pdict.items(): 
        fval = format_val(value)
        print("|%s|" % name, type(name))
        print("|%s|" % fval, type(fval))
        jlines.append([str(name), str(format_val(value))])

    lines = jlines.to_formatted_lines()
    
    for i in range(len(lines)-1): lines[i] += ','
    for line in lines: fh.write(line)
    fh.unindent()
    fh.write(")")


def write_getter_setter(fh, pdict):

    name = pdict['name']
    desc = pdict['description']

    fh.newline()
    fh.write("@property")
    fh.write("def %s(self):" % name)   
    fh.indent()
    fh.write('"""%s"""' % desc)
    fh.write("return self._%s.value" % name)
    fh.unindent()
    fh.newline()
    fh.write("@%s.setter" % name)
    fh.write("def %s(self, val):" % name)
    fh.indent()
    fh.write("self._%s.value = val" % name)
    fh.unindent()


def convert_csv_2_pyclass(csv_fpath, py_fpath):

    parser = CSVParser(csv_fpath)

    fh = PythonWriter(py_fpath)
    write_header(fh, parser.parameters)

    fh.indent()
    fh.indent()
    for pdict in parser.iterdict(): write_para_init(fh, pdict)
    fh.unindent()
    for pdict in parser.iterdict(): write_getter_setter(fh, pdict)
   
    
 
    try:
        #import_str = "from %s import InputFile" % py_fpath.replace('.py','')
        #print(import_str)
        from inputfile import InputFile

        test = InputFile()

    except Exception as e:
        raise e

if __name__ == "__main__":

    csv_fpath ='input_parameters.csv'
    py_fpath = 'inputfile.py'
    convert_csv_2_pyclass(csv_fpath, py_fpath)

