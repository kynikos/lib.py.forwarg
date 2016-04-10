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

# TODO: Support Python 2

import sys as _m_sys
import re as _m_re
from collections import OrderedDict
# TODO: Implement all argparse features
#       https://docs.python.org/3/library/argparse.html
#       Maybe for the help page this module could simply rely on argparse in
#       general
from argparse import Namespace, HelpFormatter

REMAINDER = object()
SUPPRESS = object()


class Action:
    def __init__(self, argdef, argholder):
        self.argdef = argdef
        self.argholder = argholder

    def process_flag(self):
        # Call check_value because the flag can be specified multiple
        #  times, and only the last occurrence is checked at the end of the
        #  main parsing loop
        # If no check was done, it could be possible to do something like
        #  '--option1 --option2 --option1=value', and, if --option1
        #  requires a value, an error wouldn't be raised because it would
        #  be assigned by the second instance
        # Note that check_value already checks
        #  if self.argholder.number_of_parsed_flags > 0
        self.check_value()
        self._process_flag()
        # Increment this only after _process_flag, for consistency with
        # store_value below
        self.argholder.number_of_parsed_flags += 1
        self.argholder.number_of_parsed_values_for_current_flag = 0

    def _process_flag(self):
        # This method can also be assigned dynamically when instantiating the
        # subclasses
        raise NotImplementedError()

    def store_value(self, newvalue):
        self._store_value(newvalue)
        # Increment this only after _store_value, which could raise the
        # UnwantedValueError exception, thus not storing the value
        self.argholder.number_of_parsed_values_for_all_flags += 1
        self.argholder.number_of_parsed_values_for_current_flag += 1

    def _store_value(self, newvalue):
        # This method can also be assigned dynamically when instantiating the
        # subclasses
        raise NotImplementedError()

    def check_value(self):
        raise NotImplementedError()

    def store_index(self, index):
        self.argholder.parsed_arg_indices.append(index)


class _ActionStore(Action):
    def check_value(self):
        # This method is overridden by at least ActionStoreConst
        nargs = self.argdef.nargs

        if self.argholder.number_of_parsed_flags > 0 or isinstance(
                                self.argdef, PositionalArgumentDefinition):
            if nargs in (None, '+', REMAINDER):
                if self.argholder.number_of_parsed_values_for_current_flag < 1:
                    raise InsufficientArgumentsError(self.argdef.dest)
            elif isinstance(nargs, int):
                if self.argholder.number_of_parsed_values_for_current_flag < nargs:  # NOQA
                    raise InsufficientArgumentsError(self.argdef.dest)
            # TODO: How does argparse behave if an option has nargs == '*' but
            #       no value is passed in the command line?
            elif nargs == '?':
                if self.argholder.number_of_parsed_values_for_current_flag < 1:
                    self._default_to_const()

    def _default_to_const(self):
        raise NotImplementedError()


class ActionStore(_ActionStore):
    def __init__(self, argdef, argholder):
        super().__init__(argdef, argholder)
        nargs = self.argdef.nargs
        if nargs in (None, '?'):
            self._process_flag = self._dummy
            self._store_value = self._override
        elif isinstance(nargs, int) and nargs > -1:
            self._process_flag = self._init_list
            self._store_value = self._append_limited
        elif nargs in ('*', '+', REMAINDER):
            self._process_flag = self._init_list
            self._store_value = self._append_unlimited
        else:
            raise UnrecognizedNargsError(nargs)

    def _dummy(self):
        # TODO: Raise an error if the option has already been specified?
        pass

    def _init_list(self):
        # The list must be initialized even if the option is passed only
        # once and without a value
        self.argholder.value = []

    def _override(self, newvalue):
        if self.argholder.number_of_parsed_values_for_current_flag > 0:
            raise UnwantedValueError(newvalue)
        self.argholder.value = newvalue

    def _append_limited(self, newvalue):
        if self.argholder.number_of_parsed_values_for_current_flag >= \
                                                        self.argdef.nargs:
            raise UnwantedValueError(newvalue)
        self._append_unlimited(newvalue)

    def _append_unlimited(self, newvalue):
        if self.argholder.number_of_parsed_values_for_current_flag == 0:
            self.argholder.value = [newvalue]
        else:
            self.argholder.value.append(newvalue)

    def _default_to_const(self):
        self.argholder.value = self.argdef.const


