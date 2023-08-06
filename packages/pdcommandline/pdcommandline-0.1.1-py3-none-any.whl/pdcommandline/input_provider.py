from os import EX_CANTCREAT
import sys
from pdcommandline import input_event, threads
from . import sstr
from . import console
from . import _uiLock
from . import style
from .formatter import TableUtils


# TODO: when line overflow and exception is shown, rest of input line is displayed


# try to load platform dependent raw input module
_rawInput = None
if( sys.stdin.isatty() ):
    import platform
    if platform.system().lower() == 'windows':
        from . import input_windows as _rawInputModule
        _rawInput = _rawInputModule.RawInput()
    else:
        from . import input_posix as _rawInputModule
        _rawInput = _rawInputModule.RawInput()



# default value
class _Default:
    pass



# rendering settings for input data
class InputRendererSettings:
    def __init__( self, wordWrap: bool = _Default, beforeProgress: bool = _Default, linePrefix: str = _Default, firstLinePrefix: str = _Default ):
        # get defaults from style
        s = style.Defaults.getInputQueryStyle()

        # derive from default style
        self.wordWrap       = wordWrap        if wordWrap != _Default        else s.wordWrap
        self.firstPrefix    = firstLinePrefix if firstLinePrefix != _Default else s.firstPrefix
        self.followPrefix   = linePrefix      if linePrefix != _Default      else s.followPrefix
        self.beforeProgress = beforeProgress  if beforeProgress != _Default  else s.beforeProgress



# input display renderer
class _InputRenderer:
    def __init__( self, terminal, editor, renderSettings ):
        """
        Input text display
        """
        self.terminal = terminal
        self.editor = editor
        self.renderSettings = renderSettings


    def render( self, terminalWidth: int ):
        """
        Renders the input display, returns a tuple (lines, cursorLine, cursorColumn)
        """
        # get text and cursor position from editor
        with self.editor.lock:
            text, cursorPos = self.editor._getRenderData()

        # get rendering style
        firstPrefix  = self.renderSettings.firstPrefix
        followPrefix = self.renderSettings.followPrefix
        wordWrap     = self.renderSettings.wordWrap

        # calculate follow prefix
        followIndent = 0
        if( followPrefix != None ):
            followIndent = len( followPrefix )
            if( firstPrefix == None ):
                firstPrefix = followPrefix

        # add cursor position anchor ( "\x06" )
        if( cursorPos < 1 ):
            text = sstr.SStr( "\x06", text ).asLinear()
        elif( cursorPos >= len( text ) ):
            text = sstr.SStr( text, "\x06" ).asLinear()
        else:
            tt = sstr.SStr( text ).asLinear()
            t1 = tt.substring( 0, cursorPos )
            t2 = tt.substring( cursorPos, len( text ) )
            text = sstr.SStr( t1, "\x06", t2 ).asLinear()

        # prefix first line?
        if( firstPrefix != None ):
            text = sstr.SStr( firstPrefix, text ).asLinear()

        # split into lines
        outLines = []
        if( wordWrap == True ):
            # split text with word wrap
            breakSequence = style.DEFAULT_BREAK_SEQUENCE
            outLines = TableUtils._splitContent( text,
                                                 terminalWidth,
                                                 followIndent,
                                                 followIndent,
                                                 breakSequence,
                                                 True,
                                                 True )
        else:
            # split without word wrap
            line = sstr.LStr()
            lineSize = 0
            for index in range( len( text ) ):
                c = text.getCharAt( index )
                if( c.content == "\x06" ):
                    # process anchor
                    line += sstr.LStr( c )
                else:
                    # process visible character
                    if( lineSize == ( terminalWidth ) ):
                        outLines.append( line )
                        line = sstr.SStr( " " * followIndent ).asLinear()
                        lineSize = followIndent
                    line += sstr.LStr( c )
                    lineSize += 1
            if( len( line ) > 0 ):
                outLines.append( line )

        # filter output lines ( remove cursor position anchor "\x06" )
        filteredLines = []
        cursorLine = 0
        cursorCol = 0
        currentLine = 0
        for l in outLines:
            sl = sstr.SStr( l ).asLinear()
            foundColumn = None
            for index in range( 0, len( sl ) ):
                c = sl.getCharAt( index ).content
                if( c == "\x06" ):
                    foundColumn = index
                    break
            if( foundColumn != None ):
                if( foundColumn == 0 ):
                    nl = sl.substring( 1, len( sl ) )
                elif( foundColumn == ( len( sl ) - 1 ) ):
                    nl = sl.substring( 0, len( sl ) -1 )
                else:
                    t1 = sl.substring( 0, foundColumn )
                    t2 = sl.substring( foundColumn + 1, len( sl ) )
                    nl = sstr.SStr( t1, t2 ).asLinear()
                cursorCol = foundColumn
                cursorLine = currentLine
                filteredLines.append( nl )
            else:
                filteredLines.append( sl )
            currentLine += 1

        # need to move cursor to next line? add line?
        if( cursorCol == terminalWidth ):
            cursorCol = followIndent
            cursorLine += 1
        if( len( filteredLines ) <= cursorLine ):
            filteredLines.append( sstr.SStr( " " * followIndent ).asLinear() )

        # replace follow indent on input data
        if( followIndent > 0):
            for index in range( 1, len( filteredLines ) ):
                l = filteredLines[ index ]
                l = l.substring( followIndent, len( l ) )
                filteredLines[index] = sstr.SStr( followPrefix, l ).asLinear()

        # return rendered input data
        return(
            filteredLines,
            cursorLine,
            cursorCol
        )


    def update( self ):
        """
        Redraw terminal output
        """
        self.terminal._updateDynamicContent()



