import json
import sys

from classes import typeclass
from octadocs.types import QueryResult, SelectResult
from rdflib import Graph


@typeclass
def print_json(query_result: QueryResult) -> None:
    """Print query result as JSON."""


@print_json.instance(SelectResult)
def _print_select_as_json(select_result: SelectResult):
    sys.stdout.write(json.dumps(select_result, indent=2, default=str))


@print_json.instance(Graph)
def _print_construct_as_json(graph: Graph):
    fieldnames = ('subject', 'predicate', 'object')
    sys.stdout.write(json.dumps(
        [
            dict(zip(fieldnames, triple))
            for triple in graph
        ],
        indent=2,
        default=str,
    ))
