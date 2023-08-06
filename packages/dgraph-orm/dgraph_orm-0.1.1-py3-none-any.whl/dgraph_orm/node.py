from __future__ import annotations
import typing as T
import json
import time
from pydantic import BaseModel, PrivateAttr
from fastapi.encoders import jsonable_encoder
from .gql import GQLException


class Cache(BaseModel):
    val: T.Union[Node, T.List[Node], None]
    resolver: Resolver
    timestamp: float
    raw_gql: str


class CacheManager(BaseModel):
    cache: T.Dict[str, Cache] = {}

    def remove(self, key: str) -> None:
        if key in self.cache:
            del self.cache[key]

    def add(self, *, key: str, resolver: Resolver, val: T.Any, gql_d: dict) -> None:
        self.cache[key] = Cache(
            val=val,
            resolver=resolver,
            timestamp=time.time(),
            raw_gql=json.dumps(jsonable_encoder(gql_d)),
        )

    def replace(self, key: str, cache: Cache) -> None:
        self.cache[key] = cache

    def get(self, key: str) -> T.Optional[Cache]:
        if key not in self.cache:
            return None
        return self.cache[key]

    def exists(self, key: str) -> bool:
        return key in self.cache

    def get_val(self, key: str) -> T.Optional[T.Union[Node, T.List[Node]]]:
        if c := self.cache[key]:
            return c.val

    def clear(self) -> None:
        self.cache = {}

    def is_empty(self) -> bool:
        return len(self.cache) == 0


Model = T.TypeVar("Model")


class Node(BaseModel, T.Generic[Model]):
    _cache: CacheManager = PrivateAttr(default_factory=CacheManager)
    _typename: T.ClassVar[str]

    id: str

    # TODO make equality and hashing

    @property
    def cache(self) -> CacheManager:
        return self._cache

    @staticmethod
    def nodes_by_typename() -> T.Dict[str, T.Type[Node]]:
        d = {}
        subs = Node.__subclasses__()
        for sub in subs:
            typename = sub._typename
            if typename in d:
                raise GQLException(
                    f"Two Nodes share the typename {typename}: ({sub.__name__}, {d[typename].__name__})"
                )
            d[typename] = sub
        return d

    def __repr__(self) -> str:
        r = super().__repr__()
        r = f"{r}, cache: {repr(self.cache)}" if not self.cache.is_empty() else r
        return r

    def get_root_resolver(self) -> T.Type[Resolver]:
        return Resolver.resolvers_by_typename()[self._typename]

    @staticmethod
    def should_use_new_resolver(
        old_r: Resolver, new_r: Resolver, strict: bool = False
    ) -> bool:
        old_r_j = old_r.json()
        new_r_j = new_r.json()
        if old_r_j == new_r_j:
            return False
        if strict:
            return True
        if old_r.json(exclude={"children_resolvers"}) != new_r.json(
            exclude={"children_resolvers"}
        ):
            print(
                f'excluding children resolvers here..., {old_r.json(exclude={"children_resolvers"})=}, {new_r.json(exclude={"children_resolvers"})=}'
            )
            return True
        # now do the same for children
        for child_resolver_name in new_r.children_resolvers.__fields__.keys():
            new_child_resolver = getattr(new_r.children_resolvers, child_resolver_name)
            if new_child_resolver:
                old_child_resolver = getattr(
                    old_r.children_resolvers, child_resolver_name
                )
                if not old_child_resolver:
                    return True
                if Node.should_use_new_resolver(
                    old_r=old_child_resolver,
                    new_r=new_child_resolver,
                    strict=strict,
                ):
                    return True
        return False

    def resolve(
        self,
        name: str,
        resolver: Resolver,
        refresh: bool = False,
        strict: bool = False,
        use_stale: bool = False,
    ) -> T.Optional[T.Union[Model, T.List[Model]]]:
        if refresh:
            self.cache.remove(name)
        # see if the resolvers do not match
        if cache := self.cache.get(name):
            if use_stale:
                return cache.val
            if self.should_use_new_resolver(
                old_r=cache.resolver, new_r=resolver, strict=strict
            ):
                print(
                    f"resolvers are different, removing {name} from cache, old: {cache.resolver=}, new: {resolver=}"
                )
                self.cache.remove(name)
        if not self.cache.exists(name):
            obj = getattr(self.get_root_resolver()(), name)(resolver).get(id=self.id)
            self.cache.replace(key=name, cache=obj.cache.get(name))
        return self.cache.get_val(name)


from .resolver import Resolver

Cache.update_forward_refs()
