import logging
from dataclasses import dataclass
from tkinter import Text, INSERT, END
if __name__.startswith("MetadataManagerLib") or __name__.startswith("MangaManager.MetadataManagerLib"):
    from . import ComicInfo
else:
    import ComicInfo

logger = logging.getLogger(__name__)


@dataclass()
class LoadedComicInfo:
    path: str
    comicInfoObj: ComicInfo.ComicInfo
    originalComicObj: ComicInfo.ComicInfo = None

    # Used for merge
    chapter = None
    parsed_chapter = None
    parsed_part = None
    parsed_order = None

    def __init__(self, path, comicInfo, original=None):
        self.path = path
        self.comicInfoObj = comicInfo
        if original:
            self.originalComicObj = original


class LongText:
    linked_text_field: Text = None
    name: str
    _value: str = ""

    def __init__(self, name=None):
        if name:
            self.name = name

    def set(self, value: str):
        if not self.linked_text_field:  # If its not defined then UI is not being use. Store value in class variable.
            self._value = value
            return  # self._value
        self.linked_text_field.delete(1.0, END)
        self.linked_text_field.insert(INSERT, value)

    def clear(self):
        if not self.linked_text_field:
            self._value = ""
            return
        self.linked_text_field.delete(1.0, END)

    def get(self):
        if not self.linked_text_field:  # If its not defined then UI is not being use. Store value in class variable.
            return self._value

        return self.linked_text_field.get(index1="1.0", index2='end-1c')

    def __str__(self):
        return self.name
