from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Choice:
    text: Optional[str] = None
    index: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Choice':
        assert isinstance(obj, dict)
        text = from_union([from_str, from_none], obj.get("text"))
        index = from_union([from_int, from_none], obj.get("index"))
        return Choice(text, index)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.text is not None:
            result["text"] = from_union([from_str, from_none], self.text)
        if self.index is not None:
            result["index"] = from_union([from_int, from_none], self.index)
        return result


@dataclass
class Usage:
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Usage':
        assert isinstance(obj, dict)
        prompt_tokens = from_union([from_int, from_none], obj.get("prompt_tokens"))
        completion_tokens = from_union([from_int, from_none], obj.get("completion_tokens"))
        total_tokens = from_union([from_int, from_none], obj.get("total_tokens"))
        return Usage(prompt_tokens, completion_tokens, total_tokens)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.prompt_tokens is not None:
            result["prompt_tokens"] = from_union([from_int, from_none], self.prompt_tokens)
        if self.completion_tokens is not None:
            result["completion_tokens"] = from_union([from_int, from_none], self.completion_tokens)
        if self.total_tokens is not None:
            result["total_tokens"] = from_union([from_int, from_none], self.total_tokens)
        return result


@dataclass
class Edit:
    object: Optional[str] = None
    created: Optional[int] = None
    choices: Optional[List[Choice]] = None
    usage: Optional[Usage] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Edit':
        assert isinstance(obj, dict)
        object = from_union([from_str, from_none], obj.get("object"))
        created = from_union([from_int, from_none], obj.get("created"))
        choices = from_union([lambda x: from_list(Choice.from_dict, x), from_none], obj.get("choices"))
        usage = from_union([Usage.from_dict, from_none], obj.get("usage"))
        return Edit(object, created, choices, usage)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.object is not None:
            result["object"] = from_union([from_str, from_none], self.object)
        if self.created is not None:
            result["created"] = from_union([from_int, from_none], self.created)
        if self.choices is not None:
            result["choices"] = from_union([lambda x: from_list(lambda x: to_class(Choice, x), x), from_none], self.choices)
        if self.usage is not None:
            result["usage"] = from_union([lambda x: to_class(Usage, x), from_none], self.usage)
        return result


def edit_from_dict(s: Any) -> Edit:
    return Edit.from_dict(s)


def edit_to_dict(x: Edit) -> Any:
    return to_class(Edit, x)
