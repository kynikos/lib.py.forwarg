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
# TODO: When testing, compare all the results with argparse (they must behave
#       the same); in particular, reproduce all the examples in argparse's
#       doc page
# TODO: Support Python 2

import sys as _m_sys
import re as _m_re
from collections import OrderedDict
# TODO: Maybe for the help page this module could simply rely on argparse in
# general
from argparse import HelpFormatter

REMAINDER = object()
SUPPRESS = object()


class Action:
    def __init__(self, argholder):
        self.argholder = argholder

    def process_flag(self):
        self._process_flag()
        # Increment this only after _process_flag, for consistency with
        # store_value below
        self.argholder.number_of_parsed_flags += 1
        self.argholder.number_of_parsed_values_for_current_flag = 0

    def _process_flag(self, newvalue):
        raise NotImplementedError()

    def store_value(self, newvalue):
        self._store_value(newvalue)
        # Increment this only after _store_value, which could raise the
        # UnwantedValueError exception, thus not storing the value
        self.argholder.number_of_parsed_values_for_all_flags += 1
        self.argholder.number_of_parsed_values_for_current_flag += 1

    def _store_value(self, newvalue):
        # This method is assigned dynamically when instantiating the subclasses
        raise NotImplementedError()


class ActionStore(Action):
    def __init__(self, argholder):
        super().__init__(argholder)
        nargs = self.argholder.nargs
        if nargs in (None, '?'):
            self._store_value = self._override
        elif isinstance(nargs, int):
            self._store_value = self._append_limited
        elif nargs in ('*', '+', REMAINDER):
            self._store_value = self._append_unlimited
        else:
            raise UnrecognizedNargsError(nargs)

    def _override(self, newvalue):
        if self.argholder.number_of_parsed_values_for_current_flag > 0:
            raise UnwantedValueError(newvalue)
        self.argholder.value = newvalue

    def _append_limited(self, newvalue):
        if self.argholder.number_of_parsed_values_for_current_flag >= \
                                                        self.argholder.nargs:
            raise UnwantedValueError(newvalue)
        self._append_unlimited(newvalue)

    def _append_unlimited(self, newvalue):
        if self.argholder.number_of_parsed_values_for_current_flag == 0:
            self.argholder.value = [newvalue]
        else:
            self.argholder.value.append(newvalue)

    def _process_flag(self):
        # TODO: Raise an error if the option has already been specified?
        pass


class ActionAppend(Action):
    def __init__(self, argholder):
        super().__init__(argholder)
        nargs = self.argholder.nargs
        if nargs in (None, '?'):
            self._store_value = self._append_plain
        elif isinstance(nargs, int):
            self._store_value = self._append_nested_limited
        elif nargs in ('*', '+', REMAINDER):
            self._store_value = self._append_nested_unlimited
        else:
            raise UnrecognizedNargsError(nargs)

    def _append_plain(self, newvalue):
        if self.argholder.number_of_parsed_values_for_current_flag > 0:
            raise UnwantedValueError(newvalue)
        if self.argholder.number_of_parsed_flags == 0:
            self.argholder.value = [newvalue]
        else:
            self.argholder.value.append(newvalue)

    def _append_nested_limited(self, newvalue):
        if self.argholder.number_of_parsed_values_for_current_flag >= \
                                                        self.argholder.nargs:
            raise UnwantedValueError(newvalue)
        self._append_nested_unlimited(newvalue)

    def _append_nested_unlimited(self, newvalue):
        if self.argholder.number_of_parsed_flags == 0:
            self.argholder.value = [[newvalue]]
        elif self.argholder.number_of_parsed_values_for_current_flag == 0:
            self.argholder.value.append([newvalue])
        else:
            self.argholder.value[-1].append(newvalue)

    def _process_flag(self):
        pass


