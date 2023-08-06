from pdcommandline import formatter
from . import loglevels
from . import sstr
from .stylesettings import *



# default log level
_defaultLogLevel = loglevels.LOG_INFO


# default string for breaking words inside a table
DEFAULT_BREAK_SEQUENCE = "" + chr( 0x23CE )


# behaviour for filling tables to console width
FILL_NONE       = 0
FILL_DISTRIBUTE = 1
FILL_LAST       = 2


# boarder definitions for table
class TableBorders:
    DEFAULT_BORDER_STYLE                   = sstr.Style()

    DEFAULT_BORDER_LEFT                    = "| "
    DEFAULT_BORDER_CENTER                  = " | "
    DEFAULT_BORDER_RIGHT                   = " |"

    DEFAULT_BORDER_HEADER_SEPARATOR_LEFT   = "+="
    DEFAULT_BORDER_HEADER_SEPARATOR_CENTER = "=+="
    DEFAULT_BORDER_HEADER_SEPARATOR_RIGHT  = "=+"
    DEFAULT_BORDER_HEADER_SEPARATOR_FILL   = "="

    DEFAULT_BORDER_ROW_SEPARATOR_LEFT      = "+-"
    DEFAULT_BORDER_ROW_SEPARATOR_CENTER    = "-+-"
    DEFAULT_BORDER_ROW_SEPARATOR_RIGHT     = "-+"
    DEFAULT_BORDER_ROW_SEPARATOR_FILL      = "-"

    DEFAULT_ENTRY_INDENT                   = 0

    DEFAULT_INITIAL_TO_CAPTION_LINES       = 0
    DEFAULT_INITIAL_TO_HEADER_LINES        = 0
    DEFAULT_INITIAL_TO_ROW_LINES           = 0

    DEFAULT_CAPTION_TO_CAPTION_LINES       = 0
    DEFAULT_CAPTION_TO_HEADER_LINES        = 0
    DEFAULT_CAPTION_TO_ROW_LINES           = 0

    DEFAULT_HEADER_TO_CAPTION_LINES        = 1
    DEFAULT_HEADER_TO_HEADER_LINES         = 0
    DEFAULT_HEADER_TO_ROW_LINES            = 0

    DEFAULT_ROW_TO_CAPTION_LINES           = 1
    DEFAULT_ROW_TO_HEADER_LINES            = 1

    DEFAULT_BREAK_TO_CAPTION_LINES         = 1
    DEFAULT_BREAK_TO_HEADER_LINES          = 1
    DEFAULT_BREAK_TO_ROW_LINES             = 1

    def __init__( self,
                  # border style
                  style: object                = DEFAULT_BORDER_STYLE,

                  # entry borders
                  left: str                    = DEFAULT_BORDER_LEFT,
                  center: str                  = DEFAULT_BORDER_CENTER,
                  right: str                   = DEFAULT_BORDER_RIGHT,

                  # table entry identation
                  entryIndent: int             = DEFAULT_ENTRY_INDENT,

                  # horizontal header borders
                  headerSeparatorPresent: bool = True,
                  headerSeparatorCenter: str   = DEFAULT_BORDER_HEADER_SEPARATOR_CENTER,
                  headerSeparatorLeft: str     = DEFAULT_BORDER_HEADER_SEPARATOR_LEFT,
                  headerSeparatorRight: str    = DEFAULT_BORDER_HEADER_SEPARATOR_RIGHT,
                  headerSeparatorFill: str     = DEFAULT_BORDER_HEADER_SEPARATOR_FILL,

                  # horizontal row borders
                  rowSeparatorPresent: bool    = True,
                  rowSeparatorCenter: str      = DEFAULT_BORDER_ROW_SEPARATOR_CENTER,
                  rowSeparatorLeft: str        = DEFAULT_BORDER_ROW_SEPARATOR_LEFT,
                  rowSeparatorRight: str       = DEFAULT_BORDER_ROW_SEPARATOR_RIGHT,
                  rowSeparatorFill: str        = DEFAULT_BORDER_ROW_SEPARATOR_FILL,

                  # spaces between states
                  initialToCaptionLines: int   = DEFAULT_INITIAL_TO_CAPTION_LINES,
                  initialToHeaderLines: int    = DEFAULT_INITIAL_TO_HEADER_LINES,
                  initialToRowLines: int       = DEFAULT_INITIAL_TO_ROW_LINES,
                    
                  captionToCaptionLines: int   = DEFAULT_CAPTION_TO_CAPTION_LINES,
                  captionToHeaderLines: int    = DEFAULT_CAPTION_TO_HEADER_LINES,
                  captionToRowLines: int       = DEFAULT_CAPTION_TO_ROW_LINES,
                    
                  headerToCaptionLines: int    = DEFAULT_HEADER_TO_CAPTION_LINES,
                  headerToHeaderLines: int     = DEFAULT_HEADER_TO_HEADER_LINES,
                  headerToRowLines: int        = DEFAULT_HEADER_TO_ROW_LINES,
                    
                  rowToCaptionLines: int       = DEFAULT_ROW_TO_CAPTION_LINES,
                  rowToHeaderLines: int        = DEFAULT_ROW_TO_HEADER_LINES,
                    
                  breakToCaptionLines: int     = DEFAULT_BREAK_TO_CAPTION_LINES,
                  breakToHeaderLines: int      = DEFAULT_BREAK_TO_HEADER_LINES,
                  breakToRowLines: int         = DEFAULT_BREAK_TO_ROW_LINES ):
        """
        Border definitions for table
        """
        self.style                  = style

        self.left                   = left
        self.center                 = center
        self.right                  = right

        self.entryIndent            = entryIndent

        self.headerSeparatorPresent = headerSeparatorPresent
        self.headerSeparatorLeft    = headerSeparatorLeft
        self.headerSeparatorRight   = headerSeparatorRight
        self.headerSeparatorFill    = headerSeparatorFill
        self.headerSeparatorCenter  = headerSeparatorCenter

        self.rowSeparatorPresent    = rowSeparatorPresent
        self.rowSeparatorCenter     = rowSeparatorCenter
        self.rowSeparatorLeft       = rowSeparatorLeft
        self.rowSeparatorRight      = rowSeparatorRight
        self.rowSeparatorFill       = rowSeparatorFill

        self.initialToCaptionLines = initialToCaptionLines
        self.initialToHeaderLines  = initialToHeaderLines
        self.initialToRowLines     = initialToRowLines

        self.captionToCaptionLines = captionToCaptionLines
        self.captionToHeaderLines  = captionToHeaderLines
        self.captionToRowLines     = captionToRowLines

        self.headerToCaptionLines  = headerToCaptionLines
        self.headerToHeaderLines   = headerToHeaderLines
        self.headerToRowLines      = headerToRowLines

        self.rowToCaptionLines     = rowToCaptionLines
        self.rowToHeaderLines      = rowToHeaderLines

        self.breakToCaptionLines   = breakToCaptionLines
        self.breakToHeaderLines    = breakToHeaderLines
        self.breakToRowLines       = breakToRowLines


