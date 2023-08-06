import os
import typing as tp

from take_text_preprocess.presentation import pre_process


def read_file(file_name: str, use_preprocess: bool = True, pre_processing_opt: tp.List[str] = []) -> tp.List[str]:
    """
        Reads a list of strings from a file.

    :param file_name: File path.
    :type file_name: `str`
    :param use_preprocess: Flags whether text pre processing should be used. Defaults to true.
    :type use_preprocess: `bool`
    :param pre_processing_opt: Optional pre processing options to be applied. Defaults to basic pre processing.
    :type pre_processing_opt: `tp.List[str]`
    :rtype: `tp.List[str]`
    """
    with open(file_name, 'rb') as f:
        words = [pre_process(line.strip().decode('utf-8'), pre_processing_opt)
                 if use_preprocess else line.strip().decode('utf-8')
                 for line in f.readlines() if len(line) > 0]
    return words


def create_entity_dict_from_lists(directory_path: str) -> tp.Dict[str, tp.List[str]]:
    """
       Reads words from files and stores them in a dictionary by class in a dictionary.
       
    :param directory_path: Directory path
    :type directory_path: `str`
    :return: A dictionary from entity type to word list.
    :rtype: `tp.Dict[str, tp.List[str]]`
    """
    data = {file.split('.')[0]: read_file(directory_path + file)
            for file in os.listdir(directory_path)}
    return data