class ActionStoreConst(Action):
    def __init__(self, argholder):
        super().__init__(argholder)
        # TODO: Does argparse ignore nargs in this action?
        if self.argholder.nargs is not None:
            raise UnrecognizedNargsError(self.argholder.nargs)

    def _process_flag(self):
        # TODO: Raise an error if the option has already been specified?
        self.argholder.value = self.argholder.const

    def _store_value(self, newvalue):
        raise UnwantedValueError(newvalue)


class ActionStoreTrue(ActionStoreConst):
    def _process_flag(self):
        # TODO: Raise an error if the option has already been specified?
        self.argholder.value = True


class ActionStoreFalse(ActionStoreConst):
    def _process_flag(self):
        # TODO: Raise an error if the option has already been specified?
        self.argholder.value = False


class ActionAppendConst(ActionStoreConst):
    def _process_flag(self):
        try:
            self.argholder.value.append(self.argholder.const)
        except TypeError:
            self.argholder.value = [self.argholder.const]


class ActionCount(ActionStoreConst):
    def _process_flag(self):
        try:
            self.argholder.value += 1
        except TypeError:
            self.argholder.value = 1


class ActionHelp(Action):
    # TODO: Implement
    pass


class ActionVersion(Action):
    # TODO: Implement
    pass


class ArgumentHolderGroup:
    def __init__(self, parser, title, description):
        self.parser = parser
        self.title = title
        self.description = description
        self.dest_to_argholder = OrderedDict()

    def add_argument(self, *nameorflags, action='store', nargs=None,
                     const=None, default=None, type=None, choices=None,
                     required=None, help=None, metavar=None, dest=None,
                     version=None):
        if len(nameorflags) < 1:
            raise InvalidArgumentNameError()

        # TODO: asserting isn't the best way to validate arguments...
        assert isinstance(dest, str) or dest is None

        try:
            argholder = OptionalArgumentHolder(
                            self.parser, self, nameorflags,
                            action=action, nargs=nargs, const=const,
                            default=default, type=type, choices=choices,
                            required=required, help=help, metavar=metavar,
                            dest=dest, version=version)
        except InvalidArgumentNameError:
            if len(nameorflags) > 1:
                raise MultiplePositionalArgumentNamesError(nameorflags)
            argholder = PositionalArgumentHolder(
                            self.parser, self, nameorflags,
                            action=action, nargs=nargs, const=const,
                            default=default, type=type, choices=choices,
                            required=required, help=help, metavar=metavar,
                            dest=dest, version=version)

        self.dest_to_argholder[argholder.dest] = argholder
        self.parser.dest_to_argholder[argholder.dest] = argholder


class _ArgumentHolder:
    ACTIONS = {
            'store': ActionStore,
            'store_const': ActionStoreConst,
            'store_true': ActionStoreTrue,
            'store_false': ActionStoreFalse,
            'append': ActionAppend,
            'append_const': ActionAppendConst,
            'count': ActionCount,
            'help': ActionHelp,
            'version': ActionVersion,
    }

    def __init__(self, parser, group, action, nargs, const, default, type,
                 choices, required, help, metavar, dest, version):
        self.parser = parser
        self.group = group

        # TODO: these arguments still have to be used:
        #       type
        #       choices
        #       required
        #       help
        #       metavar
        #       version (required when using action='version')

        # TODO: nargs is validated by Action.store_value, but if an option
        #       doesn't get a value, the validation is not performed
        self.nargs = nargs
        self.const = const
        self.default = default
        self.dest = dest

        # Instantiating action may require the other attributes to be already
        # set, so do it *after* storing them
        try:
            Action_ = self.ACTIONS[action]
        except KeyError:
            # TODO: asserting isn't the best way to validate arguments...
            assert issubclass(action, Action)
            Action_ = action
        self.action = Action_(self)

        self.number_of_parsed_flags = 0
        self.number_of_parsed_values_for_all_flags = 0
        self.number_of_parsed_values_for_current_flag = 0
        self.parsed_arg_indices = []
        # TODO: argparse treats default values in a much more complicated way,
        # see https://docs.python.org/3/library/argparse.html#default
        self.value = self.default

    @staticmethod
    def _make_dest(parser, rawdest):
        dest = _m_re.sub(r'[^a-zA-Z0-9_]', '_', rawdest)
        if dest[0].isdigit():
            dest = '_' + dest

        # TODO: actually, at least the 'append_const' action requires 'dest'
        #       to be defined by more than an option
        if dest in parser.dest_to_argholder:
            raise ExistingArgumentError(dest)

        return dest

    def store_index(self, index):
        self.parsed_arg_indices.append(index)


