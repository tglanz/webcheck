from dataclasses import dataclass
from typing import Callable, Iterable
from pymitter import EventEmitter

known_enhancements = []

@dataclass
class Context:
    bus: EventEmitter

def enhancement(wrapped: Callable[[any], any], *_):
    known_enhancements.append(wrapped)
    return wrapped

def get_known_enhancements() -> Iterable[Callable[[Context], None]]:
    return known_enhancements