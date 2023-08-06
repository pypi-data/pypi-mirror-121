from . import sstr
from . import style


### ############################
### Values of command line items
### ############################


# default command line value implementation
class Value:
    # parse results
    PARSE_SUCCEED           = 0
    PARSE_SUCCEED_LIST      = 1
    PARSE_INVALID_VALUE     = 2
    PARSE_UNKOWN_VALUE      = 3
    PARSE_VALUE_ALREADY_SET = 4
    PARSE_MISSING_VALUE     = 5


    # extent results
    EXTENT_SUCCEEDED        = 0
    EXTENT_FAIL             = 1


    # init value
    def __init__( self,
                  name: str,
                  description: str,                 # can also be a ColorString
                  default                           = None,
                  optional: bool                    = False,
                  array: bool                       = False,
                  allowOverride: bool               = False,
                  allowOverrideInChildren: bool     = False,
                  visibleToChildren: bool           = False,
                  inheritParentValue: bool          = False,
                  listSeparator: str                = None,
                  shortDescription: str             = None ):
        """
        Value stored in context, to be accessed by flags and parameters.
        """
        self._name = name
        self._default = default
        self._description = description
        self._optional = optional
        self._array = array
        self._allowOverride = allowOverride
        self._allowOverrideInChildren = allowOverrideInChildren
        self._visibleToChildren = visibleToChildren
        self._inheritParentValue = inheritParentValue
        self._listSeparator = listSeparator
        self._shortDescription = shortDescription
        if( array == True ):
            assert allowOverride == False, "Array parameters are always appending, override is not allowed"
            assert default == None, "Default value is not allowed on array values"
        if( listSeparator != None ):
            assert array == True, "List separator is only allowed when parsing arrays"


    def name( self ):
        """
        Returns the name of this value.
        """
        return self._name


    def typeAndRange( self ):
        """
        Returns a string containing type and range for help, "" if not available.
        """
        return ""


    def description( self, detailed: bool = False ):
        """
        Returns the description of this value.
        """
        if( detailed != False or self._shortDescription == None ):
            return sstr.SStr( self._description )
        else:
            return sstr.SStr( self._shortDescription )


    def optional( self ):
        """
        Returns True if value is optional.
        """
        return self._optional


    def default( self ):
        """
        Returns the default of this value.
        """
        return self._default


    def array( self ):
        """
        Returns true if this value is an array.
        """
        return self._array


    def allowOverride( self ):
        """
        Returns True if the value can be parsed multiple times.
        """
        return self._allowOverride


    def allowOverrideInChildren( self ):
        """
        Returns True if the value is allowed to be redifined in a child context.
        """
        return self._allowOverrideInChildren
        
    
    def visibleToChildren( self ):
        """
        Returns true if this value should be visible in child contexts.
        """
        return self._visibleToChildren


    def listSeparator( self ):
        """
        Returns the list separator for parsing this value.
        """
        return self._listSeparator


    def inheritParentValue( self ):
        """
        Returns true if a child should inherit value from parent context.
        """
        return self._inheritParentValue


    def get( self, context: object, local: bool = False ):
        """
        Get value from context.
        """
        return context.get ( self.name, local )


    def isset( self, context: object, local: bool = False):
        """
        Returns true if value is set on context.
        """
        return context.isset ( self.name, local )


    def _tryParseElement( self, context: object, data: str ):
        """
        Try to parse a element, returns a parse result.

        This function should be overwritten in child classes.

        Returns:
            ( PARSE_SUCCEEDED, parsedValue )       when parsing was successfull
            ( PARSE_INVALID_VALUE, errStr )        when parsing an invalid value
            ( PARSE_UNKOWN_VALUE, valueName )      when value is not registered at context
            ( PARSE_VALUE_ALREADY_SET, valueName ) when value is already set and not overrideable
            ( PARSE_MISSING_VALUE, valueName )     when the value is not known on current context
        """
        assert False, "to be implemented by child class"


    def _extentElement( self, context: object, completeArg: str, arg: str ):
        """
        Extent a command line value, returns an array of possible extensions, returns None if not extentable.

        This function should be overwritten in child classes.

        Returns:
            ( EXTENT_FAIL, None )                   when the command line part is not extentable
            ( EXTENT_SUCCEEDED, list )              when extention is successfull, a list of possible extentions is returned
        """
        return( Value.EXTENT_FAIL, None )


    def _tryParse( self, context: object, data: str ):
        """
        Try to parse a command line argument, returns a parse result.
        """
        # get list separator
        ls = self.listSeparator()

        # process item without list separator
        if( ls == None ):
            return self._tryParseElement( context, data )

        # process item with list separator
        else:
            if( data in ( None, "" ) ):
                return( Value.PARSE_MISSING_VALUE, None )
            elements = data.split( ls )
            result = []
            for e in elements:
                if( not e in ( "", None ) ):
                    (parseResult, parseValue) = self._tryParseElement( context, e )
                    if( parseResult == Value.PARSE_SUCCEED ):
                        result.append( parseValue )
                    else:
                        result.append( parseValue )
                        return( parseResult, parseValue )
            return( Value.PARSE_SUCCEED_LIST, result )


    def _extent( self, context: object, arg: str ):
        """
        Expand a command line value, returns an array of possible extensions, returns None if not extentable.
        """
        # get list separator
        ls = self.listSeparator()

        # process item without list separator
        if( ls == None ):
            return self._extentElement( context, arg, arg )

        # process item with list separator
        else:
            elements = arg.split( ls )
            result = []
            preStr = ""
            for index in range( len( elements ) ):
                element = elements[index]
                last = index >= ( len( elements ) - 1 )

                # is last element?
                if( last == True ):
                    # check if item is parsed succesfully
                    (pr, pv) = self._tryParseElement( context, element )
                    parseSucceeded = ( pr in ( Value.PARSE_SUCCEED, Value.PARSE_SUCCEED_LIST ) )

                    # add prefix to extension values
                    extentionValues = []
                    (eResult, extentionItems) = self._extentElement( context, preStr, element )
                    if( eResult == Value.EXTENT_FAIL ):
                        return( Value.EXTENT_FAIL, None )

                    ps = ""
                    if( preStr != "" ):
                        ps = preStr + ls

                    if( eResult != Value.EXTENT_FAIL ):
                        for e in extentionItems:
                            extentionValues.append( ps + e )

                    return( Value.EXTENT_SUCCEEDED, extentionValues )
                else:
                    # parse list elements
                    (pr, pv) = self._tryParseElement( context, element )
                    if( pr in( Value.PARSE_SUCCEED, Value.PARSE_SUCCEED_LIST ) ):
                        # parse array element
                        if( last == False ):
                            if( preStr == "" ):
                                preStr = element
                            else:
                                preStr = preStr + ls + element
                    else:
                        return( Value.EXTENT_FAIL, None )

            # return result
            return( Value.PARSE_SUCCEED_LIST, result )



