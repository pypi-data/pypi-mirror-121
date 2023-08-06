# constants for style modifiers and colors
INHERIT             = 0
DEFAULT             = 1


# color constants
BLACK               = 2
RED                 = 3
GREEN               = 4
YELLOW              = 5
BLUE                = 6
MAGENTA             = 7
CYAN                = 8
WHITE               = 9


# style modifier constants
BRIGHT              = 0b0000000000000010000
NO_BRIGHT           = 0b0000000000000100000
DIM                 = 0b0000000000001000000
NO_DIM              = 0b0000000000010000000
BOLD                = 0b0000000000100000000
NO_BOLD             = 0b0000000001000000000
ITALIC              = 0b0000000010000000000
NO_ITALIC           = 0b0000000100000000000
UNDERLINE           = 0b0000001000000000000
NO_UNDERLINE        = 0b0000010000000000000
BLINK               = 0b0000100000000000000
NO_BLINK            = 0b0001000000000000000
STRIKETHROUGH       = 0b0010000000000000000
NO_STRIKETHROUGH    = 0b0100000000000000000


# internal constants
_STYLE_DEFAULT      = 0
_STYLE_MAX          = 0b1000000000000000000
_STYLE_INV_MASK     = 0b1000000000000001111




class Style:
    def __init__( self, mod = INHERIT, fg = INHERIT, bg = INHERIT ):
        """
        Creates a new color string style.
        """
        if( mod != DEFAULT ):
            assert mod < _STYLE_MAX, "invalid modifier set"
            assert (mod & _STYLE_INV_MASK) == 0, "invalid modifier set"
        self.mod = mod
        assert fg >= 0, "invalid foreground color"
        assert fg <= 9, "invalid foreground color"
        self.fg = fg
        assert bg >= 0, "invalid background color"
        assert bg <= 9, "invalid background color"
        self.bg = bg


    def copy( self ):
        """
        Copy instance
        """
        return Style( self.mod, self.fg, self.bg )


    def _inheritStyle( self, setMask, unsetMask, lastSet ):
        """
        Inherit a single style attribute
        """
        # get flag from parent
        flagSet = False
        if( ( lastSet & setMask ) != 0 ):
            flagSet = True
        if( ( self.mod & setMask ) != 0):
            flagSet = True
        elif( ( self.mod & unsetMask ) != 0):
            flagSet = False
        return setMask if flagSet else 0


    def concrete( self, parentStyle ):
        """
        Create a style set by deriving from a parent one or use default values
        """

        # inherit style set
        if( self.mod == DEFAULT ):
            newMod = _STYLE_DEFAULT
        else:
            if( parentStyle != None ):
                lastStyle = parentStyle.mod
            else:
                lastStyle = _STYLE_DEFAULT
            newMod = 0
            newMod |= self._inheritStyle( BRIGHT,        NO_BRIGHT,        lastStyle )
            newMod |= self._inheritStyle( DIM,           NO_DIM,           lastStyle )
            newMod |= self._inheritStyle( BOLD,          NO_BOLD,          lastStyle )
            newMod |= self._inheritStyle( ITALIC,        NO_ITALIC,        lastStyle )
            newMod |= self._inheritStyle( UNDERLINE,     NO_UNDERLINE,     lastStyle )
            newMod |= self._inheritStyle( BLINK,         NO_BLINK,         lastStyle )
            newMod |= self._inheritStyle( STRIKETHROUGH, NO_STRIKETHROUGH, lastStyle )

        # inherit foreground color
        newFG = self.fg
        if( self.fg == INHERIT ):
            if( parentStyle != None ):
                newFG = parentStyle.fg
            else:
                newFG = DEFAULT

        # inherit background color
        newBG = self.bg
        if( self.bg == INHERIT ):
            if( parentStyle != None ):
                newBG = parentStyle.bg
            else:
                newBG = DEFAULT

        # return new style set
        return Style( newMod, newFG, newBG )


    def equals( self, other ) -> bool:
        """
        Check if two styles are equal
        """
        return ( self.mod == other.mod ) and ( self.fg == other.fg ) and ( self.bg == other.bg )


    @staticmethod
    def resetVT100():
        return "\x1B[m"


    def encodeVT100( self ):
        """
        Encode VT100 style set
        """
        # initialize default style set
        s = "\x1B[0"

        # set VT100 foreground
        if( ( self.fg != DEFAULT ) and ( self.fg != INHERIT ) ):
            s += ";" + str ( self.fg + 30 - 2 )

        # set VT100 background
        if( ( self.bg != DEFAULT ) and ( self.bg != INHERIT ) ):
            s += ";" + str ( self.bg + 40 - 2 )

        # set VT100 modifiers
        isBright = False
        isDim = False
        if( ( self.mod & BRIGHT ) != 0 ):
            s += ";1"
            isBright = True
        if( ( self.mod & DIM ) != 0 ):
            s += ";2"
            isDim = True
        if( ( self.mod & BOLD ) != 0 ):
            if( isBright == False ):
                s += ";1"
                isBright = True
            if( ( self.mod & BRIGHT ) == 0 ):
                if( isDim == False ):
                    s += ";2"
                    isDim = True
        if( ( self.mod & ITALIC ) != 0 ):
            s += ";3"
        if( ( self.mod & UNDERLINE ) != 0 ):
            s += ";4"
        if( ( self.mod & BLINK ) != 0 ):
            s += ";5"
        if( ( self.mod & STRIKETHROUGH ) != 0 ):
            s += ";9"         

        # return new style set
        s += "m"
        return s




