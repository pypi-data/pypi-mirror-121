import math
from . import _uiLock
from . import sstr




class Provider:
    def __init__( self ):
        self.printers = []
        self._lock = _uiLock


    def _bind( self, printer: object ):
        """
        Bind to a printer
        """
        with self._lock:
            self.printers.append( printer )


    def _unbind( self, printer: object ):
        """
        Unbind from a printer
        """
        with self._lock:
            newPrinters = []
            for p in self.printers:
                if( p != printer ):
                    newPrinters.append( p )
            self.printers = newPrinters


    def render( self, contentWidth: int, maxLines: int ):
        """
        Render text line for progress
        """
        assert False, "To be implemented by inherited class"


    def update( self ):
        """
        Update progress on bound printers
        """
        with self._lock:
            for printer in self.printers:
                printer._updateDynamicContent()




class DefaultProvider( Provider ):
    def __init__( self,
                  maxProgress: int,
                  initialProgress: int = 0,
                  style: object = None ):
        super().__init__( )
        self.maxProgress = maxProgress
        self.progress = initialProgress
        self.progressStyle = style


    def render( self, contentWidth: int, maxLines: int ):
        """
        Render text line for progress
        """
        with self._lock:
            # textual representation of progress
            maxProgressString = str ( self.maxProgress )
            doneString = str ( self.progress )
            while( len( doneString ) < len( maxProgressString ) ):
                doneString = " " + doneString
            progressString = doneString + " / " + maxProgressString

            # percentual representation of progress
            percent = math.floor( 100 * self.progress / self.maxProgress )
            if( percent < 0 ):
                percent = 0
            if( percent > 100 ):
                percent = 100
            percentString = str( percent ) + "%"
            while( len( percentString ) < 4 ):
                percentString = " " + percentString
            progressString += " (" + percentString + ")"

            # progress bar
            progressBarSize = contentWidth - len( progressString ) - 3
            if( progressBarSize > 0):
                progressSet = math.ceil( progressBarSize * self.progress / self.maxProgress )
                progressBarStr = ""
                for column in range( progressBarSize ):
                    if( column < progressSet ):
                        progressBarStr += "="
                    else:
                        progressBarStr += " "
                progressString = "[" + progressBarStr + "] " + progressString

            # return lines of progress
            progressString = sstr.SStr( progressString, style = self.progressStyle )
            return [progressString]


    def set( self, progress: int ):
        """
        Set progress an update view
        """
        with self._lock:
            self.progress = progress
            self.update ()
