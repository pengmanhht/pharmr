import pandas as pd
import re
from pathlib import Path

from pharmpy.deps import sympy
from pharmpy.model import DataInfo, Model
from pharmpy.results import ModelfitResults, Results
from pharmpy.workflows import ModelDatabase, ToolDatabase

TYPE_DICT = {
    DataInfo: 'DataInfo',
    Model: 'Model',
    ModelfitResults: 'ModelfitResults',
    Results: 'Results',
    str: 'str',
    int: 'integer',
    float: 'numeric',
    sympy.Float: 'numeric',
    bool: 'logical',
    list: 'array',
    None: 'NULL',
    pd.DataFrame: 'data.frame',
    pd.Series: 'array',
}

SKIP = [
    sympy.Expr,
    sympy.Symbol,
    Path,
    type(None),
    ModelDatabase,
    ToolDatabase
]


def py_to_r_arg(arg):
    py_to_r_dict = {'None': 'NULL',
                    'True': 'TRUE',
                    'False': 'FALSE',
                    '': '\'\''}

    try:
        return py_to_r_dict[str(arg)]
    except KeyError:
        if isinstance(arg, str):
            return f'\'{arg}\''
        else:
            return arg


def py_to_r_str(arg, example=False):
    args = {'None': 'NULL',
            'True': 'TRUE',
            'False': 'FALSE'}

    types = {r'\bint\b': 'integer',
             'float': 'numeric',
             r'\bbool\b': 'logical',
             r'\blist\b': 'vector',
             r'\bdict\b': 'list',
             'dictionary': 'list',
             'pd.DataFrame': 'data.frame',
             'pd.Series': 'data.frame',
             r'\w+\[Model\]': 'vector of Model',  # FIXME: more general pattern
             r'\w+\[ModelfitResults\]': 'vector of ModelfitResults'}  # FIXME: more general pattern

    latex = {r'\\mathsf': '',
             r'\\cdot': '*',
             r'\\text': '',
             r'\\frac': 'frac',
             r'\\log': 'log',
             r'\\exp': 'exp',
             r'\\min': 'min',
             r'\\max': 'max',
             r'\\epsilon': 'epsilon'}

    py_to_r_dict = {**args, **types, **latex}

    if not example:
        py_to_r_dict = {**py_to_r_dict, **{r'\[([0-9]+)\]_*': r'(\1)'}}

    arg_sub = arg
    for key, value in py_to_r_dict.items():
        arg_sub = re.sub(key, value, arg_sub)

    return arg_sub
