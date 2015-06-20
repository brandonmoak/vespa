import os
import importlib
import sys
print sys.argv
module = sys.argv[1]

module = importlib.import_module(module)

directory = os.path.dirname(os.path.realpath(__file__))

cfgname = raw_input("Config Name: ")


for key in module.Config.__dict__:
    if "__" not in key:
        val = module.Config.__dict__[key](raw_input("set val of {0}: ".format(key)))
        module.Config.__dict__[key] = val
        print type(module.Config.__dict__[key]), module.Config.__dict__[key], repr(module.Config.__dict__[key])


directory = directory + '\\{0}'.format(cfgname)
if not os.path.exists(directory):
    os.makedirs(directory)

with open(directory + '\\config.py', 'w') as f:
    f.write("class Config:\n")
    f.write("\n".join("    " + key + " = " + repr(module.Config.__dict__[key]) for key in module.Config.__dict__ if "__" not in key))

with open(directory + '\\__init__.py', 'w') as f:
    f.write('\n')
