# src/methods/__init__.py

from .rayleigh_ritz import RayleighRitz
from .galerkin import Galerkin
from .colocacao import MetodoColocacao
from .momentos import MetodoMomentos
from .subdominios import MetodoSubdominios
from .minimos_quadrados import MetodoMinimosQuadrados

__all__ = [
    "RayleighRitz",
    "Galerkin",
    "MetodoColocacao",
    "MetodoMomentos",
    "MetodoSubdominios",
    "MetodoMinimosQuadrados"
]