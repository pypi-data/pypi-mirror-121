from . import sstr
from . import loglevels



class LineBreakSettings:
    def __init__( self,
                  followIndent: int,
                  newLineIndent: int,
                  breakSequence: str,
                  noWordBreak: bool ):
        """
        Settings for breaking lines while formatting strings
        """
        self.followIndent  = followIndent
        self.newLineIndent = newLineIndent
        self.breakSequence = breakSequence
        self.noWordBreak   = noWordBreak


class HexDumpFormat:
    def __init__( self ):
        """
        Default formatting options for printing hex dumps.
        """
        self.groupSize               = 4
        self.maxGroupsPerLine        = 4
        self.forcePotencyOfTwoGroups = True
        self.forceFullGroups         = False
        self.nonDisplayableChar      = '\u25A1'
        self.hexDelimiter            = ' '
        self.hexGroupDelimiter       = ' '
        self.textGroupDelimiter      = ''
        self.defaultStyle            = sstr.Style()



# style for logger names
class LoggerStyle:
    def __init__( self,
                  default: sstr.Style   = None,
                  fatal: sstr.Style     = None,
                  error: sstr.Style     = None,
                  warn: sstr.Style      = None,
                  info: sstr.Style      = None,
                  insight: sstr.Style   = None,
                  debug: sstr.Style     = None
                ):
        self.defaultStyle = default
        self.levelStyles  = [ fatal, error, warn, info, insight, debug ]



# style for logging exceptions
class ExceptionLoggerStyle:
    def __init__( self ):
        self.name         = "exception"
        self.level        = loglevels.LOG_FATAL
        self.alignName    = False
        self.nameStyle    = LoggerStyle( sstr.Style( mod = sstr.BRIGHT | sstr.ITALIC, fg = sstr.RED ) )
        self.contentStyle = None
