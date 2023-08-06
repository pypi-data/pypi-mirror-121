from . import console
from . import threads
import time


# general input events
unknown             = "unknown"
inputClosed         = "closed"
abort               = "abort"

# special keys
keyBackspace        = "backspace"
keyDelete           = "del"
keyTab              = "tab"
keyEscape           = "escape"
keyEnter            = "enter"
keyControlEnter     = "ctrlenter"
keyInsert           = "insert"
keySelect           = "select"
keyHome             = "home"
keyEnd              = "end"
keyPageUp           = "pageup"
keyPageDown         = "pagedown"

keyUp               = "up"
keyDown             = "down"
keyLeft             = "left"
keyRight            = "right"

keyF1               = "F1"
keyF2               = "F2"
keyF3               = "F3"
keyF4               = "F4"
keyF5               = "F5"
keyF6               = "F6"
keyF7               = "F7"
keyF8               = "F8"
keyF9               = "F9"
keyF10              = "F10"
keyF11              = "F11"
keyF12              = "F12"
keyF13              = "F13"
keyF14              = "F14"
keyF15              = "F15"
keyF16              = "F16"
keyF17              = "F17"
keyF18              = "F18"
keyF19              = "F19"
keyF20              = "F20"

# modifiers
modShift            = "shift"
modAlt              = "alt"
modControl          = "control"



class InputEvent:
    def __init__( self, data, key, modifiers = None ):
        self.key = key
        self.data = data
        self.modifiers = modifiers if modifiers != None else []

    def __str__( self ):
        if( self.key != None ):
            return "InputEvent( key = " + self.key + ", modifiers = " + str( self.modifiers ) + " )"
        else:
            return "InputEvent( data = '" + self.data + "', modifiers = " + str( self.modifiers ) + " )"



class InputEscapeTimeout( threads.Thread ):
    def __init__( self, parser ):
        """
        Creates a new escape timeout worker
        """
        threads.Thread.__init__( self, target = self.work, name = "Input Escape Timeout", daemon = True )
        self.semaphore = threads.Semaphore()
        self.lock = threads.Lock()
        self.parser = parser
        self.fireTime = None


    def armTimer( self, timeout: float ):
        """
        Arm timer to fire once after a timeout. When timeout is 0, the timer will be dis-armed.
        """
        with self.lock:
            if( timeout != 0 ):
                self.fireTime = time.time() + timeout
            else:
                self.fireTime = None
        self.semaphore.release ()


    def shutdown(self) -> None:
        """
        Shutdown worker thread
        """
        super().shutdown()
        with self.lock:
            self.fireTime = None
        self.semaphore.release()
        

    def work( self ):
        """
        Worker function of timer thread
        """
        while( self.shutdownRequested() != True ):
            with self.lock:
                fireTime = self.fireTime

            if( fireTime == None ):
                self.semaphore.acquire()
            else:
                relative = fireTime - time.time()
                if( relative > 0 ):
                    self.semaphore.acquire( timeout = relative )

            shouldFire = False
            with self.lock:
                if( self.fireTime != None ):
                    if( time.time() >= self.fireTime ):
                        self.fireTime = None
                        shouldFire = True

            if( shouldFire == True ):
                self.parser._onEscapeTimeout()