class OptionalArgumentHolder(_ArgumentHolder):
    def __init__(self, parser, group, nameorflags, action, nargs, const,
                 default, type, choices, required, help, metavar, dest,
                 version):
        self.longflags = []
        self.shortflags = []

        for flag in nameorflags:
            if not isinstance(flag, str):
                raise InvalidArgumentNameError(flag)
            if _m_re.fullmatch(parser.longopt_arg_re, flag):
                if flag[2:] in parser.longflag_to_optargholder:
                    raise ExistingArgumentError(flag)
                self.longflags.append(flag[2:])
            elif _m_re.fullmatch(parser.shortopt_arg_re, flag):
                if flag[1:] in parser.shortflag_to_optargholder:
                    raise ExistingArgumentError(flag)
                self.shortflags.append(flag[1:])
            else:
                raise InvalidArgumentNameError(flag)

        dest = dest or self._make_dest(parser,
                                       (self.longflags + self.shortflags)[0])
        super().__init__(parser, group, action=action, nargs=nargs,
                         const=const, default=default, type=type,
                         choices=choices, required=required, help=help,
                         metavar=metavar, dest=dest, version=version)

        # Reference the object only after the whole validation
        for flag in self.longflags:
            self.parser.longflag_to_optargholder[flag] = self
        for flag in self.shortflags:
            self.parser.shortflag_to_optargholder[flag] = self


class PositionalArgumentHolder(_ArgumentHolder):
    def __init__(self, parser, group, nameorflags, action, nargs, const,
                 default, type, choices, required, help, metavar, dest,
                 version):
        self.name = nameorflags[0]

        if not isinstance(self.name, str) or \
                not _m_re.fullmatch(parser.pos_arg_re, self.name):
            raise InvalidArgumentNameError(self.name)
        if self.name in parser.name_to_posargholder:
            raise ExistingArgumentError(self.name)

        # TODO: actions other than 'store' don't make sense for positional
        #       arguments, right?
        # TODO: asserting isn't the best way to validate arguments...
        assert action is 'store'
        dest = dest or self._make_dest(parser, self.name)
        super().__init__(parser, group, action=action, nargs=nargs,
                         const=const, default=default, type=type,
                         choices=choices, required=required, help=help,
                         metavar=metavar, dest=dest, version=version)

        # Reference the object only after the whole validation
        self.parser.name_to_posargholder[self.name] = self
        self.parser.posargholders.append(self)