class OptionItem:
    def __init__( self,
                  name: str,            # name of option
                  description: str,     # can also be a ColorString
                  value: object = None,
                  shortDescription: str = None
                ):
        """
        Item of option
        """
        self.name = name
        self._description = description
        self.shortDescription = shortDescription
        if( value == None ):
            self.value = name
        else:
            self.value = value


    def description( self, detailed: bool = False ):
        """
        Returns the description of this option
        """
        if( detailed != False or self.shortDescription == None ):
            return sstr.SStr( self._description )
        else:
            return sstr.SStr( self.shortDescription )




class OptionValue( Value ):
    def __init__( self,
                  name: str,
                  description: str,                 # can also be a ColorString
                  options: list                     = [],
                  default                           = None,
                  optional: bool                    = False,
                  array: bool                       = False,
                  allowOverride: bool               = False,
                  allowOverrideInChildren: bool     = False,
                  visibleToChildren: bool           = False,
                  inheritParentValue: bool          = False,
                  listSeparator: str                = None,
                  shortDescription: str             = None ):
        """
        Value selectable from a list of options.
        """
        Value.__init__( self,
                        name = name,
                        description = description,
                        default = default,
                        optional = optional,
                        array = array,
                        allowOverride = allowOverride,
                        allowOverrideInChildren = allowOverrideInChildren,
                        visibleToChildren = visibleToChildren,
                        inheritParentValue = inheritParentValue,
                        listSeparator = listSeparator,
                        shortDescription = shortDescription )
        self._options = options


    def options( self, context: object = None ):
        """
        Return a list of possible options (OptionItems).

        This function should be overwritten in child classes.
        """
        return self._options


    def _tryParseElement( self, context: object, data: str ):
        """
        Try to parse option value.
        """
        # get options for this value
        opts = self.options( context )

        # check if option is present, return parsed data withoud error string
        for opt in opts:
            if( opt.name == data ):
                return( Value.PARSE_SUCCEED, data )

        # failed to parse option
        if( data == None ):
            return( Value.PARSE_MISSING_VALUE, None )
        return( Value.PARSE_INVALID_VALUE, "'" + data + "' is unknown" )


    def _extentElement( self, context: object, completeArg: str, arg: str ):
        """
        Expand a command line value, returns an array of possible extensions, returns None if not extentable
        """
        # get list of extentable items
        opts = self.options( context )
        if( opts != None ):
            extentions = []
            for o in opts:
                if( o.name.startswith( arg ) ):
                    extentions.append( o.name )
            return( Value.EXTENT_SUCCEEDED, extentions )
        return( Value.EXTENT_FAIL, None )



