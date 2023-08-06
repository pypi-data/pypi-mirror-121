import os
import signal
import atexit
import _thread
from .threads import RLock
from .threads import _globalThreadRegistry
from . import exceptions



# default exit code for unhandled exceptions
defaultExitCodeOnException   = 250
defaultCloseInputOnException = True



# application object
class _Application:
    def __init__( self ):
        """
        Wrapper for running command line applications
        """
        self._exitCodeOnException   = defaultExitCodeOnException
        self._closeInputOnException = defaultCloseInputOnException


    def addShutdownHook( self, hook ):
        """
        Add shut down hook function,
        Hook needs to be a function: "hook( terminate: bool ) -> bool", when True is returned, the shutdown will be ignored.
        Parameter "terminate" is true if application should be terminated immediately, False if application is interrupted (p.e. Ctrl + C).
        """
        _lifecycle.addShutdownHook( hook )


    def removeShutdownHook( self, hook ):
        """
        Removes a shutdown hook function
        """
        _lifecycle.removeShutdownHook( hook )


    def addShutdownListener( self, listener ):
        """
        Adds a shutdown listener function.
        Gets called when the shutdown of the application is performed (i.e. when all shutdown hooks are processed).
        Listener need to be a function: "listener( ) -> None"
        """
        _lifecycle.addShutdownListener( listener )


    def removeShutdownListener( self, listener ):
        """
        Removes a shutdown listener function
        """
        _lifecycle.removeShutdownListener( listener )


    def registerExitFunction( self, exit ):
        """
        Registers an at exit function. Exit functions will be called after shutdown listeners.
        An exit function need to be a function: "exit( ) -> None"
        """
        _lifecycle.registerExitFunction( exit )


    def unregisterExitFunction( self, exit ):
        """
        Un-registers an at exit function
        """
        _lifecycle.unregisterExitFunction( exit )


    def setExitCode( self, code ):
        """
        Sets the exit code of the application
        """
        _lifecycle._exitCode = code


    def getExitCode( self ):
        """
        Gets the current exit code of the application
        """
        return _lifecycle._exitCode


    def terminate( self, exitCode: int = None ):
        """
        Shuts down the application and terminates the current thread immediately.
        Sets the shutdown flag of other threads and waits until they are finished.

        Should only be called from main thread.
        """
        if( exitCode != None ):
            _lifecycle._exitCode = exitCode
        _lifecycle.setShutdownFlag()
        _lifecycle.shutdownWorkers()
        raise exceptions.TerminateException()


    def shutdown( self, exitCode: int = None ):
        """
        Shuts down the application.
        Sets the shutdown flag on all threads.
        """
        if( exitCode != None ):
            _lifecycle._exitCode = exitCode
        _lifecycle.fireShutdownListeners()
        _lifecycle.setShutdownFlag()
        _lifecycle.shutdownWorkers()


    def isShutdown( self ):
        """
        Returns true if CTRL+C was pressed and no hook intercepted the shutdown or when terminate(), shutdown() was called
        """
        return _lifecycle._shutdownFlag


    def shutdownOnException( self, errorCode: int = 250 ):
        """
        Sets the shutdown behaviour of the application on unhandled exception.
        When errorCode is None, the application will not shut down, otherwise it will shut down with the errorCode set.
        Default is "defaultExitCodeOnException".
        """
        self._errorCodeOnException = errorCode

    
    def closeInputOnException( self, value: bool ):
        """
        Abort input queries when an exception is thrown?
        Default is "defaultCloseInputOnException".
        """
        self.closeInputOnException = value


    def _setInputWorker( self, worker ):
        """
        Set input worker instance
        """
        _lifecycle._inputWorker = worker


    def _handleExceptionShutdown( self ):
        """
        Handle shutdown request from exception handler
        """
        if( self._exitCodeOnException != None ):
            self.shutdown( self._exitCodeOnException )


    def _closeInputFromException( self ):
        """
        Execption handler request input to be closed.
        """
        if( self._closeInputOnException == True ):
            from . import input_provider
            if( input_provider._rawInput != None ):
                input_provider._rawInput.close()


# application singleton
application = _Application()



