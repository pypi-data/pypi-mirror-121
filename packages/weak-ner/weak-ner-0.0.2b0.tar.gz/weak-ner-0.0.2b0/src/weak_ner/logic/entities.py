import typing as tp

from unidecode import unidecode

from weak_ner.data.read_lines import create_entity_dict_from_lists


def normalize(sentence: tp.List[str]) -> tp.List[str]:
    """
    Remove non ASCII characters and set the words to lower case.

    :param sentence: a list with words
    :type sentence: ``tp.List[str]``
    :return: a list with words with only ASCII character and lower case
    :rtype: ``tp.List[str]``
    """
    return [unidecode(word.lower()) for word in sentence]


class Entities:
    def __init__(self, directory_path: str):
        """
        Initializes the class by reading the word list files, storing the words by class and which files constitute
        each class.

        Possible pre processing options are EMAIL, URL, NUMBER and CODE.

        :param directory_path: Directory containing files to be read.
        :type directory_path: ´str´
        """
        self.__vocab_dict = create_entity_dict_from_lists(directory_path)
        self.__set_entities()
        self.__set_pos()
    
    def __set_entities(self) -> None:
        """
        Creates a set for each entity with the words from the lists of each entity.

        Example: creates a set with the 'names' words.
        """
        self.months = self.create_entity_set('substantivos_meses')
        
        self.names = self.create_entity_set('substantivos_nomes')
        self.surnames = self.create_entity_set('substantivos_sobrenome')
        self.companies = self.create_entity_set('substantivos_empresas',
                                                'substantivos_empresas_internacionais')
        self.documents = self.create_entity_set('substantivos_documentos')
        self.vocatives = self.create_entity_set('substantivos_vocativos')
        self.locations = self.create_entity_set('substantivos_paises',
                                                'substantivos_cidades',
                                                'substantivos_continentes',
                                                'substantivos_estados')
        self.financial = self.create_entity_set('substantivos_financeiros')
        self.week_days = self.create_entity_set('substantivos_dias_da_semana')
        self.animals = self.create_entity_set('substantivos_animais')
        self.relatives = self.create_entity_set('substantivos_parentescos')
        self.cars = self.create_entity_set('substantivos_carros')
    
    def __set_pos(self) -> None:
        """
        Creates a set with words from lists of the Parts of speech: pronouns,
         article and prepositions.

        Example: create a set with the 'pronouns' words.
        """
        self.pronouns = self.create_entity_set('pronomes')
        self.articles = self.create_entity_set('artigos')
        self.prepositions = self.create_entity_set('preposicoes')
        self.interjection = self.create_entity_set('interjeicoes')
    
    def create_entity_set(self, *name: str) -> tp.Set[str]:
        """
        Return a set of all words in lists that starts with the ``name``.

        :param name: a string of the list to look for
        :type name: ``str``
        :return: a set of words
        :rtype: ``tp.Set[str]``
        """
        data_values_lst = []
        for key in self.__vocab_dict.keys():
            if key.startswith(name):
                data_values_lst += normalize(self.__vocab_dict[key])
        return set(data_values_lst)