class ActionAppend(_ActionStore):
    def __init__(self, argdef, argholder):
        super().__init__(argdef, argholder)
        nargs = self.argdef.nargs
        if nargs in (None, '?'):
            self._store_value = self._append_plain
        elif isinstance(nargs, int) and nargs > -1:
            self._store_value = self._append_nested_limited
        elif nargs in ('*', '+', REMAINDER):
            self._store_value = self._append_nested_unlimited
        else:
            raise UnrecognizedNargsError(nargs)

    def _process_flag(self):
        if self.argholder.number_of_parsed_flags == 0:
            # The list must be initialized even if the option is passed only
            # once and without a value
            self.argholder.value = []

    def _append_plain(self, newvalue):
        if self.argholder.number_of_parsed_values_for_current_flag > 0:
            raise UnwantedValueError(newvalue)
        if self.argholder.number_of_parsed_flags == 0:
            self.argholder.value = [newvalue]
        else:
            self.argholder.value.append(newvalue)

    def _append_nested_limited(self, newvalue):
        if self.argholder.number_of_parsed_values_for_current_flag >= \
                                                        self.argdef.nargs:
            raise UnwantedValueError(newvalue)
        self._append_nested_unlimited(newvalue)

    def _append_nested_unlimited(self, newvalue):
        if self.argholder.number_of_parsed_flags == 0:
            self.argholder.value = [[newvalue]]
        elif self.argholder.number_of_parsed_values_for_current_flag == 0:
            self.argholder.value.append([newvalue])
        else:
            self.argholder.value[-1].append(newvalue)

    def _default_to_const(self):
        self._append_plain(self.argdef.const)


class ActionStoreConst(Action):
    def __init__(self, argdef, argholder):
        super().__init__(argdef, argholder)
        # TODO: Does argparse ignore nargs in this action?
        if self.argdef.nargs is not None:
            raise UnrecognizedNargsError(self.argdef.nargs)

    def _process_flag(self):
        # TODO: Raise an error if the option has already been specified?
        self.argholder.value = self.argdef.const

    def _store_value(self, newvalue):
        raise UnwantedValueError(newvalue)

    def check_value(self):
        # No values are needed and ever stored, so just skip this check for
        # this action
        pass


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
            self.argholder.value.append(self.argdef.const)
        except TypeError:
            self.argholder.value = [self.argdef.const]


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


class ArgumentDefinitionsGroup:
    def __init__(self, parser, title, description):
        self.parser = parser
        self.title = title
        self.description = description
        self.dest_to_argdef = OrderedDict()

    def add_argument(self, *nameorflags, action='store', nargs=None,
                     const=None, default=None, type=None, choices=None,
                     required=None, help=None, metavar=None, dest=None,
                     version=None):
        argdef = _ArgumentDefinition.create(
                self.parser, nameorflags, action, nargs, const, default, type,
                choices, required, help, metavar, dest, version)
        self.do_add_argument(argdef)
        return argdef

    def do_add_argument(self, argdef):
        argdef.set_group(self)
        self.dest_to_argdef[argdef.dest] = argdef
        self.parser.dest_to_argdef[argdef.dest] = argdef