# life cycle handler class
class _Lifecycle:
    def __init__( self ):
        """
        Shutdown handler for command line application
        """
        self._lock = RLock()
        self._hooks = []
        self._exitFunctions = []
        self._shutdownListeners = []
        self._exitPerformed = False
        self._blockSignals = False
        self._inputWorker = None
        self._shutdownFlag = False

        # application return code
        self._exitCode = 0

        # register signal handlers
        atexit.register( _Lifecycle._atExit )
        signal.signal( signal.SIGINT, _Lifecycle._signalInterrupt )
        signal.signal( signal.SIGTERM, _Lifecycle._signalShutdown )


    def setShutdownFlag( self ):
        """
        Set shutdown flag
        """
        self._shutdownFlag = True


    def addShutdownHook( self, hook ):
        """
        Add shut down hook function,
        hook needs to be a function: "hook( terminate: bool ) -> bool", when True is returned, the shutdown will be ignored.
        """
        with self._lock:
            self._hooks.append( hook )


    def removeShutdownHook( self, hook ):
        """
        Removes a shutdown hook function
        """
        with self._lock:
            assert hook in self._hooks, "hook is not installed"
            self._hooks.remove( hook )


    def addShutdownListener( self, listener ):
        """
        Adds a shutdown listener
        """
        with self._lock:
            self._shutdownListeners.append( listener )
            


    def removeShutdownListener( self, listener ):
        """
        Removes a shutdown listener
        """
        with self._lock:
            assert listener in self._shutdownListeners, "shutdown listener is not installed"
            self._shutdownListeners.remove( listener )


    def registerExitFunction( self, function ):
        """
        Registers an at exit function
        """
        with self._lock:
            if( self._exitPerformed == True ):
                function()
            if not function in self._exitFunctions:
                self._exitFunctions.append( function )


    def unregisterExitFunction( self, function ):
        """
        Registers an at exit function
        """
        with self._lock:
            if( self._exitPerformed == True ):
                return
            assert function in self._exitFunctions, "exit function is not installed"
            self._exitFunctions.remove( function )


    def shutdownWorkers( self ):
        """
        Send shut down to all worker threads
        """
        _globalThreadRegistry.shutdownAll( True )
        

    def fireShutdownListeners( self ):
        """
        Fire the shutdown listeners.
        """
        while True:
            with self._lock:
                shutdownListeners = self._shutdownListeners
                self._shutdownListeners = []
                if( len( shutdownListeners ) < 1 ):
                    return
            for listener in shutdownListeners:
                listener()


    def waitForWorkers( self ):
        """
        Wait for application to be shut down
        """
        # wait for worker threads to be shut down
        while( True ):
            try:
                _globalThreadRegistry.joinAll()
            except KeyboardInterrupt as k:
                # silently ignore keyboard interrupts
                pass
            except BaseException as e:
                exceptions.handle( e )
            finally:
                break


    @staticmethod
    def _atExit():
        _lifecycle.fireShutdownListeners()
        _lifecycle._runExitHandlers()


    @staticmethod
    def _signalInterrupt( signum, frame ):
        with _lifecycle._lock:
            if( _lifecycle._blockSignals ):
                return
        _lifecycle._signalShutdown( False )


    @staticmethod
    def _signalTerminate( signum, frame ):
        with _lifecycle._lock:
            if( _lifecycle._blockSignals ):
                return
        _lifecycle._signalShutdown( True )


    def _signalShutdown( self, terminate: bool ):
        """
        On shutdown signal
        """
        # send abort to keyboard input thread
        with self._lock:
            if( self._inputWorker != None ):
                self._inputWorker.abort()

        # execute shut down hooks
        with self._lock:
            if( self._exitPerformed == True ):
                return
            for hook in reversed( self._hooks ):
                if( hook( terminate ) == True ):
                    return

        # block signal handlers
        with self._lock:
            self._blockSignals = True

        # set shutdown flag
        self.setShutdownFlag()

        # shutdown all worker threads
        _globalThreadRegistry.shutdownAll( True )

        # raise keyboard interrupt exception to main thread
        _thread.interrupt_main()


    def _runExitHandlers( self ):
        """
        Run exit handlers
        """
        # only run once
        with self._lock:
            if( self._exitPerformed == True ):
                return
            self._exitPerformed = True

        # shutdown and join threads
        _globalThreadRegistry.shutdownAll( True )
        _globalThreadRegistry.joinAll()
        _globalThreadRegistry.shutdownAll( False )

        # run exit handlers
        with self._lock:
            for handler in self._exitFunctions:
                handler ()

        # return exit code
        os._exit( self._exitCode )

# single instance
_lifecycle = _Lifecycle()