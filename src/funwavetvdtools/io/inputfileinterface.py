import json
from abc import ABC, abstractmethod

from funwavetvdtools.error import FunException
from funwavetvdtools.io.parameter import Category, Parameter
from funwavetvdtools.misc.justifylines import JustifyLines


class InputFileInterface(ABC):

    __slots__ = ('_parameters', '_categories')
 
    @classmethod
    def get_slots(cls, slots):
        slots = tuple( "_%s" % slot for slot in slots)
        return cls.__slots__ + slots

    @abstractmethod
    def __add_parameters__(self):
        pass


    def __init_dependencies__(self):
        
        for _, p in self._parameters.items():
            p._link_dependencies(self._parameters)




    def __init__(self, **values):
        self._parameters = {}
        self._categories = {}

        self.__add_parameters__()

        self.__init_dependencies__()

        if len(values) > 0: self.set_values(**values)


    def set_values(self, **values):
        for param in values: setattr(self, param, values[param])    

    def _add_parameter(self, param):
        
        name = param.name
        if param.name in self._parameters.keys():
            msg = "FATAL: Parameter has already been added!!!"
            raise FunException(msg, AttributeError)

        catgy = param.category
        if not catgy in self._categories.keys():
            self._categories[catgy] = {}

        if name in self._categories[catgy].keys():
            msg = "FATAL: Parameter has already been added to category '%s'!!!" % catgy
            raise FunException(msg, AttributeError)

        self._parameters[name] = param
        self._categories[catgy][name] = param

    def __setattr__(self, name, value):

        if type(value) is Parameter:
            self._add_parameter(value)
        
        super().__setattr__(name, value)

    def at(self, names):
        if type(names) is str: return self._parameters[names]
        return [self._parameters[n] for n in names]
    
    @property
    def parameters(self):
        return self._parameters

    @property
    def categories(self):
        return self._categories

    def filter(self, is_minimal=True, is_grouped=False, modules=None):
        
        def add(mdl, param):      
            lst.append(param if not is_grouped else (mdl, param))

        lst = []

        # Adding central module parameters if marked as minimal (see Parameter.is_minimal),
        # or in full mode, i.e., is_minimal=False 
        for mdl in Category:
            if not mdl in self.categories: continue
            if not mdl.is_essential: continue 

            for name in self.categories[mdl]:
                param = self.categories[mdl][name]
                print(not is_minimal or param.is_minimal)
                if not is_minimal or param.is_minimal: add(mdl, param)
   
        
        if modules is None: modules = [] 
        # Filtering out central modules
        modules = [mdl for mdl in modules if not mdl.is_essential] 

    
        # Adding non-central modules with parameters that have been set 
        for mdl in Category:
            if not mdl in self.categories: continue
            if mdl.is_essential: continue

            for name in self.categories[mdl]:
                param = self.categories[mdl][name]
                if param.is_set: 
                    if not mdl in modules: modules.append(mdl)
                    break    

        # Add all parameters for marked non-central modules
        for mdl in modules:
            for param in self.categories[mdl]: add(mdl, param)


        return lst
            
    def to_list(self, is_minimal=True, is_grouped=False, modules=None):
        return self.filter(is_minimal, is_grouped, modules)

    def to_dict(self, is_minimal=True, is_grouped=False, is_detailed=False, modules=None):

        lst = self.to_list(is_minimal, is_grouped, modules)

        print(lst)
        def get_value(p):
            return p.to_dict() if is_detailed else p.value

        if is_grouped:  

            d = {}
            for mdl, param in lst:
                if not mdl in d: d[mdl] = {}
                d[mdl][param.name] = get_value(param)

            return d  

        else:
            return {p.name: get_value(p) for p in lst}

    @classmethod
    def from_dict(cls, d):

        # Checking if dict is group by Category 
        is_grouped = True
        for k in d: 
            if not k in Category:
                is_grouped = False
                break
        
        # Unwrapping Categories if present 
        if is_grouped:

            tmp_d = {}
            for mdl in d: tmp_d.updates({p: d[mdl][p] for p in d[mdl]})
            d = tmp_d
        
        def get_val(p):
            return p.value if type(p) is dict else p

        d = {p: get_val(p) for p in d} 

        # Initializing class with read parameters     
        return cls(**d) 

    def to_json(self, fpath, is_minimal=True, is_grouped=False, is_detailed=False, modules=None, **json_args):
        """
        Dumps parameter name, value pairs as JSON file"

        :param json_args: Optional arguments for json.dump function, see https://docs.python.org/3/library/json.html#basic-usage.
        """
        with open(fpath, 'w') as fh:
            lst = self.to_dict(is_minimal, is_grouped, is_detailed, modules)
            json.dump(lst, fp=fh, **json_args)


    @classmethod
    def from_json(cls, fpath):
        
        with open(fpath, 'r') as fh:
            return cls.from_dict(json.load(fh))


    def to_input(self, fpath, is_minimal=True, modules=None, with_desc=False, width=40, banner_char='-'):

        # Getting parameters
        is_grouped = True
        lst = self.to_list(is_minimal, is_grouped, modules)
        
        # Filtering out flag parameters
        lst = [(mdl, p) for mdl, p in lst if not p.is_flag]
        
        jlines = JustifyLines(['l', 'l'], seperators=' = ')
        old_mdl, _ = lst[0]
        new_mdl = old_mdl 
        params = []

 
        def write_banner(title=None):

            nonlocal banner_char, width
            banner = ''.join([banner_char]*width)
            if title is None: fh.write(banner + "\n")

            title = title.strip()
            n = width - len(title) - 2

            n2 = n//2
            n1 = n - n2

            fmt_title  = ''.join([banner_char]*n1)
            fmt_title += ' ' + title + ' '
            fmt_title += ''.join([banner_char]*n2)

            fh.write("# " + banner + "\n")
            fh.write("# " + fmt_title + "\n")
            fh.write("# " + banner + "\n")
             
        def flush_category():
            
            nonlocal old_mdl, new_mdl, params, jlines
            write_banner(old_mdl.name)    

            if with_desc: 
                for *_, desc in params:

                    write_banner()
                    raise NotImplementedError()

            for name, value, *_ in params: jlines.append([name, value])

            for line, (_, _, is_comment, _) in zip(jlines.to_formatted_lines(), params):
                if is_comment: line = "# " + line
                fh.write(line + "\n")

            fh.write("\n")

            jlines.clear()
            old_mdl = new_mdl
            params = []

        with open(fpath, 'w') as fh:

            for new_mdl, p in lst:    
                if not old_mdl == new_mdl: flush_category()

                desc = None if not with_desc else p.description
                is_comment = not new_mdl.is_essential and not p.is_set
                params.append((p.name, p.value_to_string(), is_comment, desc))
            
            flush_category()    
                 
    @classmethod
    def from_input(cls, fpath):
        raise NotImplementedError()




 


 
    
