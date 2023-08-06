__all__ = ['ENTITY_PATTERNS',
           'ENTITIES',
           'WORD_LOCATION',
           'WORD_LOCATION',
           'WORDS_NAMES',
           'WORDS_REPLACE_LOCATION_O',
           'WORDS_REPLACE_LOCATION_GEN',
           'LOCAL_ENTITY_PATTERN',
           'PERSON_ENTITY_PATTERN',
           'FINANCIAL_ENTITY_PATTERN',
           'WD_ENTITY_PATTERN',
           'WeakNERModel',
           'WeakNERRules',
           'PipelineWeakModels',
           'replace_for_porto',
           'replace_for_luz',
           'replace_for_saude',
           ]

from .list_pattern_model.list_weak_model import WeakNERModel
from .rule_based_model.rule_weak_model import WeakNERRules
from .pipeline_builder.pipeline_weak_labeling import PipelineWeakModels
from .rule_based_model.name_location_rules import replace_for_saude, replace_for_luz, replace_for_porto

from .param import ENTITY_PATTERNS, ENTITIES, WORD_LOCATION, WORDS_NAMES,\
    WORDS_REPLACE_LOCATION_O, WORDS_REPLACE_LOCATION_GEN, \
    LOCAL_ENTITY_PATTERN, PERSON_ENTITY_PATTERN, FINANCIAL_ENTITY_PATTERN, WD_ENTITY_PATTERN
