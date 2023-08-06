#!/usr/bin/env python3
import sys
import os
import re
from datetime import datetime
from os.path import expanduser
import yaml

class PLATFORM:
    AIX = 'aix'
    FREE_BSD = 'freebsd'
    LINUX = 'linux'
    MAC = 'darwin'
    WINDOWS = 'win32'
    WINDOWS_CYGWIN = 'cygwin'
    CURRENT_PLATFORM = None

    @classmethod
    def init_platform(cls) -> None:
        if sys.platform.startswith(PLATFORM.AIX):
            PLATFORM.CURRENT_PLATFORM = PLATFORM.AIX

        elif sys.platform.startswith(PLATFORM.FREE_BSD):
            PLATFORM.CURRENT_PLATFORM = PLATFORM.FREE_BSD

        elif sys.platform.startswith(PLATFORM.LINUX):
            PLATFORM.CURRENT_PLATFORM = PLATFORM.LINUX

        elif sys.platform.startswith(PLATFORM.MAC):
            PLATFORM.CURRENT_PLATFORM = PLATFORM.MAC

        elif sys.platform.startswith(PLATFORM.WINDOWS):
            PLATFORM.CURRENT_PLATFORM = PLATFORM.WINDOWS

        elif sys.platform.startswith(PLATFORM.WINDOWS_CYGWIN):
            PLATFORM.CURRENT_PLATFORM = PLATFORM.WINDOWS_CYGWIN


class TYPE:
    EMPTY_STRING = ''
    EMPTY_DICT = {}
    EMPTY_LIST = []


class InvalidCommandException(Exception):
    pass


class PlatformNotSupportedException(Exception):
    pass

def get_config():
    home = expanduser("~")
    cwd = os.getcwd()

    if os.path.exists(cwd+'/.imk/commands.yaml'):
        return cwd+'/.imk/commands.yaml'
    elif os.path.exists(home+'/.imk/commands.yaml'):
        return home+'/.imk/commands.yaml'
    else:
        print('Please Create Config File Either At Current Dir Or Root Dir')
        sys.exit()

def _format(template: str, values: dict) -> str:
    regexp = r'(\{.+?\})'
    groups = re.findall(regexp, template)

    for g in groups:
        spec = g.replace('{', '').replace('}', '')
        specs = spec.split(':', 1)
        nspec = spec
        if len(specs) > 1:
            vkey = specs[0]
            fmt_specs = specs[1].split(',')
            fmt_specs.sort()
            for fmt_spec in fmt_specs:
                k, v = [x.strip() for x in fmt_spec.split('=')]
                if k.strip() == 'default':
                    if not vkey in values:
                        values[vkey] = v.strip()
                    nspec = spec.replace(fmt_spec, '')
                if k.strip() == 'format':
                    nspec = nspec.replace(fmt_spec, v)
                if k.strip() == 'type':
                    nspec = nspec.replace(fmt_spec, '')
                    v = v.strip()
                    if v == 'int':
                        values[vkey] = int(values[vkey])
                    if v == 'float':
                        values[vkey] = float(values[vkey])
                    if v == 'str':
                        values[vkey] = str(values[vkey])
                    if v.startswith('datetime'):
                        vformat = parse_format(v)
                        values[vkey] = datetime.strptime(values[vkey], vformat)

        nspec = nspec.replace(',', '')
        if not len(nspec.split(':')) > 1:
            nspec = nspec.replace(':', '')
        template = template.replace(spec, nspec)
        # print(template)
    return template.format(**values)


def parse_format(string: str) -> str:
    regexp = r'from\((.+?)\)'
    groups = re.findall(regexp, string)
    return groups[0]


def read_config(config_path) -> dict:
    with open(config_path, "r") as stream:
        try:
            collection = yaml.safe_load(stream)
            return dict(collection)
        except yaml.YAMLError as exc:
            print(exc)
            return TYPE.EMPTY_DICT


def process(commands: dict, args: list) -> str:
    try:
        if not isinstance(commands, str) and commands is not None:
            if '$check' in commands:
                options = commands['$check']
                index = next((i for i, option in enumerate(options) if option.get(
                    "platform", '') == PLATFORM.CURRENT_PLATFORM), None)
                if index is not None:
                    return options[index].get('cmd')
                else:
                    crossplatform_option = list(
                        filter(lambda x: 'platform' not in x, options))
                    if not crossplatform_option:
                        raise PlatformNotSupportedException()
                    else:
                        return crossplatform_option[0].get('cmd')
            else:
                key = args.pop(0)
                return process(commands.get(key), args)
        elif commands and commands is not None:
            return commands
        else:
            raise InvalidCommandException()
    except IndexError:
        print("suggestions:")
        print(USER_COMMAND, "??")
        print(''.join(' - {x}\n'.format(x=x) for x in commands.keys()))
        return TYPE.EMPTY_STRING
    except InvalidCommandException:
        print('Invalid Command')
        return TYPE.EMPTY_STRING
    except PlatformNotSupportedException:
        print('Platform Is Not Supported')
        return TYPE.EMPTY_STRING


def run_command(command: str, options: dict) -> None:
    try:
        os.system(_format(command, options))
    except KeyError as ke:
        print('Option Named {0} is Missing'.format(ke))


def filter_to_categorery(argvs: list) -> dict:
    try:
        output = {
            'commands': [],
            'options': {}
        }
        argv_iter = enumerate(argvs)
        for _, arg in argv_iter:
            if arg.startswith('--'):
                output['options'][arg.replace('--', '')] = next(argv_iter)
            else:
                output['commands'].append(arg)
        return output
    except Exception:
        print('Invalid Command Options')


def main() -> None:
    PLATFORM.init_platform()
    args = list(sys.argv[1:])
    output = filter_to_categorery(args)
    if output:
        raw_config = get_config()
        config = read_config(raw_config)
        _command = process(config, output['commands'])
        if _command:
            run_command(_command, output['options'])

USER_COMMAND = ' '.join(sys.argv[1:])
if __name__ == '__main__':
    main()
