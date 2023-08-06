"""A module that does stuff like parsing text commands and processing commands"""

import re
import shlex
import inspect

_CVT_FLOAT_PTR = re.compile(r"^[-+]?(\d*[.])\d*$")
_CVT_INT_PTR = re.compile(r"^[-+]?\d+$")


class CmdBaseException(Exception):
    """base exception of this module"""

    def __init__(self, message, *args):
        self.message = message
        self.args = args
        super().__init__(self.message)

    def __str__(self):
        return self.message


class ParsingError(Exception):
    """raised when parsing error..."""


class ProcessError(Exception):
    """raised when error occurred during processing commands without error handler"""

    def __init__(self, message, exception):
        self.message = message
        self.exception = exception
        super().__init__(self.message)


class MissingRequiredArgument(CmdBaseException):
    """raised when command's positional argument is missing"""

    def __init__(self, message, param):
        self.message = message
        self.param = param
        super().__init__(self.message)


class Parser:
    def __init__(self, text, prefix):
        self.text = text
        self.index = -1
        self.prefix = prefix
        self.char = None
        self.args = None

        if self.text:
            self._parse()

    def _shift(self):
        self.index += 1
        self.char = self.text[self.index] if self.index < len(self.text) else None

    def _parse(self):
        self._shift()
        space_count = 0
        while self.char is not None:
            if self.char == " ":
                space_count += 1
            else:
                _pref = self.text[:self.index].rstrip()

                if _pref == self.prefix and space_count <= 1:
                    self.args = self.text[self.index:].lstrip()

                    break

            self._shift()


class AttrMan:
    """some kind of attributes manager"""
    def __init__(self, target, **attrs):
        self.target = target
        self.attrs = attrs

        self.dupe_attrs = {}

    def _save_dupes(self):
        """save existing or duplicate attributes"""
        if not inspect.ismethod(self.target):
            for attr in self.attrs:
                if hasattr(self.target, attr):
                    self.dupe_attrs.update({attr: getattr(self.target, attr)})
        else:
            for attr in self.attrs:
                if hasattr(self.target.__self__, attr):
                    self.dupe_attrs.update({attr: getattr(self.target.__self__, attr)})

    def _clear(self):
        if not inspect.ismethod(self.target):
            for attr in self.attrs:
                if hasattr(self.target, attr):
                    delattr(self.target, attr)
        else:
            for attr in self.attrs:
                if hasattr(self.target.__self__, attr):
                    delattr(self.target.__self__, attr)

    def set(self):
        self._save_dupes()

        if not inspect.ismethod(self.target):
            for attr in self.attrs:
                setattr(self.target, attr, self.attrs[attr])
        else:
            for attr in self.attrs:
                setattr(self.target.__self__, attr, self.attrs[attr])

    def reset(self):
        self._clear()

        if not inspect.ismethod(self.target):
            for attr in self.dupe_attrs:
                setattr(self.target, attr, self.dupe_attrs[attr])
        else:
            for attr in self.dupe_attrs:
                setattr(self.target.__self__, attr, self.dupe_attrs[attr])