class ArgumentParser:
    # Note that isolated sequences of prefix_chars are not supported
    # e.g. '-', '--', '---'
    # At instantiation, {} is replaced by prefix_chars
    POS_ARG_RE = r'[a-zA-Z0-9](?:[{0}]*[a-zA-Z0-9])*'
    LONGOPT_ARG_RE = r'[{0}]{{2}}([a-zA-Z0-9](?:[{0}]*[a-zA-Z0-9])*)'
    SHORTOPT_ARG_RE = r'[{0}]([a-zA-Z0-9])'
    OPT_SEP = '='

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
        assert isinstance(prefix_chars, str) and len(prefix_chars) > 0

        self.prefix_chars = prefix_chars
        self.pos_arg_re = self.POS_ARG_RE.format(_m_re.escape(
                                                            self.prefix_chars))
        self.longopt_arg_re = self.LONGOPT_ARG_RE.format(_m_re.escape(
                                                            self.prefix_chars))
        self.shortopt_arg_re = self.SHORTOPT_ARG_RE.format(_m_re.escape(
                                                            self.prefix_chars))

        self.argholder_groups = []
        self.dest_to_argholder = OrderedDict()
        self.name_to_posargholder = {}
        self.posargholders = []
        self.longflag_to_optargholder = {}
        self.shortflag_to_optargholder = {}

        self.parsed_args = []

    def add_argument_group(self, title=None, description=None):
        # TODO: asserting isn't the best way to validate arguments...
        assert isinstance(title, str)
        assert isinstance(description, str)

        if title in self.argholder_groups:
            raise ExistingArgumentGroupError(title)

        group = ArgumentHolderGroup(self, title, description)
        self.argholder_groups.append(group)

        return group

    def parse_args(self, args=None, namespace=None):
        # Don't try to define a parse_known_args method, since there are many
        # ambiguous cases anyway, for example in '--unknown-option value' does
        # 'value' belong to '--unknown-option' or is it a positional argument?
        # We don't know if '--unknown-option' accepts any values
        # See also http://bugs.python.org/issue16142

        # TODO: Accept a namespace compatible with argparse's
        # TODO: What should happen if an argument is specified multiple times?
        #       see what argparse does.
        #       If allowed, it could be possible to do something like
        #       '--option1 --option2 --option1=value', and, if --option1
        #       requires a value, an error wouldn't be raised because it would
        #       be assigned by the second instance

        args = args or _m_sys.argv[1:]

        # TODO: The goal is to obtain objects like:
        #   $ syncere posarg1value --option1 value1 value2 --option2=value \
        #   posarg2value1 -abc=value -defvalue posarg2value2 -ghi \
        #   value posarg3value -- --posarg2value3
        #
        #   self.parsed_args = [
        #       'posarg1value',
        #       '--option1',
        #       'value1',
        #       'value2',
        #       --option2=value,
        #       'posarg2value1',
        #       ['-', 'a', 'b', 'q=value'],
        #       ['-', 'r', 's', 'fvalue'],
        #       'posarg2value2',
        #       ['-', 'g', 't', 'i'],
        #       'value',
        #       'posarg3value',
        #       '--',
        #       '--posarg2value3',
        #   ]
        #
        #   PositionalArgumentHolder1.parsed_arg_indices = [0]
        #   OptionalArgumentHolder1.parsed_arg_indices = [1, 2, 3]
        #   OptionalArgumentHolder2.parsed_arg_indices = [4]
        #   PositionalArgumentHolder2.parsed_arg_indices = [5, 8, 13]
        #   OptionalArgumentHolder3.parsed_arg_indices = [(6, 1)]
        #   OptionalArgumentHolder4.parsed_arg_indices = [(6, 2)]
        #   OptionalArgumentHolder5.parsed_arg_indices = [(7, 3)]
        #   OptionalArgumentHolder6.parsed_arg_indices = [(9, 1)]
        #   OptionalArgumentHolder7.parsed_arg_indices = [(9, 3), 10]
        #   PositionalArgumentHolder3.parsed_arg_indices = [11]

        # TODO: Implement nargs=REMAINDER

        current_posarg_index = 0
        current_argument = self.posargholders[current_posarg_index]
        options_enabled = True
        for index, arg in enumerate(args):
            if options_enabled and arg[0] in self.prefix_chars:
                if arg[1] in self.prefix_chars:
                    name, sep, value = arg[2:].partition(self.OPT_SEP)
                    # FIXME
                    print('long', name, value)
                    try:
                        optargholder = self.longflag_to_optargholder[name]
                    except KeyError:
                        if len(arg) == 2:
                            # This is the special '--' option
                            self.parsed_args.append(arg)
                            options_enabled = False
                            continue
                        else:
                            raise UnknownArgumentError(arg)
                    else:
                        current_argument = optargholder
                        current_argument.store_index(index)
                        optargholder.action.process_flag()
                        if sep:
                            if value:
                                # optargholder can raise UnwantedValueError,
                                # but in this case it shouldn't be caught
                                optargholder.action.store_value(value)
                            else:
                                # The option ends with the separator, without
                                # a value (ambiguous, better not allow it)
                                raise InvalidArgumentError(arg)
                        # This is '--option' or '--option=value'
                        self.parsed_args.append(arg)
                else:
                    # FIXME
                    print('short', arg[1:])
                    # This is the initial '-'
                    self.parsed_args.append([arg[0]])
                    for subindex, option in enumerate(arg[1:]):
                        try:
                            optargholder = self.shortflag_to_optargholder[
                                                                        option]
                        except KeyError:
                            raise UnknownArgumentError(arg)
                        else:
                            current_argument = optargholder
                            # Add 1 to subindex because the initial prefix
                            # (e.g. '-') must be taken into account
                            current_argument.store_index((index, subindex + 1))
                            optargholder.action.process_flag()
                            # Add 2 to subindex because the initial prefix
                            # (e.g. '-') must be taken into account
                            value = arg[subindex + 2:]
                            if value == '':
                                # This is the last short option 'o'
                                self.parsed_args[-1].append(option)
                            elif value[0] == self.OPT_SEP:
                                value = value[1:]
                                if value:
                                    # optargholder can raise
                                    # UnwantedValueError, but in this case it
                                    # shouldn't be caught
                                    optargholder.action.store_value(value)
                                    # This is the short option 'o=value'
                                    # Add 1 to subindex because the initial
                                    # prefix (e.g. '-') must be taken into
                                    # account
                                    self.parsed_args[-1].append(
                                                            arg[subindex + 1:])
                                    break
                                else:
                                    # The option ends with the separator,
                                    # without a value (ambiguous, better not
                                    # allow it)
                                    raise InvalidArgumentError(arg)
                            else:
                                try:
                                    optargholder.action.store_value(value)
                                except UnwantedValueError:
                                    # This is the short option 'o'
                                    self.parsed_args[-1].append(option)
                                else:
                                    # This is the short option 'ovalue'
                                    # Add 1 to subindex because the initial
                                    # prefix (e.g. '-') must be taken into
                                    # account
                                    self.parsed_args[-1].append(
                                                            arg[subindex + 1:])
                                    break
            else:
                # FIXME
                print('value', arg)
                self.parsed_args.append(arg)
                try:
                    current_argument.action.store_value(arg)
                except UnwantedValueError:
                    current_argument = self.posargholders[current_posarg_index]
                    try:
                        current_argument.action.store_value(arg)
                    except UnwantedValueError:
                        current_posarg_index += 1
                        try:
                            current_argument = self.posargholders[
                                                        current_posarg_index]
                        except IndexError:
                            raise UnknownArgumentError()
                        else:
                            current_argument.action.store_value(arg)
                current_argument.store_index(index)

        # TODO: Also check that all arguments that require at least one value,
        #       do get a value

        # TODO: Do the positional arguments have to be parsed in a second loop,
        #       so that the various nargs settings can be properly honored?
        #       Also, it could make sense to support non-greedy nargs values
        #       such as '??', '*?' and '+?'
        # FIXME
        print(self.parsed_args)

        # TODO: return a namespace compatible with argparse's
        # TODO: Implement SUPPRESS (don't list an argument if it wasn't passed
        #       to the command line)
        return {dest: self.dest_to_argholder[dest].value
                for dest in self.dest_to_argholder}


class ForwargError(Exception):
    pass


class ExistingArgumentError(ForwargError):
    pass


class ExistingArgumentGroupError(ForwargError):
    pass


class InvalidArgumentNameError(ForwargError):
    pass


class InvalidArgumentError(ForwargError):
    pass


class MultiplePositionalArgumentNamesError(ForwargError):
    pass


class UnknownArgumentError(ForwargError):
    pass


class UnrecognizedNargsError(ForwargError):
    pass


class UnwantedValueError(ForwargError):
    pass