# editor for input query (base class)
class _InputEditorBase:
    def __init__( self ):
        self.inputProvider = None
        self.renderer = None
        self.question = None
        self.value = ""
        self.cursorPosition = 0
        self.lock = _uiLock


    def _updateRendering( self ):
        """
        Updates the attached view
        """
        if( self.renderer != None ):
            self.renderer.update()


    def _getRenderData( self ):
        text = sstr.SStr( self.question, self.value )
        cursorPos = self.cursorPosition + len( self.question )
        return( text, cursorPos )


    def _setRenderer( self, renderer ):
        """
        Register renderer
        """
        self.renderer = renderer
        self._updateRendering()


    def toggleInsertMode( self ):
        if( self.inputProvider != None ):
            self.inputProvider.insertMode = not self.inputProvider.insertMode


    def getInsertMode( self ):
        if( self.inputProvider != None ):
            return self.inputProvider.insertMode
        return True


    def _setContext( self, inputProvider, question, initialValue, initialCursorPos ):
        """
        Set editor context
        """
        self.inputProvider = inputProvider
        self.question = question
        self.value = initialValue if initialValue != None else ""
        self.cursorPosition = initialCursorPos if initialCursorPos != None else len( self.value )
        self._updateRendering()



# editor for input query
class _InputEditor( _InputEditorBase ):
    def __init__( self ):
        _InputEditorBase.__init__( self )


    def insert( self, position, char ):
        """
        Insert a character at a given position
        """
        if( position < 1 ):
            self.value = char + str( self.value )
        elif( position >= len( self.value ) ):
            self.value = str( self.value ) + char
        else:
            s = str( self.value )
            s1 = s[0:position]
            s2 = s[position:]
            self.value = s1 + char + s2
        self._updateRendering()


    def override( self, position, char ):
        """
        Override data at position
        """
        if( position < 0):
            return
        s = str( self.value )
        if( position >= len( s ) ):
            self.value = s + char
        else:
            s1 = s[0:position]
            s2 = s[position + 1:]
            self.value = s1 + char + s2
        self._updateRendering()


    def remove( self, position ):
        """
        Remove a character at a position
        """
        if( ( position < 0 ) or ( position >= len( self.value ) ) ):
            return
        s = str( self.value )
        if( position == 0 ):
            self.value = s[1:]
        else:
            s1 = s[0:position]
            s2 = s[position + 1:]
            self.value = s1 + s2
        self._updateRendering()


    def onKeyEvent( self, event ):
        """
        Process key event, returns a tuple (continueProcessing: bool, processedKey: bool, result: Alternative[str, None])
        """
        # commit value if enter is presses
        if( event.key == input_event.keyEnter ):
            if( ( input_event.modAlt in event.modifiers ) or ( input_event.modControl in event.modifiers ) ):
                self.insert( self.cursorPosition, '\n' )
                self.cursorPosition += 1
                return( True, True, self.value )
            else:
                return( False, True, self.value )
        
        # abort on escape
        if( event.key == input_event.keyEscape ):
            return( False, True, None )

        # move cursor
        if( event.key == input_event.keyLeft ):
            if( self.cursorPosition > 0 ):
                self.cursorPosition -= 1
                self._updateRendering()
                return( True, True, self.value )

        if( event.key == input_event.keyRight ):
            if( self.cursorPosition < len( self.value ) ):
                self.cursorPosition += 1
                self._updateRendering()
                return( True, True, self.value )

        if( event.key == input_event.keyHome ):
            self.cursorPosition = 0
            self._updateRendering()
            return( True, True, self.value )

        if( event.key == input_event.keyEnd ):
            self.cursorPosition = len( self.value )
            self._updateRendering()
            return( True, True, self.value )

        # delete / backspace
        if( event.key == input_event.keyDelete ):
            self.remove( self.cursorPosition )
            return( True, True, self.value )

        if( event.key == input_event.keyBackspace ):
            self.remove( self.cursorPosition - 1 )
            if( self.cursorPosition > 0 ):
                self.cursorPosition -= 1
            return( True, True, self.value )

        # toggle insert mode
        if( event.key == input_event.keyInsert ):
            self.toggleInsertMode()
            return( True, True, self.value )

        # insert data
        if( event.data != None ):
            if( self.getInsertMode() ):
                self.insert( self.cursorPosition, event.data )
            else:
                self.override( self.cursorPosition, event.data )
            self.cursorPosition += 1
            return( True, True, self.value )

        # unrecognized key - ignore and continue parsing
        return (True, False, self.value)