class ContextValue( Value ):
    def __init__( self,
                  name: str,
                  description: str,     # can also be a ColorString
                  contextStubs: list,
                  optional: bool        = False,
                  array: bool           = False,
                  shortDescription: str = None ):
        """
        Creates a new context value.
        
        When a context value is parsed, a new instance of the context will be bound to the value and the parser enters
        this context as a sub context.
        """
        Value.__init__( self,
                        name = name,
                        description = description,
                        default = None,
                        optional = optional,
                        array = array,
                        allowOverride = False,
                        allowOverrideInChildren = False,
                        visibleToChildren = False,
                        inheritParentValue = False,
                        listSeparator = None,
                        shortDescription = shortDescription )
        self._contextStubs = contextStubs


    def options( self, context: object = None ):
        """
        Return a list of possible options (OptionItems).
        """
        result = []
        for ctx in self._contextStubs:
            result.append( OptionItem (ctx.name(), ctx.description() ) )
        if( len( result ) == 0 ):
            return None
        return result


    def _tryParseElement( self, context: object, data: str ):
        """
        Try to parse a value, returns a parse result.
        """
        # check if context is found
        if( not ( data in ( None, "" ) ) ):
            for stub in self._contextStubs:
                if( stub.name() == data ):
                    return( Value.PARSE_SUCCEED, stub )

        # invalid value for action
        return( Value.PARSE_INVALID_VALUE, "'" + data + "' is unknown" )


    def _extentElement( self, context: object, completeArg: str, arg: str ):
        """
        Expand a command line value, returns an array of possible extensions, returns None if not extentable.
        """
        # get list of extentable items
        opts = self.options( context )
        if( opts != None ):
            extentions = []
            for o in opts:
                if( o.name.startswith( arg ) ):
                    extentions.append( o.name )
            return( Value.EXTENT_SUCCEEDED, extentions )
        return( Value.EXTENT_FAIL, None )




