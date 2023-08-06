import sys
from threading import RLock


# enable VT100 support on windows platform for stderr
import platform
if platform.system().lower() == 'windows':
    from ctypes import windll, c_int, byref
    stderr_handle = windll.kernel32.GetStdHandle( c_int(-12) )
    mode = c_int( 0 )
    windll.kernel32.GetConsoleMode( c_int ( stderr_handle ), byref( mode ) )
    mode = c_int( mode.value | 4 )
    windll.kernel32.SetConsoleMode( c_int ( stderr_handle ), mode )


# lock for providing thread safe access to console writers
_uiLock = RLock ()


# default console device
from . import writer
consoleprinter = writer.Printer( )
console = writer.Tee( printers = [consoleprinter], lock = _uiLock )


# set exception hook
from . import exceptions
sys.excepthook = exceptions.defaultExceptionHook


# import Logger class
from . import logger
Logger = logger.Logger


# control application life cycle
from . import lifecycle
application = lifecycle.application


# default input device
from . import input_provider as _input_provider
input = _input_provider._Input()