# text input manager
class _Input:
    def __init__( self ):
        """
        Console input driver
        """
        # check if stdin is attached to a console
        self._rawInput = _rawInput

        # init platform dependent raw input module
        if( self._rawInput != None ):
            self._rawInput.init( self._onInput )

        # input event queue
        self._inputEventsLock = threads.RLock()
        self._inputEvents = []
        self._inputWait = threads.Semaphore( 0 )
        self._isClosed = False

        # query lock
        self._queryLock = threads.RLock()

        # insert state
        self.insertMode = True


    def available( self ):
        """
        Returns true if console input is available
        """
        return self._rawInput != None


    def __call__( self,
               question: str,
               initialValue: str = None,
               initialCursorPos: int = None,
               editor: object = None,
               renderSettings: object = None,
               echo: bool = True
             ) -> str:
        return self.query(
            question,
            initialValue,
            initialCursorPos,
            editor,
            renderSettings,
            echo
        )


    def query( self,
               question: str,
               initialValue: str = None,
               initialCursorPos: int = None,
               editor: object = None,
               renderSettings: object = None,
               echo: bool = True
             ) -> str:
        """
        Ask a question on default terminal.
        """
        # lock query to be only accessable by one thread
        with self._queryLock:

            # return None if console is not available
            if( self.available() == False ):
                return None

            # return None if input is closed
            if( self._isClosed == True ):
                return None

            # get terminal
            terminal = console.getTerminal()
            if( terminal == None ):
                return None

            # need to create an editor?
            if( editor == None ):
                editor = _InputEditor( )

            # need to create render settings?
            if( renderSettings == None ):
                renderSettings = InputRendererSettings()

            # set initial value
            if( initialValue == None ):
                initialValue = ""

            # calculate initial cursor position
            if( initialCursorPos == None ):
                initialCursorPos = len( initialValue )

            # set context of editor
            editor._setContext( self, question, initialValue, initialCursorPos )

            # attach view renderer
            renderer = _InputRenderer( terminal, editor, renderSettings )
            editor._setRenderer( renderer )
            terminal.setInputRenderer( renderer )

            # remove input events occured before query
            self._flushInput()

            # push input events to editor
            editorContinue = True
            editorResult = None
            while( editorContinue ):
                event = self._waitForInputEvent()

                # abort on CTRL+C and close of input pipe
                if( ( event.key == input_event.abort ) or ( event.key == input_event.inputClosed ) ):
                    editorResult = None
                    break

                # process key evebt
                (wantContinue, processedKey, result) = editor.onKeyEvent( event )
                editorContinue = wantContinue
                editorResult = result

            # release view renderer
            editor._setRenderer( None )
            terminal.setInputRenderer( None )

            # echo to consoles
            if( echo == True ):
                if( editorResult != None ):
                    renderData, cursorPos = editor._getRenderData( )
                    console( renderData )

            # return result
            return editorResult
    

    def _flushInput( self ):
        """
        Remove all characters from input buffer
        """
        with self._inputEventsLock:
            self._inputEvents = []


    def _waitForInputEvent( self ):
        """
        Wait for an input event and return it
        """
        while( True ):
            with self._inputEventsLock:
                if( len( self._inputEvents ) > 0 ):
                    event = self._inputEvents[0]
                    self._inputEvents = self._inputEvents[1:]
                    return event
            self._inputWait.acquire()


    def _onInput( self, inputEvent ):
        """
        Process an input event
        """
        with self._inputEventsLock:
            if( inputEvent.key == input_event.inputClosed ):
                self._isClosed = True
            self._inputEvents.append( inputEvent )
        self._inputWait.release()
