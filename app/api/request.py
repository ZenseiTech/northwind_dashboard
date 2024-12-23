"""Contains the request objects."""
import json
from dataclasses import dataclass


@dataclass
class Sort:
    """Sort."""

    field: str
    direction: str

    def __repr__(self):
        """Print representation."""
        return f"""field: {self.field}
                    direction: {self.direction}"""


@dataclass
class Search:
    """Search."""

    field: str
    type: str
    operator: str
    value: list[int]

    def __repr__(self):
        """Print representation."""
        return f"""
                    field: {self.field}
                    type: {self.type}
                    operator: {self.operator}
                    value: {self.value}
                """


@dataclass
class GetRequest:
    """Request."""

    cmd: str
    limit: int
    offset: int
    searchLogic: int
    sort: list[Sort]
    search: list[Search]

    def __repr__(self):
        """Print representation."""
        return f"""
                cmd: {self.cmd}
                limit: {self.limit}
                offset: {self.offset}
                searchLogic: {self.searchLogic}
                sort: {self.sort}
                search: {self.search}
        """


def create_grid_data(data):
    """Create the grid data."""
    sort = []
    search = []
    searchLogic = "OR"

    if "searchLogic" in data:
        searchLogic = data["searchLogic"]

    if "sort" in data and data["sort"]:
        for value in data["sort"]:
            s = Sort(field=value["field"], direction=value["direction"])
            sort.append(s)

    if "search" in data and data["search"]:
        for value in data["search"]:
            s = Search(
                field=value["field"],
                type=value["type"],
                operator=value["operator"],
                value=value["value"],
            )
            search.append(s)

    # if "selected" in data and data['selected']:
    #     print(f"selected: {data['selected']}")

    return GetRequest(
        cmd=data["cmd"],
        limit=data["limit"],
        offset=data["offset"],
        searchLogic=searchLogic,
        sort=sort,
        search=search,
    )


def build_request(body):
    """Return the built request object."""
    print(body)
    data = json.loads(body)

    if data["cmd"] == "get":
        return create_grid_data(data)
    else:
        return {"Request": "Unknown cmd request"}
