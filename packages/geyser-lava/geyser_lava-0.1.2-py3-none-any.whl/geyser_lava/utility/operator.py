from inspect import stack
from types import FunctionType
from typing import Text

from geyser import Geyser


def unflatten(*args, name: Text):
    indent = ' ' * 4
    code = compile(
        f'def {name}({", ".join(args)}):\n'
        f'{indent}return locals(),\n',
        filename=stack()[1].frame.f_globals['__file__'],
        mode='exec',
        optimize=2
    ).co_consts[0]
    func = FunctionType(
        code,
        {
            '__name__': stack()[1].frame.f_globals['__name__'],
            'locals': locals,
            'print': print
        },
    )
    Geyser.functor(provides=('obj',), requires=args)(func)
    return func


def flatten(*args, name: Text):
    indent = ' ' * 4
    raw_code_header = 'def {name}({args}):\n{indent}obj = dict()\n'.format(
        indent=indent,
        name=name,
        args=', '.join(map(
            lambda it: it[0] if isinstance(it, tuple) else it,
            args
        ))
    )
    raw_code_copy = '{indent}{fill}\n'.format(
        indent=indent,
        fill=f'\n{indent}'.join(map(
            lambda it: f'obj[\'{it}\'] = {it}',
            filter(
                lambda it: isinstance(it, str),
                args
            )
        ))
    )
    raw_code_flatten = '{indent}{fill}\n'.format(
        indent=indent,
        fill=f'\n{indent}'.join(map(
            lambda it: f'\n{indent}'.join(map(
                lambda it_1: f'obj[\'{it[0]}_{it_1}\'] = {it[0]}[\'{it_1}\']',
                it[1]
            )),
            filter(
                lambda it: isinstance(it, tuple) and len(it) == 2,
                args
            )
        ))
    )
    raw_code_footer = f'{indent}return obj\n'
    raw_code = ''.join((
        raw_code_header,
        raw_code_copy,
        raw_code_flatten,
        raw_code_footer
    ))
    code = compile(
        raw_code,
        filename=stack()[1].frame.f_globals['__file__'],
        mode='exec',
        optimize=2
    ).co_consts[0]
    func = FunctionType(
        code,
        {
            '__name__': stack()[1].frame.f_globals['__name__'],
            'locals': locals,
            'print': print,
            'dict': dict,
            'isinstance': isinstance,
            'breakpoint': breakpoint
        },
    )
    provides = list()
    for arg in args:
        if isinstance(arg, str):
            provides.append(arg)
        elif isinstance(arg, tuple) and len(arg) == 2:
            for arg_inner in arg[1]:
                provides.append(f'{arg[0]}_{arg_inner}')
    requires = [
        it[0] if isinstance(it, tuple) and len(it) == 2 else it for it in args
    ]

    Geyser.functor(requires=requires, provides=set(provides))(func)
    return func
