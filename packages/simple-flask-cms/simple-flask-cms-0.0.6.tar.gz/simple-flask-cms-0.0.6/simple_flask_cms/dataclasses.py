import pydantic
import datetime
from typing import NamedTuple
import typing


class FragmentType(NamedTuple):
    name: str
    description: typing.Optional[str]
    url: typing.Optional[str]


class StrippedPage(pydantic.BaseModel):
    path: str
    title: str
    nav_title: str
    sort_order: int
    date_modified: datetime.datetime
    subpages: list = []


class Page(StrippedPage):
    content: str
    html: str = ""


class Image(pydantic.BaseModel):
    file: str
    page: str
    mime_type: str
    size: int


class StrippedFragment(pydantic.BaseModel):
    name: str
    date_modified: datetime.datetime
    fragment_type: typing.Optional[FragmentType] = None


class Fragment(StrippedFragment):
    content: str
    html: str = ""
