import sys
import traceback
import threading
from . import style
from . import loglevels
from . import sstr
from .logger import Logger, LoggerStyle




# logger for exceptions
class _ExceptionLogger:
    def __init__( self ):
        """
        Create exception logger
        """
        self.logger = None
        self.updateLoggerSettings()


    def updateLoggerSettings( self ):    
        """
        Update logger style from default style
        """
        loggerStyle = style.Defaults.getExceptionLoggerStyle()
        self.logger = Logger( loggerStyle.name, loggerStyle.level, loggerStyle.nameStyle, loggerStyle.contentStyle, loggerStyle.alignName )


    def get( self ):
        """
        Get logger instance
        """
        return self.logger

# single instance of exception logger
_exceptionLogger = _ExceptionLogger()




# exception for terminating the commandline app
class TerminateException( Exception ):
    def __init__( self ):
        Exception.__init__( self )




# format exception as string
def formatException( exception ):
        # format exception as string ( create list of lines )
        exLines = '\n'.join( traceback.format_exception( exception.__class__, exception, exception.__traceback__ ) ).replace( '\r', '\n' ).split( '\n' )

        # remove leading whitespaces
        exProcessedLines = []
        for line in exLines:
            if( line.startswith( "  " ) ):
                exProcessedLines.append( line[2:] )
            else:
                exProcessedLines.append( line )

        # remove exceeding new lines
        while( len( exProcessedLines ) > 0 ):
            if( exProcessedLines[-1].strip() == "" ):
                exProcessedLines = exProcessedLines[: len( exProcessedLines ) - 1]
            else:
                break

        # return formatted exception lines
        return '\n'.join( exProcessedLines )




# handle an uncaught exception
def handle( exception ):
    if( exception.__class__ != TerminateException ):     

        # on exception: trigger close input on application
        from . import application
        application._closeInputFromException()

        # get current thread identification
        cThread = threading.currentThread()
        if( cThread == None ):
            threadName = "main"
        else:
            threadName = cThread.name
        threadInfo = "in thread '" + threadName + "':"

        # format exception
        exStr = formatException( exception )

        # write exception to console
        if( threadInfo == None ):
            _exceptionLogger.get().write( exStr )
        else:
            _exceptionLogger.get().write( [threadInfo, exStr] )

        # signal application about an exception
        application._handleExceptionShutdown()




# default exception hook
def defaultExceptionHook( exctype, value, traceback ):
    """
    Exception hook for handling TerminateExceptions    
    """
    handle( value )
