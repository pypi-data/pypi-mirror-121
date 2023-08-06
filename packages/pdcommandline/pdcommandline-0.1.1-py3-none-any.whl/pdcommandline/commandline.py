import copy
import sys
from . import application
from . import console
from . import loglevels
from . import formatter
from . import sstr
from . import style
from .commandvalue import *




### ########################################
### Default settings for command line parser
### ########################################


# default command for extending command line
DEFAULT_EXTENT_COMMAND = "@extend@command@line@context@"



### ############################
### Parseable command line items
### ############################


class _Parseable:
    def __init__( self,
                  value: object,
                  description: str,  # can also be a ColorString
                  shortDescription: str = None,
                ):
        """
        Base class of parseable command line item
        """
        self._value = value
        self._description = description
        self._shortDescription = shortDescription
        if( description == None ):
            self._description = value.description ()


    def description( self, detailed: bool = False ):
        if( detailed != False or self._shortDescription == None ):
            return sstr.SStr( self._description )
        else:
            return sstr.SStr( self._shortDescription )


    def value( self ):
        return self._value


    def shortArg( self ):
        return None


    def longArg( self ):
        return None


    @staticmethod
    def _helpOptions( options, detailed: bool ):
        styleSet = style.Defaults.getCommandlineHelpStyle()
        # append selectable options
        if( options != None ):
            output = sstr.SStr( "\n" )
            output = sstr.SStr( styleSet.helpTextDescriptionOptions )
            dOptions = []
            for option in options:
                dOptions.append( { 'name' : "'" + option.name + "'", 'description': option.description( detailed ) } )
            maxOptLength = 0

            # get max length of option names
            for option in dOptions:
                if( len( option['name'] ) > maxOptLength ):
                    maxOptLength = len( option['name'] )
            maxOptLength += 2

            # format options
            for option in dOptions:
                optionKey = sstr.SStr( option['name'], ": ", style = styleSet.helpStyleOptionName )
                optionDescription = option['description']
                if( len( optionDescription ) != 0 ):
                    optionDescription = sstr.SStr( optionDescription, styleSet.helpTextDescriptionOptionEnd, style = styleSet.helpStyleOptionDescription )
                if( styleSet.parameterAlign == True ):
                    padCount = maxOptLength - len( optionKey )
                    if( padCount > 0 ):
                        optionKey = sstr.SStr( optionKey, " " * padCount )
                output = sstr.SStr( output, "\n", optionKey, optionDescription )
            return output
        return sstr.SStr()


    def _helpDescriptionHead( self, context, withParamName: bool, showDefault: bool, showValueDescription: bool, detailed: bool ):
        # get style set
        styleSet = style.Defaults.getCommandlineHelpStyle ()

        # description of parser flag
        output = sstr.SStr( self.description( detailed ), style = styleSet.helpStyleParseableDescription )

        # add value description
        valueName = sstr.SStr( styleSet.helpTextValuePrefix, self.value().name(), styleSet.helpTextValueSuffix, style = styleSet.helpStyleParseableValue )

        # describe type and range
        valueDescription = sstr.SStr( self.value().typeAndRange(), style = styleSet.helpStyleParseableTypeAndRange )
        d = sstr.SStr( self.value().description(), style = styleSet.helpStyleParseableDescription )
        if( showValueDescription == True ):
            if( len( valueDescription ) != 0 ):
                if( len( d ) != 0 ):
                    valueDescription = sstr.SStr( valueDescription, styleSet.helpTextParseableSeparator, d)
                else:
                    valueDescription = d
            else:
                valueDescription = d

            if( withParamName == True ):
                if( len( valueDescription ) != 0 ):
                    output = sstr.SStr( output, ":\n", valueName, ": ", valueDescription )
                else:
                    output = sstr.SStr( output, ":\n", valueName )
            else:
                if( len( valueDescription ) != 0 ):
                    output = sstr.SStr( output, ".\n", valueDescription )
        else:
            if( withParamName == True ):
                output = sstr.SStr( ":\n", valueName )

        # add default value definition
        if( showDefault == True ):
            # annotate if using inherited value from parent context
            inheritDefault = False
            inheritedDefaultValue = None
            if( context != None ):
                parentContext = context.parent()
                if( parentContext != None ):
                    if( parentContext.containsValue( self.value().name(), True ) ):
                        parentValue = parentContext.getValueDefinition( self.value().name() )
                        if ( parentValue.visibleToChildren() ):
                            # can inherit parent definition?
                            inheritDefault = True
                            inheritedDefaultValue = parentContext.get( self.value().name() )

            # show default value
            if( inheritDefault == True ):
                defaultValStr = str( inheritedDefaultValue )
                if( len( defaultValStr ) != 0 ):
                    if( len( output ) != 0 ):
                        output = sstr.SStr( output, styleSet.helpTextDescriptionSeparator )

                    fmtString = sstr.SStr( 
                                            styleSet.helpTextDescriptionDefaultPrefix,
                                            styleSet.helpTextDescriptionInheritedPrefix,
                                            styleSet.helpTextDescriptionValuePrefix,
                                            sstr.SStr( defaultValStr, style = styleSet.helpStyleDescriptionValue ),
                                            styleSet.helpTextDescriptionValueSuffix
                                         )
                    output = sstr.SStr( output, fmtString )
            else:
                defaultValue = self.value().default()
                defaultValStr = str( defaultValue ) if defaultValue != None else ""

                if( defaultValStr != "" ):
                    if( len( output ) != 0 ):
                        output = sstr.SStr( output, styleSet.helpTextDescriptionSeparator )
                    fmtString = sstr.SStr( 
                                            styleSet.helpTextDescriptionDefaultPrefix,
                                            styleSet.helpTextDescriptionValuePrefix,
                                            sstr.SStr( defaultValStr, style = styleSet.helpStyleDescriptionValue ),
                                            styleSet.helpTextDescriptionValueSuffix           
                                         )
                    output = sstr.SStr( output, fmtString )

        # append end of description
        if( len( output ) != 0 ):
            output = sstr.SStr( output, styleSet.helpTextDescriptionEnd )

        return output



