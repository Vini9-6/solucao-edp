import numpy as np
import sympy as sp
from sympy import interpolate
from methods.rayleigh_ritz import RayleighRitz
from methods.galerkin import Galerkin
from methods.colocacao import MetodoColocacao
from methods.momentos import MetodoMomentos
from methods.subdominios import MetodoSubdominios
from methods.minimos_quadrados import MetodoMinimosQuadrados

# Solver para a equação do Calor 1D usando Euler implícito

def solve_calor_1d(f_expr, u0_expr, a, b, ua, ub, n_pontos, dt, n_passos, metodo='Rayleigh-Ritz'):
    x = sp.Symbol('x')
    p = 1
    q = 0
    r = 0
    f = sp.sympify(f_expr)
    f_func = sp.lambdify(x, f, 'numpy')
    u0 = sp.lambdify(x, sp.sympify(u0_expr), 'numpy')
    x_vals = np.linspace(a, b, n_pontos)
    u = u0(x_vals)
    condicoes_contorno = {'tipo': 'dirichlet', 'valores': (ua, ub)}
    methods = {
        'Rayleigh-Ritz': RayleighRitz,
        'Galerkin': Galerkin,
        'Colocação': MetodoColocacao,
        'Momentos': MetodoMomentos,
        'Subdomínios': MetodoSubdominios,
        'Mínimos Quadrados': MetodoMinimosQuadrados
    }
    solver_cls = methods[metodo]
    resultados = [u.copy()]
    for t in range(n_passos):
        # Seleciona no máximo 6 pontos para interpolação simbólica
        n_interp = min(6, len(x_vals))
        idxs = np.linspace(0, len(x_vals)-1, n_interp, dtype=int)
        pontos = list(zip(x_vals[idxs], u[idxs]))
        u_interp = sp.interpolate(pontos, x)
        # Monta EDO para o próximo passo de tempo: (u^{n+1} - u^n)/dt = u_xx + f
        # => -u_xx + (1/dt)u^{n+1} = (1/dt)u^n + f
        edp_params = {
            'p': 1,
            'q': 0,
            'r': 1/dt,
            'f': (u_interp/dt) + f
        }
        solver = solver_cls((a, b), n_pontos, condicoes_contorno)
        u_new, _ = solver.resolver(edp_params)
        u = u_new
        resultados.append(u.copy())
    return x_vals, np.array(resultados)
