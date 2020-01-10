from dataclasses import dataclass


@dataclass
class BaseForm:

    @property
    def data(self):
        data = locals()
        return data

