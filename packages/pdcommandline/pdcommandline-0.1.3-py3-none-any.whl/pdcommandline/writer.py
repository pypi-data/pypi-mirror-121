import os
import sys
import math
import copy
from . import _uiLock
from . import sstr
from .formatter import *
from .loglevels import *
from .lifecycle import application
from pdcommandline import formatter

from pdcommandline import loglevels


# TODO: refresh output if console is shrinked / grown ?
# TODO: scroll terminal after removing progress? - eher net...




# cursor class for printer
class _Cursor:
    def __init__( self ):
        self.isApplied = False
        self.lineOffset = 0
        self.columnOffset = 0
        self.lastLineOffset = 0
        self.lastColumnOffset = 0


    def setPosition( self, lineOffest: int, column: int):
        self.lineOffset = lineOffest
        self.columnOffset = column


    def needsUpdate( self ):
        if( self.isApplied == False ):
            return True
        if( self.lineOffset != self.lastLineOffset ):
            return True
        if( self.columnOffset != self.columnOffset ):
            return True
        return False


    def remove( self ):
        if( self.isApplied ):
            self.isApplied = False
            if( self.lastLineOffset > 0 ):
                return sstr.SStr( "\x1B[" + str( self.lastLineOffset ) + "B" ).asLinear ()
        return sstr.LStr()


    def apply( self ):
        eStr = sstr.LStr()

        # need to remove before?
        if( self.isApplied ):
            eStr = self.remove()

        # set cursor row
        if( self.lineOffset > 0 ):
            eStr += sstr.SStr( "\x1B[" + str( self.lineOffset ) + "A" ).asLinear ()

        # set cursor column
        eStr += sstr.SStr( "\x1B[10000D" ).asLinear()
        if( self.columnOffset > 0 ):
            eStr += sstr.SStr( "\x1B[" + str( self.columnOffset ) + "C" ).asLinear()

        # store state information
        self.lastLineOffset = self.lineOffset
        self.lastColumnOffset = self.columnOffset
        self.isApplied = True
        return eStr




