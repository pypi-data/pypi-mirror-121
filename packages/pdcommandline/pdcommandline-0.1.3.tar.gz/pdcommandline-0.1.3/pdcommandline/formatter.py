# import style definitions
from . import sstr
from . import style
from .stylesettings import LineBreakSettings
import copy
import math



class ApplyDefaultStyle:
    def __init__( self, * content, style: object ):
        """
        Apply default style setting on content - used for formatting strings while printing to console
        """
        self.content = content
        self.style = style



class ApplyLineBreakSettings:
    def __init__( self, * content, settings: object ):
        """
        Apply default style setting on content - used for formatting strings while printing to console
        """
        self.content = content
        self.settings = settings



class ApplyIndent:
    def __init__( self, * content, indent: str ):
        """
        Apply default style setting on content - used for formatting strings while printing to console
        """
        self.content = content
        self.indent = indent



# formatting utility for tables
class TableUtils:
    @staticmethod
    def _lenSkipNondisplayable( s ):
        sx = str( s )
        l = 0
        for c in sx:
            if( c != "\x06" ):
                l += 1
        return l

    @staticmethod
    def _splitContent( text: object,
                       maxWidth: int,
                       followindent: int,
                       newlineindent: int,
                       breakSequence: str,
                       noWordBreak: bool = False,
                       filterNondisplayable: bool = False ):
        """
        Split content and return formatted lines,

        outputs a list of ColorString's containing each line
        """
        # minimum character limit
        minWidth = 0
        if( minWidth < followindent ):
            minWidth = followindent
        if( minWidth < newlineindent ):
            minWidth = newlineindent

        # allow printing at least one char and a linebreak
        minWidth += 1 + len( breakSequence )
        if( maxWidth != None ):
            if( maxWidth < minWidth ):
                maxWidth = minWidth

        # create LStr from break sequence
        lstrBreakSequence = sstr.LStr( sstr.LStrPart( breakSequence, sstr.Style() ) )

        # split into parts
        parts = []
        buffer = None
        separator = None
        separatorIssued = False

        # get single characters
        cChars = sstr.SStr( text ).asLinear().asCharList()
        for cChar in cChars:
            char = cChar.content
            if( char == '\t' ):
                char = " "
            if( char == '\r' ):
                # ignore \r char
                pass
            elif( char in (' ', '\t', '\n') ):
                # handle break char
                if( separator == None ):
                    separator = sstr.LStr( cChar )
                else:
                    separator.append( cChar )
                parts.append( { 'buffer':    buffer if buffer != None else sstr.LStr(),
                                'separator': separator } )
                buffer          = None
                separator       = None
                separatorIssued = False
            elif( char in( ',', ':', '-' ) ):
                # handle possible break
                if( buffer == None ):
                    buffer = sstr.LStr( cChar )
                else:
                    buffer.append( cChar )
                separatorIssued  = True
            else:
                # handle ordinary character
                if( separatorIssued ):
                    parts.append ( { 'buffer':    buffer    if buffer != None    else sstr.LStr(),
                                     'separator': separator if separator != None else sstr.LStr() } )
                    buffer          = None
                    separator       = None
                    separatorIssued = False
                if( buffer == None ):
                    buffer = sstr.LStr( cChar )
                else:
                    buffer.append( cChar )

        # handle rest
        if( ( buffer != None ) or ( separator != None ) ):
            parts.append( { 'buffer':    buffer    if buffer != None    else sstr.LStr(),
                            'separator': separator if separator != None else sstr.LStr() } )
        else:
            # got empty line?, return it
            if( len( parts ) == 0 ):
                return [sstr.LStr()]

        if( filterNondisplayable == True ):
            flen = TableUtils._lenSkipNondisplayable
        else:
            flen = len

        # assemble lines
        STATE_S_FIRST_LINE = 0
        STATE_S_FOLLOW     = 1
        STATE_S_NEW_LINE   = 2
        STATE_S_REST_PART  = 3
        state              = STATE_S_FIRST_LINE
        partId             = 0
        currentLine        = None
        lastSeparator      = sstr.LStr()
        rest               = sstr.LStr()
        outputLines        = []
        while( ( partId < len( parts ) ) or ( state == STATE_S_REST_PART ) ):
            if( state in ( STATE_S_FIRST_LINE, STATE_S_FOLLOW, STATE_S_NEW_LINE ) ):
                partContent = parts[partId]['buffer']
                newLine     = ( sstr.LStr() if currentLine == None else currentLine ) + lastSeparator + partContent
                if( True if maxWidth == None else flen( newLine ) <= maxWidth ):
                    # part fits into current line, just add it
                    currentLine   = newLine
                    lastSeparator = parts[partId]['separator']
                    if str( lastSeparator ).endswith( "\n" ):
                        outputLines.append( currentLine )
                        currentLine   = sstr.LStr.createSpacesDefaultStyle( newlineindent )
                        lastSeparator = sstr.LStr()
                        state         = STATE_S_NEW_LINE
                    partId += 1
                else:
                    # line overflowed
                    if( False if maxWidth == None else flen( partContent ) > (maxWidth - followindent) ):
                        # can use sparator and at least one char of the content?
                        if noWordBreak:
                            outputLines.append( ( sstr.LStr() if currentLine == None else currentLine ) + lastSeparator + partContent )
                            lastSeparator = sstr.LStr()
                            currentLine    = sstr.LStr.createSpacesDefaultStyle( followindent )
                            partId        += 1
                            state          = STATE_S_FOLLOW
                        else:
                            if( ( flen( (sstr.LStr() if currentLine == None else currentLine) + lastSeparator ) + 1 ) <= maxWidth ):
                                outputLines.append( newLine.substring( 0, maxWidth ) if maxWidth != None else newLine )
                                lastSeparator  = parts[partId]['separator']
                                rest           = ( newLine.substring( maxWidth, len( newLine ) ) if maxWidth != None else newLine )
                                currentLine    = sstr.LStr.createSpacesDefaultStyle( followindent ) + lstrBreakSequence
                                partId        += 1
                                state          = STATE_S_REST_PART
                            else:
                                outputLines.append( currentLine )
                                lastSeparator = sstr.LStr()
                                currentLine   = sstr.LStr.createSpacesDefaultStyle( followindent )
                                state         = STATE_S_FOLLOW
                    else:
                        # can place part into next line
                        outputLines.append( currentLine )
                        lastSeparator = sstr.LStr()
                        currentLine   = sstr.LStr.createSpacesDefaultStyle( followindent )
                        state         = STATE_S_FOLLOW
            elif( state == STATE_S_REST_PART ):
                newLine = ( sstr.LStr() if currentLine == None else currentLine ) + rest
                if( False if maxWidth == None else flen( newLine ) > maxWidth ):
                    outputLines.append( newLine.substring( 0, maxWidth ) )
                    rest        = newLine.substring( maxWidth, len( newLine ) )
                    currentLine = sstr.LStr.createSpacesDefaultStyle( followindent ) + lstrBreakSequence
                else:
                    currentLine = newLine
                    rest = sstr.LStr()
                    if( str( lastSeparator ).endswith( "\n" ) ):
                        outputLines.append( newLine )
                        lastSeparator = sstr.LStr()
                        currentLine   = sstr.LStr.createSpacesDefaultStyle( newlineindent )
                        state         = STATE_S_NEW_LINE
                    else:
                        state         = STATE_S_FOLLOW
        if( currentLine != None ):
            outputLines.append( currentLine )
        return outputLines


    @staticmethod
    def _formatRow( row: list,
                    layout: object,
                    columnSizes: list,
                    columnLayouts: list ):
        """
        Format a single table row
        """
        matrix = []

        # get lines for each column
        for columnIndex in range( 0, len( columnSizes ) ):
            column = None
            if( columnIndex < len( row ) ):
                column = row[columnIndex]
            
            columnLines = TableUtils._splitContent( column,
                                                    columnSizes[columnIndex],
                                                    columnLayouts[columnIndex]['followindent'],
                                                    columnLayouts[columnIndex]['newlineindent'],
                                                    layout.breakSequence,
                                                    False )
            matrix.append( columnLines )

        # get maximum line count
        maxLines = 0
        for column in matrix:
            if( len( column ) > maxLines ):
                maxLines = len( column )

        # format column matrix
        outputLines = []
        for lineId in range( 0, maxLines ):
            lineBuffer = sstr.LStr.createSpacesDefaultStyle( layout.borders.entryIndent )
            for columnId in range( 0, len( columnSizes ) ):
                if columnId == 0:
                    lineBuffer += sstr.SStr( layout.borders.left, style = layout.borders.style ).asLinear()
                else:
                    lineBuffer += sstr.SStr( layout.borders.center, style = layout.borders.style ).asLinear()
                columnText = sstr.LStr()
                if( len( matrix ) > columnId ):
                    if( len( matrix[columnId] ) > lineId ):
                        # derive style from default style of column
                        contentStyle = layout.getColumn( columnId )['contentstyle']
                        columnText = sstr.SStr( matrix[columnId][lineId], style = contentStyle ).asLinear()
                if( ( columnId < ( len( columnSizes ) - 1  ) or ( not layout.borders.right in (None, "" ) ) ) ):
                    lineBuffer += TableUtils._pad( columnText, columnSizes[columnId] )
                else:
                    lineBuffer += columnText
                if( (columnId == ( len( columnSizes ) - 1 ) ) and ( not layout.borders.right in (None, "" ) ) ):
                    lineBuffer += sstr.SStr( layout.borders.right, style = layout.borders.style ).asLinear()
            
            outputLines.append( lineBuffer )

        # return formatted table
        return outputLines


    @staticmethod
    def _pad( text: str,
              minSize: int ):
        """
        Pad line to a minimum count of characters
        """
        if( len( text ) < minSize ):
            return text + sstr.LStr.createSpacesDefaultStyle( minSize - len( text ) )
        else:
            return text


    @staticmethod
    def _layout( rows: list,
                 layout: object,
                 maxWidth: int   = None ):
        """
        Format table as array of lines
        """
        # abort layout if table is empty
        if( len( rows) < 1 ):
            return( [], [] )

        # count number of columns
        numberOfColumns = 0
        for row in rows:
            if( isinstance( row, (list, set) ) ):
                if( len( row ) > numberOfColumns ):
                    numberOfColumns = len( row )

        # abort layout if table is empty
        if( numberOfColumns < 1 ):
            return( [], [] )

        # get layout for each column
        columnLayouts = []
        for columnIndex in range (0, numberOfColumns):
            columnLayouts.append( copy.copy( layout.getColumn( columnIndex ) ) )

        # calculate minimum column widths
        columnSizes  = [0] * numberOfColumns
        columnLimits = [maxWidth] * numberOfColumns
        if( ( maxWidth != None ) or ( layout.preferLongLines == False ) ):
            for row in rows:
                if( isinstance( row, (list, set) ) ):
                    columnIndex = 0
                    for column in row:
                        columnMinWidth = 0
                        columnMaxWidth = maxWidth
                        for line in TableUtils._splitContent( column,
                                                              columnLayouts[columnIndex]['max'],
                                                              columnLayouts[columnIndex]['followindent'],
                                                              columnLayouts[columnIndex]['newlineindent'],
                                                              layout.breakSequence,
                                                              True ):
                            if( len( line ) > columnMinWidth ):
                                columnMinWidth = len( line )
                        if( columnSizes[columnIndex] < columnMinWidth ):
                            columnSizes[columnIndex] = columnMinWidth

                        for line in TableUtils._splitContent( column,
                                                              maxWidth,
                                                              columnLayouts[columnIndex]['followindent'],
                                                              columnLayouts[columnIndex]['newlineindent'],
                                                              layout.breakSequence,
                                                              False ):
                            if( columnMaxWidth != None ):
                                if( len( line ) < columnMaxWidth ):
                                    columnMaxWidth = len( line )
                        if( columnMaxWidth != None ):
                            if( columnLimits[columnIndex] > columnMaxWidth ):
                                columnLimits[columnIndex] = columnMaxWidth

                        columnIndex += 1
                else:
                    assert False, "no single line expected"
        else:
            for row in rows:
                if( isinstance( row, (list, set) ) ):
                    columnIndex = 0
                    for column in row:
                        colSize = 0
                        for line in str( column ).split ('\n'):
                            lineSize = len( line )
                            if( len( line ) > 0 ):
                                if( str( line )[-1] == " " ):
                                    lineSize -= 1
                            if( colSize < lineSize ):
                                colSize = lineSize
                        if( columnSizes[columnIndex] < colSize):
                            columnSizes[columnIndex] = colSize
                        if( columnLimits[columnIndex] != None ):
                            if( columnLimits[columnIndex] < colSize):
                                columnLimits[columnIndex] = colSize
                        else:
                            columnLimits[columnIndex] = colSize
                        columnIndex += 1
                else:
                    assert False, "no single line expected"
  
        # calculate space left
        framehorzsize  = len( layout.borders.left ) + len( layout.borders.right )
        framehorzsize += ( len( columnSizes ) - 1 ) * len( layout.borders.center )

        # percentual distribution
        columnPercent = []
        for column in columnLayouts:
            columnPercent.append( column['percent'] )
        columnPercentAccu = 0
        for percent in columnPercent:
            columnPercentAccu += percent
        if( columnPercentAccu <= 0 ):
            for index in range( 0, numberOfColumns ):
                columnPercent[index] += 1
            columnPercentAccu += numberOfColumns

        # shrink columns if table would overlow
        if( maxWidth != None ):
            tableWidth = framehorzsize
            for column in columnSizes:
                tableWidth += column
            if( tableWidth > maxWidth ):
                distribution = []
                for index in range( 0, numberOfColumns ):
                    distribution.append( ( maxWidth - framehorzsize ) * columnPercent[index] / columnPercentAccu )
                canRemove = []
                for index in range( 0, numberOfColumns ):
                    if( columnSizes[index] < distribution[index] ):
                        canRemove.append( 0 )
                    else:
                        minColSize = columnLayouts[index]['min']
                        v1         = columnSizes[index] - minColSize
                        v2         = columnSizes[index] - distribution[index]
                        v3         = math.floor( v1 if v1 < v2 else v2 )
                        canRemove.append( 0 if v3 < 0 else v3 )
                # distribute number of characters removeable
                removeableCount = 0
                for c in canRemove:
                    removeableCount += c
                needRemove    = tableWidth - maxWidth
                removePercent = needRemove / removeableCount
                for index in range( 0, numberOfColumns ):
                    toRemove            = math.floor( canRemove[index] * removePercent )
                    columnSizes[index] -= toRemove
                    canRemove[index]   -= toRemove
                    needRemove         -= toRemove
                # remove remainder
                while( needRemove > 0 ):
                    canRemoveSum = 0
                    for c in canRemove:
                        canRemoveSum += c
                    if( canRemoveSum < 1 ):
                        break
                    maxIndex = 0
                    maxValue = canRemove[0]
                    for index in range( 1, numberOfColumns ):
                        if( canRemove[index] > maxValue ):
                            maxIndex = index
                            maxValue = canRemove[index]
                    columnSizes[maxIndex] -= 1
                    canRemove[maxIndex]   -= 1
                    needRemove            -= 1

        # distribute space left - first pass
        if( maxWidth != None ):
            tableWidth = framehorzsize
            for column in columnSizes:
                tableWidth += column
            if( tableWidth < maxWidth ):
                percents    = []
                percentAccu = 0
                for column in columnLayouts:
                    percents.append( column['stretch'] )
                    percentAccu += column['stretch']
                if( percentAccu > 0 ):
                    canAppend    = []
                    canAppendSum = 0
                    for index in range( 0, numberOfColumns ):
                        maxLength = maxWidth
                        if( columnLayouts[index]['max'] != None ):
                            maxLength = columnLayouts[index]['max']
                        if( columnLimits[index] < maxLength ):
                            maxLength = columnLimits[index]
                        diff = maxLength - columnSizes[index]
                        if( diff < 0 ):
                            diff = 0
                        canAppend.append( diff )
                        canAppendSum += diff
                    if( canAppendSum > 0 ):
                        # distribute
                        wantAppend = (maxWidth - tableWidth)
                        factor     = wantAppend / canAppendSum
                        if( factor > 1 ):
                            factor = 1
                        for index in range( 0, numberOfColumns ):
                            additional = math.floor( canAppend[index] * factor )
                            columnSizes[index] += additional
                            canAppend[index]   -= additional
                            wantAppend         -= additional
                        # distribute rest
                        while( wantAppend > 0 ):
                            maxIndex = 0
                            maxValue = canAppend[0]
                            for index in range( 1, numberOfColumns ):
                                if( canAppend[index] > maxValue ):
                                    maxIndex = index
                                    maxValue = canAppend[index]
                            if( maxValue < 1 ):
                                break
                            columnSizes[maxIndex] += 1
                            canAppend[maxIndex]   -= 1
                            wantAppend            -= 1

        # distribute space left - second pass
        if( maxWidth != None ):
            if( layout.fillType == style.FILL_LAST ):
                tableWidth = framehorzsize
                for column in columnSizes:
                    tableWidth += column
                if( tableWidth < maxWidth ):
                    newLastSize = columnSizes[-1] + maxWidth - tableWidth
                    if( columnLayouts[-1]['max'] != None ):
                        maxLength = columnLayouts[-1]['max']
                        if( newLastSize > maxLength ):
                            newLastSize = maxLength
                    columnSizes[-1] = newLastSize
            elif( layout.fillType == style.FILL_DISTRIBUTE ):
                tableWidth = framehorzsize
                for column in columnSizes:
                    tableWidth += column
                if( tableWidth < maxWidth ):
                    wantAppend  = maxWidth - tableWidth
                    percents    = []
                    percentAccu = 0
                    for column in columnLayouts:
                        percents.append( column['stretch'] )
                        percentAccu += column['stretch']
                    if( percentAccu >= 0 ):
                        for index in range( 0, numberOfColumns ):
                            percents[index] += 1
                        percentAccu += numberOfColumns
                    # calculate max distribution
                    canAppend    = []
                    canAppendSum = 0
                    for index in range( 0, numberOfColumns ):
                        value = maxWidth - columnSizes[index]
                        if( columnLayouts[index]['max'] != None ):
                            if( ( value + columnSizes[index] ) > columnLayouts[index]['max'] ):
                                value = columnLayouts[index]['max'] - columnSizes[index]
                        if( value < 0 ):
                            value = 0
                        canAppend.append( value )
                        canAppendSum += value

                    # distribute free space according to stretch factor
                    factor = 0
                    for index in range( 0, numberOfColumns ):
                        factor += columnLayouts[index]['stretch'] * canAppend[index]
                    factor = wantAppend / factor
                    if( factor > 1 ):
                        factor = 1
                    for index in range( 0, numberOfColumns ):
                        additional = math.floor( canAppend[index] * factor * columnLayouts[index]['stretch'] )
                        columnSizes[index] += additional
                        canAppend[index]   -= additional
                        canAppendSum       -= additional
                        wantAppend         -= additional
                    # distribute rest
                    while( wantAppend > 0 ):
                        if( canAppendSum < 1 ):
                            break
                        maxIndex = 0
                        maxValue = canAppend[0]
                        for index in range( 1, numberOfColumns ):
                            if( canAppend[index] > maxValue ):
                                maxValue = canAppend[index]
                                maxIndex = index
                        columnSizes[index] += 1
                        canAppend[index]   -= 1
                        canAppendSum       -= 1
                        wantAppend         -= 1
        return( columnSizes, columnLayouts )


    @staticmethod
    def _writeCaption( layout: object, 
                       content: str,
                       maxWidth: int = None ):
        """
        Write caption line
        """
        styledContent = sstr.SStr( content, style = layout.headlineStyle )
        split = TableUtils._splitContent( styledContent,
                                          maxWidth,
                                          layout.captionfollowindent,
                                          layout.captionnewlineindent,
                                          layout.breakSequence,
                                          False )
        return split


    @staticmethod
    def _writeHeaderSeparator( layout: object,
                               columnSizes: list,
                               columnLayouts:list ):
        """
        Write header separator
        """
        if( layout.borders.headerSeparatorPresent == False ):
            return []
        line  = sstr.LStr.createSpacesDefaultStyle( layout.borders.entryIndent, layout.borders.style )
        line += sstr.SStr( layout.borders.headerSeparatorLeft ).asLinear()
        for columnIndex in range( 0, len( columnSizes ) ):
            if( columnIndex > 0 ):
                line += sstr.SStr( layout.borders.headerSeparatorCenter ).asLinear ()
            line += sstr.SStr( layout.borders.headerSeparatorFill ).asLinear() * columnSizes[columnIndex]
        if( len( columnSizes ) > 0 ):
            line += sstr.SStr( layout.borders.headerSeparatorRight ).asLinear()
        return [line]


    @staticmethod
    def _writeRowSeparator( layout: object,
                            columnSizes: list,
                            columnLayouts: list ):
        """
        Write row separator
        """
        if( layout.borders.rowSeparatorPresent == False ):
            return []
        line  = sstr.LStr.createSpacesDefaultStyle( layout.borders.entryIndent, layout.borders.style )
        line += sstr.SStr( layout.borders.rowSeparatorLeft ).asLinear()
        for columnIndex in range( 0, len( columnSizes ) ):
            if( columnIndex > 0 ):
                line += sstr.SStr( layout.borders.rowSeparatorCenter ).asLinear ()
            line += sstr.SStr( layout.borders.rowSeparatorFill ).asLinear() * columnSizes[columnIndex]
        if( len( columnSizes ) > 0 ):
            line += sstr.SStr( layout.borders.rowSeparatorRight ).asLinear ()
        return [line]
    

    @staticmethod
    def _writeInitialToCaption( layout: object,
                                columnSizes: list,
                                columnLayouts: list ):
        """
        Transition: initial -> caption
        """
        return [sstr.LStr()] * layout.borders.initialToCaptionLines


    @staticmethod
    def _writeInitialToHeader( layout: object,
                               columnSizes: list,
                               columnLayouts: list ):
        """
        Transition: initial -> header
        """
        return [sstr.LStr()] * layout.borders.initialToHeaderLines + \
               TableUtils._writeHeaderSeparator( layout,
                                                 columnSizes,
                                                 columnLayouts )


    @staticmethod
    def _writeInitialToRow( layout: object,
                            columnSizes: list,
                            columnLayouts: list ):
        """
        Transition: initial -> row
        """
        return [sstr.LStr()] * layout.borders.initialToRowLines + \
               TableUtils._writeRowSeparator( layout, columnSizes, columnLayouts )


    @staticmethod
    def _writeInitialToBreak( layout: object,
                              columnSizes: list,
                              columnLayouts: list ):
        """
        Transition: initial -> break
        """
        return []


    @staticmethod
    def _writeCaptionToCaption( layout: object,
                                columnSizes: list,
                                columnLayouts: list ):
        """
        Transition: caption -> caption
        """
        return [sstr.LStr()] * layout.borders.captionToCaptionLines


    @staticmethod
    def _writeCaptionToHeader( layout: object,
                               columnSizes: list,
                               columnLayouts: list ):
        """
        Transition: caption -> header
        """
        return [sstr.LStr()] * layout.borders.captionToHeaderLines + \
               TableUtils._writeHeaderSeparator( layout,
                                                 columnSizes,
                                                 columnLayouts )


    @staticmethod
    def _writeCaptionToRow( layout: object,
                            columnSizes: list,
                            columnLayouts: list ):
        """
        Transition: caption -> row
        """
        return [sstr.LStr()] * layout.borders.captionToRowLines + \
               TableUtils._writeRowSeparator( layout,
                                              columnSizes,
                                              columnLayouts )


    @staticmethod
    def _writeCaptionToBreak( layout: object,
                              columnSizes: list,
                              columnLayouts: list ):
        """
        Transition: caption -> break
        """
        return []


    @staticmethod
    def _writeHeaderToCaption( layout: object,
                               columnSizes: list,
                               columnLayouts: list ):
        """
        Transition: header -> caption
        """
        return [sstr.LStr()] * layout.borders.headerToCaptionLines


    @staticmethod
    def _writeHeaderToHeader( layout: object,
                              columnSizes: list,
                              columnLayouts: list ):
        """
        Transition: header -> header
        """
        return [sstr.LStr()] * layout.borders.headerToHeaderLines


    @staticmethod
    def _writeHeaderToRow( layout: object,
                           columnSizes: list,
                           columnLayouts: list ):
        """
        Transition: header -> row
        """
        return [sstr.LStr()] * layout.borders.headerToRowLines + \
               TableUtils._writeHeaderSeparator( layout,
                                                 columnSizes,
                                                 columnLayouts )


    @staticmethod
    def _writeHeaderToBreak( layout: object,
                             columnSizes: list,
                             columnLayouts: list ):
        """
        Transition: header -> break
        """
        return TableUtils._writeHeaderSeparator( layout,
                                                 columnSizes,
                                                 columnLayouts )


    @staticmethod
    def _writeRowToCaption( layout: object,
                            columnSizes: list,
                            columnLayouts: list ):
        """
        Transition: row -> caption
        """
        return TableUtils._writeRowSeparator( layout, 
                                              columnSizes,
                                              columnLayouts ) + \
               [sstr.LStr()] * layout.borders.rowToCaptionLines


    @staticmethod
    def _writeRowToHeader( layout: object,
                           columnSizes: list,
                           columnLayouts: list ):
        """
        Transition: row -> header
        """
        return TableUtils._writeRowSeparator( layout,
                                              columnSizes,
                                              columnLayouts ) + \
               [sstr.LStr()] * layout.borders.rowToHeaderLines + \
               TableUtils._writeHeaderSeparator( layout,
                                                 columnSizes,
                                                 columnLayouts )


    @staticmethod
    def _writeRowToRow( layout: object,
                        columnSizes: list,
                        columnLayouts: list ):
        """
        Transition: row -> row
        """
        return TableUtils._writeRowSeparator ( layout,
                                               columnSizes,
                                               columnLayouts )


    @staticmethod
    def _writeRowToBreak( layout: object,
                          columnSizes: list,
                          columnLayouts: list ):
        """
        Transition: row -> break
        """
        return TableUtils._writeRowSeparator( layout,
                                              columnSizes,
                                              columnLayouts )


    @staticmethod
    def _writeBreakToCaption( layout: object,
                              columnSizes: list,
                              columnLayouts: list ):
        """
        Transition: break -> caption
        """
        return [sstr.LStr()] * layout.borders.breakToCaptionLines


    @staticmethod
    def _writeBreakToHeader( layout: object,
                             columnSizes: list,
                             columnLayouts: list ):
        """
        Transition: break -> header
        """
        return [sstr.LStr()] * layout.borders.breakToHeaderLines


    @staticmethod
    def _writeBreakToRow( layout: object,
                          columnSizes: list,
                          columnLayouts: list ):
        """
        Transition: break -> row
        """
        return [sstr.LStr()] * layout.borders.breakToRowLines


    @staticmethod
    def _writeBreakToBreak( layout: object,
                            columnSizes: list,
                            columnLayouts: list ):
        """
        Transition: break -> break
        """
        return []


    @staticmethod
    def formatContent( content: list,
                       layout: object,
                       columnSizes: list,
                       columnLayouts: list,
                       maxWidth: int ):
        """
        Format table content as array of lines
        """
        outputLines   = []
        STATE_INITIAL = 0
        STATE_CAPTION = 1
        STATE_HEADER  = 2
        STATE_ROW     = 3
        STATE_BREAK   = 4
        state         = STATE_INITIAL
        contentId     = 0
        while( contentId < len( content ) ):
            currentType = content[contentId]['type']
            currentContent = content[contentId]['content']
            if( state == STATE_INITIAL ):
                if currentType == 'caption':
                    outputLines  = outputLines + TableUtils._writeInitialToCaption( layout,
                                                                                    columnSizes,
                                                                                    columnLayouts )
                    outputLines  = outputLines + TableUtils._writeCaption( layout,
                                                                           currentContent,
                                                                           maxWidth )
                    contentId   += 1
                    state        = STATE_CAPTION
                elif( currentType == 'header' ):
                    outputLines  = outputLines + TableUtils._writeInitialToHeader( layout,
                                                                                   columnSizes,
                                                                                   columnLayouts )
                    outputLines  = outputLines + TableUtils._formatRow( currentContent,
                                                                        layout,
                                                                        columnSizes,
                                                                        columnLayouts )
                    contentId   += 1
                    state        = STATE_HEADER
                elif( currentType == 'row' ):
                    outputLines  = outputLines + TableUtils._writeInitialToRow( layout,
                                                                                columnSizes,
                                                                                columnLayouts )
                    outputLines  = outputLines + TableUtils._formatRow( currentContent,
                                                                        layout,
                                                                        columnSizes,
                                                                        columnLayouts )
                    contentId   += 1
                    state        = STATE_ROW
                elif( currentType == 'break' ):
                    outputLines  = outputLines + TableUtils._writeInitialToBreak( layout,
                                                                                  columnSizes,
                                                                                  columnLayouts )
                    contentId   += 1
                    state        = STATE_BREAK
                else:
                    assert False, "type not implemented"
                
            elif( state == STATE_CAPTION ):
                if( currentType == 'caption' ):
                    outputLines  = outputLines + TableUtils._writeCaptionToCaption( layout,
                                                                                    columnSizes,
                                                                                    columnLayouts )
                    outputLines  = outputLines + TableUtils._writeCaption( layout,
                                                                           currentContent,
                                                                           maxWidth )
                    contentId   += 1
                    state        = STATE_CAPTION
                elif( currentType == 'header' ):
                    outputLines  = outputLines + TableUtils._writeCaptionToHeader( layout,
                                                                                   columnSizes,
                                                                                   columnLayouts )
                    lines        = TableUtils._formatRow( currentContent,
                                                          layout,
                                                          columnSizes,
                                                          columnLayouts )
                    outputLines  = outputLines + lines
                    contentId   += 1
                    state        = STATE_HEADER
                elif( currentType == 'row' ):
                    outputLines  = outputLines + TableUtils._writeCaptionToRow( layout,
                                                                                columnSizes,
                                                                                columnLayouts )
                    lines        = TableUtils._formatRow( currentContent,
                                                          layout,
                                                          columnSizes,
                                                          columnLayouts )
                    outputLines  = outputLines + lines
                    contentId   += 1
                    state        = STATE_ROW
                elif( currentType == 'break' ):
                    outputLines  = outputLines + TableUtils._writeCaptionToBreak( layout,
                                                                                  columnSizes,
                                                                                  columnLayouts )
                    contentId   += 1
                    state        = STATE_BREAK
                else:
                    assert False, "type not implemented"

            elif( state == STATE_HEADER ):
                if currentType == 'caption':
                    outputLines  = outputLines + TableUtils._writeHeaderToCaption( layout,
                                                                                   columnSizes,
                                                                                   columnLayouts )
                    outputLines  = outputLines + TableUtils._writeCaption( layout,
                                                                           currentContent,
                                                                           maxWidth )
                    contentId   += 1
                    state        = STATE_CAPTION
                elif( currentType == 'header' ):
                    outputLines  = outputLines + TableUtils._writeHeaderToHeader( layout,
                                                                                  columnSizes,
                                                                                  columnLayouts )
                    lines        = TableUtils._formatRow( currentContent,
                                                          layout,
                                                          columnSizes,
                                                          columnLayouts )
                    outputLines  = outputLines + lines
                    contentId   += 1
                    state        = STATE_HEADER
                elif( currentType == 'row' ):
                    outputLines  = outputLines + TableUtils._writeHeaderToRow( layout,
                                                                               columnSizes,
                                                                               columnLayouts )
                    lines        = TableUtils._formatRow( currentContent,
                                                          layout,
                                                          columnSizes,
                                                          columnLayouts )
                    outputLines  = outputLines + lines
                    contentId   += 1
                    state        = STATE_ROW
                elif( currentType == 'break' ):
                    outputLines  = outputLines + TableUtils._writeHeaderToBreak( layout,
                                                                                 columnSizes,
                                                                                 columnLayouts )
                    contentId   += 1
                    state        = STATE_BREAK
                else:
                    assert False, "type not implemented"

            elif( state == STATE_ROW ):
                if( currentType == 'caption' ):
                    outputLines  = outputLines + TableUtils._writeRowToCaption( layout,
                                                                                columnSizes,
                                                                                columnLayouts )
                    outputLines  = outputLines + TableUtils._writeCaption( layout,
                                                                           currentContent,
                                                                           maxWidth )
                    contentId   += 1
                    state        = STATE_CAPTION
                elif( currentType == 'header' ):
                    outputLines  = outputLines + TableUtils._writeRowToHeader( layout,
                                                                               columnSizes,
                                                                               columnLayouts )
                    lines        = TableUtils._formatRow( currentContent,
                                                          layout,
                                                          columnSizes,
                                                          columnLayouts )
                    outputLines  = outputLines + lines
                    contentId   += 1
                    state        = STATE_HEADER
                elif( currentType == 'row' ):
                    outputLines  = outputLines + TableUtils._writeRowToRow( layout,
                                                                            columnSizes,
                                                                            columnLayouts )
                    lines        = TableUtils._formatRow( currentContent,
                                                          layout,
                                                          columnSizes,
                                                          columnLayouts )
                    outputLines  = outputLines + lines
                    contentId   += 1
                    state        = STATE_ROW
                elif( currentType == 'break' ):
                    outputLines  = outputLines + TableUtils._writeRowToBreak( layout,
                                                                              columnSizes,
                                                                              columnLayouts )
                    contentId   += 1
                    state        = STATE_BREAK
                else:
                    assert False, "type not implemented"

            elif( state == STATE_BREAK ):
                if currentType == 'caption':
                    outputLines  = outputLines + TableUtils._writeBreakToCaption( layout,
                                                                                  columnSizes,
                                                                                  columnLayouts )
                    outputLines  = outputLines + TableUtils._writeCaption( layout,
                                                                           currentContent,
                                                                           maxWidth )
                    contentId   += 1
                    state        = STATE_CAPTION
                elif( currentType == 'header' ):
                    outputLines  = outputLines + TableUtils._writeBreakToHeader( layout,
                                                                                 columnSizes,
                                                                                 columnLayouts )
                    lines        = TableUtils._formatRow( currentContent,
                                                          layout,
                                                          columnSizes,
                                                          columnLayouts )
                    outputLines  = outputLines + lines
                    contentId   += 1
                    state        = STATE_HEADER
                elif( currentType == 'row' ):
                    outputLines  = outputLines + TableUtils._writeBreakToRow( layout,
                                                                              columnSizes,
                                                                              columnLayouts )
                    lines        = TableUtils._formatRow( currentContent,
                                                          layout,
                                                          columnSizes,
                                                          columnLayouts )
                    outputLines  = outputLines + lines
                    contentId   += 1
                    state        = STATE_ROW
                else:
                    assert False, "type not implemented"

            else:
                assert False, "invalid state"

        # go to break state
        if( state == STATE_INITIAL ):
            outputLines = outputLines + TableUtils._writeInitialToBreak( layout,
                                                                         columnSizes,
                                                                         columnLayouts )
            state       = STATE_BREAK
        elif( state == STATE_CAPTION ):
            outputLines = outputLines + TableUtils._writeCaptionToBreak( layout,
                                                                         columnSizes,
                                                                         columnLayouts )
            state       = STATE_BREAK
        elif( state == STATE_HEADER ):
            outputLines = outputLines + TableUtils._writeHeaderToBreak( layout,
                                                                        columnSizes,
                                                                        columnLayouts )
            state       = STATE_BREAK
        elif( state == STATE_ROW ):
            outputLines = outputLines + TableUtils._writeRowToBreak( layout,
                                                                     columnSizes,
                                                                     columnLayouts )
            state       = STATE_BREAK
        elif( state == STATE_BREAK ):
            pass
        else:
            assert False, "invalid state"

        # return output
        return outputLines




