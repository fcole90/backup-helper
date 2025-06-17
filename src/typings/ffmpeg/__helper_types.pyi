from typing import TypedDict

type DictKey = str | int | float | bool | None
type CLIValue = str | int | float | bool | None

class EmptyDict(TypedDict):
    pass
