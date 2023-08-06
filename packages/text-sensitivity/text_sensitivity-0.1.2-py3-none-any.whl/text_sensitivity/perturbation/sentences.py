from typing import Optional

from text_sensitivity.perturbation.base import OneToOnePerturbation


def to_upper() -> OneToOnePerturbation:
    return OneToOnePerturbation.from_function(str.upper, 'not_upper', 'upper')


def to_lower() -> OneToOnePerturbation:
    return OneToOnePerturbation.from_function(str.lower, 'not_lower', 'lower')


def repeat_n_times(n: int = 10, connector: Optional[str] = ' '):
    """Repeat a string n times."""
    if connector is None:
        connector = ''

    def repeat_n(string: str) -> str:
        return connector.join([string] * n)

    return OneToOnePerturbation.from_function(repeat_n, label_to='repeated')
