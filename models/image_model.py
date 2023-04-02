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
class Datum:
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Datum':
        assert isinstance(obj, dict)
        url = from_union([from_str, from_none], obj.get("url"))
        return Datum(url)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.url is not None:
            result["url"] = from_union([from_str, from_none], self.url)
        return result


@dataclass
class Image:
    created: Optional[int] = None
    data: Optional[List[Datum]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Image':
        assert isinstance(obj, dict)
        created = from_union([from_int, from_none], obj.get("created"))
        data = from_union([lambda x: from_list(Datum.from_dict, x), from_none], obj.get("data"))
        return Image(created, data)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.created is not None:
            result["created"] = from_union([from_int, from_none], self.created)
        if self.data is not None:
            result["data"] = from_union([lambda x: from_list(lambda x: to_class(Datum, x), x), from_none], self.data)
        return result


def image_from_dict(s: Any) -> Image:
    return Image.from_dict(s)


def image_to_dict(x: Image) -> Any:
    return to_class(Image, x)