# default table borders
_defaultBorders = TableBorders()


# default table borders ( no borders )
_defaultBordersNoBorders = TableBorders( left                   = "",
                                         center                 = "  ",
                                         right                  = "",
                                         entryIndent            = 2,
                                         headerSeparatorPresent = False,
                                         headerSeparatorCenter  = "  ",
                                         headerSeparatorLeft    = "",
                                         headerSeparatorRight   = "",
                                         headerSeparatorFill    = "",
                                         rowSeparatorPresent    = False,
                                         rowSeparatorCenter     = "  ",
                                         rowSeparatorLeft       = "",
                                         rowSeparatorRight      = "",
                                         rowSeparatorFill       = "" )


# layout for formatting tables
class TableLayout:
    DEFAULT_HEADLINE_STYLE        = sstr.Style()
    DEFAULT_CONTENT_STYLE         = sstr.Style()
    DEFAULT_MIN_WIDTH             = 4
    DEFAULT_MAX_WIDTH             = None
    DEFAULT_PERCENT               = 1
    DEFAULT_STRETCH               = 1
    DEFAULT_FOLLOWINDENT          = 4
    DEFAULT_NEWLINEINDENT         = 2
    DEFAULT_CAPTION_FOLLOWINDENT  = 4
    DEFAULT_CAPTION_NEWLINEINDENT = 2
    DEFAULT_PREFER_LONG_LINES     = True
    DEFAULT_FILL_TYPE             = FILL_LAST


    def __init__( self,
                  borders: object           = _defaultBorders,
                  minWidth: int             = DEFAULT_MIN_WIDTH,
                  maxWidth: int             = DEFAULT_MAX_WIDTH,
                  percent: float            = DEFAULT_PERCENT,
                  stretch: float            = DEFAULT_STRETCH,
                  followindent: int         = DEFAULT_FOLLOWINDENT,
                  newlineindent: int        = DEFAULT_NEWLINEINDENT,
                  captionfollowindent: int  = DEFAULT_CAPTION_FOLLOWINDENT,
                  captionnewlineindent: int = DEFAULT_CAPTION_NEWLINEINDENT,
                  breakSequence: str        = DEFAULT_BREAK_SEQUENCE,
                  preferLongLines: bool     = DEFAULT_PREFER_LONG_LINES,
                  fillType: int             = DEFAULT_FILL_TYPE,
                  contentStyle: object      = DEFAULT_CONTENT_STYLE,
                  headlineStyle: object     = DEFAULT_HEADLINE_STYLE ):
        """
        Layout for formatting columns
        """
        self.columns              = []
        self.borders              = borders
        self.defaults             = { 'min':           minWidth,
                                      'max':           maxWidth,
                                      'percent':       percent,
                                      'stretch':       stretch,
                                      'followindent':  followindent,
                                      'newlineindent': newlineindent,
                                      'contentstyle':  contentStyle }
        self.captionfollowindent  = captionfollowindent
        self.captionnewlineindent = captionnewlineindent
        self.breakSequence        = breakSequence
        self.preferLongLines      = preferLongLines
        self.fillType             = fillType
        self.headlineStyle        = headlineStyle


    def addColumn( self,
                   minWidth: int        = None,
                   maxWidth: int        = None,
                   percent: float       = None,
                   stretch: float       = None,
                   followindent: int    = None,
                   newlineindent: int   = None,
                   contentStyle: object = None ):
        """
        Add a column to the layout
        """
        self.columns.append ( { 'min':           minWidth      if minWidth != None      else self.defaults['min'],
                                'max':           maxWidth      if maxWidth != None      else self.defaults['max'],
                                'percent':       percent       if percent != None       else self.defaults['percent'],
                                'stretch':       stretch       if stretch != None       else self.defaults['stretch'],
                                'followindent':  followindent  if followindent != None  else self.defaults['followindent'],
                                'newlineindent': newlineindent if newlineindent != None else self.defaults['newlineindent'],
                                'contentstyle':  contentStyle  if contentStyle != None  else self.defaults['contentstyle'] } )


    def getColumn( self,
                   index: int ):
        """
        Returns the layout for a single column
        """
        if( ( index >= 0 ) and ( index < len( self.columns ) ) ):
            return self.columns[index]
        else:
            return self.defaults


