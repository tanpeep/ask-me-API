from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, cast, Callable


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


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


@dataclass
class Message:
    role: Optional[str] = None
    content: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Message':
        assert isinstance(obj, dict)
        role = from_union([from_str, from_none], obj.get("role"))
        content = from_union([from_str, from_none], obj.get("content"))
        return Message(role, content)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.role is not None:
            result["role"] = from_union([from_str, from_none], self.role)
        if self.content is not None:
            result["content"] = from_union([from_str, from_none], self.content)
        return result


@dataclass
class Choice:
    message: Optional[Message] = None
    finish_reason: Optional[str] = None
    index: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Choice':
        assert isinstance(obj, dict)
        message = from_union([Message.from_dict, from_none], obj.get("message"))
        finish_reason = from_union([from_str, from_none], obj.get("finish_reason"))
        index = from_union([from_int, from_none], obj.get("index"))
        return Choice(message, finish_reason, index)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.message is not None:
            result["message"] = from_union([lambda x: to_class(Message, x), from_none], self.message)
        if self.finish_reason is not None:
            result["finish_reason"] = from_union([from_str, from_none], self.finish_reason)
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
class Chat:
    id: Optional[str] = None
    object: Optional[str] = None
    created: Optional[int] = None
    model: Optional[str] = None
    usage: Optional[Usage] = None
    choices: Optional[List[Choice]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Chat':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        object = from_union([from_str, from_none], obj.get("object"))
        created = from_union([from_int, from_none], obj.get("created"))
        model = from_union([from_str, from_none], obj.get("model"))
        usage = from_union([Usage.from_dict, from_none], obj.get("usage"))
        choices = from_union([lambda x: from_list(Choice.from_dict, x), from_none], obj.get("choices"))
        return Chat(id, object, created, model, usage, choices)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.object is not None:
            result["object"] = from_union([from_str, from_none], self.object)
        if self.created is not None:
            result["created"] = from_union([from_int, from_none], self.created)
        if self.model is not None:
            result["model"] = from_union([from_str, from_none], self.model)
        if self.usage is not None:
            result["usage"] = from_union([lambda x: to_class(Usage, x), from_none], self.usage)
        if self.choices is not None:
            result["choices"] = from_union([lambda x: from_list(lambda x: to_class(Choice, x), x), from_none], self.choices)
        return result


def chat_from_dict(s: Any) -> Chat:
    return Chat.from_dict(s)


def chat_to_dict(x: Chat) -> Any:
    return to_class(Chat, x)
