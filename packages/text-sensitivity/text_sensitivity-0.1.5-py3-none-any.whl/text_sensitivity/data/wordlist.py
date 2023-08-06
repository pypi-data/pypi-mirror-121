from typing import List, Dict, Optional, Union
import numpy as np
import pandas as pd

from text_explainability.default import Readable

from text_sensitivity.internationalization import get_locale


Label = Union[str, int]


class WordList(Readable):
    def __init__(self, wordlist: pd.DataFrame, main_column: Optional[Label] = None):
        self.wordlist = wordlist
        self.__wordlist = wordlist.copy(deep=True)
        self.main_column = main_column

    @classmethod
    def from_list(cls, wordlist: List[str], name: Label = 'words'):
        return cls(pd.DataFrame(wordlist, columns=[name]))

    @classmethod
    def from_dictionary(cls,
                        wordlist: Dict,
                        key_name: Label = 'key',
                        value_name: Label = 'value',
                        value_as_main: bool = False):
        main_column = value_name if value_as_main else key_name
        return cls(pd.DataFrame(wordlist, columns=[key_name, value_name]), main_column=main_column)

    @classmethod
    def from_dict(cls, *args, **kwargs):
        """Alias for `WordList.from_dictionary()`."""
        return cls.from_dictionary(*args, **kwargs)

    @classmethod
    def from_csv(cls, filename: str, main_column: Optional[Label] = None, *args, **kwargs):
        return cls(pd.read_csv(filename, *args, **kwargs), main_column=main_column)

    @classmethod
    def from_json(cls, filename: str, main_column: Optional[Label] = None, *args, **kwargs):
        return cls(pd.read_json(filename, *args, **kwargs), main_column=main_column)

    @classmethod
    def from_excel(cls, filename: str, main_column: Optional[Label] = None, *args, **kwargs):
        return cls(pd.read_excel(filename, *args, **kwargs), main_column=main_column)

    @classmethod
    def from_pickle(cls, filename: str, main_column: Optional[Label] = None, *args, **kwargs):
        return cls(pd.read_pickle(filename, *args, **kwargs), main_column=main_column)

    @classmethod
    def from_file(cls, filename: str, main_column: Optional[Label] = None, *args, **kwargs):
        import os
        extension = str.lower(os.path.splitext(filename)[1])

        if extension == 'csv':
            return cls.from_csv(filename=filename, main_column=main_column, *args, **kwargs)
        elif extension == 'json':
            return cls.from_json(filename=filename, main_column=main_column, *args, **kwargs)
        elif extension in ['xls', 'xlsx']:
            return cls.from_excel(filename=filename, main_column=main_column, *args, **kwargs)
        elif extension == 'pkl':
            return cls.from_pickle(filename=filename, main_column=main_column, *args, **kwargs)
        else:
            return cls(pd.read_table(filename, main_column=main_column, *args, **kwargs),
                       main_column=main_column)

    def get(self,
            sort_by: Optional[Label] = None,
            **sort_kwargs):
        wordlist = self.wordlist.sort_values(by=sort_by, **sort_kwargs) if sort_by is not None else self.wordlist
        col = wordlist.iloc[:, 0] if self.main_column is None or self.main_column not in self.wordlist.columns \
              else wordlist.loc[:, self.main_column]
        return list(col)

    def random(self,
               n: int,
               likelihood_column: Optional[Label] = None,
               seed: Optional[int] = None):
        if n >= len(self.wordlist.index):
            return self.get()
        if likelihood_column is not None:
            likelihood_column = self.wordlist[likelihood_column].values / self.wordlist[likelihood_column].sum()
        np.random.seed(seed)
        return list(np.random.choice(self.get(), size=n, replace=False, p=likelihood_column))

    def filter(self,
               column: Label,
               values: Union[Label, List[Label]]):
        if not isinstance(values, list):
            values = [values]
        self.wordlist = self.wordlist[self.wordlist[column].isin(values)]
        return self

    def reset(self):
        self.wordlist = self.__wordlist.copy(deep=True)
        return self

    def __len__(self):
        return len(self.get())


class WordListGetterMixin:
    def get(self, *args, **kwargs):
        return self.wordlist.get(*args, **kwargs)

    def random(self, *args, **kwargs):
        return self.wordlist.random(*args, **kwargs)

    def filter(self, *args, **kwargs):
        return self.wordlist.filter(*args, **kwargs)

    def reset(self):
        return self.wordlist.reset()

    def __len__(self):
        return len(self.wordlist)


class Countries(WordListGetterMixin):
    def __init__(self,
                 language: Union[str, List[str]] = get_locale()):
        """List of countries, in language name.

        Args:
            language (Union[str, List[str]], optional): ISO 3166-1 language code(s). Defaults to get_locale().

        Raises:
            ValueError: Unknown language code.
        """
        from country_list import countries_for_language, available_languages

        if isinstance(language, list):  # list of languages
            language = [str.lower(lang) for lang in language]
            for lang in language:
                if lang not in available_languages():
                    raise ValueError(f'Unknown language "{lang}"')
            self.wordlist = WordList(pd.DataFrame([dict(countries_for_language(lang)) for lang in language],
                                     index=language).T.reset_index(),
                                     main_column=language[0])
        else:  # single language
            if language not in available_languages():
                raise ValueError(f'Unknown language "{language}"')
            self.wordlist = WordList.from_dictionary(countries_for_language(str.lower(language)),
                                                     key_name='language_code',
                                                     value_name='country_name',
                                                     value_as_main=True)


class Cities(WordListGetterMixin):
    def __init__(self,
                 country: Optional[Union[str, List[str]]] = None,
                 ascii_safe: bool = False):
        import os
        filename = 'lists/top_100_cities.csv'
        filepath = os.path.join(os.path.dirname(__file__), filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError('Run text_sensitivity/data/lists/regenerate.py to regenerate files.')
        main_column = 'ascii_name' if ascii_safe else 'name'
        self.wordlist = WordList.from_csv(filepath, main_column=main_column, sep=';')

        if country is not None:
            self.filter('country_code', country)

    def random(self, n: int, seed: Optional[int] = None):
        return self.wordlist.random(n, likelihood_column='population', seed=seed)
