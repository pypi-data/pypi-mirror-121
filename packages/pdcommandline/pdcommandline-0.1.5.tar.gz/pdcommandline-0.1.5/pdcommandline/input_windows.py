import sys
import msvcrt
from . import input_event
from . import threads
from . import application




# thread reading input data asynchronously
class _InputThread( threads.Thread ):
    def __init__( self, rawInput ):
        """
        Input thread for reading data from console input
        """
        super().__init__( target = self.work, name = "Console Input Thread", daemon = True )
        self._rawInput = rawInput
        self._isShutdown = False
        self._inputParser = input_event.InputEventParserWindows( self._parserCallback )
        self._lock = threads.RLock()


    def work( self ):
        """
        Read characters from console input
        """
        while( self.shutdownRequested() != True ):
            try:
                data = msvcrt.getwch()
                with self._lock:
                    if( self._isShutdown == False ):
                        for c in data:
                            self._inputParser.parse( c )
            except BaseException as e:
                print( str( e ) )
                self.shutdown()


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




# raw keyboard input handler for windows
class RawInput:
    def __init__( self ):
        """
        Raw input class for posix terminals
        """
        self._lock = threads.RLock()
        self._isStarted = False
        self._inputCallback = None
        self._oldFlags = None
        application.registerExitFunction( self.close )
        self._thread = None


    def init( self, inputCallback ):
        """
        Init raw input handler, disable echo on console
        """
        with self._lock:
            assert self._isStarted == False
            self._inputCallback = inputCallback
            self._isStarted = True
            self._thread = _InputThread( self )
            self._thread.start ()


    def close( self ):
        """
        Close input handler when application terminates
        """
        with self._lock:
            if( self._isStarted == True ):
                if( self._thread != None ):
                    self._thread.shutdown()


    def _onInput( self, inputData ):
        """
        Got data from input thread
        """
        if( self._inputCallback != None ):
            self._inputCallback( inputData )
