from . import formatter
from . import loglevels
from . import sstr
from . import style
from .style import LoggerStyle



# logger class
class Logger:
    def __init__( self,
                  name: str,
                  defaultLevel         = loglevels.LOG_DEFAULT,
                  nameStyle: object    = None,
                  contentStyle: object = None,
                  alignName: bool      = True
                ):
        """
        Creates a new logger
        """
        self.name               = name
        self.defaultLevel       = defaultLevel
        self.loggerNameStyle    = nameStyle
        self.loggerContentStyle = contentStyle
        self.alignLoggerName    = alignName

        # handle to console
        self.console = None

        # cache of computed names
        self.computedVersion      = None
        self.computedName         = [ None, None, None, None, None, None ]
        self.computedContentStyle = [ None, None, None, None, None, None ]
        self.computedLineBreaks   = None

        # register logger
        _loggerRegistry.register( self )


    def __call__( self,
                  logMessage: str   = None,
                  fatal: str        = None,
                  error: str        = None,
                  warn: str         = None,
                  info: str         = None,
                  insight: str      = None,
                  debug: str        = None ):
        """
        Write log data to console
        """
        self.write( logMessage, fatal, error, warn, info, insight, debug )


    def write( self,
                   logMessage: str   = None,
                   fatal: str        = None,
                   error: str        = None,
                   warn: str         = None,
                   info: str         = None,
                   insight: str      = None,
                   debug: str        = None ):
        """
        Write log data to console
        """
        # check for ambigious arguments
        if( 
               ( fatal   != None )
            or ( error   != None )
            or ( warn    != None )
            or ( info    != None )
            or ( insight != None )
            or ( debug   != None ) ):
            assert logMessage == None, "can not combine logMessage with fatal, error, warn, info, insight, debug"

        # set message depending on log levels
        levelStr = [None, None, None, None, None, None]
        firstLevel = None
        if( logMessage != None ):
            firstLevel = self.defaultLevel
            levelStr[self.defaultLevel] = logMessage
        else:
            if( debug != None ):
                levelStr[5] = debug
                firstLevel = 5
            if( insight != None ):
                levelStr[4] = insight
                firstLevel = 4
            if( info != None ):
                levelStr[3] = info
                firstLevel = 3
            if( warn != None ):
                levelStr[2] = warn
                firstLevel = 2
            if( error != None ):
                levelStr[1] = error
                firstLevel = 1
            if( fatal != None ):
                levelStr[0] = fatal
                firstLevel = 0

        # abort if no log level is used
        if( firstLevel == None ):
            return

        # invalidate cached formatting settings?
        if self.computedVersion != _loggerRegistry.version:
            self.computedName         = [ None, None, None, None, None, None ]
            self.computedContentStyle = [ None, None, None, None, None, None ]
            self.computedLineBreaks   = _loggerRegistry._getLineBreaks()
            self.computedVersion      = _loggerRegistry.version

        # init console handle
        if( self.console == None ):
            from . import console
            self.console = console    

        # write to console
        currentLevel = firstLevel
        while( currentLevel <= loglevels.LOG_MAX_LEVEL ):

            # find next level
            nextLevel = currentLevel + 1
            while( nextLevel <= loglevels.LOG_MAX_LEVEL ):
                if( levelStr[nextLevel] == None ):
                    nextLevel += 1
                else:
                    break

            # compute formatted name
            if( self.computedName[currentLevel] == None ):
                levelNameStyle = None
                if( self.loggerNameStyle != None ):
                    if( self.loggerNameStyle.defaultStyle != None ):
                        levelNameStyle = self.loggerNameStyle.defaultStyle
                        if( self.loggerNameStyle.levelStyles[currentLevel] != None ):
                            levelNameStyle = self.loggerNameStyle.levelStyles[currentLevel].concrete( levelNameStyle )
                    else:
                        levelNameStyle = self.loggerNameStyle.levelStyles[currentLevel]
                self.computedName[currentLevel] = _loggerRegistry.computeName( self.name, currentLevel, levelNameStyle )

            # compute content default style
            if( self.computedContentStyle[currentLevel] == None ):
                levelContentStyle = _loggerRegistry.getContentStyle( currentLevel )
                if( self.loggerContentStyle != None ):
                    if( self.loggerContentStyle.defaultStyle != None ):
                        levelContentStyle = self.loggerContentStyle.defaultStyle.concrete( levelContentStyle )
                        if( self.loggerContentStyle.levelStyles[currentLevel] != None ):
                            levelContentStyle = self.loggerContentStyle.levelStyles[currentLevel].concrete( levelContentStyle )
                    else:
                        levelContentStyle = self.loggerContentStyle.levelStyles[currentLevel].concrete( levelContentStyle )
                if( levelContentStyle == None ):
                    levelContentStyle = sstr.Style()
                self.computedContentStyle[currentLevel] = levelContentStyle

            # force content of level to be a list
            if( isinstance( levelStr[currentLevel], ( list, tuple ) ) ):
                content = levelStr[currentLevel]
            else:
                content = [ levelStr[currentLevel] ]

            # process content elements
            outArray = self._processFirstContentLine( [], content[0] if len( content ) > 0 else None, self.computedName[currentLevel] )
            for index in range( 1, len( content ) ):
                outArray = self._processFollowingContentLine( outArray, content[index])

            # write to console
            self.console.write( outArray,
                                currentLevel,
                                nextLevel,
                                self.computedContentStyle[currentLevel],
                                self.computedLineBreaks.followBreakSettings,
                                self.computedLineBreaks.followIndent,
                                self.computedLineBreaks.firstBreakSettings,
                                self.computedLineBreaks.firstIndent )

            # continue on next level
            currentLevel = nextLevel


    def getLineWidthLimit( self ):
        """
        Returns the line width limit for rendering on the console, None if no console is attached
        """
        # init console handle
        if( self.console == None ):
            from . import console
            self.console = console
        
        # get console width
        cWidth = None
        cTerminal = console.getTerminal()
        if( cTerminal != None ):
            cWidth = cTerminal._detectMaxWidth()

        # subract indent size
        if( cWidth != None ):
            # subtract indentation
            lineBreaks = _loggerRegistry._getLineBreaks()
            cWidth -= lineBreaks.followBreakSettings.followIndent

            # limit minimum size
            if( cWidth < 1 ):
                cWidth = 1

        # return content width limit
        return cWidth


    def _processFirstContentLine( self, target, content, loggerName ):
        """
        Produce first content Line...
        """
        # got a layoutable content element?
        if( isinstance( content, formatter.Layoutable ) ):
            return target + [ loggerName, content ]

        # non layoutable content, i.e. string or string may with formatting settings
        return target + [ sstr.SStr( loggerName, self._resolveContent( content ) ) ]


    def _processFollowingContentLine( self, target, content ):
        """
        Produce first content Line...
        """
        # got a layoutable content element?
        if( isinstance( content, formatter.Layoutable ) ):
            return target + [ content ]

        # got a string content...
        return target + [ sstr.SStr( self.computedLineBreaks.followInitialIndent, content ) ]


    def _resolveContent( self, content ):
        """
        Resolve content as SStr
        """
        # abort if we got no content
        if( content == None ):
            return sstr.LStr()

        # check if content is list or tuple
        if( isinstance( content, ( list, tuple ) ) ) :
            outElements = []
            for element in content:
                outElements.append( self._resolveContent( element ) )
            return sstr.SStr( *outElements )

        # ignore applying line break settings and indents
        if( isinstance( content, ( formatter.ApplyIndent, formatter.ApplyLineBreakSettings ) ) ):
            return self._resolveContent( content.content )

        # apply style settings
        if( isinstance( content, formatter.ApplyDefaultStyle ) ):
            return sstr.SStr( self._resolveContent( content.content ), style = content.style )

        # return content as SStr
        return sstr.SStr( content )




