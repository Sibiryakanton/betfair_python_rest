from dataclasses import dataclass
from .base import BaseForm


@dataclass
class AbstractLocaleField(BaseForm):
    locale: str