class InputEventParserVT100:
    def __init__( self, callback ):
        """
        Parser for input events
        """
        self.escapedData = None
        self.escapeTimeout = 0.05
        self.debugPrint = False

        self.escapeThread = InputEscapeTimeout( self )
        self.escapeThread.start ()
        self.lock = threads.RLock()
        self.callback = callback
        self.closed = False


    def parse( self, data ):
        """
        Parse input data and return an array of input events
        """
        events = self._parse( data )
        if( self.closed == False ):
            self.callback( events )


    def _parse( self, data ):
        """
        internal: parse input data
        """
        with self.lock:
            if( data == None ):
                return

            if( self.debugPrint ):
                console.write( "RAW INPUT DATA: " + str( bytearray( data.encode() ) ) )

            # check for VT100 escape sequence currently running
            if( self.escapedData != None ):
                self.escapedData += data
                self.escapeThread.armTimer( self.escapeTimeout )
                return self.parseEscapeSequence()

            # check for start of VT100 escape sequence
            if( data == "\x1B" ):
                self.escapedData = data
                self.escapeThread.armTimer( self.escapeTimeout )
                return self.parseEscapeSequence()

            # parse characters
            return self._parseChar( data )


    def _onEscapeTimeout( self ):
        """
        Timeout for escape parsing
        """
        events = []
        with self.lock:
            if( self.escapedData in ( "", None ) ):
                return

            if( self.debugPrint ):
                console.write( "ESCAPE timeout: " + str( bytearray( self.escapedData.encode() ) ) )

            for c in self.escapedData:
                events = events + self._parseChar( "\x1B" )
            self.escapedData = None

        if( self.closed == False ):
            self.callback( events )


    def _parseChar( self, data, alt: bool = False ):
        """
        Parse character
        """
        # special character received?
        if( data == "\n" ):
            if( alt == True ):
                return [ InputEvent( None, keyEnter, [modAlt] ) ]
            else:
                return [ InputEvent( None, keyEnter ) ]
        if( data == "\t" ):
            if( alt == True ):
                return [ InputEvent( None, keyTab, [modAlt] ) ]
            else:
                return [ InputEvent( None, keyTab ) ]
        if( data == "\x7F" ):
            if( alt == True ):
                return [ InputEvent( None, keyBackspace, [modAlt] ) ]
            else:
                return [ InputEvent( None, keyBackspace ) ]
        if( data == "\x0A" ):
            if( alt == True ):
                return [ InputEvent( None, keyEnter, [modAlt, modControl] ) ]
            else:
                return [ InputEvent( None, keyEnter, [modControl] ) ]
        if( data == "\x1B" ):
            return [ InputEvent( None, keyEscape ) ]

        # check for non displayable (unrecognized) data
        oKey = ord( data[0] )
        if( oKey < 32 ):
            if( ( oKey > 0) and ( oKey < 27 ) ):
                oChar = chr( 96 + oKey )
                if( alt == True ):
                    return [ InputEvent( oChar, None, [modAlt, modControl] ) ]
                else:
                    return [ InputEvent( oChar, None, [modControl] ) ]
            return [ InputEvent( None, unknown ) ]

        # return as normal key event
        if( alt == True ):
            return [ InputEvent( data, None, [modAlt] ) ]
        else:
            return [ InputEvent( data, None ) ]


    def parseEscapeSequence( self ):
        """
        Parse escapt sequence, returns an array of InputEvent's
        """
        # parse in VT100 char code
        parsePos = 0
        parseError = False
        group = None
        mod = None
        end = None
        rest = None

        # ensure and skip escape char
        assert len( self.escapedData ) > 0 and ( self.escapedData[0] == '\x1B' ), "failed parsing escape sequence"
        parsePos += 1

        # parse group: 'O' or '['+number
        if( len( self.escapedData ) > parsePos ):
            # group starts with 'O'?
            if( self.escapedData[parsePos] == 'O' ):
                group = 'O'
                parsePos += 1
            elif( self.escapedData[parsePos] == '[' ):
                group = '['
                parsePos += 1
                # read number
                while( ( len( self.escapedData ) > parsePos ) and ( self.escapedData[parsePos] in "0123456789" ) ):
                    group += self.escapedData[parsePos]
                    parsePos += 1
            elif( self.escapedData[parsePos] == '?' ):
                group = '?'
                parsePos += 1

        # parse modifiers
        if( not ( group == '?' ) ):
            if( len( self.escapedData ) > parsePos ):
                if( self.escapedData[parsePos] == ';' ):
                    parsePos += 1
                    while( ( len( self.escapedData ) > parsePos ) and ( self.escapedData[parsePos] in "0123456789" ) ):
                        mod = mod + self.escapedData[parsePos] if mod != None else self.escapedData[parsePos]
                        parsePos += 1

        # parse end
        if( len( self.escapedData ) > parsePos ):
            end = self.escapedData[parsePos]
            parsePos += 1

        # parse rest
        if( len( self.escapedData ) > parsePos ):
            rest = self.escapedData[parsePos:]

        # decode input events
        events = []

        # decode parsed escape sequence
        if( end != None ):
            if( end == '\x1B' ):
                # skip invalid sequence and return plain chars
                if( ( group in ( "", None ) ) and ( mod in ( "", None ) ) ):
                    events.append( InputEvent( None, keyEscape ) )
                else:
                    before = self.escapedData[1:(parsePos - 1)]
                    self.escapedData = self.escapedData[(parsePos - 1):]
                    for c in before:
                        events = events + self._parseChar( c )
                    return events
            else:
                decoded = self._decodeEscapeSequence( group, mod, end )
                if( decoded == None ):
                    rest = self.escapedData
                else:
                    events = events + decoded

                # push rest to normal char queue
                if( rest != None ):
                    for c in rest:
                        events = events + self._parseChar( c )

            # reset escape parser
            self.escapedData = None

        # return parsed events
        return events


    def _decodeEscapeSequence( self, group, mod, end ):
        """
        Decode parsed escape sequence
        """
        specialKey = None
        dataKey = None
        decodedModifiers = []

        # === VT52 / VT100 / VT220 parsing

        # special keys
        if( end == '~' ):
            if( group == "[1" ):
                specialKey = keyHome
            if( group == "[2" ):
                specialKey = keyInsert
            elif( group == "[3" ):
                specialKey = keyDelete
            elif( group == "[4" ):
                specialKey = keyEnd
            elif( group == "[5" ):
                specialKey = keyPageUp
            elif( group == "[6" ):
                specialKey = keyPageDown
            elif( group == "[15" ):
                specialKey = keyF5
            elif( group == "[17" ):
                specialKey = keyF6
            elif( group == "[18" ):
                specialKey = keyF7
            elif( group == "[19" ):
                specialKey = keyF8
            elif( group == "[20" ):
                specialKey = keyF9
            elif( group == "[21" ):
                specialKey = keyF10
            elif( group == "[23" ):
                specialKey = keyF11
            elif( group == "[24" ):
                specialKey = keyF12
            elif( group == "[25" ):
                specialKey = keyF13
            elif( group == "[26" ):
                specialKey = keyF14
            elif( group == "[28" ):
                specialKey = keyF15
            elif( group == "[29" ):
                specialKey = keyF16
            elif( group == "[31" ):
                specialKey = keyF17
            elif( group == "[32" ):
                specialKey = keyF18
            elif( group == "[33" ):
                specialKey = keyF19
            elif( group == "[34" ):
                specialKey = keyF20


        # arrow keys
        elif( end == 'A' ):
            if( group in ( None, 'O', '[', '[1' ) ):
                specialKey = keyUp

        elif( end == 'B' ):
            if( group in ( None, 'O', '[', '[1' ) ):
                specialKey = keyDown

        elif( end == 'C' ):
            if( group in ( None, 'O', '[', '[1' ) ):
                specialKey = keyRight

        elif( end == 'D' ):
            if( group in ( None, 'O', '[', '[1' ) ):
                specialKey = keyLeft

        # home keys
        elif( end == 'H' ):
            if( group in ( None, 'O', '[', '[1' ) ):
                specialKey = keyHome

        elif( end == 'F' ):
            if( group in ( None, 'O', '[', '[1' ) ):
                specialKey = keyEnd

        # Enter
        elif( end == 'M' ):
            if( group in ( None, '?', 'O', '[', '[1' ) ):
                specialKey = keyEnter

        # Space
        elif( end == ' ' ):
            if( group in ( None, '?', 'O', '[', '[1' ) ):
                dataKey = " "

        # Tab
        elif( end == 'I' ):
            if( group in ( None, '?', 'O', '[', '[1' ) ):
                specialKey = keyTab

        elif( end == 'Z' ):
            if( group in ( None, 'O', '[', '[1' ) ):
                specialKey = keyTab
                decodedModifiers = [modShift]

        # function keys
        elif( end == 'P' ):
            if( group in ( None, '?', 'O', '[', '[1' ) ):
                specialKey = keyF1

        elif( end == 'Q' ):
            if( group in ( None, '?', 'O', '[', '[1' ) ):
                specialKey = keyF2

        elif( end == 'R' ):
            if( group in ( None, '?', 'O', '[', '[1' ) ):
                specialKey = keyF3

        elif( end == 'S' ):
            if( group in ( None, '?', 'O', '[', '[1' ) ):
                specialKey = keyF4

        # num pad keys
        elif( end == 'j' ):
            if( group in ( None, '?', 'O', '[', '[1' ) ):
                dataKey = "*"

        elif( end == 'k' ):
            if( group in ( None, '?', 'O', '[', '[1' ) ):
                dataKey = "+"

        elif( end == 'l' ):
            if( group in ( None, '?', 'O', '[', '[1' ) ):
                dataKey = ","

        elif( end == 'm' ):
            if( group in ( None, '?', 'O', '[', '[1' ) ):
                dataKey = "-"

        elif( end == 'n' ):
            if( group in ( None, '?', 'O', '[', '[1' ) ):
                dataKey = "."

        elif( end == 'o' ):
            if( group in ( None, '?', 'O', '[', '[1' ) ):
                dataKey = "/"

        elif( end == 'p' ):
            if( group in ( '?', 'O', '[', '[1' ) ):
                dataKey = "0"

        elif( end == 'q' ):
            if( group in ( '?', 'O', '[', '[1' ) ):
                dataKey = "1"

        elif( end == 'r' ):
            if( group in ( '?', 'O', '[', '[1' ) ):
                dataKey = "2"

        elif( end == 's' ):
            if( group in ( '?', 'O', '[', '[1' ) ):
                dataKey = "3"

        elif( end == 't' ):
            if( group in ( '?', 'O', '[', '[1' ) ):
                dataKey = "4"

        elif( end == 'u' ):
            if( group in ( '?', 'O', '[', '[1' ) ):
                dataKey = "5"

        elif( end == 'v' ):
            if( group in ( '?', 'O', '[', '[1' ) ):
                dataKey = "6"

        elif( end == 'w' ):
            if( group in ( '?', 'O', '[', '[1' ) ):
                dataKey = "7"

        elif( end == 'x' ):
            if( group in ( '?', 'O', '[', '[1' ) ):
                dataKey = "8"

        elif( end == 'y' ):
            if( group in ( '?', 'O', '[', '[1' ) ):
                dataKey = "9"

        elif( end == 'X' ):
            if( group in ( None, '?', 'O', '[', '[1' ) ):
                dataKey = "="

        elif( end == 'E' ):
            if( group in ( None, 'O', '[', '[1' ) ):
                specialKey = keyHome

        # decode modifiers
        if( mod == "2" ):
            decodedModifiers = [modShift]
        elif( mod == "3" ):
            decodedModifiers = [modAlt]
        elif( mod == "4" ):
            decodedModifiers = [modShift, modAlt]
        elif( mod == "5" ):
            decodedModifiers = [modControl]
        elif( mod == "6" ):
            decodedModifiers = [modShift, modControl]
        elif( mod == "7" ):
            decodedModifiers = [modAlt, modControl]
        elif( mod == "8" ):
            decodedModifiers = [modShift, modAlt, modControl]
        elif( not mod in( "", None ) ):
            # failed decoding key
            if( self.debugPrint ):
                console.write( "DECODE VT100 SEQ: group = '" + str( group ) + "', mod = '" + str( mod ) + "', end = '" + str( end ) + "'" )
            return None

        # got key valid key?
        if( dataKey != None ):
            return [ InputEvent( dataKey, None, decodedModifiers ) ]
        if( specialKey != None ):
            return [ InputEvent( None, specialKey, decodedModifiers ) ]

        # got ALT + key?
        if( ( group in ( "", None ) ) and ( mod in ( "", None ) ) ):
            return self._parseChar( end, alt = True )

        # failed decoding key
        if( self.debugPrint ):
            console.write( "DECODE VT100 SEQ: group = '" + str( group ) + "', mod = '" + str( mod ) + "', end = '" + str( end ) + "'" )
        return None


    def close( self ):
        """
        Close input event parser and return array of input events
        """
        with self.lock:
            if( self.closed == True ):
                return
            self.closed = True
            self.escapeThread.shutdown()
        self.callback( [ InputEvent( None, inputClosed ) ] )