class _ArgumentDefinition:
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

    @classmethod
    def create(cls, parser, nameorflags, action, nargs, const, default, type,
               choices, required, help, metavar, dest, version):
        if len(nameorflags) < 1:
            raise InvalidArgumentNameError()

        # TODO: asserting isn't the best way to validate arguments...
        assert isinstance(dest, str) or dest is None

        try:
            return OptionalArgumentDefinition(
                            parser, nameorflags,
                            action=action, nargs=nargs, const=const,
                            default=default, type=type, choices=choices,
                            required=required, help=help, metavar=metavar,
                            dest=dest, version=version)
        except InvalidArgumentNameError:
            if len(nameorflags) > 1:
                raise MultiplePositionalArgumentNamesError(nameorflags)
            return PositionalArgumentDefinition(
                            parser, nameorflags,
                            action=action, nargs=nargs, const=const,
                            default=default, type=type, choices=choices,
                            required=required, help=help, metavar=metavar,
                            dest=dest, version=version)

    def __init__(self, parser, action, nargs, const, default, type, choices,
                 required, help, metavar, dest, version):
        self.parser = parser

        # TODO: These arguments still have to be used
        if type is not None:
            # TODO: See at least
            #       https://docs.python.org/3/library/argparse.html#type
            #       https://docs.python.org/3/library/argparse.html#default
            raise NotImplementedError()
        if choices is not None:
            raise NotImplementedError()
        if required is not None:
            raise NotImplementedError()
        if help is not None:
            raise NotImplementedError()
        if metavar is not None:
            raise NotImplementedError()
        if version is not None:
            # TODO: Required when using action='version'
            raise NotImplementedError()

        # TODO: currently nargs is only validated when instantiating action,
        #       i.e. at parse time, but it should be validated now at
        #       definition time
        self.nargs = nargs
        self.const = const
        self.default = default
        self.dest = dest

        # Instantiating action may require the other attributes to be already
        # set, so do it *after* storing them
        # TODO: Also support argparse's Action classes? Otherwise warn that
        #       they aren't supported
        try:
            self.action = self.ACTIONS[action]
        except KeyError:
            # TODO: asserting isn't the best way to validate arguments...
            assert issubclass(action, Action)
            self.action = action

    def set_group(self, group):
        self.group = group

    @staticmethod
    def _make_dest(parser, rawdest):
        dest = _m_re.sub(r'[^a-zA-Z0-9_]', '_', rawdest)
        if dest[0].isdigit():
            dest = '_' + dest

        # TODO: actually, at least the 'append_const' action requires 'dest'
        #       to be defined by more than an option
        if dest in parser.dest_to_argdef:
            raise ExistingArgumentError(dest)

        return dest

    def create_parsed_values_holder(self, parsedargs):
        return _ArgumentHolder(self, parsedargs)


class OptionalArgumentDefinition(_ArgumentDefinition):
    def __init__(self, parser, nameorflags, action, nargs, const,
                 default, type, choices, required, help, metavar, dest,
                 version):
        self.longflags = []
        self.shortflags = []

        for flag in nameorflags:
            if not isinstance(flag, str):
                raise InvalidArgumentNameError(flag)
            if _m_re.fullmatch(parser.longopt_arg_re, flag):
                if flag[2:] in parser.longflag_to_optargdef:
                    raise ExistingArgumentError(flag)
                self.longflags.append(flag[2:])
            elif _m_re.fullmatch(parser.shortopt_arg_re, flag):
                if flag[1:] in parser.shortflag_to_optargdef:
                    raise ExistingArgumentError(flag)
                self.shortflags.append(flag[1:])
            else:
                raise InvalidArgumentNameError(flag)

        dest = dest or self._make_dest(parser,
                                       (self.longflags + self.shortflags)[0])
        super().__init__(parser, action=action, nargs=nargs,
                         const=const, default=default, type=type,
                         choices=choices, required=required, help=help,
                         metavar=metavar, dest=dest, version=version)

        # Reference the object only after the whole validation
        for flag in self.longflags:
            self.parser.longflag_to_optargdef[flag] = self
        for flag in self.shortflags:
            self.parser.shortflag_to_optargdef[flag] = self


class PositionalArgumentDefinition(_ArgumentDefinition):
    def __init__(self, parser, nameorflags, action, nargs, const,
                 default, type, choices, required, help, metavar, dest,
                 version):
        self.name = nameorflags[0]

        if not isinstance(self.name, str) or \
                not _m_re.fullmatch(parser.pos_arg_re, self.name):
            raise InvalidArgumentNameError(self.name)
        if self.name in parser.name_to_posargdef:
            raise ExistingArgumentError(self.name)

        # TODO: actions other than 'store' don't make sense for positional
        #       arguments, right?
        # TODO: asserting isn't the best way to validate arguments...
        assert action is 'store'
        dest = dest or self._make_dest(parser, self.name)
        super().__init__(parser, action=action, nargs=nargs,
                         const=const, default=default, type=type,
                         choices=choices, required=required, help=help,
                         metavar=metavar, dest=dest, version=version)

        # Reference the object only after the whole validation
        self.parser.name_to_posargdef[self.name] = self
        self.parser.posargdefs.append(self)