# default layout
_defaultTableLayout = TableLayout()


# default layout without borders
_defaultTableLayoutNoBorders = TableLayout( borders = _defaultBordersNoBorders )




# layout for formatting trees
_defaultTreeHeadLayout = _defaultTableLayout
_defaultTreeContentLayout = _defaultTableLayout


# styles for rendering tree edges
_defaultTreeEdgeStyles = [
    sstr.Style( fg = sstr.GREEN,   mod = sstr.BRIGHT ),
    sstr.Style( fg = sstr.YELLOW,  mod = sstr.BRIGHT ),
    sstr.Style( fg = sstr.RED,     mod = sstr.BRIGHT ),
    sstr.Style( fg = sstr.BLUE,    mod = sstr.BRIGHT ),
    sstr.Style( fg = sstr.MAGENTA, mod = sstr.BRIGHT ),
    sstr.Style( fg = sstr.CYAN,    mod = sstr.BRIGHT )
]


# layout for rendering trees
class TreeLayout:
    def __init__( self,
                  headLayout: object      = None,
                  contentLayout: object   = None,
                  levelIndent: int        = 3,
                  contentIndent: int      = 1,
                  lineClearance: int      = 1,
                  sameContentLayout: bool = True,
                  sameContentIndent: bool = True,
                  edgeStyles: list        = None ):
        """
        Tree layout
        """
        self.headLayout        = headLayout    if headLayout != None else _defaultTreeHeadLayout
        self.contentLayout     = contentLayout if headLayout != None else _defaultTreeContentLayout
        self.levelIndent       = levelIndent
        self.contentIndent     = contentIndent
        self.lineClearance     = lineClearance
        self.sameContentLayout = sameContentLayout
        self.sameContentIndent = sameContentIndent
        self.edgeStyles        = edgeStyles    if edgeStyles != None else _defaultTreeEdgeStyles