class Layoutable:
    """
    Layoutable item
    """
    pass




class TableContent:
    def __init__( self ):
        """
        Table content
        """
        self.content = []


    def caption( self, text: object ):
        """
        Add a caption to the table formatter
        """
        self.content.append( { 'type':    'caption',
                               'content': text } )


    def header( self,
                row: list ):
        """
        Add a table header
        """
        self.content.append( { 'type':    'header',
                               'content': row } )


    def row( self, row: list ):
        """
        Add a table row
        """
        self.content.append( { 'type':    'row',
                               'content': row } )


    def space( self ):
        """
        Add a space (break)
        """
        self.content.append( { 'type':    'break',
                               'content': None } )




class Table( TableContent, Layoutable ):
    def __init__( self,
                  layout: object = None ):
        """
        Formatted table
        """
        super().__init__()

        # set layout
        if layout is None:
            self.layout = style.Defaults.getTableLayout()
        else:
            self.layout = layout


    def format( self,
                maxWidth: int             = None,
                defaultStyle: object      = None,
                lineBreakSettings: object = None ):
        """
        Format table
        """
        # layout use for formatting tables
        layout = self.layout

        # calculate table layout
        maxFormatWidth = maxWidth
        if( maxFormatWidth != None ):
            maxFormatWidth -= layout.borders.entryIndent
        rowsForLayout = []
        for content in self.content:
            if( content['type'] in ('row', 'header') ):
                rowsForLayout.append( content['content'] )
        (columnSizes, columnLayouts) = TableUtils._layout( rowsForLayout,
                                                           layout,
                                                           maxFormatWidth )

        # format table
        return TableUtils.formatContent( self.content,
                                         layout,
                                         columnSizes,
                                         columnLayouts,
                                         maxWidth )