class _ArgumentHolder:
    def __init__(self, argdef, parsedargs):
        self.argdef = argdef
        self.parsedargs = parsedargs

        self.action = self.argdef.action(argdef, self)
        self.number_of_parsed_flags = 0
        self.number_of_parsed_values_for_all_flags = 0
        self.number_of_parsed_values_for_current_flag = 0
        self.parsed_arg_indices = []
        self.value = self.argdef.default


class ParseResults:
    # Keep the parse results separate from the generic argument definitions, so
    # that more command lines can be parsed with the same parser object
    # This behavior is consistent with argparse; the namespace attribute is
    # analogous to argparse's parse_args return value
    def __init__(self, parser, args, namespace):
        self.parser = parser

        if namespace is None:
            self._namespace = Namespace()
        else:
            # TODO: asserting isn't the best way to validate arguments...
            assert isinstance(namespace, Namespace)
            self._namespace = namespace

        self.argdef_to_argholder = {argdef:
                                    argdef.create_parsed_values_holder(self)
                                    for argdef
                                    in self.parser.dest_to_argdef.values()}
        self.splitline = []

        self.current_posarg_index = 0
        try:
            self.current_argholder = self.argdef_to_argholder[
                            self.parser.posargdefs[self.current_posarg_index]]
        except IndexError:
            # There may not be any positional arguments defined
            self.current_argholder = None
            self.options_enabled = True
        else:
            self.options_enabled = self.current_argholder.argdef.nargs is not \
                                                                    REMAINDER
        self.ContinueLoop = type('ContinueLoop', (Exception, ), {})

        self._parse(args)

    @property
    def namespace(self):
        # This property exists only for backward compatibility with argparse;
        # when possible, read the values directly from the argument holoder's
        # attributes
        for argdef in self.argdef_to_argholder:
            # namespace could have been initialized in the constructor with
            # already some # attributes from another parser, so check that they
            # are not overwritten
            # TODO: asserting isn't the best way to validate arguments...
            assert not hasattr(self._namespace, argdef.dest)
            if argdef.default is not SUPPRESS:
                setattr(self._namespace, argdef.dest,
                        self.argdef_to_argholder[argdef].value)

        return self._namespace

    def _parse(self, args):
        # Don't try to define a parse_known_args method, since there are many
        # ambiguous cases anyway, for example in '--unknown-option value' does
        # 'value' belong to '--unknown-option' or is it a positional argument?
        # We don't know if '--unknown-option' accepts any values
        # See also http://bugs.python.org/issue16142

        # TODO: Check that args is an iterable of strings?
        args = _m_sys.argv[1:] if args is None else args

        for index, arg in enumerate(args):
            if self.options_enabled and arg[0] in self.parser.prefix_chars:
                if arg[1] in self.parser.prefix_chars:
                    try:
                        self._parse_long_flag(index, arg)
                    except self.ContinueLoop:
                        continue
                else:
                    self._parse_short_flag_cluster(index, arg)
            else:
                self._parse_value(index, arg)

        # TODO: Do the positional arguments have to be parsed in a second loop,
        #       so that the various nargs settings can be properly honored?
        #       Also, it could make sense to support non-greedy nargs values
        #       such as '??', '*?' and '+?'
        #       For example compose a string with as many characters as the
        #       number of found positional arguments; then apply the regular
        #       expression qualifiers to it, subdividing it into one group for
        #       each positional argument definition; then assign the actual
        #       values to the various argument parsed-value holders according
        #       to the number of characters in each match group.

        for argholder in self.argdef_to_argholder.values():
            argholder.action.check_value()

    def _parse_long_flag(self, index, arg):
        name, sep, value = arg[2:].partition(self.parser.OPT_SEP)
        try:
            argdef = self.parser.longflag_to_optargdef[name]
        except KeyError:
            if len(arg) == 2:
                # This is the special '--' option
                self.splitline.append((arg, None))
                self.options_enabled = False
                raise self.ContinueLoop()
            else:
                raise UnknownArgumentError(arg)
        else:
            self.current_argholder = self.argdef_to_argholder[argdef]
            self.current_argholder.action.store_index(index)
            self.current_argholder.action.process_flag()
            if sep:
                if value:
                    # current_argholder can raise UnwantedValueError,
                    # but in this case it shouldn't be caught
                    self.current_argholder.action.store_value(value)
                else:
                    # The option ends with the separator, without
                    # a value (ambiguous, better not allow it)
                    # TODO: But does argparse support this?
                    raise InvalidArgumentError(arg)
            if argdef.nargs is REMAINDER:
                self.options_enabled = False
            # This is '--option' or '--option=value'
            self.splitline.append((arg, self.current_argholder))

    def _parse_short_flag_cluster(self, index, arg):
        # This is the initial '-'
        self.splitline.append([(arg[0], None)])
        for subindex, option in enumerate(arg[1:]):
            try:
                argdef = self.parser.shortflag_to_optargdef[option]
            except KeyError:
                raise UnknownArgumentError(arg)
            else:
                self.current_argholder = self.argdef_to_argholder[argdef]
                # Add 1 to subindex because the initial prefix
                # (e.g. '-') must be taken into account
                self.current_argholder.action.store_index((index,
                                                           subindex + 1))
                self.current_argholder.action.process_flag()
                # Add 2 to subindex because the initial prefix
                # (e.g. '-') must be taken into account
                value = arg[subindex + 2:]
                if value == '':
                    # This is the last short option 'o'
                    self.splitline[-1].append((option, self.current_argholder))
                elif value[0] == self.parser.OPT_SEP:
                    value = value[1:]
                    if value:
                        # current_argholder can raise
                        # UnwantedValueError, but in this case it
                        # shouldn't be caught
                        self.current_argholder.action.store_value(value)
                        # This is the short option 'o=value'
                        # Add 1 to subindex because the initial
                        # prefix (e.g. '-') must be taken into
                        # account
                        self.splitline[-1].append((arg[subindex + 1:],
                                                   self.current_argholder))
                        # Set 'options_enabled' here, *before* the
                        # 'break'
                        if argdef.nargs is REMAINDER:
                            self.options_enabled = False
                        break
                    else:
                        # The option ends with the separator,
                        # without a value (ambiguous, better not
                        # allow it)
                        # TODO: But does argparse support this?
                        raise InvalidArgumentError(arg)
                else:
                    try:
                        self.current_argholder.action.store_value(value)
                    except UnwantedValueError:
                        # This is the short option 'o'
                        self.splitline[-1].append((option,
                                                   self.current_argholder))
                    else:
                        # This is the short option 'ovalue'
                        # Add 1 to subindex because the initial
                        # prefix (e.g. '-') must be taken into
                        # account
                        self.splitline[-1].append((arg[subindex + 1:],
                                                   self.current_argholder))
                        # Set 'options_enabled' here, *before* the
                        # 'break'
                        if argdef.nargs is REMAINDER:
                            self.options_enabled = False
                        break
                # This is reached if no 'break' has been
                # enctountered
                if argdef.nargs is REMAINDER:
                    self.options_enabled = False

    def _parse_value(self, index, arg):
        try:
            self.current_argholder.action.store_value(arg)
        except UnwantedValueError:
            try:
                self.current_argholder = self.argdef_to_argholder[
                            self.parser.posargdefs[self.current_posarg_index]]
            except IndexError:
                # This can be raised if e.g. there's only one optional
                # '-O' argument defined and no positional ones, and the
                # command-line arguments are e.g. '-O val1 val2'
                raise UnknownArgumentError(arg)
            else:
                try:
                    self.current_argholder.action.store_value(arg)
                except UnwantedValueError:
                    self.current_posarg_index += 1
                    try:
                        argdef = self.parser.posargdefs[
                                                    self.current_posarg_index]
                    except IndexError:
                        raise UnknownArgumentError(arg)
                    else:
                        self.current_argholder = self.argdef_to_argholder[
                                                                        argdef]
                        self.current_argholder.action.store_value(arg)
                        if argdef.nargs is REMAINDER:
                            self.options_enabled = False
        except AttributeError:
            # AttributeError could be raised if current_argholder is
            #  None, which can happen at the first loop if there are
            #  no defined positional arguments
            raise UnknownArgumentError(arg)
        self.splitline.append((arg, self.current_argholder))
        self.current_argholder.action.store_index(index)


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
        # TODO: these arguments still have to be used
        if prog is not None:
            raise NotImplementedError()
        if usage is not None:
            raise NotImplementedError()
        if description is not None:
            raise NotImplementedError()
        if epilog is not None:
            raise NotImplementedError()
        if parents != []:
            raise NotImplementedError()
        if formatter_class is not HelpFormatter:
            raise NotImplementedError()
        if fromfile_prefix_chars is not None:
            raise NotImplementedError()
        if argument_default is not None:
            raise NotImplementedError()
        if conflict_handler != 'error':
            raise NotImplementedError()
        if add_help is not True:
            raise NotImplementedError()
        if allow_abbrev is not True:
            raise NotImplementedError()

        # TODO: asserting isn't the best way to validate arguments...
        assert isinstance(prefix_chars, str) and len(prefix_chars) > 0

        # TODO: Implement/Improve error/exit messages

        self.prefix_chars = prefix_chars
        self.pos_arg_re = self.POS_ARG_RE.format(_m_re.escape(
                                                            self.prefix_chars))
        self.longopt_arg_re = self.LONGOPT_ARG_RE.format(_m_re.escape(
                                                            self.prefix_chars))
        self.shortopt_arg_re = self.SHORTOPT_ARG_RE.format(_m_re.escape(
                                                            self.prefix_chars))

        self.title_to_group = {}
        self.dest_to_argdef = OrderedDict()
        self.name_to_posargdef = {}
        self.posargdefs = []
        self.longflag_to_optargdef = {}
        self.shortflag_to_optargdef = {}

    def add_argument_group(self, title=None, description=None):
        # TODO: asserting isn't the best way to validate arguments...
        # TODO: argparse accepts title=None???
        assert isinstance(title, str)

        # TODO: 'description' needs to be implemented
        if description is not None:
            raise NotImplementedError()

        if title in self.title_to_group:
            raise ExistingArgumentGroupError(title)

        group = ArgumentDefinitionsGroup(self, title, description)
        self.title_to_group[title] = group

        return group

    def add_argument(self, *nameorflags, action='store', nargs=None,
                     const=None, default=None, type=None, choices=None,
                     required=None, help=None, metavar=None, dest=None,
                     version=None):
        argdef = _ArgumentDefinition.create(
                        self, nameorflags, action, nargs, const, default, type,
                        choices, required, help, metavar, dest, version)
        if isinstance(argdef, PositionalArgumentDefinition):
            try:
                group = self.add_argument_group('positional arguments')
            except ExistingArgumentGroupError:
                group = self.title_to_group['positional arguments']
        elif isinstance(argdef, OptionalArgumentDefinition):
            try:
                group = self.add_argument_group('optional arguments')
            except ExistingArgumentGroupError:
                group = self.title_to_group['optional arguments']
        else:
            # Just in case in the future more argument types were implemented?
            raise UnknownArgumentType(argdef.dest)
        group.do_add_argument(argdef)
        return argdef

    def parse_args(self, args=None, namespace=None):
        # Don't try to define a parse_known_args method, since there are many
        # ambiguous cases anyway, for example in '--unknown-option value' does
        # 'value' belong to '--unknown-option' or is it a positional argument?
        # We don't know if '--unknown-option' accepts any values
        # See also http://bugs.python.org/issue16142

        # For backward compatibility with argparse, ParseResults.namespace
        # should # be returned, but then what would be the point of using
        # forwarg?
        # TODO: document this difference
        return ParseResults(self, args, namespace)


class ForwargError(Exception):
    pass


class ExistingArgumentError(ForwargError):
    pass


class ExistingArgumentGroupError(ForwargError):
    pass


class InsufficientArgumentsError(ForwargError):
    pass


class InvalidArgumentNameError(ForwargError):
    pass


class InvalidArgumentError(ForwargError):
    pass


class MultiplePositionalArgumentNamesError(ForwargError):
    pass


class UnknownArgumentError(ForwargError):
    pass


class UnknownArgumentType(ForwargError):
    pass


class UnrecognizedNargsError(ForwargError):
    pass


class UnwantedValueError(ForwargError):
    pass