class Action( _Parseable ):
    def __init__( self, value: object, actionName: str = None, description: str = None, shortDescription: str = None ):
        """
        Creates a new command line action
        """
        _Parseable.__init__( self, value, description, shortDescription )
        self._actionName = actionName


    def name( self ):
        if( self._actionName != None ):
            return self._actionName
        else:
            return self._value.name ()


    def _helpDescription( self, parentContext, detailed: bool ):
        # get style set
        styleSet = style.Defaults.getCommandlineHelpStyle ()

        # prepare output
        output = self._helpDescriptionHead( parentContext, False, False, False, detailed )

        # got selectable options?
        value = self.value()
        options = None
        if( hasattr( value, 'options' ) ):
            options = self.value().options()
            output = sstr.SStr( output, _Parseable._helpOptions( options, detailed ) )

        # show help on context
        if( styleSet.showRunHelp == True ):
            if( parentContext != None ):
                ctx = parentContext

                callcontexts = []
                while( ctx != None ):
                    callcontexts.append( ctx )
                    ctx = ctx.parent()
                callcontexts.reverse()

                callcontext = sstr.SStr( )
                if( len( callcontexts ) > 0 ):
                    callcontext = sstr.SStr( callcontext, sstr.SStr( callcontexts[0].name(), style = styleSet.helpStyleRunHelpFirstContext ) )
                for index in range( 1, len( callcontexts ) ):
                    callcontext = sstr.SStr( callcontext, " ", sstr.SStr( callcontexts[index].name(), style = styleSet.helpStyleRunHelpFollowContext ) )

                actionStr = sstr.SStr(
                                        styleSet.helpTextRunHelpRunValuePrefix,
                                        sstr.SStr( self.name(), style = styleSet.helpStyleRunHelpRunValue ),
                                        styleSet.helpTextRunHelpRunValueSuffix               
                                     )

                runStr = sstr.SStr(
                                    styleSet.helpTextRunHelpRunPrefix,
                                    " ",
                                    styleSet.helpTextRunHelpRunCmdPrefix,
                                    callcontext,
                                    " ",
                                    actionStr,
                                    " ",
                                    styleSet.helpTextRunHelpRunHelpParameter,
                                    styleSet.helpTextRunHelpRunCmdSuffix,
                                    " ",
                                    styleSet.helpTextRunHelpRunSuffix
                                  )
                output = sstr.SStr( output, "\n", runStr )

        # return help description
        return output
        


class Flag( _Parseable ):
    def __init__( self, value: object, enable: bool, shortArg: str = None, longArg: str = None, description: str = None, group: str = None, shortDescription: str = None  ):
        """
        Command line parameter with following value
        """
        _Parseable.__init__( self, value, description, shortDescription )
        self._shortArg = shortArg
        self._longArg = longArg
        self._enable = enable
        self._group = group


    def shortArg( self ):
        return self._shortArg


    def longArg( self ):
        return self._longArg


    def enable( self ):
        return self._enable


    def group( self ):
        if( self._group == None ):
            return style.Defaults.getCommandlineHelpStyle().defaultParameterGroup
        return self._group


    def _helpDescription( self, parentContext, detailed: bool ):
        """
        Returns the help description for this item
        """
        # get style set
        styleSet = style.Defaults.getCommandlineHelpStyle ()

        # descript parser flag
        output = self.description( detailed ).asLinear()

        if( output != None ):
            output += styleSet.helpTextDescriptionEnd.asLinear()
        return output



class Parameter( Flag ):
    def __init__( self, value: object, shortArg: str = None, longArg: str = None, paramName: str = None, description: str = None, group: str = None, shortDesciption: str = None ):
        """
        Command line parameter with following value
        """
        _Parseable.__init__( self, value, description, shortDesciption )
        self._shortArg = shortArg
        self._longArg = longArg
        self._group = group
        self._paramName = paramName


    def shortArg( self ):
        return self._shortArg


    def longArg( self ):
        return self._longArg


    def group( self ):
        if( self._group == None ):
            return style.Defaults.getCommandlineHelpStyle().defaultParameterGroup
        return self._group


    def name( self ):
        """
        Returns the name of the parameter
        """
        if( self._paramName != None ):
            return self._paramName
        else:
            return self._value.name ()


    def _helpDescription( self, parentContext, detailed ):
        """
        Returns the help description for this item
        """
        # get head
        output = self._helpDescriptionHead( parentContext, True, True, True, detailed ).asLinear()

        # got selectable options?
        value = self.value()
        options = None
        if( hasattr( value, 'options' ) ):
            options = self.value().options()
            output += _Parseable._helpOptions( options, detailed ).asLinear()

        # return help description
        return output




class Argument (_Parseable):
    def __init__( self, value: object, argName: str = None, description: str = None, shortDescription: str = None ):
        """
        Parseable argument
        """
        _Parseable.__init__( self, value, description, shortDescription )
        self._argName = argName


    def name( self ):
        """
        Returns the name of the argument
        """
        if( self._argName != None ):
            return self._argName
        else:
            return self._value.name ()


    def _helpDescription( self, parentContext, detailed: bool ):
        output = self._helpDescriptionHead( parentContext, False, False, False, detailed ).asLinear()

        # got selectable options?
        value = self.value()
        options = None
        if( hasattr( value, 'options' ) ):
            options = self.value().options()
            output += _Parseable._helpOptions( options, detailed ).asLinear()

        # return help description
        return output




