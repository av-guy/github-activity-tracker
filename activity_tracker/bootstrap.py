from kink import di

from .providers.github import EventsProvider, GitHub
from .caches.in_memory import CacheProvider, InMemory

di[EventsProvider[GitHub]] = EventsProvider(GitHub())
di[CacheProvider[InMemory]] = CacheProvider(InMemory())


def initialize():
    pass
