from enum import Enum


class SORT_ORDER(Enum):
    FRAMEWORK = 100
    LIBRARY = 200
    APPLICATION = 300


class StaticFile:
    def __init__(self, name, path, url=None, sort_order=None, link=True,
                 enabled_by_default=True):

        self.name = name
        self.path = path
        self.url = url
        self.sort_order = sort_order or SORT_ORDER.APPLICATION
        self.link = link
        self.enabled_by_default = enabled_by_default
        self.enabled = True

        # this value is only for the object representation
        # and is meant for debugging
        self.static_url_prefix = ''

    def __repr__(self):
        return '<{}({}, sort_order={}, enabled={}, {}{} -> {})>'.format(  # NOQA: FS002
            self.__class__.__name__,
            self.name,
            repr(self.sort_order),
            repr(self.enabled),
            self.static_url_prefix,
            self.url,
            self.path,
        )


class StyleSheet(StaticFile):
    pass


class Script(StaticFile):
    pass