# line break and formatting settings
class _LoggerBreakSettings:
    def __init__( self, firstBreakSettings, followBreakSettings, firstIndent, followIndent, followInitialIndent ):
        """
        Creates line break settings for a logger.
        """
        self.firstBreakSettings = firstBreakSettings
        self.followBreakSettings = followBreakSettings
        self.firstIndent = firstIndent
        self.followIndent = followIndent
        self.followInitialIndent = followInitialIndent




# registry of known loggers
class _LoggerRegistry:
    def __init__( self ):
        """
        Registry for loggers
        """
        from .threads import RLock
        self.lock                   = RLock()
        self.loggers                = []
        self.maxNameSize            = 0
        self.version                = 0
        self.defaultNameStyle       = None
        self.defaultContentStyle    = None
        self.breakSettings          = None
        self.defaultNameStyleSet    = False
        self.defaultContentStyleSet = False
        self.breakSettingsSet       = False

        # update default styles ( get from default style settings )
        self.setDefaultNameStyle( None )
        self.setDefaultContentStyle( None )
        self.setLinebreakSettings( None )


    def register( self, logger ):
        """
        Registers a logger
        """
        with self.lock:
            if( not logger in self.loggers ):
                self.loggers.append( logger )
                if( logger.alignLoggerName == True ):
                    nameLen = len( logger.name )
                    if( nameLen > self.maxNameSize ):
                        self.maxNameSize = nameLen
                self.version += 1


    def computeName( self, name, level, levelStyle ):
        """
        Compute formatted name for a log level
        """
        # format logger name
        s = name
        s = "[" + s + " " * ( self.maxNameSize - len( s ) ) + "] "

        # get default style
        baseStyle = sstr.Style( sstr.DEFAULT, sstr.DEFAULT, sstr.DEFAULT )
        if( self.defaultNameStyle != None ):
            if( self.defaultNameStyle.defaultStyle != None ):
                baseStyle = self.defaultNameStyle.defaultStyle.concrete( baseStyle )
            if( self.defaultNameStyle.levelStyles[level] != None ):
                if( baseStyle != None ):
                    baseStyle = self.defaultNameStyle.levelStyles[level].concrete( baseStyle )
                else:
                    baseStyle = self.defaultNameStyle.levelStyles[level]

        # got level style?
        if( baseStyle != None ):
            if( levelStyle != None ):
                baseStyle = levelStyle.concrete( baseStyle )
        else:
            baseStyle = levelStyle

        # create styled string
        return sstr.SStr( s, style = baseStyle )


    def getContentStyle( self, level ):
        """
        Get style for content by level
        """
        if( self.defaultContentStyle != None ):
            style = self.defaultContentStyle.defaultStyle
            if( self.defaultContentStyle.levelStyles[level] != None ):
                style = self.defaultContentStyle.levelStyles[level].concrete( style )
            return style
        return None


    def setDefaultNameStyle( self, default ):
        """
        Set default style for formatting logger names
        """
        with self.lock:
            if( default != None ):
                self.defaultNameStyleSet = True
                self.defaultNameStyle = default
            else:
                self.defaultNameStyleSet = False
                self.defaultNameStyle = style.Defaults.getLoggerNameStyle()
            self.version += 1


    def updateDefaultNameStyle( self ):
        """
        Update default name style
        """
        with self.lock:
            if( self.defaultNameStyleSet == False ):
                self.setDefaultNameStyle( self, None )


    def setDefaultContentStyle( self, default ):
        """
        Set default style for formatting logger context
        """
        with self.lock:
            if( style != None ):
                self.defaultContentStyleSet = True
                self.defaultContentStyle = default
            else:
                self.defaultContentStyleSet = False
                self.defaultContentStyle = style.Defaults.getLoggerContentStyle()
            self.version += 1


    def updateDefaultContentStyle( self ):
        """
        Update default content style
        """
        with self.lock:
            if( self.defaultContentStyleSet == False ):
                self.setDefaultContentStyle( self, None )


    def setLinebreakSettings( self, linebreaks ):
        """
        Set linebreak settings for formatting logger context
        """
        with self.lock:
            if( linebreaks == None ):
                self.breakSettingsSet = False
                linebreaks = style.Defaults.getLoggerLinebreakSettings()
            else:
                self.breakSettingsSet = True

            # break settings for first element
            firstLinebreaks = linebreaks
            firstIndentStr = ""

            # break settings for following elements
            followIndent = linebreaks.followIndent
            newLineIndent = linebreaks.newLineIndent - followIndent
            if( newLineIndent < 0 ):
                newLineIndent = 0
            followInitialIndentStr = " " * newLineIndent
            followIndentStr = " " * followIndent
            followLinebreaks = formatter.LineBreakSettings( 0, newLineIndent, linebreaks.breakSequence, linebreaks.noWordBreak )

            # update line break settings
            self.breakSettings = _LoggerBreakSettings( firstLinebreaks, followLinebreaks, firstIndentStr, followIndentStr, followInitialIndentStr )
            self.version += 1


    def updateDefaultLinebreakSettings( self ):
        """
        Update line break settings
        """
        with self.lock:
            if( self.breakSettingsSet == False ):
                self.setLinebreakSettings( self, None )
        

    def _getLineBreaks( self ):
        """
        Return computed line break settings
        """
        with self.lock:
            return self.breakSettings


# single instance of logger registry
_loggerRegistry = _LoggerRegistry()
