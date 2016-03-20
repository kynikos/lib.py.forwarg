# forwarg - Command-line argument parser for Python.
# Copyright (C) 2016 Dario Giovannetti <dev@dariogiovannetti.net>
#
# This file is part of forwarg.
#
# forwarg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# forwarg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with forwarg.  If not, see <http://www.gnu.org/licenses/>.

# TODO: Implement all argparse features
#       https://docs.python.org/3/library/argparse.html
# TODO: Support Python 2

import sys as _m_sys
import re as _m_re
from collections import OrderedDict


class HelpFormatter:
    # TODO
    pass


class ArgumentGroup:
    def __init__(self, parser, title, description):
        self.parser = parser
        self.title = title
        self.description = description
        self.dest_to_argument = OrderedDict()

    def add_argument(self, *nameorflags, action=None, nargs=None, const=None,
                     default=None, type=None, choices=None, required=None,
                     help=None, metavar=None, dest=None, version=None):
        if len(nameorflags) < 1:
            raise InvalidArgumentNameError()

        # TODO: asserting isn't the best way to validate arguments...
        assert isinstance(dest, str) or dest is None

        try:
            argument = OptionalArgument(
                            self.parser, self, nameorflags,
                            action=action, nargs=nargs, const=const,
                            default=default, type=type, choices=choices,
                            required=required, help=help, metavar=metavar,
                            dest=dest, version=version)
        except InvalidArgumentNameError:
            if len(nameorflags) > 1:
                raise MultiplePositionalArgumentNamesError(nameorflags)
            argument = PositionalArgument(
                            self.parser, self, nameorflags,
                            action=action, nargs=nargs, const=const,
                            default=default, type=type, choices=choices,
                            required=required, help=help, metavar=metavar,
                            dest=dest, version=version)

        self.dest_to_argument[argument.dest] = argument
        self.parser.dest_to_argument[argument.dest] = argument


class _Argument:
    NAME_RE = r'[a-zA-Z0-9](?:-?[a-zA-Z0-9])*'

    def __init__(self, parser, group, action, nargs, const, default, type,
                 choices, required, help, metavar, dest, version):
        self.parser = parser
        self.group = group

        # TODO: these arguments still have to be used:
        #       action
        #       nargs
        #       const
        #       default
        #       type
        #       choices
        #       required
        #       help
        #       metavar
        #       version (required when using action='version')
        self.dest = dest

        # TODO: The '-' must changed to a '_' in the associated attribute
        # TODO: Names starting with a digit require the 'dest' parameter
        if dest in self.parser.dest_to_argument:
            raise ExistingArgumentError(dest)

    def _make_dest(self, rawdest):
        # TODO
        return rawdest


class OptionalArgument(_Argument):
    def __init__(self, parser, group, nameorflags, action, nargs, const,
                 default, type, choices, required, help, metavar, dest,
                 version):
        self.longflags = []
        self.shortflags = []

        for flag in nameorflags:
            flagname = flag.lstrip('-')
            if not isinstance(flag, str) or \
                    flag[0] != parser.prefix_char or \
                    not _m_re.match(self.NAME_RE, flagname):
                raise InvalidArgumentNameError(flagname)
            if flag[1] == parser.prefix_char:
                if flagname in parser.longflag_to_optarg:
                    raise ExistingArgumentError(flagname)
                self.longflags.append(flagname)
            else:
                if flagname in parser.shortflag_to_optarg:
                    raise ExistingArgumentError(flagname)
                self.shortflags.append(flagname)

        dest = dest or self._make_dest((self.longflags + self.shortflags)[0])

        super().__init__(parser, group, action=action, nargs=nargs,
                         const=const, default=default, type=type,
                         choices=choices, required=required, help=help,
                         metavar=metavar, dest=dest, version=version)

        # Reference the object only after the whole validation
        for flag in self.longflags:
            self.parser.longflag_to_optarg[flag] = self
        for flag in self.shortflags:
            self.parser.shortflag_to_optarg[flag] = self


class PositionalArgument(_Argument):
    def __init__(self, parser, group, nameorflags, action, nargs, const,
                 default, type, choices, required, help, metavar, dest,
                 version):
        self.name = nameorflags[0]

        if not isinstance(self.name, str) or \
                not _m_re.match(self.NAME_RE, self.name):
            raise InvalidArgumentNameError(self.name)
        if self.name in parser.name_to_posarg:
            raise ExistingArgumentError(self.name)

        dest = dest or self._make_dest(self.name)

        super().__init__(parser, group, action=action, nargs=nargs,
                         const=const, default=default, type=type,
                         choices=choices, required=required, help=help,
                         metavar=metavar, dest=dest, version=version)

        # Reference the object only after the whole validation
        self.parser.name_to_posarg[self.name] = self


class ArgumentParser:
    def __init__(self, prog=None, usage=None, description=None, epilog=None,
                 parents=[], formatter_class=HelpFormatter,
                 prefix_chars='-', fromfile_prefix_chars=None,
                 argument_default=None, conflict_handler='error',
                 add_help=True, allow_abbrev=True):
        # TODO: these arguments still have to be used:
        #       prog
        #       usage
        #       description
        #       epilog
        #       parents
        #       formatter_class
        #       fromfile_prefix_chars
        #       argument_default
        #       conflict_handler
        #       add_help
        #       allow_abbrev
        # TODO: asserting isn't the best way to validate arguments...
        assert isinstance(prefix_chars, str)
        assert len(prefix_chars) == 1

        self.prefix_char = prefix_chars

        self.argument_groups = []
        self.dest_to_argument = OrderedDict()
        self.name_to_posarg = {}
        self.longflag_to_optarg = {}
        self.shortflag_to_optarg = {}

    def add_argument_group(self, title=None, description=None):
        # TODO: asserting isn't the best way to validate arguments...
        assert isinstance(title, str)
        assert isinstance(description, str)

        if title in self.argument_groups:
            raise ExistingArgumentGroupError(title)

        group = ArgumentGroup(self, title, description)
        self.argument_groups.append(group)

        return group

    def parse_args(self, args=None, namespace=None):
        # TODO: namespace should be compatible with argparse's
        knownargs, unknownargs = self.parse_known_args(args, namespace)
        if unknownargs:
            raise UnknownArgumentsError(unknownargs)
        # TODO: return a namespace compatible with argparse's
        return knownargs

    def parse_known_args(self, args=None, namespace=None):
        # TODO: namespace should be compatible with argparse's
        args = args or _m_sys.argv[1:]
        # TODO
        for arg in args:
            # FIXME
            print(arg)

        # TODO: return a namespace compatible with argparse's


class ForwargError(Exception):
    pass


class ExistingArgumentError(ForwargError):
    pass


class ExistingArgumentGroupError(ForwargError):
    pass


class InvalidArgumentNameError(ForwargError):
    pass


class MultiplePositionalArgumentNamesError(ForwargError):
    pass


class UnknownArgumentsError(ForwargError):
    pass