class NumberValue( Value ):
    def __init__( self,
                  name: str,
                  description: str,                 # can also be a ColorString
                  min: int                          = None,
                  max: int                          = None,
                  clamp: bool                       = False,
                  float: bool                       = False,
                  step: float                       = 1,
                  default                           = None,
                  optional: bool                    = False,
                  array: bool                       = False,
                  allowOverride: bool               = False,
                  allowOverrideInChildren: bool     = False,
                  visibleToChildren: bool           = False,
                  inheritParentValue: bool          = False,
                  listSeparator: str                = None,
                  shortDescription: str             = None ):
        """
        Number value with optional range boundaries.
        """
        Value.__init__( self,
                        name = name,
                        description = description,
                        default = default,
                        optional = optional,
                        array = array,
                        allowOverride = allowOverride,
                        allowOverrideInChildren = allowOverrideInChildren,
                        visibleToChildren = visibleToChildren,
                        inheritParentValue = inheritParentValue,
                        listSeparator = listSeparator,
                        shortDescription = shortDescription )
        self._min   = min
        self._max   = max
        self._clamp = clamp
        self._float = float
        self._step  = step


    def typeAndRange( self ):
        """
        Returns the type and range of this value.
        """
        rangeInfo = ""
        if( self._min != None ):
            if( self._max != None ):
                rangeInfo = " in range " + str( self._min ) + ".." + str( self._max )
            else:
                rangeInfo = " >= " + str( self._min )
        else:
            if( self._max != None ):
                rangeInfo = " <= " + str( self._max)
            else:
                rangeInfo = ""
        return "number" + rangeInfo


    def min( self ):
        """
        Get minimum of value.
        """
        return self._min


    def max( self ):
        """
        Get maximum of value.
        """
        return self._max


    def clamp( self ):
        """
        Returns true if value is clamped.
        """
        return self._clamp


    def float( self ):
        """
        Returns true if value is floating point.
        """
        return self._float


    def step( self ):
        """
        Returns the step size of this value.
        """
        return self._step


    def _flagEnable( self, lastValue, enable: bool ):
        """
        Enable / Disable from flag, behaves like _tryParseElement.
        """
        # get default value
        if( lastValue == None ):
            lastValue = self._default

        if( enable == True ):
            newValue = lastValue + 1
            if( self.max() < newValue ):
                if( self.clamp () ):
                    newValue = self.max ()
                else:
                    return( Value.PARSE_INVALID_VALUE, "expected value <= " + str( self.max() ) )
            return( Value.PARSE_SUCCEED, newValue)
        else:
            newValue = lastValue - 1
            if( self.min() > newValue ):
                if( self.clamp () ):
                    newValue = self.min ()
                else:
                    return( Value.PARSE_INVALID_VALUE, "expected value >= " + str( self.min() ) )
            return( Value.PARSE_SUCCEED, newValue)


    def _tryParseElement( self, context: object, data: str ):
        """
        Try to parse number value.
        """
        # calculate bounds, check if sign will be accepted
        minValue = self.min()
        maxValue = self.max()

        # try to read number
        number = None
        err = None
        try:
            if( self.float () ):
                number = float( data )
            else:
                number = int( data, base = 0 )
        except:
            number = None
            if( self.float () ):
                err = "expected float value"
            else:
                err = "expected integer value"

        # compute data string
        dataStr = "nothing"
        if( data != None ):
            dataStr = "'" + str( data ) + "'"

        # error while parsing?
        if( err != None ):
            return( Value.PARSE_INVALID_VALUE, err + ", got " + dataStr )

        # number in range?
        if( minValue != None ):
            if( minValue > number):
                return( Value.PARSE_INVALID_VALUE, "expected number to be >= " + str( minValue ) + ", got " + dataStr )
        if( maxValue != None ):
            if( maxValue < number):
                return( Value.PARSE_INVALID_VALUE, "expected number to be <= " + str( maxValue ) + ", got " + dataStr )

        # return parsed numner
        return( Value.PARSE_SUCCEED, number )