# default layout for rendering trees
_defaultTreeLayout = TreeLayout()




# default size of console, used when detection fails
_defaultConsoleWidth = 80
_defaultProgressWidth = None



# command line help style
class CommandlineHelp:
    def __init__( self,
                  tableLayout           = _defaultTableLayoutNoBorders,
                  defaultParameterGroup = "",
                  parameterAlign        = True,
                  parameterNewline      = True,
                  showRunHelp           = True
                ):
        """
        Creates a command line help style set
        """
        # help layout
        self.tableLayout                        = tableLayout
        self.defaultParameterGroup              = defaultParameterGroup
        self.parameterAlign                     = parameterAlign
        self.parameterNewLine                   = parameterNewline
        self.showRunHelp                        = showRunHelp

        # prefix and suffix of values
        self.helpTextValuePrefix                = sstr.SStr( "<" )
        self.helpStyleValueName                 = sstr.Style()
        self.helpTextValueSuffix                = sstr.SStr( ">" )
        self.helpStyleValue                     = sstr.Style()

        # help text parts & styles
        self.helpTextDescriptionHeadLine        = sstr.SStr( "description:\n", mod = sstr.BRIGHT | sstr.ITALIC )
        self.helpStyleContextDescr              = sstr.Style( )
        self.helpTextUsage                      = sstr.SStr( "usage:\n", mod = sstr.BRIGHT | sstr.ITALIC )
        self.helpStyleContext                   = sstr.Style( mod = sstr.BRIGHT | sstr.ITALIC )
        self.helpStyleFirstContext              = sstr.Style( mod = sstr.BRIGHT | sstr.ITALIC )
        self.helpStyleFollowContext             = sstr.Style( mod = sstr.BRIGHT | sstr.ITALIC )
        self.helpTextParameters                 = sstr.SStr( "[parameters*]", mod = sstr.ITALIC )
        self.helpStyleArgument                  = sstr.Style( )
        self.helpStyleAction                    = sstr.Style( )
        self.helpStyleValue                     = sstr.Style( )

        # help for actions
        self.helpTextActionParams               = sstr.SStr( "..." )
        self.helpTextActionArrayBegin           = sstr.SStr( "{" )
        self.helpTextActionArrayEnd             = sstr.SStr( "}*" )
        self.helpTextActionScopeEnd             = sstr.SStr( "--" )
        self.helpStyleActionArray               = sstr.Style( mod = sstr.ITALIC )
        self.helpTextOptionalBegin              = sstr.SStr( "[" )
        self.helpTextOptionalEnd                = sstr.SStr( "]" )
        self.helpTextArrayModifier              = sstr.SStr( "*" )
        self.helpStyleOptional                  = sstr.Style( mod = sstr.ITALIC )

        # help for arguments
        self.helpTextHeadlineArguments          = sstr.SStr( "arguments:" )
        self.helpStyleHeadlineArguments         = sstr.Style( mod = sstr.ITALIC | sstr.BRIGHT )
        self.helpStyleArgumentKey               = sstr.Style( mod = sstr.ITALIC )
        self.helpStyleActionKey                 = sstr.Style( mod = sstr.ITALIC )

        # help for parameters
        self.helpTextHeadlineParameters         = sstr.SStr( "parameters:" )
        self.helpStyleHeadlineParamGroup        = sstr.Style( mod = sstr.ITALIC | sstr.BRIGHT )
        self.helpStyleHeadlineParameters        = sstr.Style( mod = sstr.ITALIC | sstr.BRIGHT )

        self.helpTextParameterSeparator         = sstr.SStr( ", " )
        self.helpStyleLongParameterName         = sstr.Style( )
        self.helpStyleShortParameterName        = sstr.Style( )
        self.helpStyleLongParameter             = sstr.Style( )
        self.helpStyleShortParameter            = sstr.Style( )
        self.helpStyleParameterValue            = sstr.Style( mod = sstr.ITALIC )

        # help for parseable nodes
        self.helpTextParseableSeparator         = sstr.SStr( ", " )
        self.helpStyleParseableDescription      = sstr.Style( )
        self.helpStyleParseableValue            = sstr.Style( mod = sstr.ITALIC )
        self.helpStyleParseableTypeAndRange     = sstr.Style( )
        self.helpStyleParseableDescription      = sstr.Style( )

        # help for parameter description
        self.helpTextDescriptionSeparator       = sstr.SStr( ", " )
        self.helpTextDescriptionDefaultPrefix   = sstr.SStr( "default is " )
        self.helpTextDescriptionInheritedPrefix = sstr.SStr( "inherited: " )
        self.helpTextDescriptionOptions         = sstr.SStr( "\n\noptions:", mod = sstr.ITALIC )
        self.helpTextDescriptionOptionEnd       = sstr.SStr( "." )
        self.helpStyleOptionName                = sstr.Style( mod = sstr.ITALIC )
        self.helpStyleOptionDescription         = sstr.Style( )
        self.helpTextDescriptionValuePrefix     = sstr.SStr( "'" )
        self.helpStyleDescriptionValue          = sstr.Style( mod = sstr.ITALIC )
        self.helpTextDescriptionValueSuffix     = sstr.SStr( "'" )
        self.helpTextDescriptionEnd             = sstr.SStr( "." )

        # show run for context specific help
        self.helpStyleRunHelpFirstContext       = sstr.Style( )
        self.helpStyleRunHelpFollowContext      = sstr.Style( )
        self.helpTextRunHelpRunPrefix           = sstr.SStr( "\nrun" )
        self.helpTextRunHelpRunSuffix           = sstr.SStr( "for more informations." )
        self.helpTextRunHelpRunCmdPrefix        = sstr.SStr( "'" )
        self.helpTextRunHelpRunValuePrefix      = sstr.SStr( "<" )
        self.helpStyleRunHelpRunValueName       = sstr.Style( )
        self.helpTextRunHelpRunValueSuffix      = sstr.SStr( ">" )
        self.helpStyleRunHelpRunValue           = sstr.Style( )
        self.helpTextRunHelpRunCmdSuffix        = sstr.SStr( "'" )
        self.helpTextRunHelpRunHelpParameter    = sstr.SStr( "--help" )

