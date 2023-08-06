"""In programming, a factory is a function that returns an Object.

Functions are easy to understand because they have clear inputs and outputs.
Most gdsfactory functions take some inputs and return a Component object.
Some of these inputs are other functions.

- Component: Object with.
    - name
    - references to other components (x, y, rotation)
    - polygons in different layers
    - ports dictionary
- ComponentFactory: function that returns a Component.
- Route: Dictionary with 3 keys.
    - references: list of references (straights, bends and tapers)
    - ports: dict(input=PortIn, output=PortOut)
    - length: float (how long is this route)
- RouteFactory: function that returns a Route.

"""
import dataclasses
import pathlib
from typing import Callable, Dict, List, Optional, Tuple, Union

from phidl.device_layout import Path

from gdsfactory.component import Component, ComponentReference
from gdsfactory.cross_section import CrossSection
from gdsfactory.port import Port


@dataclasses.dataclass
class Route:
    references: List[ComponentReference]
    ports: Tuple[Port, Port]
    length: float


@dataclasses.dataclass
class Routes:
    references: List[ComponentReference]
    lengths: List[float]
    ports: Optional[List[Port]] = None
    bend_radius: Optional[float] = None


Float2 = Tuple[float, float]
Float3 = Tuple[float, float, float]
Floats = Tuple[float, ...]

Layer = Tuple[int, int]
Layers = Tuple[Layer, ...]
RouteFactory = Callable[..., Route]
ComponentFactory = Callable[..., Component]
ComponentFactoryDict = Dict[str, ComponentFactory]
PathFactory = Callable[..., Path]
PathType = Union[str, pathlib.Path]

ComponentOrFactory = Union[ComponentFactory, Component]
ComponentOrPath = Union[PathType, Component]
ComponentOrReference = Union[Component, ComponentReference]
NameToFunctionDict = Dict[str, ComponentFactory]
Number = Union[float, int]
Coordinate = Tuple[float, float]
Coordinates = Tuple[Tuple[float, float], ...]
ComponentOrPath = Union[Component, PathType]
CrossSectionFactory = Callable[..., CrossSection]
CrossSectionOrFactory = Union[CrossSection, Callable[..., CrossSection]]


def get_name_to_function_dict(*functions) -> Dict[str, Callable]:
    """Returns a dict with function name as key and function as value."""
    return {func.__name__: func for func in functions}


def parse_port_name(name: str) -> str:
    if "_" in name:
        return name
    try:
        name = int(name)
    except ValueError:
        pass
    return name


__all__ = [
    "ComponentFactory",
    "ComponentOrFactory",
    "ComponentOrPath",
    "ComponentOrReference",
    "Coordinate",
    "Coordinates",
    "Layer",
    "NameToFunctionDict",
    "Number",
    "PathType",
    "Route",
    "Routes",
    "RouteFactory",
    "get_name_to_function_dict",
]
