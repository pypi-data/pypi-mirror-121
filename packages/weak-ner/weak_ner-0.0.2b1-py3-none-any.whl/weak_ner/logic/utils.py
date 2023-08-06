import typing as tp

from unidecode import unidecode


def create_entity_set(vocab_dict: tp.Dict[str, tp.List[str]], *name: str) -> tp.Set[str]:
    """
    Return a set of all words in lists that starts with the ``name``.

    :param vocab_dict: dictionary with a list of words with similar meaning
    :type vocab_dict: ``tp.Dict[str, tp.List[str]]``
    :param name: a string of the list to look for
    :type name: ``str``
    :return: a set of words
    :rtype: ``tp.Set[str]``
    """
    data_values_lst = []
    for key in vocab_dict.keys():
        if key.startswith(name):
            data_values_lst += normalize(vocab_dict[key])
    return set(data_values_lst)


def normalize(sentence: tp.List[str]) -> tp.List[str]:
    """
    Remove non ASCII characters and set the words to lower case.

    :param sentence: a list with words
    :type sentence: ``tp.List[str]``
    :return: a list with words with only ASCII character and lower case
    :rtype: ``tp.List[str]``
    """
    return [unidecode(word.lower()) for word in sentence]