class Context:
    def __init__( self, name: str, description: str, shortDescription: str = None ):
        """
        Initialize a new context
        """
        self._name             = name
        self._description      = description
        self._parent           = None
        self._values           = []
        self._parseables       = []
        self._valueData        = {}
        self._valueSet         = []
        self._shortDescription = shortDescription


    def name( self ):
        """
        Returns the name of this parse context
        """
        return self._name
        

    def description( self, detailed: bool = False ):
        """
        Returns the description of this context
        """
        if( detailed != False or self._shortDescription == None ):
            return sstr.SStr( self._description )
        else:
            return sstr.SStr( self._shortDescription )


    def parent( self ):
        """
        Returns the parent of this parse context
        """
        return self._parent


    def addParsable( self, *parseables ):
        """
        Registers a parseable object
        """
        for parseable in parseables:
            value = parseable.value ()
            self._addValue( value )

            # check type
            isFlag = isinstance( parseable, Flag )
            isParameter = isinstance( parseable, Parameter )

            # check if we are adding a flag or parameter
            if( isFlag or isParameter ):
                short = parseable.shortArg ()
                long = parseable.longArg ()
                if( short != None ):
                    # check if we got a parseable with the same short arg registered
                    for p in self._parseables:
                        if( p.shortArg() == short ):
                            assert False, "A parsable with the short name '-" + short + "' is already registered."
                if( long != None ):
                    # check if we got a parseable with the same short arg registered
                    for p in self._parseables:
                        if( p.longArg() == long ):
                            assert False, "A parsable with the long name '--" + long + "' is already registered."

            else:
                # do not allow to add arguments or actions after an array element
                hasArray = False
                for p in self._parseables:
                    if( isinstance( p, (Argument, Action) ) ):
                        if( p.value().array() ):
                            hasArray = True
                if( hasArray ):
                    assert False, "Can not add Argument or Action after an array"

                # do not allow non-optionals after optionals
                isOptional = parseable.value().optional()
                if( not isOptional ):
                    gotOptionalBefore = False
                    for p in self._parseables:
                        if( isinstance( p, (Argument, Action) ) ):
                            if( p.value().optional() ):
                                gotOptionalBefore = True
                                break
                    assert gotOptionalBefore == False, "Can not add non-optional parseable after optional parseable" 

            # add to list of parseable items
            self._parseables.append( parseable )


    def parseables( self ):
        """
        Returns a list of all known parseables
        """
        return self._parseables


    def valueNames( self, local: bool = True ):
        """
        List all value keys known by context
        """
        return self._collectValueNames( local, False, [] )


    def getValueDefinition( self, valueName: str ):
        """
        Returns a value definition by name, None if not found
        """
        return self._getValueDefinition( valueName, False )


    def containsValue( self, valueName: str, inherit: bool ):
        """
        Returns True if the context contains a value identified by name
        """
        # defined in local context?
        for p in self._parseables:
            if( p.value().name() == valueName):
                return True

        # inheritable from parent scope and visible to child scopes?
        if( inherit == True ):
            if( self._parent != None ):
                parentVal = self._parent.getValueDefinition( valueName )
                if( parentVal != None ):
                    if( parentVal.visibleToChildren () ):
                        return True

        # value not contained        
        return False


    def isset( self, valueName: str, local: bool ):
        """
        Returns true if value is set on context.
        """
        return self._isset( valueName, local, False )


    def get( self, valueName: str ):
        """
        Get value from context or return default value if not set, returns None if value is unknown
        """
        # get value
        value = self.getValueDefinition( valueName )
        if( value == None ):
            return None

        # get data from array value
        if( value.array() == True ):
            if( value.inheritParentValue() ):
                data = []
                if( self.parent() != None ):
                    data = self.parent().get( valueName )
                    if( data == None ):
                        data = []
                localData = None
                if( self.isset( valueName, True ) ):
                    localData = self._valueData[valueName]
                else:
                    localData = value.default ()
                if( localData != None ):
                    data = data + localData
                return data
            else:
                if( self.isset( valueName, True ) ):
                    return self._valueData[valueName]
                else:
                    if( value.default() != None ):
                        return value.default()
                    else:
                        return []
        
        # get data from non array value
        else:
            if( self.isset( valueName, True ) ):
                return self._valueData[valueName]
            else:
                # can inherit from parent context?
                if( value.inheritParentValue() ):
                    if( self.parent() != None ):
                        if( self.parent().isset( valueName, False ) ):
                            return self.parent().get( valueName )
                # return default value
                return value.default()


    def parseCommandline( self, argv: list = None ):
        """
        Parse command line on this context
        """
        # get copy of command line arguments
        if( argv == None ):
            data = _CommandLineData( sys.argv )
        else:
            data = _CommandLineData ( argv )

        # instanciate context
        instance = self._create( None )

        # want command line extension?
        extent = None
        if( data.peek () == DEFAULT_EXTENT_COMMAND ):
            data.pop()
            extent = _ExtentContext( )

        # run parser on context
        instance._parse( data, True, extent )

        # extention done?
        if( extent != None ):
            application.terminate( 0 )

        # return parsed instance
        return instance


    def _create(self, parent):
        """
        Create sub context and assign with parent
        """
        tmp         = copy.deepcopy( self )
        tmp._parent = parent
        return tmp


    def _addValue( self, value: object ):
        """
        Add a value to this context
        """
        for v in self._values:
            if( v.name() == value.name() ):
                if( v == value ):
                    return
                else:
                    assert False, "A different value with name '" + str( v.name() ) + "' is already registered at this context"
        self._values.append( value )


    def _collectValueNames( self, local: bool, inherit: bool, elements: list ):
        """
        Collect the names of all reachable values
        """
        # collect value from parent
        if( local == False ):
            if( self.parent() != None ):
                elements = self.parent()._collectValueNames( local, True, elements )
        
        # collect local values
        if( inherit == True ):
            for v in self._values:
                if( v.visibleToChildren() ):
                    if( not v.name() in elements ):
                        elements.append( v.name () )
        else:
            for v in self._values:
                if( not v.name() in elements ):
                    elements.append( v.name () )
        return elements


    def _getValueDefinition( self, valueName: str, inherit: bool ):
        """
        Returns a value definition by name, None if not found
        """
        for v in self._values:
            if( v.name() == valueName ):
                if( inherit == False ):
                    return v
                else:
                    if( v.visibleToChildren() ):
                        return v
        if( self.parent() != None ):
            return self.parent().getValueDefinition( valueName, True )
        return None


    def _setFlag( self, valueName: str, enable: bool ):
        """
        Set a value from flag,
        Returns a tuple( parseResult, parseValue )
        """
        # find value definition
        valueInstance = None
        for v in self._values:
            if( v.name() == valueName ):
                valueInstance = v
                break

        # check if value is present
        if( valueInstance == None ):
            return( Value.PARSE_UNKOWN_VALUE, valueName )


        # already set in parent and child override is not allowed?
        alreadySetInParent = False
        if( self.parent() != None ):
            if( self.parent().isset( valueName, False ) ):
                alreadySetInParent = True
        if( alreadySetInParent ):
            if( valueInstance.allowOverrideInChildren() == False ):
                return( Value.PARSE_VALUE_ALREADY_SET, valueName )

        # working on array?
        if( valueInstance.array() ):
            # process on array
            arrData = []
            if( valueName in self._valueSet ):
                arrData = self._valueData[valueName]
            arrData.append( enable )
            self._valueData[valueName] = arrData
            self._valueSet.append( valueName )
            return ( Value.PARSE_SUCCEED, self._valueData[valueName] )

        # not working on an array..
        else:
            # try to set value from flag...
            alreadySet = ( valueName in self._valueSet )
            if( alreadySet == False ):
                # set value by flag
                ( parseResult, parseValue ) = valueInstance._flagEnable( self.get (valueName ), enable )
                if( parseResult == Value.PARSE_SUCCEED ):
                    self._valueData[valueName] = parseValue
                    if( not valueName in self._valueSet ):
                        self._valueSet.append( valueName )
                    return ( Value.PARSE_SUCCEED, self._valueData[valueName] )
                elif( parseResult == Value.PARSE_SUCCEED_LIST ):
                    assert False, "Value returns list but is not an array element"
                return (parseResult, parseValue)

            else:
                if( valueInstance.allowOverride() ):
                    ( parseResult, parseValue ) = valueInstance._flagEnable( self.get (valueName ), enable )
                    if( parseResult == Value.PARSE_SUCCEED ):
                        self._valueData[valueName] = parseValue
                        return ( Value.PARSE_SUCCEED, self._valueData[valueName] )
                    elif( parseResult == Value.PARSE_SUCCEED_LIST ):
                        assert False, "Value returns list but is not an array element"
                    return (parseResult, parseValue)
                else:
                    return( Value.PARSE_VALUE_ALREADY_SET, valueName )


    def _set( self, valueName: str, data, isList: bool ):
        """
        Set a value by name,
        Returns a tuple( parseResult, parseValue )
        """
        # find value definition
        valueInstance = None
        for v in self._values:
            if( v.name() == valueName ):
                valueInstance = v
                break

        # check if value is present
        if( valueInstance == None ):
            return( Value.PARSE_UNKOWN_VALUE, valueName )

        # already set in parent and child override is not allowed?
        alreadySetInParent = False
        if( self.parent() != None ):
            if( self.parent().isset( valueName, False ) ):
                alreadySetInParent = True
        if( alreadySetInParent ):
            if( valueInstance.allowOverrideInChildren() == False ):
                return( Value.PARSE_VALUE_ALREADY_SET, valueName )

        # working on array?
        if( valueInstance.array() ):
            # process on array
            arrData = []
            if( valueName in self._valueSet ):
                arrData = self._valueData[valueName]
            if( isList == True ):
                arrData = arrData + data
            else:
                arrData.append( data )
            self._valueSet.append( valueName )
            self._valueData[valueName] = arrData
            return( Value.PARSE_SUCCEED, arrData )

        # not working on an array..
        else:
            # try to set value
            alreadySet = ( valueName in self._valueSet )
            if( alreadySet == False ):
                self._valueSet.append( valueName )
                if( isList == True ):
                    self._valueData[valueName] = data[-1]
                else:
                    self._valueData[valueName] = data
                return( Value.PARSE_SUCCEED, data )
            else:
                if( valueInstance.allowOverride() ):
                    if( isList == True ):
                        self._valueData[valueName] = data[-1]
                    else:
                        self._valueData[valueName] = data
                    return( Value.PARSE_SUCCEED, data )
                else:
                    return( Value.PARSE_VALUE_ALREADY_SET, valueName )


    def _isset( self, valueName: str, local: bool, inherit: bool ):
        """
        Returns true if value is set on context.
        """
        # check if set on local node
        if( valueName in self._valueSet ):
            if( inherit == True ):
                value = self.getValueDefinition( valueName )
                if( value.visibleToChildren() ):
                    return True
            else:
                return True

        # check inside parent node
        if( local == False):
            if( self.parent () != None ):
                return self.parent ()._isset( valueName, local, True )

        # not set
        return False


    def _parseErrorShow( self, text, context, extent: object ):
        """
        Displays a parsing error
        """
        # if extent requested
        if( extent != None ):
            extent.onExtendFailed( self )

        # show error
        if( text != None ):
            if( text != "" ):
                console( "error parsing commandline: " + text + "\n", loglevels.LOG_ALWAYS )
        ctxHelp = None
        if( context != None ):
            ctxHelp = "--help"
            currentCtx = self
            while( currentCtx != None ):
                ctxHelp = currentCtx.name() + " " + ctxHelp
                currentCtx = currentCtx.parent()

        if( ctxHelp != None ):
            console( "run '" + ctxHelp + "' for more informations.", loglevels.LOG_ALWAYS )
        application.terminate( -1 )


    def _parseErrorMissing( self, value: object, extent: object ):
        """
        Value definition missing, show error and exit application
        """
        # if extent requested
        if( extent != None ):
            extent.onExtendFailed( self )

        # show error
        missing = []

        # find parseables to define missing value
        for p in self._parseables:
            pv = p.value()
            if( pv.name() == value.name() ):
                if( isinstance( p, ( Argument, Action ) ) ):
                    missing.append( "argument '" + p.name() + "'")
                else:
                    # process flags / parameters
                    if( isinstance( p, Flag ) ):
                        flagName = None
                        if( p.longArg() != None ):
                            flagName = '--' + p.longArg()
                        elif( p.shortArg() != None ):
                            flagName = '-' + p.shortArg()
                        if( flagName != None ):
                            missing.append( "flag '" + flagName + "'")
                    elif( isinstance( p, Parameter ) ):
                        parameterName = None
                        if( p.longArg() != None ):
                            parameterName = '--' + p.longArg()
                        elif( p.shortArg() != None ):
                            parameterName = '-' + p.shortArg()
                        if( parameterName != None ):
                            missing.append( "parameter '" + parameterName + "'")

        # display parsing error
        if( len( missing ) == 0 ):
            errorText = "missing value '" + value.name() + "'."
        else:
            errorText = ""
            for index in range( 0, len( missing ) ):
                if( index > 0):
                    if( index == ( len ( missing ) - 1 ) ):
                        errorText += ' or '
                    else:
                        errorText += ', '
                errorText += missing[index]
            errorText += " needs to be specified."
        self._parseErrorShow( errorText, self, extent )


    def _parseErrorUnexpectedArgument( self, arg, extent: object ):
        """
        When parsing an unexpected argument...
        """
        # if extent requested
        if( extent != None ):
            extent.onExtendFailed( self )

        # show error
        errText = "did not expect extra argument '" + arg + "'."
        self._parseErrorShow( errText, self, extent )


    def _parseErrorUnexpectedParameter( self, param, extent: object ):
        """
        When parsing an unexpected flag or parameter
        """
        # if extent requested
        if( extent != None ):
            extent.onExtendFailed( self )

        # show error
        pText = "flag"
        if( param.startswith( '--' ) ):
            pText = "parameter"
        errText = pText + " '" + param + "' is unknown."
        self._parseErrorShow( errText, self, extent )


    def _parseErrorNoParameterExpectedAfterArgument( self, invocation: str, isParameter: bool, extent: object ):
        """
        When parsing a flag or parameter after an argument.
        """
        # if extent requested
        if( extent != None ):
            extent.onExtendFailed( self )

        # show error
        errText = "did not expect a " + ("parameter" if isParameter else "flag" ) + " ('" + invocation + "') after an argument."
        self._parseErrorShow( errText, self, extent )


    def _parseError( self, parseResult, parseValue, extent: object, parameter: object, longInvocation: bool, argument: object ):
        # if extent requested
        if( extent != None ):
            extent.onExtendFailed( self )

        # format error source
        if( parameter != None ):
            if( isinstance( parameter, Parameter ) ):
                errStr = "parameter"
            else:
                errStr = "flag"
            if( longInvocation == True ):
                errStr += " --" + parameter.longArg()
            else:
                errStr += " -" + parameter.shortArg()
        else:
            errStr = "argument <" + argument.name() + ">"

        # format error
        if( parseResult == Value.PARSE_INVALID_VALUE ):
            self._parseErrorShow( "invalid value for " + errStr + ": " + parseValue + ".", self, extent )
        elif( parseResult == Value.PARSE_UNKOWN_VALUE ):
            self._parseErrorShow( "can not assign " + errStr + " to value '" + parseValue + "'", self, extent )
        elif( parseResult == Value.PARSE_VALUE_ALREADY_SET ):
            self._parseErrorShow( errStr + " is already defined.", self, extent )
        elif( parseResult == Value.PARSE_MISSING_VALUE ):
            self._parseErrorShow( "missing value for " + errStr, self, extent )
        else:
            self._parseErrorShow( "unknown error while parsing " + errStr, self, extent )


    def _showHelpForParameter( self, parentContext, parameter: object, longInvocation: bool ):
        """
        Show help content for a single parameter
        """
        description = formatter.Table()
        description.caption( parameter._helpDescription( parentContext, detailed = True ) )
        console( description, loglevels.LOG_ALWAYS )


    def _showHelp( self, parentContext, parameter: object = None, longInvocation: bool = False):
        """
        Show help and exit.
        """
        # get style set
        styleSet = style.Defaults.getCommandlineHelpStyle ()

        # show description of current context (not when help is requested on a parameter)
        if( parameter == None ):
            descrString = self.description( True )
            if( ( descrString != None ) and ( len( descrString ) > 0 ) ):
                description = formatter.Table()
                descrText = styleSet.helpTextDescriptionHeadLine.asLinear ()
                descrText += sstr.SStr( descrString, ".", style = styleSet.helpStyleContextDescr ).asLinear()
                description.caption( descrText )
                console( description, level = loglevels.LOG_ALWAYS )
                console( '', level = loglevels.LOG_ALWAYS )

        # get canonical invocation info
        contextHelpStrs = [ str( self.name () ) ]
        ctx = self.parent ()
        while( ctx != None ):
            contextHelpStrs.append( str( ctx.name() ) )
            ctx = ctx.parent()
        
        # format canonical usage
        ctxHelp = sstr.LStr()
        ctxHelp += sstr.SStr( styleSet.helpTextUsage ).asLinear()
        hsFirst = True
        contextHelpStrs.reverse()
        for hs in contextHelpStrs:
            if( hsFirst == False ):
                ctxHelp += sstr.SStr( " " ).asLinear ()
                ctxStyle = styleSet.helpStyleFollowContext
            else:
                hsFirst = False
                ctxStyle = styleSet.helpStyleFirstContext
            ctxHelp += sstr.SStr( hs, style = ctxStyle ).asLinear()

        # format parameters
        if( parameter != None ):
            # display help for a concrete parameter
            if( longInvocation == True ):
                paramHelp = sstr.SStr( " --", parameter.longArg(), style = styleSet.helpStyleLongParameter )
            else:
                paramHelp = sstr.SStr( " -", parameter.shortArg(), style = styleSet.helpStyleShortParameter )
            ctxHelp += paramHelp.asLinear()

            # format parameter value
            paramSValue = sstr.SStr( styleSet.helpTextValuePrefix, sstr.SStr( parameter.value().name(), style = styleSet.helpStyleValueName ), styleSet.helpTextValueSuffix, style = styleSet.helpStyleValue )
            paramValue = sstr.SStr( paramSValue, style = styleSet.helpStyleParameterValue )
            ctxHelp += sstr.SStr( " " ).asLinear()
            ctxHelp += paramValue.asLinear()

            # format as table
            ctxHelpTable = formatter.Table ()
            ctxHelpTable.caption( ctxHelp )
            console( ctxHelpTable, level = loglevels.LOG_ALWAYS )
            console( '', level = loglevels.LOG_ALWAYS )
            self._showHelpForParameter( parentContext, parameter, longInvocation )
            application.terminate( 0 )

        else:
            # got parameters?
            gotParameters = False
            for p in self._parseables:
                if( isinstance( p, ( Flag, Parameter ) ) ):
                    gotParameters = True
                    break
            if( gotParameters == True ):
                ctxHelp += sstr.SStr( " " ).asLinear()
                ctxHelp += styleSet.helpTextParameters.asLinear()

            # list arguments
            for p in self._parseables:
                if( isinstance( p, ( Argument, Action ) ) ):
                    isOptional = p.value().optional()
                    isArray = p.value().array()
                    isAction = isinstance( p, Action )

                    # get parameter string
                    pname = p.name()
                    if( pname != None ):
                        pstr = sstr.SStr(
                                            styleSet.helpTextValuePrefix,
                                            sstr.SStr( p.name(), style = styleSet.helpStyleValue ),
                                            styleSet.helpTextValueSuffix
                                        )
                    else:
                        pstr = sstr.SStr(
                                            styleSet.helpTextValuePrefix,
                                            sstr.SStr( p.value().name(), style = styleSet.helpStyleValue ),
                                            styleSet.helpTextValueSuffix
                                        )

                    # get styled parameter string
                    if( isAction == True ):
                        pstr = sstr.SStr( pstr, style = styleSet.helpStyleAction )
                    else:
                        pstr = sstr.SStr( pstr, style = styleSet.helpStyleArgument )

                    # format optional and array modifiers
                    if( isAction == True):
                        astr = sstr.SStr( pstr, " ", styleSet.helpTextActionParams )
                        if( isArray == True ):
                            pstr = sstr.SStr( 
                                                styleSet.helpTextActionArrayBegin,
                                                astr,
                                                " ",
                                                styleSet.helpTextActionScopeEnd,
                                                styleSet.helpTextActionArrayEnd,
                                                " ",
                                                astr, 
                                                style = styleSet.helpStyleActionArray
                                            )
                        else:
                            pstr = astr
                    else:
                        if( isOptional == True):
                            pstr = sstr.SStr( styleSet.helpTextOptionalBegin, pstr )
                        if( ( isArray == True ) and ( isAction == False ) ):
                            pstr = sstr.SStr( pstr, styleSet.helpTextArrayModifier )
                        if( isOptional == True ):
                            pstr = sstr.SStr( pstr, styleSet.helpTextOptionalEnd, style = styleSet.helpStyleOptional )

                    # append styled parameter to current help string
                    if( len( ctxHelp ) > 0 ):
                        ctxHelp += sstr.SStr( " " ).asLinear()
                    ctxHelp += pstr.asLinear()

            # format as table
            ctxHelpTable = formatter.Table ()
            ctxHelpTable.caption( ctxHelp )
            console( ctxHelpTable, level = loglevels.LOG_ALWAYS )

            # show all arguments and actions
            helpTable = formatter.Table( layout = style.Defaults.getCommandlineHelpStyle().tableLayout )
            firstArg = True
            for p in self._parseables:
                if( isinstance( p, ( Argument, Action ) ) ):
                    if( firstArg == True ):
                        helpTable.caption( sstr.SStr( styleSet.helpTextHeadlineArguments, style = styleSet.helpStyleHeadlineArguments ) )
                    elif( style.Defaults.getCommandlineHelpStyle().parameterNewLine == True ):
                        helpTable.space()
                    firstArg = False

                    # format arguments as table
                    head = sstr.SStr(
                                        styleSet.helpTextValuePrefix,
                                        sstr.SStr( p.name(), style = styleSet.helpStyleValueName ),
                                        styleSet.helpTextValueSuffix
                                    )
                    if( isinstance( p, Action ) ):
                        head = sstr.SStr( head, style = styleSet.helpStyleActionKey )
                    else:
                        head = sstr.SStr( head, style = styleSet.helpStyleArgumentKey )
                    argumentDescription = p._helpDescription( parentContext, detailed = False )
                    helpTable.row([head, argumentDescription])

            # group flags and parameters by group, preserve order
            paramGroups = []
            for p in self._parseables:
                if( isinstance( p, ( Flag, Parameter ) ) ):
                    groupIndex = None
                    for g in range( len ( paramGroups ) ):
                        group = paramGroups[g]
                        if( p.group() == group["groupName"] ):
                            groupIndex = g
                            break
                    if( groupIndex == None ):
                        paramGroups.append(
                            {
                                "groupName": p.group(),
                                "members": [p]
                            }
                        )
                    else:
                        paramGroups[groupIndex]['members'].append( p )

            # render flags and parameters by group
            for group in paramGroups:
                if( len( helpTable.content ) > 0 ):
                    helpTable.space()
                name = sstr.SStr( group["groupName"], style = styleSet.helpStyleHeadlineParamGroup )
                if( group["groupName"] != "" ):
                    name = sstr.SStr( name, " " )
                name = sstr.SStr( name, styleSet.helpTextHeadlineParameters, style = styleSet.helpStyleHeadlineParameters )
                helpTable.caption( name )

                # render all flags and parameters to table
                firstParameter = True
                for member in group['members']:
                    memberKey = sstr.SStr()
                    if( ( not member.longArg() in ( None, "" ) ) ):
                        memberKey = sstr.SStr( memberKey, sstr.SStr( "--", sstr.SStr( member.longArg(), style = styleSet.helpStyleLongParameterName ), style = styleSet.helpStyleLongParameter ) )
                    if( ( not member.shortArg() in ( None, "" ) ) ):
                        if( len( memberKey ) != 0 ):
                            memberKey = sstr.SStr( memberKey, styleSet.helpTextParameterSeparator )
                        memberKey = sstr.SStr( memberKey, sstr.SStr( "-", sstr.SStr( member.shortArg(), style = styleSet.helpStyleShortParameterName ), style = styleSet.helpStyleShortParameter ) )
                    if( len( memberKey ) != 0 ):
                        if( isinstance( member, Parameter ) ):
                            memberKey = sstr.SStr( memberKey, " " )

                            memberKeyValue = sstr.SStr(
                                                        styleSet.helpTextValuePrefix,
                                                        sstr.SStr( member.value().name(), style = styleSet.helpStyleValueName ),
                                                        styleSet.helpTextValueSuffix,
                                                        style = styleSet.helpStyleValue
                                                      )
                            memberKeyValue = sstr.SStr( memberKeyValue, style = styleSet.helpStyleParameterValue )
                            memberKey = sstr.SStr( memberKey, memberKeyValue )
                            
                    memberDescription = member._helpDescription( parentContext, detailed = False )
                    if( len( memberKey ) != 0 ):
                        if( ( firstParameter == False ) and ( style.Defaults.getCommandlineHelpStyle().parameterNewLine == True ) ):
                            helpTable.space()
                        helpTable.row( [memberKey, memberDescription] )
                    firstParameter = False

            # write help table
            if( len( helpTable.content ) > 0 ):
                console( "", level = loglevels.LOG_ALWAYS )
                console( helpTable, level = loglevels.LOG_ALWAYS )

            # help request printed, exit command line tool with success
            application.terminate( 0 )


    def _parse( self, data, isTopContext: bool, extent ):
        """
        Run parser on current context
        """
        # current argument
        argumentParsed = False
        argumentIndex = 0

        # split registered parseables
        namedParseables = []
        unnamedParseables = []
        for p in self._parseables:
            if( isinstance( p, (Flag, Parameter) ) ):
                namedParseables.append( p )
            else:
                unnamedParseables.append( p )

        # parse command line arguments
        currentData = data.pop()
        while( currentData != None):
            lastData = data.isLast ()

            # process command line data
            parseAsArgument = False

            allowScopeEnd = self.parent() != None
            for argId in range( argumentIndex, len( unnamedParseables ) ):
                if( unnamedParseables[argId].value().optional() == False ):
                    allowScopeEnd = False
                    break

            if( currentData == '--' ):
                if( ( extent != None ) and ( lastData == True ) ):
                    if( argumentIndex == 0 ):
                        extent.onMinusMinus( self, currentData, allowScopeEnd )
                    else:
                        if( argumentIndex < len( unnamedParseables ) ):
                            extent.onArgumentOrAction( self, unnamedParseables[argumentIndex].value() , '--' )
                        else:
                            if( self._parent != None ):
                                extent.onContextEnd( self, currentData )
                            application.terminate( 0 )
                else:
                    if( self.parent() == None ):
                        # no parent to process further data
                        self._parseErrorUnexpectedArgument( currentData, extent )
                    else:
                        # end context, continue parsing on parent node
                        break

            elif( currentData == '-' ):
                if( ( extent != None ) and ( lastData == True ) and ( argumentIndex == 0 ) ):
                    extent.onMinus( self, '-', '', allowScopeEnd )
                else:
                    # parse as argument
                    parseAsArgument = True

            elif( currentData.startswith( '--' ) ):
                if( ( extent != None ) and ( lastData == True ) and ( argumentIndex == 0 ) ):
                    extent.onMinusMinus( self, currentData, False )
                else:
                    # parse long arg
                    flagOrParameter = None
                    for p in self._parseables:
                        if( p.longArg() == currentData[2:] ):
                            flagOrParameter = p
                            break
                    if( flagOrParameter == None ):
                        if( currentData == '--help'):
                            if( extent == None ):
                                self._showHelp( self )
                        else:
                            self._parseErrorUnexpectedParameter( currentData, extent )

                    # parse flag or parameter?
                    if( currentData == '--help' ):
                        # continue parsing on next argument
                        currentData = data.pop()
                    else:
                        if( isinstance( flagOrParameter, Parameter ) ):
                            paramData = data.pop()
                            lastData = data.isLast ()
                            # parse parameter data
                            if( argumentParsed == True ):
                                self._parseErrorNoParameterExpectedAfterArgument( currentData, True, extent )
                            # extend current parameter?
                            if( ( extent != None ) and ( lastData == True ) ):
                                extent.onParameterValue( self, flagOrParameter, "", paramData )
                            else:
                                (parseResult, parseValue) = flagOrParameter.value()._tryParse( self, paramData )
                                if( parseResult == Value.PARSE_SUCCEED):
                                    # parse succeeded
                                    isList = False
                                elif( parseResult == Value.PARSE_SUCCEED_LIST):
                                    # parse succeeded, got list
                                    isList = True
                                else:
                                    # show help on parameter ?
                                    if( paramData == '--help' ):
                                        if( extent == None ):
                                            self._showHelp( self, parameter = flagOrParameter, longInvocation = True )
                                    else:
                                        self._parseError( parseResult, parseValue, extent, flagOrParameter, True, None )

                                # set parameter data
                                if( paramData != '--help' ):
                                    (parseResult, parseValue) = self._set (flagOrParameter.value().name(), parseValue, isList )
                                    if( not parseResult in ( Value.PARSE_SUCCEED, Value.PARSE_SUCCEED_LIST ) ):
                                        # handle parsing error
                                        self._parseError( parseResult, parseValue, extent, flagOrParameter, True, None )
                                    currentData = data.pop()

                        else:
                            # set from flag
                            if( argumentParsed == True ):
                                self._parseErrorNoParameterExpectedAfterArgument( currentData, False, extent )
                            (parseResult, parseValue) = self._setFlag (flagOrParameter.value().name(), flagOrParameter.enable() )
                            if( not parseResult in ( Value.PARSE_SUCCEED, Value.PARSE_SUCCEED_LIST ) ):
                                self._parseError( parseResult, parseValue, extent, flagOrParameter, True, None )

                            # continue parsing on next argument
                            currentData = data.pop()


            elif( currentData.startswith( '-' ) ):
                remainingData = currentData[1:]
                currentExtentPrefix = '-'
                while( len ( remainingData ) > 0 ):
                    # parse short arg
                    flagOrParameter = None
                    flagValue = remainingData[0]
                    for p in self._parseables:
                        if( p.shortArg() == flagValue ):
                            flagOrParameter = p
                            break
                    if( flagOrParameter == None ):
                        self._parseErrorUnexpectedParameter( '-' + flagValue, extent )
                    currentExtentPrefix += flagValue

                    # remove flag
                    remainingData = remainingData[1:]

                    # parse flag or parameter?
                    if( isinstance( flagOrParameter, Parameter ) ):
                        if( argumentParsed == True ):
                            self._parseErrorNoParameterExpectedAfterArgument( '-' + flagValue, True, extent )
                        paramData = remainingData
                        if( paramData == "" ):
                            if( not data.isLast () ):
                                currentExtentPrefix = ""
                            paramData = data.pop()
                            lastData = data.isLast ()

                        # extent current parameter value?
                        if( ( extent != None ) and ( lastData == True ) ):
                            extent.onParameterValue( self, flagOrParameter, currentExtentPrefix, paramData if paramData != None else '' )

                        # parse parameter data
                        (parseResult, parseValue) = flagOrParameter.value()._tryParse( self, paramData )
                        if( not parseResult in ( Value.PARSE_SUCCEED, Value.PARSE_SUCCEED_LIST ) ):
                            if( paramData == '--help' ):
                                self._showHelp( self, parameter = flagOrParameter, longInvocation = False )
                            self._parseError( parseResult, parseValue, extent, flagOrParameter, False, None )

                        # set parameter data
                        (parseResult, parseValue) = self._set (flagOrParameter.value().name(), parseValue, parseResult == Value.PARSE_SUCCEED_LIST )
                        if( not parseResult in ( Value.PARSE_SUCCEED, Value.PARSE_SUCCEED_LIST ) ):
                            self._parseError( parseResult, parseValue, extent, flagOrParameter, False, None )

                        # continue parsing on next argument
                        break
                    else:
                        # set from flag
                        if( argumentParsed == True ):
                            self._parseErrorNoParameterExpectedAfterArgument( '-' + flagValue, False, extent )
                        (parseResult, parseValue) = self._setFlag (flagOrParameter.value().name(), flagOrParameter.enable() )
                        if( not parseResult in ( Value.PARSE_SUCCEED,  Value.PARSE_SUCCEED_LIST ) ):
                            self._parseError( parseResult, parseValue, extent, flagOrParameter, False, None )

                        # extend next flag or parameter
                        if( ( extent != None ) and ( lastData == True ) ):
                            if( remainingData in ( "", None ) ):
                                extent.onMinus( self, currentExtentPrefix, '', allowScopeEnd )

                # run on next frame
                currentData = data.pop()

            else:
                # parse as argument
                parseAsArgument = True

            # parse argument
            if( parseAsArgument ):
                if( argumentIndex >= len( unnamedParseables ) ):
                    # extent end of scope?
                    if( self._parent != None):
                        if( extent != None ):
                            if ( currentData in ( '-', '--' ) ):
                                extent.onContextEnd( self, currentData )
                    # extra argument?
                    self._parseErrorUnexpectedArgument( currentData, extent )
                argValue = unnamedParseables[argumentIndex]
                if( ( extent != None ) and ( lastData == True ) ):
                    # extend argument
                    extent.onArgumentOrAction( self, argValue, currentData )
                else:
                    (parseResult, parseValue) = argValue.value()._tryParse( self, currentData )
                    if( parseResult in( Value.PARSE_SUCCEED, Value.PARSE_SUCCEED_LIST ) ):
                        # is an action?
                        if( isinstance( argValue, Action ) ):
                            # parse action in sub context
                            subContext = parseValue._create( self )
                            subContext._parse( data, False, extent )

                            # set parsed sub context
                            assert parseResult == Value.PARSE_SUCCEED
                            (parseResult, parseValue) = self._set( argValue.value().name(), subContext, False )
                            if( not parseResult in( Value.PARSE_SUCCEED , Value.PARSE_SUCCEED_LIST ) ):
                                self._parseError( parseResult, parseValue, extent, None, False, argValue )
                            else:
                                currentData = data.pop()                        

                        # is an argument?
                        else:
                            # parse argument
                            (parseResult, parseValue) = self._set( argValue.value().name(), parseValue, parseResult == Value.PARSE_SUCCEED_LIST )
                            if( not parseResult in( Value.PARSE_SUCCEED , Value.PARSE_SUCCEED_LIST ) ):
                                self._parseError( parseResult, parseValue, extent, None, False, argValue )
                            else:
                                currentData = data.pop()

                    else:
                        self._parseError( parseResult, parseValue, extent, None, False, argValue )
                    
                    # argument parsed, continue on next one
                    argumentParsed = True
                    if( argValue.value().array() == False ):
                        argumentIndex += 1

        # check for missing values
        for valueName in self.valueNames():
            valueDefinition = self.getValueDefinition( valueName )
            if( valueDefinition.optional() == False ):
                valueIsSet = self.isset( valueName, not valueDefinition.inheritParentValue () )
                if( valueIsSet == False ):
                    # write command line error and exit
                    self._parseErrorMissing( valueDefinition, extent )

        # check for extra arguments on command line
        if( isTopContext == True ):
            extraData = data.peek()
            if( extraData != None ):
                self._parseErrorUnexpectedArgument( extraData, extent )




