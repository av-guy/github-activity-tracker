from kink import di
from .providers.github import Provider, GitHub

di[Provider[GitHub]] = Provider(GitHub())


def initialize():
    pass