class InputEventParserWindows:
    def __init__( self, callback ):
        self.debugPrint = False

        self.callback = callback
        self.closed = False
        self.scanMode = None
        self.lock = threads.RLock()

    def parse( self, data ):
        if( self.debugPrint ):
            console.write( "RAW INPUT DATA: " + str( bytearray( data.encode() ) ) + " (" + str (ord( data ) ) + ")" )

        # parse scan code?
        if( self.scanMode != None ):
            self._parseScanCode( data )
            self.scanMode = None
            return

        # enter scan mode?
        if( data == "\0" ):
            self.scanMode = "\0"
            return
        if( data == "\xE0" ):
            self.scanMode = "\xE0"
            return

        # parse as normal character
        self._parseCharacter( data )


    def _parseCharacter( self, data ):
        # special keys
        if( data == "\x03" ):
            from . import lifecycle
            self._onEvent( [InputEvent( None, abort )] )
            lifecycle.shutdown._signalShutdown( False )
            return
        if( data == "\x08" ):
            self._onEvent( [InputEvent( None, keyBackspace )] )
            return
        if( data == "\x7f" ):
            self._onEvent( [InputEvent( None, keyBackspace, [modControl] )] )
            return
        if( data == "\x1B" ):
            self._onEvent( [InputEvent( None, keyEscape )] )
            return
        if( data == "\t" ):
            self._onEvent( [InputEvent( None, keyTab )] )
            return
        if( data == "\n" ):
            self._onEvent( [InputEvent( None, keyEnter, [modControl] )] )
            return
        if( data == "\r" ):
            self._onEvent( [InputEvent( None, keyEnter )] )
            return
        
        # return as normal character
        self._onEvent( [InputEvent( data, None )] )


    def _parseScanCode( self, data ):
        extended = self.scanMode == "\xE0"

        modifiers = []
        specialKey = None
        dataKey = None

        if( data == "\x01" ):
            specialKey = keyEscape
            modifiers = [modAlt]
        
        elif( data == "\x0E" ) and ( extended == False ):
            specialKey = keyBackspace
            modifiers = [modAlt]
        
        elif( data == "\x0F" ):
            specialKey = keyTab
            modifiers = [modShift]
        
        elif( data == "\x1C" ) and ( extended == False ):
            specialKey = keyEnter
            modifiers = [modAlt]
        
        elif( data == "\x3B" ) and ( extended == False ):
            specialKey = keyF1
        
        elif( data == "\x3C" ) and ( extended == False ):
            specialKey = keyF2
        
        elif( data == "\x3D" ) and ( extended == False ):
            specialKey = keyF3
        
        elif( data == "\x3E" ) and ( extended == False ):
            specialKey = keyF4
        
        elif( data == "\x3F" ) and ( extended == False ):
            specialKey = keyF5
        
        elif( data == "\x40" ) and ( extended == False ):
            specialKey = keyF6
        
        elif( data == "\x41" ) and ( extended == False ):
            specialKey = keyF7
        
        elif( data == "\x42" ) and ( extended == False ):
            specialKey = keyF8
        
        elif( data == "\x43" ) and ( extended == False ):
            specialKey = keyF9
        
        elif( data == "\x44" ) and ( extended == False ):
            specialKey = keyF10

        elif( data == "\x47" ):
            specialKey = keyHome

        elif( data == "\x48" ):
            specialKey = keyUp

        elif( data == "\x4B" ):
            specialKey = keyLeft

        elif( data == "\x4D" ):
            specialKey = keyRight

        elif( data == "\x4F" ):
            specialKey = keyEnd

        elif( data == "\x49" ):
            specialKey = keyPageUp

        elif( data == "\x50" ):
            specialKey = keyDown

        elif( data == "\x51" ):
            specialKey = keyPageDown

        elif( data == "\x52" ):
            specialKey = keyInsert

        elif( data == "\x53" ):
            specialKey = keyDelete

        elif( data == "\x54" ) and ( extended == False ):
            specialKey = keyF1
            modifiers = [modShift]
        
        elif( data == "\x55" ) and ( extended == False ):
            specialKey = keyF2
            modifiers = [modShift]
        
        elif( data == "\x56" ) and ( extended == False ):
            specialKey = keyF3
            modifiers = [modShift]
        
        elif( data == "\x57" ) and ( extended == False ):
            specialKey = keyF4
            modifiers = [modShift]
        
        elif( data == "\x58" ) and ( extended == False ):
            specialKey = keyF5
            modifiers = [modShift]
        
        elif( data == "\x59" ) and ( extended == False ):
            specialKey = keyF6
            modifiers = [modShift]
        
        elif( data == "\x5A" ) and ( extended == False ):
            specialKey = keyF7
            modifiers = [modShift]
        
        elif( data == "\x5B" ) and ( extended == False ):
            specialKey = keyF8
            modifiers = [modShift]
        
        elif( data == "\x5C" ) and ( extended == False ):
            specialKey = keyF9
            modifiers = [modShift]
        
        elif( data == "\x5D" ) and ( extended == False ):
            specialKey = keyF10
            modifiers = [modShift]

        elif( data == "\x5E" ) and ( extended == False ):
            specialKey = keyF1
            modifiers = [modControl]
        
        elif( data == "\x5F" ) and ( extended == False ):
            specialKey = keyF2
            modifiers = [modControl]
        
        elif( data == "\x60" ) and ( extended == False ):
            specialKey = keyF3
            modifiers = [modControl]
        
        elif( data == "\x61" ) and ( extended == False ):
            specialKey = keyF4
            modifiers = [modControl]
        
        elif( data == "\x62" ) and ( extended == False ):
            specialKey = keyF5
            modifiers = [modControl]
        
        elif( data == "\x63" ) and ( extended == False ):
            specialKey = keyF6
            modifiers = [modControl]
        
        elif( data == "\x64" ) and ( extended == False ):
            specialKey = keyF7
            modifiers = [modControl]
        
        elif( data == "\x65" ) and ( extended == False ):
            specialKey = keyF8
            modifiers = [modControl]
        
        elif( data == "\x66" ) and ( extended == False ):
            specialKey = keyF9
            modifiers = [modControl]
        
        elif( data == "\x67" ) and ( extended == False ):
            specialKey = keyF10
            modifiers = [modControl]

        elif( data == "\x68" ) and ( extended == False ):
            specialKey = keyF1
            modifiers = [modAlt]
        
        elif( data == "\x69" ) and ( extended == False ):
            specialKey = keyF2
            modifiers = [modAlt]
        
        elif( data == "\x6A" ) and ( extended == False ):
            specialKey = keyF3
            modifiers = [modAlt]
        
        elif( data == "\x6B" ) and ( extended == False ):
            specialKey = keyF4
            modifiers = [modAlt]
        
        elif( data == "\x6C" ) and ( extended == False ):
            specialKey = keyF5
            modifiers = [modAlt]
        
        elif( data == "\x6D" ) and ( extended == False ):
            specialKey = keyF6
            modifiers = [modAlt]
        
        elif( data == "\x6E" ) and ( extended == False ):
            specialKey = keyF7
            modifiers = [modAlt]
        
        elif( data == "\x6F" ) and ( extended == False ):
            specialKey = keyF8
            modifiers = [modAlt]
        
        elif( data == "\x70" ) and ( extended == False ):
            specialKey = keyF9
            modifiers = [modAlt]
        
        elif( data == "\x71" ) and ( extended == False ):
            specialKey = keyF10
            modifiers = [modAlt]
 
        elif( data == "\x73" ):
            specialKey = keyLeft
            modifiers = [modControl]
 
        elif( data == "\x74" ):
            specialKey = keyRight
            modifiers = [modControl]
 
        elif( data == "\x75" ):
            specialKey = keyEnd
            modifiers = [modControl]
 
        elif( data == "\x76" ):
            specialKey = keyPageDown
            modifiers = [modControl]

        elif( data == "\x77" ):
            specialKey = keyHome
            modifiers = [modControl]

        elif( data == "\x7F" ):
            specialKey = keyBackspace
            modifiers = [modControl]
 
        elif( data == "\x84" ):
            specialKey = keyPageUp
            modifiers = [modControl]
        
        elif( data == "\x85" ) and ( extended == True ):
            specialKey = keyF11
        
        elif( data == "\x86" ) and ( extended == True ):
            specialKey = keyF12
        
        elif( data == "\x87" ) and ( extended == True ):
            specialKey = keyF11
            modifiers = [modShift]
        
        elif( data == "\x88" ) and ( extended == True ):
            specialKey = keyF12
            modifiers = [modShift]
        
        elif( data == "\x89" ) and ( extended == True ):
            specialKey = keyF11
            modifiers = [modControl]
        
        elif( data == "\x8A" ) and ( extended == True ):
            specialKey = keyF12
            modifiers = [modControl]
        
        elif( data == "\x8B" ) and ( extended == True ):
            specialKey = keyF11
            modifiers = [modAlt]
        
        elif( data == "\x8C" ) and ( extended == True ):
            specialKey = keyF12
            modifiers = [modAlt]
 
        elif( data == "\x8D" ):
            specialKey = keyUp
            modifiers = [modControl]
 
        elif( data == "\x91" ):
            specialKey = keyDown
            modifiers = [modControl]
 
        elif( data == "\x92" ):
            specialKey = keyInsert
            modifiers = [modControl]
 
        elif( data == "\x93" ):
            specialKey = keyDelete
            modifiers = [modControl]
       
        elif( data == "\x94" ) and ( extended == False ):
            specialKey = keyTab
            modifiers = [modControl]

        elif( data == "\x97" ) and ( extended == False ):
            specialKey = keyHome
            modifiers = [modAlt]

        elif( data == "\x98" ) and ( extended == False ):
            specialKey = keyUp
            modifiers = [modAlt]

        elif( data == "\x99" ) and ( extended == False ):
            specialKey = keyPageUp
            modifiers = [modAlt]

        elif( data == "\x9B" ) and ( extended == False ):
            specialKey = keyLeft
            modifiers = [modAlt]

        elif( data == "\x9D" ) and ( extended == False ):
            specialKey = keyRight
            modifiers = [modAlt]

        elif( data == "\x9F" ) and ( extended == False ):
            specialKey = keyEnd
            modifiers = [modAlt]

        elif( data == "\xA0" ) and ( extended == False ):
            specialKey = keyDown
            modifiers = [modAlt]

        elif( data == "\xA1" ) and ( extended == False ):
            specialKey = keyPageDown
            modifiers = [modAlt]

        elif( data == "\xA2" ) and ( extended == False ):
            specialKey = keyInsert
            modifiers = [modAlt]

        elif( data == "\xA3" ) and ( extended == False ):
            specialKey = keyDelete
            modifiers = [modAlt]
        
        elif( data == "\xA5" ) and ( extended == False ):
            specialKey = keyTab
            modifiers = [modAlt]
        
        elif( data == "\xA6" ) and ( extended == False ):
            specialKey = keyEnter
            modifiers = [modAlt]
            

        # dispatch key event
        if( specialKey != None ):
            self._onEvent( [InputEvent( None, specialKey, modifiers )] )
            return
        if( dataKey != None ):
            self._onEvent( [InputEvent( dataKey, None, modifiers )] )
            return
        self._onEvent( [InputEvent( None, unknown )] )


    def _onEvent( self, events ):
        with self.lock:
            if( self.closed == False ):
                self.callback( events )

    def close( self ):
        with self.lock:
            if( self.closed == True ):
                return
            self.closed = True
        self.callback( [ InputEvent( None, inputClosed ) ] )
    