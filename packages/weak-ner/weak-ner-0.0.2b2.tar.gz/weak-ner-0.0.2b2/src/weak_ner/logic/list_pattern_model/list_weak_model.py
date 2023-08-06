import typing as tp
import re

from unidecode import unidecode

from take_text_preprocess.presentation import pre_process

from weak_ner.logic.param import ENTITY_PATTERNS, ENTITIES
from weak_ner.logic.entities import Entities


class WeakNERModel:
    """
        Class responsible for assigning entity labels to words based on lists of each entity class.

        Methods:
        --------
            * label_entities: Get the label entities of a sentence, the begin of entity is labeled as B-`label`,
                            the rest of a entity is labeled as I-`label`, and `O` with the word isn't a entity.


    """
    
    def __init__(self, entity_sets: Entities, use_preprocess: bool = True, pre_processing_options: tp.List[str] = []):
        """
        Initializes the class by reading the word list files, storing the words by class and which files constitute
        each class.
        
        Possible pre processing options are EMAIL, URL, NUMBER and CODE.
        
        :param entity_sets: Entities class with the entities set read from the lists.
        :type entity_sets: ´Entities´
        :param use_preprocess: Flags whether text pre processing should be used. Defaults to true.
        :type use_preprocess: `bool`
        :param pre_processing_options: Optional pre processing options to be applied. Defaults to basic pre processing.
        :type pre_processing_options: `tp.List[str]`
        """
        self.__use_preprocessing = use_preprocess
        self.__pre_processing_options = pre_processing_options
        
        self.__entity_sets = entity_sets
        
        self.__patterns = ENTITY_PATTERNS
        self.__entities = ENTITIES
        
        self.__list_based_entities = {'DOC': self.__entity_sets.documents,
                                      'COMP': self.__entity_sets.companies,
                                      'WD': self.__entity_sets.week_days,
                                      'REL': self.__entity_sets.relatives,
                                      'VOC': self.__entity_sets.vocatives}
        
        self.__create_allowed_dict()
        self.__entity_function = {'GEN': self.__find_entity_from_patterns,
                                  'PERS': self.__find_entity_from_patterns,
                                  'LOC': self.__find_entity_from_patterns,
                                  'FIN': self.__find_entity_from_patterns,
                                  'DATE': self.__find_entity_from_patterns,
                                  'ADDR': self.__find_entity_from_patterns,
                                  'DOC': self.__get_ner_from_list,
                                  'COMP': self.__get_ner_from_list,
                                  'WD': self.__get_ner_from_list,
                                  'REL': self.__get_ner_from_list,
                                  'VOC': self.__get_ner_from_list,
                                  'PHONE': self.__get_common_entities,
                                  'MONEY': self.__get_common_entities,
                                  'NUMBER': self.__get_common_entities,
                                  'EMAIL': self.__get_common_entities}
    
    def label_entities(self, tags: str, sentence: str) -> tp.Tuple[str, str]:
        """
        Get the label entities of a sentence, the begin of entity is labeled as B-`label`,
        the rest of a entity is labeled as I-`label`, and `O` with the word isn't a entity.
        
        The function return a string with a label for each word of the sentence.

        :param tags: POS string of a message.
        :type tags: ``str``
        :param sentence: Sentence being processed.
        :type sentence: ``str``
        :return: A tuple with the preprocessed sentence and the labels for the words on the sentence.
        :rtype: `tp.Tuple[str, str]`
        """
        if self.__use_preprocessing:
            split_sentence = pre_process(sentence, self.__pre_processing_options).split()
        else:
            split_sentence = sentence.split()
        
        entity_list = ['O' for i in range(len(split_sentence))]
        all_entities = self.__get_all_entities(tags=tags, sentence=' '.join(split_sentence))
        if len(all_entities) > 0:
            sorted_entities = sorted(all_entities, key=lambda current_entity: current_entity['start'])
            if len(sorted_entities) > 1:
                sorted_entities = self.__remove_redundant_entities(sorted_entities)
            
            for entity in sorted_entities:
                entity_list[entity['start']] = 'B-' + entity['label']
                
                if entity['start'] != entity['end']:
                    for j in range(entity['start'] + 1, entity['end'] + 1):
                        entity_list[j] = 'I-' + entity['label']
        
        return ' '.join(split_sentence), ' '.join(str(label) for label in entity_list)
    
    def __create_allowed_dict(self) -> None:
        """
        Create a dictionary for each entity with the lists of allowed words in the category.
        
        Example: For entity Person a list with all names and surnames allowed as this entity.
        """
        names_set = self.__entity_sets.prepositions.union(self.__entity_sets.names, self.__entity_sets.surnames, {'e'})
        location_set = self.__entity_sets.locations
        financial_set = self.__entity_sets.prepositions.union(self.__entity_sets.financial)
        dates_set = self.__entity_sets.months.union(self.__entity_sets.prepositions, self.__entity_sets.week_days,
                                                    {'date', 'number'})
        not_permitted_generic = self.__entity_sets.financial.union(self.__entity_sets.names,
                                                                   self.__entity_sets.surnames,
                                                                   self.__entity_sets.documents,
                                                                   self.__entity_sets.months,
                                                                   self.__entity_sets.companies,
                                                                   self.__entity_sets.locations,
                                                                   self.__entity_sets.articles,
                                                                   self.__entity_sets.pronouns,
                                                                   self.__entity_sets.week_days,
                                                                   self.__entity_sets.relatives)
        not_permitted_generic = not_permitted_generic.union({'favor', 'vez', 'dia', 'mês', 'mes'})
        self.allowed_dict = {'PERS': names_set,
                             'LOC': location_set,
                             'FIN': financial_set,
                             'GEN': not_permitted_generic,
                             'DATE': dates_set}
    
    @staticmethod
    def __get_common_entities(sentence: str, target_entity: str, tags=None, allowed_entity_words=None) -> tp.List[str]:
        """
        Get entities based in placeholders.
        
        :param sentence: Sentence being processed.
        :type sentence: ``str``
        :param target_entity: Target label being searched.
        :type target_entity: ``str``
        :return: Words on the sentence that match the target label.
        :rtype: ``tp.List[str]``
        """
        return [word for word in sentence.split() if word == target_entity.lower()]
    
    @staticmethod
    def __get_ner_from_list(tags: str, sentence: str, target_entity: str,
                            allowed_entity_words: tp.List[str]) -> tp.List[str]:
        """
        Get entities based of lists.

        :param sentence: Sentence being processed.
        :type sentence: ``str``
        :param allowed_entity_words: Words that are allowed on the target entity.
        :type allowed_entity_words: ``tp.List[str]``
        :param target_entity: Entity being searched for.
        :type target_entity: ``str``
        :param tags: POS Tags for the sentence being processed.
        :type tags: ``str``
        :return: List of words from the sentence that are allowed on the target entity.
        :rtype: ``tp.List[str]``
        """
        if target_entity == 'COMP':
            return [word for word, tag in zip(sentence.split(), tags.split())
                    if tag == 'SUBS' and word in allowed_entity_words]
        else:
            return [word for word in sentence.split() if word in allowed_entity_words]
    
    def __correct_function(self, identified_entity: str, target_label: str) -> str:
        """
        Correct current entities found with regex patterns.
        The correction is based on whether the entities are in the allowed lists or not.
        The entity types considered are generic, localization, person, date.
        For address entities the method checks if the sentence starts with 'rua' or 'avenida' or 'bairro'.
        
        If after removing the not allowed word the found pattern starts with preposition,
        the first preposition is removed.
        If it ends with a preposition, the last preposition is removed.

        Returns a string with the found pattern with only allowed words, if nothing is allowed it returns empty.
        
        :param identified_entity: a string with the pattern match
        :type identified_entity: ``str``
        :param target_label:  Target label being searched.
        :type target_label: ``str``
        :return: Words in the sentence matching the entity pattern after correction.
        :rtype: ``str``
        """
        allowed_set = self.allowed_dict.get(target_label, None)
        if target_label == 'GEN':
            first_correction = ' '.join([word for word in identified_entity.split() if word not in allowed_set])
        
        elif target_label == 'LOC':
            first_correction = identified_entity if identified_entity in allowed_set else ''
        
        elif target_label == 'ADDR':
            lower_entities = identified_entity.lower()
            if lower_entities.startswith('rua') or \
                    lower_entities.startswith('av') or \
                    lower_entities.startswith('avenida') or \
                    lower_entities.startswith('bairro'):
                first_correction = identified_entity
            else:
                first_correction = ''
        
        else:
            first_correction = ' '.join([word for word in identified_entity.split() if word in allowed_set])
            if first_correction == 'number':
                first_correction = ''
        
        split_correction = first_correction.split()
        if len(split_correction) > 0 and split_correction[0] in self.__entity_sets.prepositions:
            split_correction = split_correction[1:]
        if len(split_correction) > 0 and split_correction[-1] in self.__entity_sets.prepositions:
            split_correction = split_correction[:-1]
        
        return ' '.join([word for word in split_correction])
    
    def __find_pattern(self, entity_pattern: str, tags: str, sentence: str, target_entity: str) -> tp.List[str]:
        """
        Find words with certain POS tags based in a POS pattern,
        returns a list with all matched pattern after a correction, basically
        check if the word is or isn't of that entity (label).

        :param entity_pattern: POS Tag pattern to for the target label.
        :type entity_pattern: ``str``
        :param tags: POS tags of the words on the sentence message
        :type tags: ``str``
        :param sentence: Sentence being processed.
        :type sentence: ``str``
        :param target_entity: Target label being searched.
        :type target_entity: ``str``
        :return: Words in the sentence matching the entity pattern after correction.
        :rtype: ``tp.List[str]``
        """
        found_pattern_lst = []
        split_message = sentence.split()
        if target_entity == 'DATE':
            found_pattern_lst += [word for word in split_message if word in self.__entity_sets.months]
        
        for match in re.finditer(entity_pattern, tags):
            message_start = len(tags[:match.start()].split())
            message_end = len(tags[:match.end()].split())
            found_pattern = ' '.join(
                split_message[message_start: message_end])
            corrected_pattern = self.__correct_function(found_pattern, target_entity)
            if corrected_pattern:
                found_pattern_lst.append(corrected_pattern)
        
        return found_pattern_lst
    
    def __find_entity_from_patterns(self, tags: str, sentence: str, target_entity: str,
                                    allowed_entity_words: tp.List[str] = None) -> tp.List[str]:
        """
        Finds all occurrences of an entity's POS Tag patterns in a sentence.
        Return a list with all matched and corrected entities.
    
        :param tags: POS tags of the words on the sentence message
        :type tags: ``str``
        :param sentence: Sentence being processed.
        :type sentence: ``str``
        :param target_entity: Target entity being searched.
        :type target_entity: ``str``
        :return: List of words on the sentence that match the entity.
        :rtype: ``tp.List[str]``
        """
        total_found_patterns = []
        patterns = self.__patterns.get(target_entity, None)
        for pattern in patterns:
            found_patterns = self.__find_pattern(pattern, tags, sentence, target_entity)
            if len(found_patterns) > 0:
                total_found_patterns.append(found_patterns)
        return [pattern for pattern_group in total_found_patterns for pattern in pattern_group]
    
    @staticmethod
    def __find_all_indexes(sentence: str, found_entity: str) -> tp.List[int]:
        """
        Returns the indexes of the words in the `sentence` that match words on the `found_entity`.
    
        :param sentence: Sentence being processed.
        :type sentence: ``str``
        :param found_entity: Words on the sentence that represent an entity.
        :type found_entity: ``str``
        :return: Indexes of the words on the sentence that match an entity.
        :rtype: ``tp.List[int]``
        """
        match_indexes = []
        length = len(sentence.split())
        index = 0
        len_target_entity = len(found_entity.split())
        while index <= length - len_target_entity:
            if sentence.split()[
               index:(index + len_target_entity)] == found_entity.split():
                match_indexes.append(index)
            index += 1
        return match_indexes
    
    def __check_entities_list(self, sentence: str) -> None:
        """
        Verifies if there is a chance the sentence contains entities PERSON, LOCATION, FINANCIAL or DATE.
        If it does, the method adds the entities to the list of labels to be accounted for during the labeling process.

        :param sentence: Sentence being processed.
        :type sentence: ``str``
        """
        if any(word in self.__entity_sets.names or word in self.__entity_sets.surnames for word in sentence.split()):
            self.__entities.append('PERS')
        if any(word in self.__entity_sets.locations for word in sentence.split()):
            self.__entities.append('LOC')
        if any(word in self.__entity_sets.financial for word in sentence.split()):
            self.__entities.append('FIN')
        if any(word in self.__entity_sets.months or word == 'date' for word in sentence.split()):
            self.__entities.append('DATE')
        if any(word in sentence.split() for word in ['rua', 'av', 'avenida', 'bairro']):
            self.__entities.append('ADDR')
    
    def __fill_ner(self, entity_placements: tp.List[tp.Dict[str, tp.Union[int, str]]], target_entity: str,
                   found_entities: tp.List[str], sentence: str) -> tp.List[tp.Dict[str, tp.Union[int, str]]]:
        """
        Populates a list with dictionaries containing the start, end and label
         of all found entities of the target labels.

        :param entity_placements: a list with the the indexes and label of a entity
        :type entity_placements: ``tp.List[tp.Dict[str, tp.Union[int, str]]]``
        :param target_entity: Target entity being searched.
        :type target_entity: ``str``
        :param found_entities: List of words that match the pattern for an entity.
        :type found_entities: ``tp.List[str]``
        :param sentence: Sentence being processed.
        :type sentence: ``str``
        :return: the input ner updated with the founded entities.
        :rtype: ``tp.List[tp.Dict[str, tp.Union[int, str]]]``
        """
        for entity in set(found_entities):
            entity_len = len(entity.split())
            if entity_len > 0:
                indexes = self.__find_all_indexes(sentence, entity)
                for index in indexes:
                    entity_instance = {
                        'start': index,
                        'end': int(index + entity_len - 1),
                        'label': target_entity
                    }
                    entity_placements.append(entity_instance)
        
        return entity_placements
    
    def __get_all_entities(self, tags: str, sentence: str) -> tp.List[tp.Dict[str, tp.Union[int, str]]]:
        """
        Get all entities indexes and label of found entities in a sentence,
        based in all possibles entities. The entities can be found in 3
        different ways, based in Placeholder, regex or a search in a list.
        
        Returns a list of a list, with the start index, end index, and
        label of the entity.

        :param tags: POS tags of the words on the sentence message.
        :type tags: ``str``
        :param sentence: Sentence being processed.
        :type sentence: ``str``
        :return: a list with the the indexes and label of all founded entities
        :rtype: ``tp.List[tp.Dict[str, tp.Union[int, str]]]``
        """
        normalized_sentence = unidecode(sentence.lower())
        entity_placements = []
        self.__check_entities_list(normalized_sentence)
        
        for entity in self.__entities:
            find_entity_matches = self.__entity_function.get(entity, None)
            found_entities = find_entity_matches(tags=tags,
                                                 sentence=normalized_sentence,
                                                 target_entity=entity,
                                                 allowed_entity_words=self.__list_based_entities.get(entity, []))
            
            entity_placements = self.__fill_ner(entity_placements=entity_placements,
                                                target_entity=entity,
                                                found_entities=found_entities,
                                                sentence=normalized_sentence)
        return entity_placements
    
    @staticmethod
    def __remove_redundant_entities(entity_placements: tp.List[tp.Dict[str, tp.Union[int, str]]]) \
            -> tp.List[tp.Dict[str, tp.Union[int, str]]]:
        """
        Removes redundant entities which may be contained by other entity matches.

        :param entity_placements: a list with the indexes and label of found entities
        :type entity_placements: ``tp.List[tp.Dict[str, tp.Union[int, str]]]``
        :return: the input list sorted by the start index
        :rtype: ``tp.List[tp.Dict[str, tp.Union[int, str]]]``
        """
        k = 0
        label_output = [entity_placements[0]]
        for placement in entity_placements:
            if label_output[k]['start'] <= placement['start'] <= label_output[k]['end']:
                if (placement['end'] - placement['start']) > (label_output[k]['end'] - label_output[k]['start']):
                    label_output[k] = placement
            else:
                label_output.append(placement)
                k += 1
        return label_output
