import re
from sly import Lexer


class MindsDBLexer(Lexer):
    reflags = re.IGNORECASE
    ignore = ' \t\n\r'

    tokens = {
        CREATE, USE, DROP,

        # SHOW Keywords

        SHOW, SCHEMAS, DATABASES, TABLES, TABLE, FULL, VARIABLES, SESSION, STATUS,
        GLOBAL, PROCEDURE, FUNCTION, INDEX, CREATE, WARNINGS, ENGINES, CHARSET, COLLATION,
        VIEW, VIEWS, PREDICTOR, PREDICTORS, INTEGRATION, INTEGRATIONS,
        STREAM, STREAMS, PUBLICATION, PUBLICATIONS,

        # Mindsdb special
        LATEST,

        ENGINE, TRAIN, TEST, PREDICT, MODEL,

        # SELECT Keywords
        WITH, SELECT, DISTINCT, FROM, WHERE, AS,
        LIMIT, OFFSET, ASC, DESC, NULLS_FIRST, NULLS_LAST,
        GROUP_BY, HAVING, ORDER_BY,
        STAR,

        JOIN, INNER, OUTER, CROSS, LEFT, RIGHT, ON,

        UNION, ALL,

        # Special
        COMMA, LPAREN, RPAREN, PARAMETER,

        # Operators
        PLUS, MINUS, DIVIDE, MODULO,
        EQUALS, NEQUALS, GREATER, GEQ, LESS, LEQ,
        AND, OR, NOT, IS,
        IN, LIKE, CONCAT, BETWEEN, WINDOW,

        # Data types
        CAST, ID, INTEGER, FLOAT, STRING, NULL, TRUE, FALSE}

    # Custom commands

    USE = r'\bUSE\b'
    CREATE = r'\bCREATE\b'
    ENGINE = r'\bENGINE\b'
    TRAIN = r'\bTRAIN\b'
    TEST = r'\bTEST\b'
    PREDICT = r'\bPREDICT\b'
    MODEL = r'\bMODEL\b'
    DROP = r'\bDROP\b'

    # SHOW

    SHOW = r'\bSHOW\b'
    SCHEMAS = r'\bSCHEMAS\b'
    DATABASES = r'\bDATABASES\b'
    TABLES = r'\bTABLES\b'
    TABLE = r'\bTABLE\b'
    FULL = r'\bFULL\b'
    VARIABLES = r'\bVARIABLES\b'
    SESSION = r'\bSESSION\b'
    STATUS = r'\STATUS\b'
    GLOBAL = r'\bGLOBAL\b'
    PROCEDURE = r'\bPROCEDURE\b'
    FUNCTION = r'\bFUNCTION\b'
    INDEX = r'\bINDEX\b'
    WARNINGS = r'\bWARNINGS\b'
    ENGINES = r'\bENGINES\b'
    CHARSET = r'\bCHARSET\b'
    COLLATION = r'\bCOLLATION\b'

    VIEW = r'\bVIEW\b'
    VIEWS = r'\bVIEWS\b'
    STREAM = r'\bSTREAM\b'
    STREAMS = r'\bSTREAMS\b'
    PREDICTOR = r'\bPREDICTOR\b'
    PREDICTORS = r'\bPREDICTORS\b'
    INTEGRATION = r'\bINTEGRATION\b'
    INTEGRATIONS = r'\bINTEGRATIONS\b'
    PUBLICATION = r'\bPUBLICATION\b'
    PUBLICATIONS = r'\bPUBLICATIONS\b'

    # SELECT

    # Keywords
    ON = r'\bON\b'
    ASC = r'\bASC\b'
    DESC = r'\bDESC\b'
    NULLS_FIRST = r'\bNULLS FIRST\b'
    NULLS_LAST = r'\bNULLS LAST\b'
    WITH = r'\bWITH\b'
    SELECT = r'\bSELECT\b'
    DISTINCT = r'\bDISTINCT\b'
    FROM = r'\bFROM\b'
    AS = r'\bAS\b'
    WHERE = r'\bWHERE\b'
    LIMIT = r'\bLIMIT\b'
    OFFSET = r'\bOFFSET\b'
    GROUP_BY = r'\bGROUP BY\b'
    HAVING = r'\bHAVING\b'
    ORDER_BY = r'\bORDER BY\b'
    STAR = r'\*'
    LATEST = r'\bLATEST\b'

    JOIN = r'\bJOIN\b'
    INNER = r'\bINNER\b'
    OUTER = r'\bOUTER\b'
    CROSS = r'\bCROSS\b'
    LEFT = r'\bLEFT\b'
    RIGHT = r'\bRIGHT\b'

    UNION = r'\bUNION\b'
    ALL = r'\bALL\b'

    # Special
    COMMA = r','
    LPAREN = r'\('
    RPAREN = r'\)'
    PARAMETER = r'\?'

    # Operators
    PLUS = r'\+'
    MINUS = r'-'
    DIVIDE = r'/'
    MODULO = r'%'
    EQUALS = r'='
    NEQUALS = r'!='
    GEQ = r'>='
    GREATER = r'>'
    LEQ = r'<='
    LESS = r'<'
    AND = r'\bAND\b'
    OR = r'\bOR\b'
    NOT = r'\bNOT\b'
    IS = r'\bIS\b'
    LIKE = r'\bLIKE\b'
    IN = r'\bIN\b'
    CAST = r'\bCAST\b'
    CONCAT = r'\|\|'
    BETWEEN = r'\bBETWEEN\b'
    WINDOW = r'\bWINDOW\b'

    # Data types
    NULL = r'\bNULL\b'
    TRUE = r'\bTRUE\b'
    FALSE = r'\bFALSE\b'

    @_(r'([a-zA-Z_][a-zA-Z_0-9]*|`([^`]+)`)(\.([a-zA-Z_][a-zA-Z_.0-9]*|`([^`]+)`))*')
    def ID(self, t):
        return t

    @_(r'\d+\.\d+')
    def FLOAT(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INTEGER(self, t):
        t.value = int(t.value)
        return t

    @_(r'"[^"]*"',
       r"'[^']*'")
    def STRING(self, t):
        if t.value[0] == '"':
            t.value = t.value.strip('\"')
        else:
            t.value = t.value.strip('\'')
        return t
