from os.path import dirname, basename, isfile, join
import glob
import importlib

module_list = glob.glob(join(dirname(__file__), "*Method.py"))
MODULES = [basename(f)[:-3] for f in module_list if isfile(f)]
def import_all(mod: str):
    """Imports of a module, similar to `from package import *` but specifically for this package

    Args:
        mod (str): A file name in `FuncNotify` directoory/package
    """    
    module = importlib.import_module(f'.{mod}') 
    print(module)
    globals().update({k: v for (k, v) in module.__dict__.items() if not k.startswith('_')})
    
