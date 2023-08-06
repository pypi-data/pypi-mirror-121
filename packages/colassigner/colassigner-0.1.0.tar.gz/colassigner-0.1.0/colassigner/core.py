from abc import ABCMeta
from collections.abc import Mapping
from dataclasses import dataclass
from functools import wraps
from typing import Optional, Type, Union

dic_methods = ["get", "keys", "items", "values"]
forbidden_names = [*dic_methods, "mro"]
CALL_RECORDS = []
CURRENT_CALLER: Optional["CurrentCaller"] = None

PP_ATT_NAME = "__parent_prefixes__"
PREFIX_ATT_NAME = "_prefix"
DEFAULT_PREFIX = ""
DEFAULT_PP = ()
PREFIX_SEP = "__"


@dataclass
class CurrentCaller:
    cls: str
    att: str


@dataclass
class CallRecord:
    caller_cls: str
    called_cls: str
    caller_att: str
    called_att: str

    @property
    def edge(self):
        return {
            "to": ".".join([self.caller_cls, self.caller_att]),
            "from": ".".join([self.called_cls, self.called_att]),
        }


class ColMeta(ABCMeta):
    def __init__(cls, name, bases, dict):
        prefix = dict.get(PREFIX_ATT_NAME, DEFAULT_PREFIX)
        parent_prefs = dict.get(PP_ATT_NAME, DEFAULT_PP)
        for k, v in dict.items():
            if isinstance(v, ColMeta):
                new_pp = tuple(p for p in [*parent_prefs, prefix] if p)
                setattr(v, PP_ATT_NAME, new_pp)
        return super().__init__(name, bases, dict)

    def __new__(cls, name, bases, local):
        for attr in local:
            if (attr in forbidden_names) or (
                PREFIX_SEP in attr and not attr.startswith("_")
            ):
                raise ValueError(
                    f"Column name can't be either {forbidden_names}. "
                    f"And can't contain the string {PREFIX_SEP}. "
                    f"{attr} is given"
                )
            value = local[attr]
            if (
                callable(value)
                and not attr.startswith("_")
                and not isinstance(value, type)
            ):
                # TODO: all this drawing needs to be revisited
                local[attr] = decor_w_current(value, name, attr)
        return super().__new__(cls, name, bases, local)

    def __getattribute__(cls, attid):

        if attid.startswith("_") or (attid in forbidden_names):
            return super().__getattribute__(attid)

        colval = super().__getattribute__(attid)
        prefix = super().__getattribute__(PREFIX_ATT_NAME)
        parent_prefixes = super().__getattribute__(PP_ATT_NAME)
        if isinstance(colval, ColMeta):
            return colval

        colname = PREFIX_SEP.join(
            filter(None, [*parent_prefixes, prefix, attid])
        )

        if CURRENT_CALLER is not None:
            CALL_RECORDS.append(
                CallRecord(
                    CURRENT_CALLER.cls, cls.__name__, CURRENT_CALLER.att, attid
                )
            )
        return colname

    def __getcoltype__(cls, attid):
        colval = super().__getattribute__(attid.split(PREFIX_SEP)[-1])
        return colval


class ColAccessor(metaclass=ColMeta):
    """describe raw columns with datatypes

    other than types to describe column type,
    attributes can be used to describe

    - a foreign key, if it is a string
    - nested structure, if it is another ColAccessor class

    class TableCols(ColAccessor):
        col1 = int
        col2 = str
        foreign_key1 = "name_of_key"

        class SubCols(ColAccessor):
            _prefix = "something"  # sets prefix
            ...

    """

    __parent_prefixes__ = DEFAULT_PP  # should never be set manually
    _prefix = DEFAULT_PREFIX


class ColAssigner(Mapping, ColAccessor):
    """define functions that create columns in a dataframe

    later the class attributes can be used to access the column"""

    def __init__(self):
        self._callables = {}
        self._add_callables()

    def __getitem__(self, key):
        return self._callables[key]

    def __iter__(self):
        for k in self._callables.keys():
            yield k

    def __len__(self):
        return len(self._callables)

    def _add_callables(self):
        for mid in self.__dir__():
            if mid.startswith("_") or (mid in dic_methods):
                continue
            m = getattr(self, mid)
            if isinstance(m, ColMeta):
                for k, v in m().items():
                    colname = getattr(m, v.__name__, k)
                    self._callables[colname] = v
                continue

            self._callables[mid] = m


def allcols(cls: Union[Type[ColAccessor], Type[ColAssigner]]):
    out = []
    for attid in dir(cls):
        if attid.startswith("_") or attid in dic_methods:
            continue
        attval = getattr(cls, attid)
        if isinstance(attval, type) and any(
            [kls in attval.mro() for kls in [ColAccessor, ColAssigner]]
        ):
            out += allcols(attval)
            continue
        if ColAccessor in cls.mro():
            out.append(attval)
    return out


def get_col_type(accessor: Type[ColAccessor], attname: str):
    return accessor.__getcoltype__(attname)


def decor_w_current(f, clsname, attr):
    @wraps(f)
    def wrapper(*args, **kwds):
        global CURRENT_CALLER
        CURRENT_CALLER = CurrentCaller(clsname, attr)
        out = f(*args, **kwds)
        CURRENT_CALLER = None
        return out

    return wrapper


def get_cr_graph():
    return [cr.edge for cr in CALL_RECORDS]
