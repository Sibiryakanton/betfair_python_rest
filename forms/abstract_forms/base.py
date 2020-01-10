from dataclasses import dataclass
from abc import abstractmethod


@dataclass
class BaseForm:

    @abstractmethod
    def data(self):
        raise AttributeError('the data attribute is required')