class TreeElement:
    def __init__( self,
                  headLine: str  = None,
                  children: list = None ):
        """
        Element of formatted tree
        """
        self.children = children if children != None else []
        self.head     = TableContent()
        self.content  = TableContent()
        if( headLine != None ):
            self.head.caption( headLine )


    def add( self,
             element: object ):
        """
        Add child element
        """
        self.children.append( element )


    def _countLevels( self ):
        """
        Count levels of tree
        """
        levels = 1
        for child in self.children:
            lc = 1 + child._countLevels()
            if( lc > levels ):
                levels = lc
        return levels


    def _collectHeadRows( self,
                          rows: list ):
        """
        Collect head rows of tree items
        """
        # collect head rows of self
        for row in self.head.content:
            if( row['type'] in ('header', 'row')):
                rows.append( row['content'] )
        # collect heads of children
        for child in self.children:
            rows = rows + child._collectHeadRows( rows )
        return rows


    def _collectContentRows( self,
                             rows: list ):
        """
        Collect head rows of tree contents
        """
        for row in self.content.content:
            if( row['type'] in ('header', 'row')):
                rows.append( row['content'] )
        # collect heads of children
        for child in self.children:
            child._collectContentRows( rows )


    def _format( self,
                 outputLines,
                 indentation,
                 startIndentation,
                 contentColumnSizes,
                 contentColumnLayouts,
                 contentBaseIndent,
                 treeLayout,
                 maxWidth,
                 level ):
        """
        Format tree entry (recursive)
        """
        # init indentation strings
        indentSpaceStr  = " "
        indentFollowStr = "|"
        indentItemStr   = "+"
        indentLastStr   = "+"

        # set length of indentation
        count = treeLayout.levelIndent - 2
        indentSpaceStr  += " " * count
        indentFollowStr += " " * count
        indentItemStr   += "-" * count
        indentLastStr   += "-" * count

        # style for edges
        style = treeLayout.edgeStyles[level % len( treeLayout.edgeStyles )]

        # add space after indentation
        indentSpaceStr  = sstr.SStr( indentSpaceStr + ' ', style = style ).asLinear()
        indentFollowStr = sstr.SStr( indentFollowStr + ' ', style = style ).asLinear()
        indentItemStr   = sstr.SStr( indentItemStr + ' ', style = style ).asLinear()
        indentLastStr   = sstr.SStr( indentLastStr + ' ', style = style ).asLinear()
        
        # create sub indentation
        newIndentation = indentation + [ indentFollowStr ]

        # create indentation string
        indentString = sstr.SStr( *indentation ).asLinear()

        # create indentation string
        startIndentString = sstr.SStr( *startIndentation, style = style ).asLinear()

        # format head of tree item
        if( maxWidth != None ):
            maxHeadWidth = maxWidth - len( indentString )
            if( maxHeadWidth < 1 ):
                maxHeadWidth = 1
        else:
            maxHeadWidth = None
        headTable = Table( treeLayout.headLayout )
        headTable.content = self.head.content
        headLines = headTable.format( maxHeadWidth )
        for lineIndex in range( len( headLines ) ):
            line = headLines[lineIndex]
            if( len( self.children ) > 0 ):
                # add tree bar to 2nd line and followers
                if( lineIndex >= 1 ):
                    if( str( line ).startswith( ' ' ) ):
                        line = sstr.SStr( '|', style = style ).asLinear() + line.substring(1, len( line ) )
                    else:
                        line = sstr.SStr( '|', style = style ).asLinear() + line
            if( lineIndex == 0 ):
                outputLines = outputLines + [ startIndentString + line ]
            else:
                outputLines = outputLines + [ indentString + line ]

        # format content of tree item
        contentPrefix = indentString.copy()
        if( len( self.children ) > 0 ):
            contentPrefix += sstr.SStr( "|", style = style ).asLinear()
        else:
            contentPrefix += sstr.SStr( " " ).asLinear()
            pass
        if( treeLayout.sameContentLayout == True ):
            if( maxWidth != None ):
                if( treeLayout.sameContentIndent == True ):
                    maxContentWidth = maxWidth - contentBaseIndent
                else:
                    maxContentWidth = maxWidth
                maxContentWidth -= treeLayout.contentIndent
                if( maxContentWidth < 1 ):
                    maxContentWidth = 1
            else:
                maxContentWidth = None
            if( treeLayout.sameContentIndent != True ):
                cSize = contentColumnSizes + []
                cSize[-1] += contentBaseIndent - len( contentPrefix )
            else:
                cSize = contentColumnSizes
            contentLines = TableUtils.formatContent( self.content.content,
                                                     treeLayout.contentLayout,
                                                     cSize,
                                                     contentColumnLayouts,
                                                     maxContentWidth)
            if( treeLayout.sameContentIndent == True ):
                count = 1 + contentBaseIndent - len( contentPrefix )
                contentPrefix += sstr.SStr( " " * count ).asLinear()
            contentPrefix += sstr.SStr( " " * treeLayout.contentIndent ).asLinear()
            for lineIndex in range( len( contentLines ) ):
                line = contentLines[lineIndex]
                outputLines = outputLines + [ contentPrefix + line ]
        else:
            # format content of tree item, dont care about same layouts
            if( maxWidth != None ):
                maxContentWidth = maxWidth - len( indentString ) - treeLayout.contentIndent
                if( treeLayout.sameContentIndent == True ):
                    maxContentWidth -= ( contentBaseIndent - len( contentPrefix ) )
                    maxContentWidth -= 1
                maxContentWidth -= 1
                if( maxContentWidth < 1 ):
                    maxContentWidth = 1
            else:
                maxContentWidth = None
            contentTable = Table( treeLayout.contentLayout )
            contentTable.content = self.content.content
            contentLines = contentTable.format( maxContentWidth )
            contentPrefix += " " * treeLayout.contentIndent
            if( treeLayout.sameContentIndent == True ):
                count = 1 + ( contentBaseIndent + treeLayout.contentIndent ) - len( contentPrefix )
                contentPrefix += " " * count
            for lineIndex in range( len( contentLines ) ):
                line = contentLines[lineIndex]
                outputLines = outputLines + [ contentPrefix + line ]

        # format children
        for childIndex in range( len( self.children ) ):
            child = self.children[childIndex]
            lastChild = childIndex >= ( len( self.children ) -1 )
            newIndentation = indentation + ( [ indentSpaceStr ] if lastChild else [ indentFollowStr ] )
            newStartIndentation = indentation + ( [ indentLastStr ] if lastChild else [ indentItemStr ] )

            # line clearance before child tree item
            for index in range( treeLayout.lineClearance ):
                outputLines.append( indentString + indentFollowStr )

            # format child
            outputLines = child._format( outputLines,
                                         newIndentation,
                                         newStartIndentation,
                                         contentColumnSizes,
                                         contentColumnLayouts,
                                         contentBaseIndent,
                                         treeLayout,
                                         maxWidth,
                                         level + 1 )

        # return rendered tree
        return outputLines




