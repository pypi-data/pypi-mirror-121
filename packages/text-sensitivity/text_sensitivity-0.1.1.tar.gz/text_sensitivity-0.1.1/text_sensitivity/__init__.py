from text_sensitivity.test import compare_accuracy, compare_precision, compare_recall
from text_sensitivity.perturbation import Perturbation, OneToOnePerturbation, OneToManyPerturbation
from text_sensitivity.data.random import (RandomData, RandomAscii, RandomDigits, RandomEmojis,
                                          RandomLower, RandomPunctuation, RandomSpaces, RandomUpper,
                                          RandomWhitespace, combine_generators)

__version__ = '0.1.1'