# printer writing to a file or console
class Printer:
    def __init__( self,
                  logfile: str            = None,       #< None: write to console, str: filename of output file
                  level: int              = None,
                  append: bool            = True,
                  maxWidth: int           = None,       #< None: auto width, 0: no line size limit, >0: max number of chars per line
                  forceShowProgress: bool = None,       #< None: output progress only on consoles, False for not showing progress, True for showing progress always
                  forceColorOutput: bool  = None,       #< None: color output on consoles only, False for non color output, True for showing color output always
                  maxProgressLines: int   = None,       #< None: limit progress lines by screen height, >=1: absolute limit of progress lines
                  lock: object            = None
                ):
        """
        Creates a new printer instance
        """
        self.logfile                      = logfile
        self.level                        = level if level != None else loglevels.LOG_DEFAULT
        self.maxWidth                     = maxWidth
        self.fileHandle                   = None
        self.isClosed                     = False
        self.progressProvider             = None
        self.progressProviderStack        = []
        self.dynamicContent               = None
        self.lastProgressContent          = None
        self.lastDynamicContent           = None
        self.forceShowProgress            = forceShowProgress
        self.forceColorOutput             = forceColorOutput
        self.maxProgressLines             = maxProgressLines
        self.cursorShown                  = True
        self.inputRenderer                = None
        self.cursor                       = _Cursor()
        self.isInitialized                = False

        self._lock = lock
        if( self._lock == None ):
            self._lock = _uiLock

        application.registerExitFunction( self.close )
        if( self.logfile != None ):
            try:
                self.fileHandle = open( logfile, 'a' if append == True else 'w' )
            except Exception as error:
                # can not open file for writing
                self.fileHandle = None
                self.isClosed   = True
                raise error


    def _initialize( self ):
        """
        Initialize output, must be called in locked state
        """
        if( self.isInitialized == True ):
            return
        self.isInitialized = True
        self._setShowCursor( False )


    def _uninitialize( self ):
        """
        Uninitialize output, must be called in locked state
        """
        if( self.isInitialized == True ):
            self._commitLastProgress()

            # clean up cursor state
            if( self._colorOutput() != True ):
                return
            self._writeRaw( self.cursor.remove(), end = '' )
            self._writeRaw( "\x1B[?25h \r", end = '' )


    def _commitLastProgress( self ):
        """
        Commit last progress to console
        """
        if( self.lastDynamicContent != None and len( self.lastDynamicContent ) > 0 ):
            self._removeDynamicContent( self._getMaxWidth(), self._getMaxProgressLines() )
            eStr = sstr.LStr()
            if( self.lastProgressContent != None ):
                for line in self.lastProgressContent:
                    eStr += sstr.SStr( line, '\n' ).asLinear ()
            self._writeRaw( eStr, end = '' )


    def close( self ):
        """
        Close output of printer
        """
        with self._lock:
            if( self.isClosed == False ):
                self._uninitialize()

                # close handle
                if( self.fileHandle != None ):
                    self.fileHandle.close()
                    application.unregisterExitFunction( self.close )
                self.isClosed = True


    def getTerminal( self ):
        """
        Returns self if attached to a terminal, returns None otherwise
        """
        if( self.fileHandle == None ):
            if( sys.stderr.isatty () ):
                return self
        return None


    def setInputRenderer( self, renderer ):
        """
        Set input renderer
        """
        with self._lock:
            self.inputRenderer = renderer
            if( renderer == None ):
                self._setShowCursor( False )
            else:
                self._setShowCursor( True )
        self._updateDynamicContent()


    def _colorOutput( self ):
        """
        Returns True if this output should be not colored
        """
        if( ( self.fileHandle == None ) and (sys.stderr.isatty() == True ) ):
            # write to console
            if( self.forceColorOutput == False ):
                return False
            else:
                return True
        else:
            # write to file
            if( self.forceColorOutput == True ):
                return True
            else:
                return False


    def _setShowCursor( self, state: bool ):
        """
        Set cursor show flag
        """
        with self._lock:
            if( self._colorOutput() != True ):
                return

            if( self.cursorShown != state):
                if( state != False ):
                    # show cursor
                    self._writeRaw( "\x1B[?25h", end = '' )
                else:
                    # hide cursor
                    self._writeRaw( self.cursor.remove(), end = '' )
                    self._writeRaw( "\x1B[?25l", end = '' )
                self.cursorShown = state
    

    def _writeRaw( self,
                   content: object,
                   end: str = '\n',
                   flush: bool = False ):
        """
        Write raw line to output
        """
        if isinstance( content, (sstr.SStr, sstr.LStr ) ):
            econtent = sstr.SStr( content, end )
            enc = econtent.encode( not self._colorOutput() )
        else:
            enc = str( content + end )
        
        if self.fileHandle == None:
            sys.stderr.write( enc )
            if( flush == True ):
                sys.stderr.flush()
        else:
                self.fileHandle.write( enc )
        

    def _write( self,
                lines: list,
                consoleWidth: int ):
        """
        Write some lines
        """
        assert self.isClosed == False, "Can not write already closed printer"

        # remove progress output
        consoleHeight = self._getMaxProgressLines()
        self._removeDynamicContent( consoleWidth, consoleHeight )

        # write lines to log
        for line in lines:
            self._writeRaw( sstr.SStr( line ).asLinear() )

        # update progress output
        self._updateDynamicContent( consoleWidth, consoleHeight )


    def write( self,
               content: object,
               level: int                     = None,
               limit: int                     = None,
               defaultStyle: object           = None,
               lineBreakSettings: object      = None,
               indent: str                    = None,
               firstLineBreakSettings: object = None,
               firstLineIndent: str           = None ):
        """
        Write tables, trees or text to the printer
        """
        with self._lock:
            # make sure output is initialized
            self._initialize()

            # check log level if this entry should be printed
            if( self._checkLevel( level, limit ) == False ):
                return

            # take current indentation into account
            consoleWidth = self._getMaxWidth()

            # compute formatted lines & write
            if( isinstance( content, (list, tuple) ) ):
                contentArray = content
            else:
                contentArray = [ content ]            
            if( firstLineIndent == None ):
                firstLineIndent = indent
            if( firstLineBreakSettings == None ):
                firstLineBreakSettings = lineBreakSettings
            lines = self._computeLines( contentArray, defaultStyle, lineBreakSettings, consoleWidth, indent, firstLineBreakSettings, firstLineIndent )
            self._write( lines, consoleWidth )


    def _computeLines( self, content, defaultStyle, lineBreakSettings, consoleWidth, indent, firstLineBreakSettings, firstLineIndent ):
        # compute max width
        maxWidth     = consoleWidth
        if maxWidth != None:
            if( indent != None ):
                maxWidth -= len( indent )
            if maxWidth < 1:
                maxWidth = 1

        # recurse on elements
        target = []
        for element in content:
            if( isinstance( element, formatter.ApplyDefaultStyle ) ):
                # apply default style for child elements
                if( element.style != None ):
                    newDefaultStyle = element.style.concrete( defaultStyle )
                else:
                    newDefaultStyle = defaultStyle
                target = target + self._computeLines( element.content, newDefaultStyle, lineBreakSettings, consoleWidth, indent, firstLineBreakSettings, firstLineIndent )

            elif( isinstance( element, formatter.ApplyLineBreakSettings ) ):
                # apply line break settings for child elements
                target = target + self._computeLines( element.content, defaultStyle, element.settings, consoleWidth, indent, firstLineBreakSettings, firstLineIndent )

            elif( isinstance( element, formatter.ApplyIndent ) ):
                # apply indentation for child elements
                if( indent == None ):
                    newIndent = element.indent
                else:
                    newIndent = sstr.SStr( indent, element.indent )
                target = target + self._computeLines( element.content, defaultStyle, lineBreakSettings, consoleWidth, newIndent, firstLineBreakSettings, firstLineIndent )

            else:
                # format content
                currentLines = []
                if( isinstance( element, ( str, sstr.SStr, sstr.LStr ) ) ):
                    if( defaultStyle != None ):
                        element = sstr.SStr( element, style = defaultStyle )
                    currentLines = self._formatString( element, maxWidth, firstLineBreakSettings )
                elif( isinstance( element, formatter.Layoutable ) ):
                    currentLines = element.format( maxWidth, defaultStyle, lineBreakSettings )
                else:
                    currentLines = self._formatString( sstr.SStr( element, style = defaultStyle ), maxWidth, firstLineBreakSettings )

                # apply indentation
                if( firstLineIndent != None ):
                    nLines = []
                    for line in currentLines:
                        nLines.append( sstr.SStr( firstLineIndent, line, style = defaultStyle ) )
                    currentLines = nLines
                target = target + currentLines
            
            # do not use first line indent and break settings anymore.
            firstLineIndent = indent
            firstLineBreakSettings = lineBreakSettings

        # return computed output lines
        return target


    def _detectMaxWidth( self ):
        """
        Detect console width
        """
        # write to file?
        if self.fileHandle != None:
            return None

        # redirected via pipe?
        if( sys.stderr.isatty() == False ):
            return None

        # check if we are running inside a console
        try:
            console = os.get_terminal_size()
        except:
            console = None

        # compute console width
        if( console == None ):
            return style.Defaults.getDefaultConsoleWidth()
        width = console[0]
        if( isinstance( width, ( int, float ) ) ):
            if( width > 0 ):
                return width
        return style.Defaults.getDefaultConsoleWidth() 


    def _getMaxWidth( self ):
        """
        Get maximum line width
        """
        if( self.maxWidth == None ):
            return self._detectMaxWidth()
        if( self.maxWidth == 0 ):
            return None
        return self.maxWidth


    def _formatString( self,
                       text: str,
                       maxWidth: int,
                       lineBreakSettings: object ):
        """
        Format text, return array of printable lines
        """
        # default line break settings
        followIndent  = 0
        newLineIndent = 0
        breakSequence = style.DEFAULT_BREAK_SEQUENCE
        noWordBreak   = True

        # line break settings set?
        if( lineBreakSettings != None ):
            followIndent  = lineBreakSettings.followIndent
            newLineIndent = lineBreakSettings.newLineIndent
            breakSequence = lineBreakSettings.breakSequence
            noWordBreak   = lineBreakSettings.noWordBreak

        # format text
        return TableUtils._splitContent( text,
                                         maxWidth,
                                         followIndent,
                                         newLineIndent,
                                         breakSequence,
                                         noWordBreak )


    def _checkLevel( self,
                     level: int,
                     limit: int ):
        """
        Check request level should be written
        """
        ownLevel = self.level
        if( ownLevel == None ):
            ownLevel = style.Defaults.getLogLevel()
        if( limit != None ):
            if( limit <= ownLevel ):
                return False
        if( level == None):
            return True
        if( level <= ownLevel ):
            return True
        return False


    def setProgressProvider( self,
                             progress,
                             keepLastProgress: bool = False ):
        """
        Set progress provider
        """
        with self._lock:
            # make sure output is initialized
            if( progress != None ):
                self._initialize()

            # set progress
            self.progressProviderStack.append( self.progressProvider )
            if( self.progressProvider != None ):
                self.progressProvider._unbind( self )
                if( keepLastProgress ):
                    self._commitLastProgress()
            self.progressProvider = progress
            if( self.progressProvider != None ):
                self.progressProvider._bind( self )
            if( self.isInitialized == True ):
                self._updateDynamicContent()


    def popProgressProvider( self ):
        """
        Restore progress provider
        """
        with self._lock:
            lastProvider = None
            if( len( self.progressProviderStack ) > 0 ):
                lastProvider = self.progressProviderStack[-1]
                self.progressProviderStack = self.progressProviderStack[:len( self.progressProviderStack) - 1]
            if( self.progressProvider != None ):
                self.progressProvider._unbind( self )
            self.progressProvider = lastProvider
            if( self.progressProvider != None ):
                self.progressProvider._bind( self )
            self._updateDynamicContent()


    def _getMaxProgressLines( self ):
        # output accepts colors?
        if( self._colorOutput() == False ):
            return 1

        # check if we are running inside a console
        try:
            console = os.get_terminal_size()
        except:
            console = None

        # compute progress height
        if( console == None ):
            return 1
        height = console[1]
        if( isinstance( height, ( int, float ) ) ):
            height = int( height ) - 1
            if( self.maxProgressLines != None and self.maxProgressLines > 0 ):
                if( height > self.maxProgressLines ):
                    height = self.maxProgressLines
            if( height > 0 ):
                return height
        return 1


    def _eraseDynamicContentStr( self, linesToErase: int ):
        """
        Remove last written progress line from output
        """
        eStr = sstr.LStr()
        eStr += self.cursor.remove()
        if( linesToErase == 0 ):
            return eStr
        if( linesToErase > 1 ):
            # go to begin of progress output
            eStr += sstr.SStr( "\x1B[10000D" ).asLinear()
            eStr += sstr.SStr( "\x1B[" + str( linesToErase - 1 ) + "A" ).asLinear()

            # clear lines
            eStr += sstr.SStr( "\x1B[2K" ).asLinear()
            for i in range( 1, linesToErase ):
                eStr += sstr.SStr( "\x1B[1B" + "\x1B[2K" ).asLinear()

            # return to line after dynamic content
            eStr += sstr.SStr( "\x1B[" + str( linesToErase - 1 ) + "A" ).asLinear()

        else:
            clear = " " * len( self.lastDynamicContent[0] )
            eStr += sstr.SStr( '\r' + clear + '\r' ).asLinear()
        return eStr


    def _removeDynamicContent( self, consoleWidth: int, consoleHeight: int ):
        """
        Remove last written progress line from output
        """
        # calculate number of lines to remove
        linesToErase = 0
        if( self.lastDynamicContent != None ):
            linesToErase = len( self.lastDynamicContent )
            # remove dynamic content
            self._writeRaw( self._eraseDynamicContentStr( linesToErase ), end = '' )
            self.lastDynamicContent = None


    def _collectDynamicContent( self, consoleWidth: int, consoleHeight: int ):
        """
        Collects the dynamic output
        """
        # abort if progress output is disabled for this printer
        if( self.forceShowProgress == False):
            return ( [], 0, 0 )

        # calculate progress width, abort if not forced and not on terminal
        progressWidth = consoleWidth
        if( progressWidth == None ):
            if( self.forceShowProgress == True ):
                progressWidth = style.Defaults.getDefaultProgressWidth()
            else:
                return ( [], 0, 0 )

        # render input view
        maxInputLines = consoleHeight - 1
        iLines = []
        iLine = 0
        cursorColOffset = 0
        inputBeforeProgress = True
        if( self.inputRenderer != None ):
            inputBeforeProgress = self.inputRenderer.renderSettings.beforeProgress
            (iLines, iLine, cursorColOffset) = self.inputRenderer.render( progressWidth )

        # limit number of input lines
        while( len( iLines ) > maxInputLines ):
            iLines = iLines[1:]
            if( iLine > 1 ):
                iLine -= 1

        # render progress
        self.lastProgressContent = []
        if( self.progressProvider != None ):
            maxProgressLines = maxInputLines - len( iLines )
            if( maxProgressLines > 0 ):
                lines = self.progressProvider.render( progressWidth, maxProgressLines )
                for line in lines:
                    if( not isinstance( line, (sstr.SStr, sstr.LStr ) ) ):
                        self.lastProgressContent.append( sstr.SStr( line ) )
                    else:
                        self.lastProgressContent.append( line )

        # calculate cursor line offset
        cursorLineOffest = len( iLines ) - 1 - iLine

        # merge input lines + progress lines, calculate cursor row offset
        if( inputBeforeProgress ):
            mergedLines = iLines + self.lastProgressContent
            cursorLineOffest += len( self.lastProgressContent )
        else:
            mergedLines = self.lastProgressContent + iLines

        # return dynamic lines
        return ( mergedLines, cursorLineOffest, cursorColOffset )


    def _dynamicContentStr( self ):
        """
        Write dynmic content
        """
        if( self.dynamicContent == None ):
            return sstr.SStr( "" ).asLinear()
        eStr = sstr.SStr( "" ).asLinear()
        for pli in range( len( self.dynamicContent ) ):
            pl = self.dynamicContent[pli]
            if( pli == ( len( self.dynamicContent ) - 1 ) ):
                eStr += sstr.SStr( pl ).asLinear()
            else:
                eStr += sstr.SStr( pl, "\n" ).asLinear()
        return eStr


    def _updateDynamicContentStr( self ):
        """
        Update last written progress line from output
        """
        eStr = self.cursor.remove()
        if( self.lastDynamicContent != None ):
            if( len( self.lastDynamicContent ) == 0 ):
                # got no old dynamic content, add new one
                eStr += self._dynamicContentStr()
                return eStr

            if( len( self.lastDynamicContent ) > 1 ):
                linesToErase = len( self.lastDynamicContent )
                # go to begin of progress output
                eStr += sstr.SStr( "\x1B[10000D" ).asLinear()
                if( linesToErase > 1 ):
                    eStr += sstr.SStr( "\x1B[" + str( linesToErase - 1 ) + "A" ).asLinear ()

                # update lines
                lineId = 0
                if( self.dynamicContent != None ):
                    for line in self.dynamicContent:
                        content = sstr.SStr( line )
                        lastLen = len( self.lastDynamicContent[lineId] ) if len( self.lastDynamicContent ) > lineId else 0
                        contentLeft = lastLen - len( content )
                        content = sstr.SStr( content, " " * contentLeft )
                        eStr += content.asLinear()
                        lineId += 1
                        if( lineId < len( self.dynamicContent ) ):
                            eStr += sstr.SStr( '\n' ).asLinear()
                        linesToErase -= 1

                # clear remaining lines
                for i in range( linesToErase ):
                    eStr += sstr.SStr( "\x1B[1B" + "\x1B[2K" ).asLinear ()

                # return to line after dynamic content
                if( linesToErase > 0 ):
                    eStr += sstr.SStr( "\x1B[" + str( linesToErase ) + "A" ).asLinear()

            else:
                # clear single line
                content = ""
                if( self.dynamicContent != None and len( self.dynamicContent ) > 0 ):
                    content = self.dynamicContent[0]
                contentLeft = len( self.lastDynamicContent[0] ) - len( content )
                content = sstr.SStr( '\r', content, " " * contentLeft, '\r' )
                eStr += content.asLinear()
                
                # write more lines of dynamic content
                if( self.dynamicContent != None ):
                    for lid in range( 1, len( self.dynamicContent ) ):
                        eStr += sstr.SStr( '\n', self.dynamicContent[lid] ).asLinear ()
        else:
            # got no old dynamic content, add new one
            eStr += self._dynamicContentStr()

        if( self.cursorShown == True):
            eStr += self.cursor.apply()
        return eStr


    def _updateDynamicContent( self, consoleWidth: int = None, consoleHeight: int = None ):
        """
        Updates the dynamic content
        """
        # get current console layout
        if( consoleWidth == None ):
            consoleWidth = self._getMaxWidth()
        if( consoleHeight == None ):
            consoleHeight = self._getMaxProgressLines()

        # update dynamic content
        with self._lock:
            # collect dynamic content
            ( self.dynamicContent, cursorLineOffset, cursorColOffset ) = self._collectDynamicContent( consoleWidth, consoleHeight )

            # set cursor position
            self.cursor.setPosition( cursorLineOffset, cursorColOffset )

            # surpress update if content did not change
            if( self.dynamicContent == None and self.lastDynamicContent == None ):
                return

            # check for changes
            if( self.dynamicContent != None and self.lastDynamicContent != None ) and ( len( self.dynamicContent ) == len( self.lastDynamicContent ) ):
                noChange = True
                if( self.cursorShown == True ):
                    if( self.cursor.needsUpdate() ):
                        noChange = False
                if( noChange == True ):
                    for lid in range( len( self.dynamicContent ) ):
                        if( self.dynamicContent[lid].asLinear().encode() != self.lastDynamicContent[lid].asLinear().encode() ):
                            noChange = False
                            break;
                if( noChange == True ):
                    return

            # update content
            es = self._updateDynamicContentStr()
            self.lastDynamicContent = self.dynamicContent
            self._writeRaw( es, end = '', flush = True )


    def __call__( self, *args, **kwargs ):
        """
        Shortcut for printing to the log
        """
        with self._lock:
            self.write (*args, **kwargs)