class SStr:
    def __init__( self, *content, mod: int = INHERIT, fg: int = INHERIT, bg: int = INHERIT, style = None ):
        """
        Styled string class (tree item)
        """
        if( style != None ):
            assert mod == INHERIT, "ambigious: mod and style parameter present"
            assert fg  == INHERIT, "ambigious: fg and style parameter present"
            assert bg  == INHERIT, "ambigious: bg and style parameter present"
            self.style = style
        else:
            self.style = Style( mod, fg, bg )
            
        # take content
        self.content = []
        if( content != None ):
            for c in content:
                self.content.append( c )


    def _collectLinear( self, parts, parentStyle ):
        """
        Flatten to be a linear string
        """
        concreteStyle = self.style.concrete( parentStyle )
        for c in self.content:
            if( c != None ):
                # Ignore None on content element
                if( isinstance( c, SStr ) ):
                    # flatten SStr
                    c._collectLinear( parts, concreteStyle )
                elif( isinstance( c, LStr ) ):
                    # flatten linearized string
                    for lc in c.parts:
                        parts.append( lc.copy() )
                else:
                    # interprete as normal string content
                    parts.append( LStrPart( str( c ), concreteStyle ) )


    def asLinear( self, parentStyle = None ):
        """
        Return styled string as linear representation
        """
        parts = []
        self._collectLinear( parts, parentStyle )
        return LStr( *parts )


    def __str__( self ) -> str:
        """
        Return as plain string without color encoding
        """
        s = ""
        for c in self.content:
            s += str ( c )
        return s


    def __len__( self ) -> int:
        """
        Returns the length of this string
        """
        l = 0
        for c in self.content:
            if( isinstance( c, ( SStr, LStr ) ) ):
                l += c.__len__()
            else:
                l += len( str( c ) )
        return l

    
    def encode( self, plain = False ) -> str:
        """
        Encode as VT100 string or plain string
        """
        if( plain == True ):
            return self.__str__()
        else:
            return self.asLinear().encode()




class LStrPart:
    def __init__( self, content, style ):
        """
        Part of linearized style string
        """
        self.content = content
        self.style = style


    def copy( self ):
        """
        Copy instance
        """
        return LStrPart( "" + self.content, self.style.copy() )




