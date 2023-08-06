import sys
import termios
from threading import RLock

from . import input_event
from .threads import Thread
from . import application




# thread reading input data asynchronously
class _InputThread( Thread ):
    def __init__( self, rawInput ):
        """
        Input thread for reading data from console input
        """
        super().__init__( target = self.work, name = "Console Input Thread", daemon = True )
        self._rawInput = rawInput
        self._isShutdown = False
        self._inputParser = input_event.InputEventParserVT100( self._parserCallback )
        self._lock = RLock()


    def work( self ):
        """
        Read characters from console input
        """
        while( self.shutdownRequested() != True ):
            data = sys.stdin.read( 1 )
            with self._lock:
                if( self._isShutdown == False ):
                    self._inputParser.parse( data )


    def _parserCallback( self, events ):
        for event in events:
            self._rawInput._onInput( event )


    def shutdown( self ):
        """
        Shutdown input thread
        """
        with self._lock:
            if( self._isShutdown == True ):
                return
            self._isShutdown = True
        self._inputParser.close()
        return super().shutdown()




# raw keyboard input handler for posix
class RawInput:
    def __init__( self ):
        """
        Raw input class for posix terminals
        """
        self._lock = RLock()
        self._isStarted = False
        self._inputCallback = None
        self._oldFlags = None
        application.registerExitFunction( self.close )
        self._thread = None


    def init( self, inputCallback ):
        """
        Init raw input handler, disable echo on console
        """
        # register at application
        from . import application
        application._setInputWorker( self )

        # start worker
        with self._lock:
            assert self._isStarted == False
            self._inputCallback = inputCallback
            self._isStarted = True
            self._enableInteractiveMode()
            self._thread = _InputThread( self )
            self._thread.start ()


    def close( self ):
        """
        Close input handler when application terminates
        """
        with self._lock:
            if( self._isStarted == True ):
                self._restoreMode()
                if( self._thread != None ):
                    self._thread.shutdown()


    def _onInput( self, inputData ):
        """
        Got data from input thread
        """
        if( self._inputCallback != None ):
            self._inputCallback( inputData )


    def _enableInteractiveMode( self ):
        """
        Enable interactive mode (disable echo, consume single characters)
        """
        if( sys.stdin.isatty() ):
            if( self._oldFlags == None ):
                fd = sys.stdin.fileno()
                (iflag, oflag, cflag, lflag, ispeed, ospeed, cc) = termios.tcgetattr( fd )
                self._oldFlags = lflag
                lflag &= ~( termios.ECHO | termios.ICANON  )
                new_attr = [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]
                termios.tcsetattr( fd, termios.TCSANOW, new_attr )


    def abort( self ):
        """
        Application received a CTRL+C event
        """
        self._onInput( input_event.InputEvent( None, input_event.abort ) )


    def _restoreMode( self ):
        """
        Restore console mode
        """
        if( self._oldFlags ):
            fd = sys.stdin.fileno()
            (iflag, oflag, cflag, lflag, ispeed, ospeed, cc) = termios.tcgetattr( fd )
            new_attr = [iflag, oflag, cflag, self._oldFlags, ispeed, ospeed, cc]
            termios.tcsetattr( fd, termios.TCSANOW, new_attr )
