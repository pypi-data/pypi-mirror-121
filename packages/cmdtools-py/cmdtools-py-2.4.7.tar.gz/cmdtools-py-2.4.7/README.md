<div id="headline" align="center">
  <h1>cmdtools</h1>
  <p>A module for parsing and processing commands.</p>
  <a href="https://github.com/HugeBrain16/cmdtools/actions/workflows/python-package.yml">
    <img src="https://github.com/HugeBrain16/cmdtools/actions/workflows/python-package.yml/badge.svg" alt="tests"></img>
  </a>
  <a href="https://pypi.org/project/cmdtools-py">
    <img src="https://img.shields.io/pypi/dw/cmdtools-py" alt="downloads"></img>
    <img src="https://badge.fury.io/py/cmdtools-py.svg" alt="PyPI version"></img>
    <img src="https://img.shields.io/pypi/pyversions/cmdtools-py" alt="Python version"></img>
  </a>
  <a href="https://codecov.io/gh/HugeBrain16/cmdtools">
    <img src="https://codecov.io/gh/HugeBrain16/cmdtools/branch/main/graph/badge.svg?token=mynvRn223H"/>
  </a>
</div> 

## Installation

```
pip install --upgrade cmdtools-py
```
install latest commit from GitHub  
```
pip install git+https://github.com/HugeBrain16/cmdtools.git
```
## Examples

more examples [here](https://github.com/HugeBrain16/cmdtools/tree/main/examples)

### Basic example

```py
import cmdtools


def ping():
    print("pong.")


cmd = cmdtools.Cmd('/ping')
cmd.process_cmd(ping)
```
  
### Command with arguments

```py
import cmdtools


def give(name, item_name, item_amount):
    print(f"You gave {item_amount} {item_name}s to {name}")


# surround argument that contains whitespaces with quotes
# set `convert_args` to `True` to automatically convert numbers argument

# this will raise an exception,
# if the number of arguments provided is less than the number of positional callback parameters.
cmd = cmdtools.Cmd('/give Josh "Golden Apple" 10', convert_args=True)

# check for command instance arguments data type.
# format indicates ['str','str','int'].
# integer or float can also match string format, and character 'c' if the argument only has 1 digit.

# `max_args` set to 3, check the first 3 arguments, the rest will get ignored, 
# otherwise if it set to default,
# it will raise an exception if the number of arguments is not equal to the number of formats
if cmd.match_args('ssi', max_args=3):
    cmd.process_cmd(give)
else:
    print('Correct Usage: /give <name: [str]> <item-name: [str]> <item-amount: [int]>')
```

## Links

PyPI project: https://pypi.org/project/cmdtools-py  
Source code: https://github.com/HugeBrain16/cmdtools  
Issues tracker: https://github.com/HugeBrain16/cmdtools/issues  
Documentation: ...
