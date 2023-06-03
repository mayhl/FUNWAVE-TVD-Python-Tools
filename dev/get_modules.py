



import os

import numpy as np


def get_py_files(base_dpath):

    # Getting .py files ignore __init__.py files
    py_files = []
    for dir_info in os.walk(base_dpath):
        dpath = dir_info[0]
        dir_files = dir_info[2]
    
        for dir_file in dir_files:
            dir_file = dir_file.strip()
            if dir_file[-3:] == '.py':
                if not "__init__.py" in dir_file:
                    py_files.append(os.path.join(dpath,dir_file))

    return py_files


def get_file_packages(py_fpath, debug=False):

    packages = []
    with open(py_fpath, 'r') as fh:
        for line in fh:
            line = line.strip()
            if 'import' == line[:6] or 'from' == line[:5]:
                if debug: print(line)
                package = line.split(' ')[1]
                if debug: print(package)

                if '.' in package: package = package.split('.')[0]
                if debug: print(package)

                package = package.strip()
                if debug: print(package)
                if debug: print('----------')

                packages.append(package)

    return packages

def get_all_packages(py_fpaths, debug=False):

    packages = []

    for py_fpath in py_fpaths: 
        packages.extend(get_file_packages(py_fpath, debug))

    packages = list(np.unique(packages))

    remove_list = [ 'FUNWAVE_plotly_functions', 'funwavetvdtools']

    for package in remove_list:
        if package in packages:
            packages.remove(package)
        else:
            raise Exception('%s no longer exists.' % package)

    return packages



if __name__ == "__main__":

    
    src_dpath = '/Users/rdchlmyl/repos/FUNWAVE-TVD-Python-Tools2'
    debug = True
                
    py_fpaths = get_py_files(src_dpath)


    packages = get_all_packages(py_fpaths, debug)
    print(packages)
