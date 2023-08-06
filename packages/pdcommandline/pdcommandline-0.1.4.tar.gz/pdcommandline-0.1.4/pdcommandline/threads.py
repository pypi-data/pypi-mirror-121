from threading import *
from threading import Thread as _BaseThread
from . import exceptions



# registry of running threads
class ThreadRegistry:
    def __init__( self ):
        """
        Registry of threads
        """
        self._lock = RLock ()
        self._running = []
        self._shutdownFlag = False


    def register( self, thread ):
        """
        Registers a running thread
        """
        with self._lock:
            if( self._shutdownFlag == True ):
                thread.shutdown()
            self._running.append( thread )


    def unregister( self, thread ):
        """
        Unregisters a running thread
        """
        with self._lock:
            self._running.remove( thread )


    def shutdownAll( self, workersOnly: bool ):
        """
        Shut down all threads
        """
        with self._lock:
            self._shutdownFlag = True
            for thread in self._running:
                # shutdown worker threads
                try:
                    if( ( thread.daemon == False) or ( workersOnly == False ) ):
                        if( thread.shutdownRequested() == False ):
                            thread.shutdown()
                except:
                    pass


    def joinAll( self ):
        """
        Join all threads
        """
        while( True ):
            # iterate worker threads
            joinThread = None
            with self._lock:
                index = 0
                joinThread = None
                while( len( self._running ) > index ):
                    if( self._running[index].daemon == False ):
                        joinThread = self._running[index]
                        break
                    else:
                        index += 1
                if( joinThread == None ):
                    return

            # join worker thread
            try:
                joinThread.join ()
            except exceptions.TerminateException as t:
                # silently ignore
                pass
            except BaseException as e:
                exceptions.handle( e )

            # remove worker thread
            with self._lock:
                self._running.remove( joinThread )



# global registry of running threads
_globalThreadRegistry = ThreadRegistry ()



# thread base class
class Thread( _BaseThread ):
    def __init__( self, group=None, target=None, name=None,
                 args=(), kwargs=None, daemon=None ):
        """
        Monitored thread base class
        """
        _BaseThread.__init__( self, group = group, target = self._targetProxy, name = name, args = args, kwargs = kwargs, daemon = daemon )
        self._targetFunc = target
        self._shutdownFlag = False


    def shutdown( self ) -> None:
        """
        Shutdown running thread
        """
        self._shutdownFlag = True


    def shutdownRequested( self ) -> bool:
        """
        Check if shutdown flag is requested
        """
        return self._shutdownFlag


    def start( self ) -> None:
        """
        Start thread
        """
        self._onStart()
        return super().start()


    def _targetProxy( self ) -> None:
        """
        Proxy for run method
        """
        try:
            if( self._targetFunc != None ):
                self._targetFunc()
            self._onTerminate()
        except exceptions.TerminateException as t:
            # silently ignore
            self._onTerminate()
        except Exception as e:
            exceptions.handle( e )
            self._onTerminate()


    def _onStart( self ):
        """
        Called on thread start.
        """
        _globalThreadRegistry.register( self )


    def _onTerminate( self ):
        """
        Called on thread termination
        """
        _globalThreadRegistry.unregister( self )