# default style for command line help
_defaultCommandLineHelp = CommandlineHelp ()



# Input query settings
class InputQuery:
    def __init__( self ):
        self.wordWrap       = False
        self.firstPrefix    = ""
        self.followPrefix   = "  "
        self.beforeProgress = False

# default input query settings
_defaultInputQuery = InputQuery()



# default line break settings for logger
_defaultLoggerBreakSettings = LineBreakSettings (
    followIndent  = 2,
    newLineIndent = 2,
    breakSequence = DEFAULT_BREAK_SEQUENCE,
    noWordBreak   = True
)



# default logger name styles
_defaultLoggerNameStyles = LoggerStyle (
    default = None,
    fatal   = sstr.Style( mod = sstr.BRIGHT | sstr.ITALIC, fg = sstr.RED ),
    error   = sstr.Style( mod = sstr.BRIGHT, fg = sstr.RED ),
    warn    = sstr.Style( mod = sstr.BRIGHT, fg = sstr.YELLOW ),
    info    = sstr.Style( mod = sstr.BRIGHT, fg = sstr.GREEN ),
    insight = sstr.Style( mod = sstr.BRIGHT, fg = sstr.BLUE ),
    debug   = sstr.Style( mod = sstr.BRIGHT, fg = sstr.CYAN )
)



# default logger content styles
_defaultLoggerContentStyles = LoggerStyle (
    default = None,
    fatal   = None,
    error   = None,
    warn    = None,
    info    = None,
    insight = None,
    debug   = None    
)

# default style for logging exceptions
_defaultExceptionLoggerStyle = ExceptionLoggerStyle()



