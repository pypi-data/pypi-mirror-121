import typing as tp

import regex

from weak_ner.logic.entities import Entities
from weak_ner.logic.rule_based_model.name_location_rules import replace_for_saude, replace_for_luz, replace_for_porto

from weak_ner.logic.param import WORD_LOCATION, WORDS_NAMES, WORDS_REPLACE_LOCATION_O, WORDS_REPLACE_LOCATION_GEN, \
    LOCAL_ENTITY_PATTERN, PERSON_ENTITY_PATTERN, FINANCIAL_ENTITY_PATTERN, WD_ENTITY_PATTERN


class WeakNERRules:
    """
        Class responsible for correcting entity labels in a sentence.
        The corrections are based on rules created by the patterns observed on portuguese syntax.
        
        Methods:
        -------
            * correct_tags: Correct a labeled sentence based in rules.
    """
    
    def __init__(self,  entity_sets: Entities):
        """
            Initializes the class with the default words and entity patterns.

        :param entity_sets: Entities class with the entities set read from the lists.
        :type entity_sets: ´Entities´
        """
        self.__entity_sets = entity_sets
        
        self.__set_local_name()
        self.__compile_pattern()
        
        self.__functions_2_apply = [self.__apply_rules_location_name,
                                    self.__apply_rules_location,
                                    self.__apply_rules_names,
                                    self.__apply_rules_financial,
                                    self.__apply_rules_wd]
        
        self.__words_location = WORD_LOCATION
        self.__words_names = WORDS_NAMES
        self.__words_replace_location_o = WORDS_REPLACE_LOCATION_O
        self.__words_replace_location_gen = WORDS_REPLACE_LOCATION_GEN
    
    def correct_tags(self, sentence: str, ner: str) -> tp.Tuple[str, str]:
        """
        Correct a labeled sentence based in rules. First it verifies the
        need for correction, after that the rules are applies and the new labels are returned.

        :param sentence: string of a message
        :type sentence: ``str``
        :param ner: string of the label of words in a sentence
        :type ner: ``str``
        :return: A tuple with the preprocessed sentence and the new labels for the words on the sentence.
        :rtype: `tp.Tuple[str, str]`
        """
        for current_function in self.__functions_2_apply:
            ner = current_function(sentence=sentence, ner=ner)
        return sentence, ner
    
    def __set_local_name(self):
        """
        Create a set with the intersection between the list of local and the list of names and surnames.
        """
        self.local_or_name = [local for local in self.__entity_sets.locations if self.__check_local_is_name(local)]
    
    def __compile_pattern(self) -> None:
        """
        Compile regex patterns beforehand to match local, person, financial and weekday patterns.
        """
        self.local_pattern = regex.compile(LOCAL_ENTITY_PATTERN)
        self.person_pattern = regex.compile(PERSON_ENTITY_PATTERN)
        self.financial_pattern = regex.compile(FINANCIAL_ENTITY_PATTERN)
        self.wd_pattern = regex.compile(WD_ENTITY_PATTERN)
    
    def __check_local_is_name(self, local: str) -> bool:
        """
        Check if all words in a local is in the name or surnames list.
        Basically check if the local could be a name.

        :param local: a local name
        :type local: ``str``
        :return: if the location could be a name.
        :rtype: ``bool``
        """
        return all([word in self.__entity_sets.names or word in self.__entity_sets.surnames
                    or word in self.__entity_sets.prepositions for word in local.split()])
    
    @staticmethod
    def __replace_for_other(ner: tp.List[str], index: int) -> tp.List[str]:
        """
        Replace the label in the index with the label 'O'

        Example:
        Previous labels: ['O', 'B-LOC', 'O', 'B-PERS']
        Index: 1
        New labels: ['O', 'O', 'O', 'B-PERS']

        :param ner: list with all the labels of a sentence
        :type ner: ``tp.List[str]``
        :param index: a number indicate which label to change
        :type index: ``int``
        :return: a list with all the new labels of a sentence
        :rtype: ``tp.List[str]``
        """
        ner[index] = 'O'
        return ner
    
    @staticmethod
    def __replace_for_entity(ner: tp.List[str], index: int) -> tp.List[str]:
        """
        Replace the label in the index with the label 'B-GEN'

        Example:
        Previous labels: ['O', 'B-LOC', 'O', 'B-PERS']
        Index: 1
        New labels: ['O', 'B-GEN', 'O', 'B-PERS']

        :param ner: list with all the labels of a sentence
        :type ner: ``tp.List[str]``
        :param index: a number indicate which label to change
        :type ner: ``int``
        :return: a list with all the new labels of a sentence
        :rtype: ``tp.List[str]``
        """
        ner[index] = 'B-GEN'
        return ner
    
    def __replace_local_or_name(self, sentence: tp.List[str], ner: tp.List[str], index: int) -> tp.List[str]:
        """
        Replace the label of a word that could be a name or a local. If
        the word is the first word of the sentence replace the label by
        'B-PERS'. Else if the previous word is any word that imply
        location the label is replace to 'B-LOC'. Else if the previous
        word is any word that imply name the label is replace to 'B-PERS'.
        Else is replace by 'O'.

        Example:

        First example:

        Sentence: 'Mariana gostaria de falar sobre ...'
        Previous Labels: 'B-LOC O O O O ...'
        New Labels: 'B-PERS O O O O ...'

        Second example:

        Sentence: 'Eu sou de Mariana ....'
        Previous Labels: 'O O O B-LOC ...'
        New Labels: 'O O O B-LOC ... '

        Third example:

        Sentence: 'Quero falar com Mariana ...'
        Previous Labels: 'O O O B-LOC ...'
        New Labels: 'O O O B-PERS ...'

        Last example:

        Sentence: 'Eu não sei Mariana ....'
        Previous Labels: 'O O O B-LOC ...'
        New Labels: 'O O O B-GEN ...'

        :param sentence: list with words of a sentence
        :type sentence: ``tp.List[str]``
        :param ner: list with all the labels of a sentence
        :type ner: ``tp.List[str]``
        :param index: a number indicate which label to change
        :type ner: ``int``
        :return: a list with all the new labels of a sentence
        :rtype: ``tp.List[str]``
        """
        if index == 0:
            ner[index] = 'B-PERS'
        elif sentence[index - 1] in self.__words_location:
            ner[index] = 'B-LOC'
        elif sentence[index - 1] in self.__words_names or sentence[index - 1] in self.interjection:
            ner[index] = 'B-PERS'
        else:
            ner[index] = 'B-GEN'
        return ner

    def __apply_rules_location(self, sentence: str, ner: str) -> str:
        """
        If the entity pattern 'O B-LOC O' can be found in a labeled sentence
        it applies a set of rules to correct the labeling.
        
        The rules are:
        If the word is in one of the preset lists it changes to either O or GEN, depending on the list it is found in.
        If the word is saude it utilizes the rule for this word.

        :param sentence: string of a message
        :type sentence: ``str``
        :param ner: string of the label of words in a sentence
        :type ner: ``str``
        :return: string with the news labels.
        :rtype: ``str``
        """
        msg_list = sentence.split()
        ner_list = ner.split()
        
        for match in self.local_pattern.finditer(ner, overlapped=True):
            ind = len(ner[:match.end() - 2].split()) - 1
            if msg_list[ind] in self.__words_replace_location_o:
                ner_list = self.__replace_for_other(ner_list, ind)
            elif msg_list[ind] in self.__words_replace_location_gen:
                ner_list = self.__replace_for_entity(ner_list, ind)
            elif msg_list[ind] == 'saude':
                ner_list = replace_for_saude(msg_list, ner_list, ind)
        return ' '.join(ner_list)
    
    def __apply_rules_location_name(self, sentence: str, ner: str) -> str:
        """
        Find a word that could be a name or location and apply the rules.

        :param sentence: string of a message
        :type sentence: ``str``
        :param ner: string of the label of words in a sentence
        :type ner: ``str``
        :return: string with the news labels.
        :rtype: ``str``
        """
        msg_list = sentence.split()
        ner_list = ner.split()
        
        for index in range(len(msg_list)):
            word = msg_list[index]
            if word in self.local_or_name and ner_list[index] == 'B-LOC':
                if word == 'porto':
                    ner_list = replace_for_porto(msg_list,
                                                        ner_list,
                                                        index)
                elif word == 'luz':
                    ner_list = replace_for_luz(msg_list,
                                                      ner_list,
                                                      index)
                else:
                    ner_list = self.__replace_local_or_name(msg_list,
                                                            ner_list,
                                                            index)
        return ' '.join(ner_list)
    
    def __apply_rules_names(self, sentence: str, ner: str) -> str:
        """
        If the entity pattern 'O B-PERS O' can be found in a labeled sentence
        it applies a set of rules to correct the labeling.
        
        The rules are:
        If the word is in the list of surname, but not in the list of names the label is changed to 'O'.

        :param sentence: string of a message
        :type sentence: ``str``
        :param ner: string of the label of words in a sentence
        :type ner: ``str``
        :return: string with the news labels.
        :rtype: ``str``
        """
        msg_list = sentence.split()
        ner_list = ner.split()
        
        for match in self.person_pattern.finditer(ner, overlapped=True):
            ind = len(ner[:match.end() - 2].split()) - 1
            if msg_list[ind] in self.__entity_sets.surnames and msg_list[ind] not in self.__entity_sets.names:
                ner_list[ind] = 'O'
        return ' '.join(ner_list)
    
    def __apply_rules_financial(self, sentence: str, ner: str) -> str:
        """
        If the entity pattern '-FIN B-GEN ...' can be found in a labeled sentence
        it applies the following rule to correct the labeling.
        
        If the GEN entity starts with a preposition the label is changed to FIN.
  
        :param sentence: string of a message
        :type sentence: ``str``
        :param ner: string of the label of words in a sentence
        :type ner: ``str``
        :return: string with the news labels.
        :rtype: ``str``
        """
        msg_list = sentence.split()
        ner_list = ner.split()
        
        for match in self.financial_pattern.finditer(ner, overlapped=True):
            ind = len(ner[:match.start() + 3].split())
            end = len(ner[:match.end()].split())
            if msg_list[ind] in self.__entity_sets.prepositions:
                for i in range(ind, end):
                    ner_list[i] = 'I-FIN'
        return ' '.join(ner_list)
    
    def __apply_rules_wd(self, sentence: str, ner: str) -> str:
        """
        If the entity pattern 'B-WD B-...' can be found in a labeled sentence
        it changes the B-WD label to the neighbouring label.
  
        Exemple:
        Sentence: Segunda via do boleto
        Before: B-WD B-DOC 0 B-FIN
        After: B-FIN I-FIN I-FIN I-FIN
  
        :param sentence: string of a message
        :type sentence: ``str``
        :param ner: string of the label of words in a sentence
        :type ner: ``str``
        :return: string with the new labels
        :rtype: ``str``
        """
        
        msg_list = sentence.split()
        ner_list = ner.split()
        for match in self.wd_pattern.finditer(sentence):
            start = len(sentence[:match.start()].split())
            if start < len(msg_list) - 3 and msg_list[start + 1] in ['via'] and \
                    msg_list[start + 2] in self.__entity_sets.prepositions and ner_list[start + 3] != 'O':
                entity = ner_list[start + 3][2:]
                if entity == 'FIN':
                    ner_list[start] = 'B-' + entity
                    for k in range(1, 4):
                        ner_list[start + k] = 'I-' + entity
                else:
                    ner_list[start] = 'B-DOC'
                    ner_list[start + 1] = 'I-DOC'
        return ' '.join(ner_list)