class _PrinterOutputfileScope:
    def __init__( self,
                  tee: object,
                  logfile: str,
                  level: int,
                  append: bool,
                  maxWidth: int ):
        """
        Scope helper to add an additional output file
        """
        self.tee      = tee
        self.logfile  = logfile
        self.level    = level
        self.append   = append
        self.printer  = None
        self.maxWidth = maxWidth


    def __enter__( self ):
        assert self.printer == None, "Scope must not be used twice"
        self.printer = Printer ( self.logfile,
                                 self.level,
                                 self.append,
                                 self.maxWidth )
        self.tee.addPrinter( self.printer )
        return self.printer


    def __exit__( self,
                  type,
                  value,
                  traceback ):
        self.tee.removePrinter( self.printer )
        self.printer.close()
        self.printer = None
        return False




class Tee:
    def __init__( self, printers: list = None, lock: object = None ):
        """
        Tee instance for writing to multiple printers
        """
        self._lock = lock
        if( self._lock == None ):
            self._lock = _uiLock

        self.printers = []
        self.progressProvider = None
        if not printers is None:
            for printer in printers:
                self.addPrinter( printer )

    def addPrinter( self,
                    printer ):
        """
        Add a printer
        """
        with self._lock:
            self.printers.append( printer )
            printer.setProgressProvider( self.progressProvider, False )


    def removePrinter( self,
                       printer ):
        """
        Remove a printer
        """
        with self._lock:
            printers = []
            for p in self.printers:
                if( p != printer ):
                    printers.append( p )
                else:
                    p.popProgressProvider()
            self.printers = printers


    def additionalOutput( self,
                          logfile: str,
                          level: int    = None,
                          append: bool  = True,
                          maxWidth: int = None ):
        """
        Add an output file (scope based)
        """
        return _PrinterOutputfileScope( self,
                                        logfile,
                                        level,
                                        append,
                                        maxWidth )


    def close( self ):
        """
        Close output of printer
        """
        with self._lock:
            for printer in self.printers:
                printer.close()


    def write( self,
               content: object,
               level: int                     = None,
               limit: int                     = None,
               defaultStyle: object           = None,
               lineBreakSettings: object      = None,
               indent: str                    = None,
               firstLineBreakSettings: object = None,
               firstLineIndent: str           = None ):
        """
        Write tables, trees or text to the printer
        """
        with self._lock:
            for printer in self.printers:
                printer.write( content,
                               level,
                               limit,
                               defaultStyle,
                               lineBreakSettings,
                               indent,
                               firstLineBreakSettings,
                               firstLineIndent )


    def setProgressProvider( self,
                             progress,
                             keepLastProgress: bool = False ):
        """
        Set progress provider
        """
        with self._lock:
            for printer in self.printers:
                printer.setProgressProvider( progress, keepLastProgress )
            self.progressProvider = progress


    def getTerminal( self ):
        """
        Returns the terminal writer instance or None if we are not on a tty.
        """
        with self._lock:
            for printer in self.printers:
                term = printer.getTerminal()
                if( term != None ):
                    return term
        return None


    def __call__( self, *args, **kwargs ):
        """
        Shortcut for printing to the log
        """
        with self._lock:
            self.write (*args, **kwargs)
