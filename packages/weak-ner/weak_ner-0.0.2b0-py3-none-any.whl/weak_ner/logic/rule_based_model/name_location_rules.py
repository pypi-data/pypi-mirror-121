import typing as tp


def replace_for_saude(sentence: tp.List[str], ner: tp.List[str], index: int) -> tp.List[str]:
    """
    Replace the label of the word 'saude' based in the context. If before has the word 'jardim'
    the label is changed to 'LOC'. If before has the word 'plano' the label is changed to 'GEN'. Else
    is changed to 'O'.

    Example:
    Sentence: 'Em jardim da saude'
    Previous label: 'O B-LOC O B-LOC'
    New label: 'O B-LOC I-LOC I-LOC'

    Sentence: 'Meu plano de saude'
    Previous label: 'O B-GEN O B-LOC'
    New label: 'O B-GEN I-GEN I-GEN'

    :param sentence: list with words of a sentence
    :type sentence: ``tp.List[str]``
    :param ner: list with all the labels of a sentence
    :type ner: ``tp.List[str]``
    :param index: a number indicate which label to change
    :type ner: ``int``
    :return: a list with all the new labels of a sentence
    :rtype: ``tp.List[str]``
    """
    ner[index] = 'O'
    if index > 1:
        if sentence[index - 2] == 'jardim':
            ner[index - 1] = 'I-LOC'
            ner[index] = 'I-LOC'
        elif sentence[index - 2] == 'plano':
            ner[index - 1] = 'I-GEN'
            ner[index] = 'I-GEN'
    return ner


def replace_for_luz(sentence: tp.List[str], ner: tp.List[str], index: int) -> tp.List[str]:
    """
    Replace the label of the word 'luz' based in the context. If
    before has the word 'conta' or 'fatura' the label is changed
    to 'FIN'. Else is changed to 'GEN'.

    Example:
    Sentence: 'Minha conta de luz'
    Previous label: 'O B-FIN O B-LOC'
    New label: 'O B-FIN I-FIN I-FIN'

    Sentence: 'A minha luz esta paga'
    Previous label: 'O O B-LOC O O'
    New label: 'O O B-GEN O O'

    :param sentence: list with words of a sentence
    :type sentence: ``tp.List[str]``
    :param ner: list with all the labels of a sentence
    :type ner: ``tp.List[str]``
    :param index: a number indicate which label to change
    :type ner: ``int``
    :return: a list with all the new labels of a sentence
    :rtype: ``tp.List[str]``
    """
    ner[index] = 'B-GEN'
    if index > 1:
        if sentence[index - 2] in ['conta', 'fatura']:
            ner[index - 1] = 'I-FIN'
            ner[index] = 'I-FIN'
    return ner


def replace_for_porto(sentence: tp.List[str], ner: tp.List[str], index: int) -> tp.List[str]:
    """
    Replace the label of the word 'porto' based in the context. If the word that precedes it is
    'cartao' or 'cartao da' the label is changed to 'FIN'.
    If instead the word before it is 'da' the label is changed to 'COMP'.

    Example:
    Sentence: 'Meu cartão Porto'
    Previous label: 'O B-FIN B-LOC'
    New label: 'O B-FIN I-FIN'

    Sentence: 'Queria falar com a porto'
    Previous label: 'O O O O B-LOC'
    New label: 'O O O O B-COMP'


    :param sentence: list with words of a sentence
    :type sentence: ``tp.List[str]``
    :param ner: list with all the labels of a sentence
    :type ner: ``tp.List[str]``
    :param index: a number indicate which label to change
    :type ner: ``int``
    :return: a list with all the new labels of a sentence
    :rtype: ``tp.List[str]``
    """
    if index > 0:
        if sentence[index - 1] == 'cartao':
            ner[index] = 'I-FIN'
        elif sentence[index - 1] in ['da', 'a']:
            ner[index] = 'B-COMP'
        elif index > 1 and ' '.join(
                sentence[index - 2:index]) == 'cartao da':
            ner[index - 1] = 'I-FIN'
            ner[index] = 'I-FIN'
    return ner
