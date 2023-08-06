from dbt.adapters.base import Column
from dataclasses import dataclass
from dbt.adapters.base.relation import BaseRelation
from dbt.exceptions import RuntimeException

from dbt.adapters.base import Column
from dataclasses import dataclass
from dbt.adapters.postgres.relation import PostgresRelation
from dbt.contracts.graph.parsed import ParsedSourceDefinition, ParsedNode
from dbt.utils import filter_null_values, deep_merge, classproperty

from typing import (
    Optional, TypeVar, Any, Type, Dict, Union, Iterator, Tuple, Set
)
from dbt.contracts.relation import (
    RelationType, ComponentName, HasQuoting, FakeAPIObject, Policy, Path
)

Self = TypeVar('Self', bound='BaseRelation')

@dataclass(frozen=True, eq=False, repr=False)
class CratedbAdapterRelation(BaseRelation):
    def relation_max_name_length(self):
        return 63

class CratedbAdapterColumn(Column):
    pass  # redshift does not inherit from postgres here

"""
@dataclass(frozen=True, eq=False, repr=False)
class CratedbAdapterRelation(BaseRelation):
    def __post_init__(self):
        # Check for length of Postgres table/view names.
        # Check self.type to exclude test relation identifiers
        if (self.identifier is not None and self.type is not None and
                len(self.identifier) > self.relation_max_name_length()):
            raise RuntimeException(
                f"Relation name '{self.identifier}' "
                f"is longer than {self.relation_max_name_length()} characters"
            )

    def relation_max_name_length(self):
        return 63


class CratedbAdapterColumn(Column):
    @property
    def data_type(self):
        # on postgres, do not convert 'text' to 'varchar()'
        if self.dtype.lower() == 'text':
            return self.dtype
        return super().data_type
"""