class Cmd:
    """main class for parsing commands"""

    def __init__(self, command_string, prefix="/", max_args=0, convert_args=False):
        self.name = None
        self.args = []
        self.command_string = command_string
        self.convert_args = convert_args
        self.prefix = prefix
        self.max_args = max_args

        # parse command
        res = Parser(self.command_string, self.prefix)
        argres = []
        if res.args is not None:
            argres = shlex.split(res.args)

        if self.max_args == 0:
            self.max_args = len(argres) - 1 if (len(argres) - 1) >= 0 else 0

        if (len(argres) - 1) >= 0 and (len(argres) - 1) > self.max_args:
            raise ParsingError(f"arguments exceeds max arguments: {self.max_args}")

        while (len(argres) - 1) >= 0 and (len(argres) - 1) < self.max_args:  # insert empty arguments
            argres.append("")

        if argres:
            self.name = argres[0]
            self.args = argres[1:]

            if convert_args:
                self._cvt_cmd()

    def _get_args_type_char(self, max_args=0):
        """get command arguments data types in char format"""
        argtype = list()

        if max_args == 0:
            for arg in self.args[0: len(self.args)]:
                if not arg:
                    continue

                argtype.append(type(arg).__name__[0])  # get type char
        else:
            for arg in self.args[0:max_args]:
                if not arg:
                    continue

                argtype.append(type(arg).__name__[0])  # get type char

        return argtype

    def _cvt_cmd(self):
        """evaluate literal arguments"""
        cvt = [(_CVT_FLOAT_PTR, float), (_CVT_INT_PTR, int)]

        for i in range(len(self.args)):
            if not self.args[i]:
                break  # empty args

            for cvt_ in cvt:
                res = cvt_[0].match(self.args[i])

                if res:
                    self.args[i] = cvt_[1](
                        self.args[i]
                    )
                    break  # has found the correct data type

    def match_args(self, format_match, max_args=0):
        """match argument formats, only works with converted arguments"""

        # format example: 'ssf', arguments: ['hell','o',10.0] matched

        if max_args <= 0 and self.max_args > -1:
            max_args = self.max_args

        if not format_match:
            raise ValueError("no format specified")

        format_match = format_match.replace(" ", "")
        format_match = list(format_match)

        argtype = self._get_args_type_char(max_args)

        if len(format_match) != len(argtype):
            raise ValueError("format length is not the same as the arguments length")

        return self._match_args(argtype, format_match)

    def _match_args(self, argtype, format_match):
        """match arguments by arguments data types"""
        matched = 0
        for i, arg_type in enumerate(argtype):
            arg_len = len(str(self.args[i]))
            if arg_type in ("i", "f"):
                if format_match[i] == "s":
                    matched += 1  # allow int or float as 's' format
                elif format_match[i] == "c" and arg_len == 1 and arg_type == "i":
                    matched += 1  # and char if only a digit for int
                elif arg_type == format_match[i]:
                    matched += 1
            elif arg_type == "s":
                if format_match[i] == "c" and arg_len == 1:
                    matched += 1
                elif arg_type == format_match[i]:
                    matched += 1

        if matched == len(format_match):
            return True

        return False

    def process_cmd(self, callback, error_callback=None, attrs=None):
        """process command..."""
        if attrs is None:
            attrs = {}

        if (
            inspect.isfunction(callback) is False
            and inspect.ismethod(callback) is False
        ):
            raise TypeError("callback is not a function or method")
        if (
            error_callback
            and inspect.isfunction(error_callback) is False
            and inspect.ismethod(callback) is False
        ):
            raise TypeError("error handler callback is not a function")

        if not isinstance(attrs, dict):
            raise TypeError("attributes must be in dict object")

        cman = AttrMan(callback, **attrs)
        ecman = AttrMan(error_callback, **attrs) if error_callback is not None else None

        cman.set()
        ecman.set() if ecman is not None else None

        ret = None
        try:
            cargspec = inspect.getfullargspec(callback)
            cparams = cargspec.args
            cdefaults = cargspec.defaults

            # remove 'self' or 'cls' from parameters if method
            if inspect.ismethod(callback):
                if len(cparams) > 0:
                    cparams = cparams[1:]

            if cdefaults is None:
                if len(self.args) < len(cparams):
                    raise MissingRequiredArgument(
                        "missing required argument: "
                        + cparams[len(self.args)],
                        param=cparams[len(self.args)],
                    )

            else:

                posargs_length = len(cparams) - len(cdefaults)

                if len(self.args) < posargs_length:
                    raise MissingRequiredArgument(
                        "missing required argument: "
                        + cparams[len(self.args)],
                        param=cparams[len(self.args)],
                    )

            if cargspec.varargs is None:
                ret = callback(*self.args[: len(cparams)])
            else:
                ret = callback(*self.args)

        except Exception as exception:
            if error_callback is None:
                raise ProcessError(
                    "an error occurred during processing callback '"
                    + f"{callback.__name__}()' for command '{self.name}, "
                    + "no error handler callback specified.",
                    exception,
                ) from exception

            error_callback(error=exception)

        cman.reset()
        ecman.reset() if ecman is not None else None

        return ret

    def __str__(self):
        message = (
            "<"
            + f'Raw: "{self.command_string}", '
            + f'Name: "{self.name}", '
            + f"Args: {self.args}>"
        )

        return message


class AioCmd(Cmd):
    async def process_cmd(self, callback, error_callback=None, attrs=None):
        """coroutine process cmd"""
        if attrs is None:
            attrs = {}

        if (
            inspect.isfunction(callback) is False
            and inspect.ismethod(callback) is False
        ):
            raise TypeError("callback is not a function or method")
        if (
            error_callback
            and inspect.isfunction(error_callback) is False
            and inspect.ismethod(callback) is False
        ):
            raise TypeError("error handler callback is not a function")

        if not isinstance(attrs, dict):
            raise TypeError("attributes must be in dict object")

        cman = AttrMan(callback, **attrs)
        ecman = AttrMan(error_callback, **attrs) if error_callback is not None else None

        cman.set()
        ecman.set() if ecman is not None else None

        ret = None
        try:
            cargspec = inspect.getfullargspec(callback)
            cparams = cargspec.args
            cdefaults = cargspec.defaults

            # remove 'self' or 'cls' from parameters if method
            if inspect.ismethod(callback):
                if len(cparams) > 0:
                    cparams = cparams[1:]

            if cdefaults is None:
                if len(self.args) < len(cparams):
                    raise MissingRequiredArgument(
                        "missing required argument: "
                        + cparams[len(self.args)],
                        param=cparams[len(self.args)],
                    )

            else:

                posargs_length = len(cparams) - len(cdefaults)

                if len(self.args) < posargs_length:
                    raise MissingRequiredArgument(
                        "missing required argument: "
                        + cparams[len(self.args)],
                        param=cparams[len(self.args)],
                    )

            if cargspec.varargs is None:
                ret = await callback(*self.args[: len(cparams)])
            else:
                ret = await callback(*self.args)

        except Exception as exception:
            if error_callback is None:
                raise ProcessError(
                    "an error occurred during processing callback '"
                    + f"{callback.__name__}()' for command '{self.name}, "
                    + "no error handler callback specified.",
                    exception,
                ) from exception

            error_callback(error=exception)

        cman.reset()
        ecman.reset() if ecman is not None else None

        return ret
