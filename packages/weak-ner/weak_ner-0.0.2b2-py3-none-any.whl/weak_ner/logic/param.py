NAME_PATTERNS = [r'(SUBS\s){1,4}PREP(\sSUBS){1,3}((\sPREP|\sCONJ)\sSUBS)?',
                 r'(SUBS\s){1,4}SUBS\s?',
                 r'SUBS']

DATE_PATTERNS = [r'NUM\sPREP\sSUBS\sPREP\sNUM\s(NUM\sCONJ\s){1,2}NUM',
                 r'NUM\sCONJ\sNUM\sPREP\sSUBS\s(PREP(\sNUM)*)?',
                 r'NUM\sPREP\sSUBS((\sPREP)?(\sNUM))?',
                 r'NUM\sART\sPREP\sSUBS',
                 r'NUM\sPREP\sSUBS',
                 r'(SUBS\s|VERB\s)NUM']

FINANCIAL_PATTERNS = [r'SUBS\sPREP\s(SUBS\sPREP\s|ART\s){0,1}SUBS',
                      r'SUBS(\sART)?(\sSUBS)?']

LOCATION_PATTERNS = [r'ADJ\sSUBS',
                     r'SUBS\sPREP\sSUBS',
                     r'SUBS(\sSUBS){0,3}']

ADDRESS_PATTERNS = [r'SUBS\sPREP(\sSUBS){2,3}',
                    r'INT\sPREP(\sSUBS){2,3}',
                    r'INT\sPON\s',
                    r'(SUBS\s){2,4}PREP\sSUBS',
                    r'(SUBS\s){1,3}INT\s(SUBS\s)?PREP\sSUBS',
                    r'INT\s(SUBS\s){1,3}PREP\sSUBS',
                    r'(INT\s){2}(SUBS\s){0,2}PREP\sSUBS',
                    r'(INT\s)?SUBS(\sSUBS)*',
                    r'INT\sPREP\sSUBS\s(PREP\s)?(NUM)?']

GENERIC_PATTERNS = [r'ART\sPRON\sSUBS(\sPREP\sSUBS){0,1}',
                    r'ART\sSUBS\sPREP\sSUBS',
                    r'ART(\sSUBS){1,3}',
                    r'ART\sPREP\sSUBS\sPREP\sSUBS',
                    r'SUBS(\sPREP\sSUBS){1,2}',
                    r'PREP\sSUBS\s(PREP\s){0,1}SUBS',
                    r'PRON\sSUBS(\sPREP\sSUBS){0,1}']

ENTITIES = ['GEN', 'DOC', 'COMP', 'WD', 'REL', 'VOC', 'PHONE', 'MONEY', 'NUMBER', 'EMAIL']
ENTITY_PATTERNS = {'PERS': NAME_PATTERNS,
                   'DATE': DATE_PATTERNS,
                   'FIN': FINANCIAL_PATTERNS,
                   'LOC': LOCATION_PATTERNS,
                   'ADDR': ADDRESS_PATTERNS,
                   'GEN': GENERIC_PATTERNS}

WORD_LOCATION = ['de', 'em', 'para', 'pra']
WORDS_NAMES = ['a', 'o', 'com', 'e', 'da', 'do']
WORDS_REPLACE_LOCATION_O = ['modelo', 'datas', 'pendencias', 'graca']
WORDS_REPLACE_LOCATION_GEN = ['registro', 'marcacao', 'passagem']

LOCAL_ENTITY_PATTERN = r'((^|O\s)B-LOC(\sO|$))'
PERSON_ENTITY_PATTERN = r'((^|O\s)B-PERS(\sO|$))'
FINANCIAL_ENTITY_PATTERN = r'-FIN\sB-GEN(\sI-GEN)*'
WD_ENTITY_PATTERN = r'segunda'
