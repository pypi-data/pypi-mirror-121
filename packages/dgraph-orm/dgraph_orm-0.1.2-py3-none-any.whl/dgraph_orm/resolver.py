from __future__ import annotations
import typing as T
import json
from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder
from .execute import execute
from .gql import GQLException
from .dgraph_model import DGraphModel
from .node import Node


def parse_filter(filter: DGraphModel) -> str:
    print(f"{filter=}")
    return filter.to_gql_str()


def parse_nested_q(field_name: str, nested_q: BaseModel):
    if isinstance(nested_q, DGraphModel):
        filter_s = parse_filter(nested_q)
        return f"{field_name}: {{ {filter_s} }}"
    outer_lst: T.List[str] = []
    for key, val in nested_q:
        if val is None:
            continue
        # for order, not filter
        if not isinstance(val, BaseModel):
            outer_lst.append(f"{key}: {val}")
            continue
        val: BaseModel
        inner_lst: T.List[str] = []
        for inner_key, inner_val in val.dict(exclude_none=True).items():
            inner_str = f"{inner_key}: {json.dumps(jsonable_encoder(inner_val))}"
            inner_lst.append(inner_str)
        outer_lst.append(f'{key}: {{ {",".join(inner_lst)} }}')
    return f'{field_name}: {{ {",".join(outer_lst)} }}'


Model = T.TypeVar("Model", bound=Node)
FilterType = T.TypeVar("FilterType", bound=DGraphModel)
OrderType = T.TypeVar("OrderType", bound=DGraphModel)


class Resolver(BaseModel, T.Generic[Model, FilterType, OrderType]):
    class Input(BaseModel):
        def to_str(self) -> str:
            field_names = self.dict(exclude_none=True).keys()
            inner_params: T.List[str] = []
            for field_name in field_names:
                val = getattr(self, field_name)
                if isinstance(val, BaseModel):
                    inner_params.append(
                        parse_nested_q(field_name=field_name, nested_q=val)
                    )
                else:
                    inner_params.append(
                        f"{field_name}: {json.dumps(jsonable_encoder(val))}"
                    )
            if inner_params:
                return f'({",".join(inner_params)})'
            return ""

    class Children(BaseModel):
        pass

    class QueryInput(Input):
        filter: FilterType = None
        first: int = None
        offset: int = None
        order: OrderType = None

    model: T.ClassVar[T.Type[Model]]
    children_resolvers: Children = Field(default_factory=Children)
    query_input: QueryInput = Field(default_factory=QueryInput)

    def gql_fields_str(self) -> str:
        """This does not include the top level..."""
        fields = [*self.model.__fields__.keys(), "__typename"]
        for resolver_name in self.Children.__fields__.keys():
            resolver: Resolver = getattr(self.children_resolvers, resolver_name, None)
            if resolver:
                child_gql_str = resolver.params_and_fields()
                fields.append(f"{resolver_name} {child_gql_str}")
        return f'{{ {",".join(fields)} }}'

    def params_and_fields(self) -> str:
        return f"{self.query_input.to_str()}{self.gql_fields_str()}"

    def _get(self, kwargs_d: dict) -> T.Optional[Model]:
        kwargs = {k: v for k, v in kwargs_d.items() if v is not None}
        if not kwargs:
            raise GQLException(
                f".get requires one field to be given of {list(kwargs_d.keys())}"
            )
        inner_params = ",".join(
            [
                f"{field_name}: {json.dumps(jsonable_encoder(val))}"
                for field_name, val in kwargs.items()
            ]
        )
        query_name = f"get{self.model.__name__}"
        s = f"{{ {query_name}({inner_params}){self.gql_fields_str()} }}"
        print(s)
        obj = execute(query_str=s)["data"][query_name]
        if obj:
            return self.parse_obj_nested(obj)
        return None

    def query(self) -> T.List[Model]:
        query_name = f"query{self.model.__name__}"
        s = f"{{ {query_name}{self.params_and_fields()} }}"
        print(s)
        lst: T.List[dict] = execute(query_str=s)["data"][query_name]
        return [self.parse_obj_nested(d) for d in lst]

    def parse_obj_nested(self, gql_d: dict) -> T.Optional[Model]:
        """Each obj will be its own. If you want to change this, consider changing the parse"""
        if not gql_d:
            return None
        typename = gql_d.get("__typename", None)
        if not typename:
            raise GQLException(f"No typename in {gql_d=}")
        nodes_by_typename = Node.nodes_by_typename()  # TODO precompute?
        o: Node = nodes_by_typename[typename].parse_obj(gql_d)
        other_fields = set(gql_d.keys()) - set(o.__fields__.keys()) - {"__typename"}
        for field in other_fields:
            resolver = getattr(self.children_resolvers, field, None)
            if not resolver:
                raise GQLException(f"No resolver {field} found!")
            nested_d = gql_d[field]
            val = (
                [resolver.parse_obj_nested(d) for d in nested_d]
                if type(nested_d) == list
                else resolver.parse_obj_nested(nested_d)
            )
            o.cache.add(key=field, resolver=resolver, val=val, gql_d=gql_d)
        return o

    @staticmethod
    def resolvers_by_typename() -> T.Dict[str, T.Type[Resolver]]:
        d = {}
        subs = Resolver.__subclasses__()
        for sub in subs:
            typename = sub.model._typename
            if typename in d:
                raise GQLException(
                    f"Two Resolvers share the typename {typename}: ({sub.__name__}, {d[typename].__name__})"
                )
            d[typename] = sub
        return d

    def first(self, _: int) -> Resolver:
        self.query_input.first = _
        return self

    def offset(self, _: int) -> Resolver:
        self.query_input.offset = _
        return self

    def filter(self, _: FilterType) -> Resolver:
        self.query_input.filter = _
        return self

    def order(self, _: OrderType) -> Resolver:
        self.query_input.order = _
        return self

    def get(self, id: str = None) -> Model:
        kwargs_d = {"id": id}
        return self._get(kwargs_d=kwargs_d)