class Tree( Layoutable ):
    def __init__( self,
                  children: list = None,
                  layout: object = None ):
        """
        Formatted tree
        """
        self.children = children if children != None else []
        self.layout   = layout   if layout != None   else style.Defaults.getTreeLayout()


    def add( self,
             element: object ):
        """
        Add child element
        """
        self.children.append( element )


    def format( self,
                maxWidth: int             = None,
                defaultStyle: object      = None,
                lineBreakSettings: object = None ):
        """
        Format tree
        """
        # initial content max width
        contentMaxWidth = maxWidth

        # get maximum tree depth (levels)
        levels = 0
        for child in self.children:
            lc = child._countLevels()
            if( lc > levels ):
                levels = lc

        # is tree empty?
        if( levels < 0 ):
            return []

        # calulate maxWidth for headlines after leveling
        if maxWidth != None:
            if maxWidth < 1:
                maxWidth = 1

        # calulate maxWidth for content after leveling
        contentBaseIndent = ( self.layout.levelIndent * ( levels - 1 ) ) # + self.layout.contentIndent
        contentLayoutWidth = None
        if( contentMaxWidth != None ):
            contentMaxWidth -= contentBaseIndent
            if( self.layout.sameContentIndent and self.layout.sameContentLayout ):
                contentMaxWidth -= 1
            contentLayoutWidth = contentMaxWidth - self.layout.contentLayout.borders.entryIndent
            contentLayoutWidth -= self.layout.contentIndent
            if( contentLayoutWidth < 1 ):
                contentLayoutWidth = 1

        # layout content
        contentRows = []
        for child in self.children:
            child._collectContentRows( contentRows )
        if( self.layout.sameContentLayout ):
            ( contentColumnSizes, contentLayouts ) = TableUtils._layout( contentRows,
                                                                        self.layout.contentLayout,
                                                                        contentLayoutWidth )
        else:
            contentColumnSizes = None
            contentLayouts = None

        # format tree
        outputLines = []
        for childIndex in range( len( self.children ) ):
            child = self.children[childIndex]
            # line clearance before child tree item
            if( childIndex > 0 ):
                for index in range( self.layout.lineClearance ):
                    outputLines.append( "" )

            outputLines = child._format( outputLines,
                                         [],
                                         [],
                                         contentColumnSizes,
                                         contentLayouts,
                                         contentBaseIndent,
                                         self.layout,
                                         maxWidth,
                                         0 )
        return outputLines