class LStr:
    def __init__( self, *parts ):
        """
        Linear representation of styled string class
        """
        self.parts = []
        self.append( *parts )


    def append( self, *parts ) -> None:
        """
        Appends linear string parts
        """
        if( parts != None ):
            for p in parts:
                assert isinstance( p, LStrPart ), "only _LStrParts are allowed to build a LStr"
                # append to last linear part when style matches
                if( len( self.parts ) > 0 ):
                    if( self.parts[-1].style.equals( p.style ) ):
                        self.parts[-1].content += p.content
                    else:
                        self.parts.append( p )
                else:
                    self.parts.append( p )


    def __add__( self, other ):
        """
        Add operator
        """
        n = self.copy()
        assert isinstance( other, LStr ), "only LStr's are supported to add"
        n.append( *other.parts )
        return n


    def __iadd__( self, other ):
        """
        Inline add operator
        """
        assert isinstance( other, LStr ), "only LStr's are supported to add"
        self.append( *other.parts )
        return self


    def substring( self, begin, end ):
        """
        Returns a substring of this LStr
        """
        assert begin >= 0

        # determine number of charaters to copy
        l = self.__len__ ()
        eCount = end - begin
        if( eCount < 0 ):
            eCount = 0
        count = l - begin
        if( eCount < count ):
            count = eCount

        # empty string?
        if( count < 1 ):
            return LStr()

        # find first part to copy from
        sparts = []
        partIdx = 0
        partBegin = 0
        pStart = 0
        while( partIdx < len( self.parts ) ):
            pl = len( self.parts[partIdx].content )
            # check if inside current part
            if( ( begin >= pStart ) and ( begin < (pStart + pl ) ) ):
                partBegin = begin - pStart
                break
            # iterate next part
            partIdx += 1
            pStart += pl

        # copy data from string parts
        outputCount = 0
        while( ( partIdx < len( self.parts ) ) and ( outputCount < count ) ):
            # get part truncated at start
            if( partBegin > 0 ):
                pa = LStrPart( self.parts[partIdx].content[partBegin:], self.parts[partIdx].style )
            else:
                pa = self.parts[partIdx].copy()

            # limit output size to count
            outputCount += len ( pa.content )
            if( outputCount > count ):
                # clamp last element
                remove = outputCount - count
                pa = LStrPart( pa.content[0: len( pa.content ) - remove], pa.style )
            sparts.append( pa )
            partBegin = 0

            # continue on next part
            partIdx += 1

        # return substring
        return LStr( *sparts )


    def getCharAt( self, position: int ) -> LStrPart:
        """
        Returns a LStrPart representing a single styled character at a position, returns None if position is invalid
        """
        # index invalid?
        if( position < 0 ):
            return None

        # find character inside parts
        offset = 0
        for partIndex in range( 0, len( self.parts ) ):
            part = self.parts[partIndex]
            nextOffset = offset + len( part.content )
            if( ( position >= offset ) and ( position < nextOffset ) ):
                partOffset = position - offset
                return LStrPart( part.content[partOffset], part.style )
            offset = nextOffset

        # index not found
        return None

    
    def asCharList( self ):
        """
        Returns a list of consisting of single characters as LStrPart
        """
        chars = []
        for p in self.parts:
            for c in p.content:
                chars.append( LStrPart( c, p.style ) )
        return chars


    def asLinear( self ):
        """
        Return as linear styled string
        """
        return self.copy()


    def copy( self ):
        """
        Copy instance
        """
        parts = []
        for p in self.parts:
            parts.append( p.copy() )
        return LStr( *parts )


    def __str__( self ) -> str:
        """
        Return as plain string without color encoding
        """
        s = ""
        for p in self.parts:
            s += p.content
        return s


    def __len__( self ) -> int:
        """
        Returns the length of this string
        """
        l = 0
        for p in self.parts:
            l += len( p.content )
        return l


    def encode( self, plain: bool = False ) -> str:
        """
        Encode as VT100 string or plain string
        """
        if( plain == True ):
            return self.__str__()
        else:
            buffer = ""
            for p in self.parts:
                buffer += p.style.encodeVT100()
                buffer += p.content
            buffer += Style.resetVT100()
            return buffer


    @staticmethod
    def createSpacesDefaultStyle( count: int, style = None ):
        """
        Create a LStr from a number of spaces
        """
        if( count < 1 ):
            return LStr()
        else:
            return LStr( LStrPart( " " * count, Style() if style == None else style ) )


    def __mul__( self, count: int ):
        """
        Multiply string with count.
        """
        n = LStr()
        for i in range( count ):
            for p in self.parts:
                n.append( p.copy() )
        return n


    @staticmethod
    def _parseStyle( lastStyle, styleStr ):
        """
        Parse VT100 style string.
        """
        # by default, keep style
        default = INHERIT

        # parse mode request
        requests = styleStr.split(";")
        newStyle = Style( )
        for r in requests:
            if( r != "" ):
                ir = int( r )
                if( ir == 0 ):
                    # default values
                    newStyle.fg = default
                    newStyle.bg = default
                    newStyle.mod = default
                
                elif( ( ir >= 30 ) and ( ir <= 37 ) ):
                    # foreground color
                    newStyle.fg = ir + 2 - 30
                
                elif( ( ir >= 40 ) and ( ir <= 47 ) ):
                    # backgroundground color
                    newStyle.bg = ir + 2 - 40

                # parse modifiers
                elif( ir == 1 ):
                    newStyle.mod |= BRIGHT
                elif( ir == 2 ):
                    newStyle.mod |= DIM
                elif( ir == 3 ):
                    newStyle.mod |= ITALIC
                elif( ir == 4 ):
                    newStyle.mod |= UNDERLINE
                elif( ir == 5 ):
                    newStyle.mod |= BLINK
                elif( ir == 9 ):
                    newStyle.mod |= STRIKETHROUGH

                # fail silently on parser error
                else:
                    pass

        # combine parsed style with last one
        if( lastStyle != None ):
            return newStyle.concrete( lastStyle )
        return newStyle


    @staticmethod
    def parseVT100( text ):
        """
        Parse from VT100 encoded string
        """
        # parse VT100 content
        text = str( text )
        currentStyle = Style()
        parts = []
        textBuffer = ""

        #  read characters and encoding
        index = 0
        commandState = False
        commandBuffer = ""
        while( index < len( text ) ):
            ch = text[index]
            if( commandState == False ):
                if( ch == "\x1B" ):
                    commandState = True
                else:
                    textBuffer += ch
            else:
                # push previous text buffer
                if( textBuffer != "" ):
                    parts.append( LStrPart( textBuffer, currentStyle ) )
                    textBuffer = ""

                # start color command?
                if( commandBuffer == '' ):
                    if( ch == '[' ):
                        commandBuffer += ch
                    else:
                        textBuffer += "\x1B" + ch
                        commandState = False
                elif( commandBuffer != '' ):
                    # only accept chars '0' - '9, ';', 'm'
                    if( ch in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ';', 'm' ) ):
                        if( ch != 'm' ):
                            commandBuffer += ch
                        else:
                            # got style command
                            currentStyle = LStr._parseStyle( currentStyle, commandBuffer[1:] )
                            commandBuffer = ''
                            commandState = False
                    else:
                        # skip current command
                        textBuffer += "\x1B" + commandBuffer + ch
                        commandBuffer = ""
                        commandState = False

                else:
                    # push to text buffer
                    textBuffer += "\x1B" + commandBuffer + ch
                    commandBuffer = ""
                    commandState = False

            # consume current character
            index += 1

        # push rest of parsed characters to output
        if( commandState == True ):
            textBuffer += "\x1B" + commandBuffer
        if( textBuffer != "" ):
            parts.append( LStrPart( textBuffer, currentStyle ) )

        # return parsed content as LStr
        return LStr( *parts )