# defaults for this commandline application
class Defaults:
    """
    Default style settings
    """
    
    @staticmethod
    def getLogLevel():
        """
        Returns the default log level for writing
        """
        global _defaultLogLevel
        return _defaultLogLevel


    @staticmethod
    def setLogLevel( value: int ):
        """
        Sets the default log level for writing
        """
        assert value >= 0
        assert value <= loglevels.LOG_MAX_LEVEL
        global _defaultLogLevel
        _defaultLogLevel = value


    @staticmethod
    def getTableLayout():
        """
        Returns the default table layout
        """
        global _defaultTableLayout
        return _defaultTableLayout


    @staticmethod
    def setTableLayout( layout: object ):
        """
        Sets the default table layout
        """
        global _defaultTableLayout
        _defaultTableLayout = layout


    @staticmethod
    def getTableLayoutNoBorders():
        """
        Returns the default table layout (without borders)
        """
        global _defaultTableLayoutNoBorders
        return _defaultTableLayoutNoBorders


    @staticmethod
    def setTableLayoutNoBorders( layout: object ):
        """
        Sets the default table layout (without borders)
        """
        global _defaultTableLayoutNoBorders
        _defaultTableLayoutNoBorders = layout


    @staticmethod
    def getTreeLayout():
        """
        Returns the default layout for rendering trees
        """
        global _defaultTreeLayout
        return _defaultTreeLayout


    @staticmethod
    def setTreeLayout( layout: object ):
        """
        Returns the default layout for rendering trees
        """
        global _defaultTreeLayout
        _defaultTreeLayout = layout
        

    @staticmethod
    def getDefaultConsoleWidth():
        """
        Returns the assumed console width when detection fails
        """
        global _defaultConsoleWidth
        return _defaultConsoleWidth


    @staticmethod
    def setDefaultConsoleWidth( width: int ):
        """
        Sets the assumed console width when detection fails
        """
        assert width > 0
        global _defaultConsoleWidth
        _defaultConsoleWidth = width
        

    @staticmethod
    def getDefaultProgressWidth():
        """
        Returns the assumed console width when detection fails
        """
        global _defaultConsoleWidth
        global _defaultProgressWidth
        if( _defaultProgressWidth != None ):
            return _defaultProgressWidth
        return _defaultConsoleWidth


    @staticmethod
    def setDefaultProgressWidth( width: int ):
        """
        Sets the assumed console width when detection fails
        """
        if( width != None ):
            assert width > 0
        global _defaultProgressWidth
        _defaultProgressWidth = width


    @staticmethod
    def getCommandlineHelpStyle():
        """
        Returns the default style set for command line help
        """
        global _defaultCommandLineHelp
        return _defaultCommandLineHelp


    @staticmethod
    def setCommandlineHelpStyle( style: object ):
        """
        Sets the default style set for command line help
        """
        global _defaultCommandLineHelp
        _defaultCommandLineHelp = style
        

    @staticmethod
    def getInputQueryStyle( ):
        """
        Returns the default style for input querys
        """
        global _defaultInputQuery
        return _defaultInputQuery        


    @staticmethod
    def setInputQueryStyle( style: object ):
        """
        Sets the default style for input querys
        """
        global _defaultInputQuery
        _defaultInputQuery = style


    @staticmethod
    def getLoggerNameStyle():
        """
        Returns the default style for logger names
        """
        global _defaultLoggerNameStyles
        return _defaultLoggerNameStyles


    @staticmethod
    def setLoggerNameStyle( style: object ):
        """
        Sets the default style for logger names
        """
        global _defaultLoggerNameStyles
        _defaultLoggerNameStyles = style
        from . import logger
        logger._loggerRegistry.updateDefaultNameStyle()


    @staticmethod
    def getLoggerContentStyle():
        """
        Returns the default style for logger content
        """
        global _defaultLoggerContentStyles
        return _defaultLoggerContentStyles


    @staticmethod
    def setLoggerContentStyle( style: object ):
        """
        Sets the default style for logger content
        """
        global _defaultLoggerContentStyles
        _defaultLoggerContentStyles = style
        from . import logger
        logger._loggerRegistry.updateDefaultContentStyle()


    @staticmethod
    def getLoggerLinebreakSettings():
        """
        Returns the default line break settings for logger content
        """
        global _defaultLoggerBreakSettings
        return _defaultLoggerBreakSettings


    @staticmethod
    def setLoggerLinebreakSettings( settings ):
        """
        Sets the default line break settings for logger content
        """
        global _defaultLoggerBreakSettings
        _defaultLoggerBreakSettings = settings
        from . import logger
        logger._loggerRegistry.updateDefaultLinebreakSettings()


    @staticmethod
    def getExceptionLoggerStyle():
        """
        Returns the default exception logging style
        """
        global _defaultExceptionLoggerStyle
        return _defaultExceptionLoggerStyle


    @staticmethod
    def setExceptionLoggerStyle( style ):
        """
        Sets the default exception logging style
        """
        global _defaultExceptionLoggerStyle
        _defaultExceptionLoggerStyle = style
        from .exceptions import _exceptionLogger
        _exceptionLogger.updateLoggerSettings()
