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

from collections import OrderedDict


class HelpFormatter:
    # TODO
    pass


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

        self.argument_groups = OrderedDict()
        self.nameorflag_to_group = {}

    def add_argument_group(self, title=None, description=None):
        # TODO: asserting isn't the best way to validate arguments...
        assert isinstance(title, str)
        assert isinstance(description, str)

        if title in self.argument_groups:
            raise ExistingArgumentGroupError()

        group = ArgumentGroup(self, title, description)
        self.argument_groups[title] = group

        return group

    def parse_args(self, args=None, namespace=None):
        knownargs, unknownargs = self.parse_known_args(args, namespace)
        if unknownargs:
            raise UnknownArgumentsError()
        return knownargs

    def parse_known_args(self, args=None, namespace=None):
        # TODO
        pass


class ArgumentGroup:
    def __init__(self, parser, title, description):
        self.parser = parser
        self.title = title
        self.description = description
        self.arguments = OrderedDict()

    def add_argument(self, *nameorflags, action=None, nargs=None, const=None,
                     default=None, type=None, choices=None, required=None,
                     # the version keyword is required when using
                     # action='version'
                     help=None, metavar=None, dest=None, version=None):
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
        #       dest
        #       version
        # TODO: asserting isn't the best way to validate arguments...
        for nameorflag in nameorflags:
            assert isinstance(nameorflag, str)

        Jnameorflags = ' '.join(nameorflags)

        for nameorflag in nameorflags:
            if nameorflag in self.parser.nameorflag_to_group:
                raise ExistingArgumentError()
            self.parser.nameorflag_to_group[nameorflag] = [self.title,
                                                           Jnameorflags]

        if nameorflags[0][0] == self.parser.prefix_char:
            argument = OptionalArgument(self.parser, *nameorflags)
        elif len(nameorflags) == 1:
            argument = PositionalArgument(self.parser, nameorflags[0])
        else:
            raise MultiplePositionalArgumentNamesError()

        self.arguments[Jnameorflags] = argument


class _Argument:
    NAME_RE = r'[a-zA-Z0-9][a-zA-Z0-9_-]*'


class OptionalArgument(_Argument):
    def __init__(self, parser, *flags):
        # TODO
        pass


class PositionalArgument(_Argument):
    def __init__(self, parser, name):
        # TODO
        pass


class ForwargError(Exception):
    pass


class ExistingArgumentError(ForwargError):
    pass


class ExistingArgumentGroupError(ForwargError):
    pass


class MultiplePositionalArgumentNamesError(ForwargError):
    pass


class UnknownArgumentsError(ForwargError):
    pass