### ########################
### internal: helper classes
### ########################


class _CommandLineData:
    def __init__( self, argv ):
        """
        Creates a new array of parseable command line data
        """
        self.argv = copy.deepcopy (argv)
        # pop command
        self.command = self.pop()

    def peek( self ):
        """
        Peeks the next command line option, returns None if end is reached.
        """
        if( len( self.argv ) == 0 ):
            return None
        return self.argv[0]
        

    def pop( self ):
        """
        Pops the next command line option, returns None if end is reached.
        """
        if( len( self.argv ) == 0 ):
            return None
        data = self.argv[0]
        self.argv = self.argv[1:]
        return data


    def isLast( self ):
        """
        Returns true if this is the last command line argument
        """
        return len( self.argv ) == 0




class _ExtentContext:
    def __init( self ):
        """
        Context for extenting command lines.
        """
        pass


    def printExtList( self, extList ):
        extList = sorted( extList )
        for ext in extList:
            sys.stdout.write( ext + '\n' )
        sys.stdout.flush()


    def onExtendFailed( self, context ):
        """
        Fail on command line extension
        """
        application.terminate( 90 )


    def onArgumentOrAction( self, context, argumentValue, currentData ):
        """
        Extend argument or action
        """
        value = argumentValue.value()
        ( eResult, eData ) = value._extent( context, currentData )
        if( eResult == Value.EXTENT_FAIL ):
            application.terminate( 91 )
        else:
            if( eData != None ):
                items = []
                for e in eData:
                    items.append( e )
                self.printExtList( items )
        application.terminate( 0 )


    def onParameterValue( self, context, parameter, currentPrefix, paramData ):
        """
        Extend parameter value 
        """
        value = parameter.value()
        ( eResult, eData ) = value._extent( context, paramData )
        if( eResult == Value.EXTENT_FAIL ):
            application.terminate( 92 )
        else:
            cp = ""
            if( not currentPrefix in ( None, "" ) ):
                cp = currentPrefix + " "
            if( eData != None ):
                items = []
                for e in eData:
                    items.append( cp + e )
                self.printExtList( items )
        application.terminate( 0 )


    def onMinus( self, context, currentPrefix, currentData, allowScopeEnd ):
        """
        Extend token beginning with '-'
        """
        cData = currentPrefix + currentData

        # collect possible extensions
        extentions = [ ]
        for parseable in context._parseables:
            if( isinstance( parseable, (Flag, Parameter ) ) ):
                short = parseable.shortArg ()
                if( not short in ( None, "" ) ):
                    extentions.append( short )

        # only show single -flag
        if( len ( cData ) < 2 ):

            # print possible extentions
            items = []
            for e in extentions:
                items.append( cData + e )
            self.printExtList( items )

            # also print possible minus minus extentions
            if( cData == "-" ):
                self.onMinusMinus( context, cData, allowScopeEnd )

        else:
            # print current flag if valid
            if ( cData[1:] in extentions ):
                self.printExtList( [ cData ] )

        # done
        application.terminate( 0 )


    def onMinusMinus( self, context, currentData, allowScopeEnd: bool ):
        """
        Extend token beginning with '--'
        """
        # collect possible extensions
        extentions = [ "--help" ]
        for parseable in context._parseables:
            if( isinstance( parseable, (Flag, Parameter ) ) ):
                long = parseable.longArg ()
                if( not long in ( None, "" ) ):
                    extentions.append( "--" + long )

        # print possible extentions
        if( len( currentData ) <= 2 ):
            items = []
            if( allowScopeEnd ):
                items.append( "--" )
            for e in extentions:
                items.append( e )
            self.printExtList( items )
        else:
            items = []
            for e in extentions:
                if( e.startswith( currentData ) ):
                    items.append( e )
            self.printExtList( items )
        application.terminate( 0 )


    def onContextEnd( self, context, currentData):
        self.printExtList( ['--'] )
        application.terminate( 0 )
