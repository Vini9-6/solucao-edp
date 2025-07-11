import numpy as np
import sympy as sp
from methods.rayleigh_ritz import RayleighRitz
from methods.galerkin import Galerkin
from methods.colocacao import MetodoColocacao
from methods.momentos import MetodoMomentos
from methods.subdominios import MetodoSubdominios
from methods.minimos_quadrados import MetodoMinimosQuadrados

def solve_onda_1d(f_expr, u0_expr, v0_expr, a, b, ua, ub, n_pontos, dt, n_passos, metodo='Rayleigh-Ritz', lamb=1.0):
    x = sp.Symbol('x')
    p = 1
    q = 0
    r = 0
    f = sp.sympify(f_expr)
    u0 = sp.lambdify(x, sp.sympify(u0_expr), 'numpy')
    v0 = sp.lambdify(x, sp.sympify(v0_expr), 'numpy')
    x_vals = np.linspace(a, b, n_pontos)
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
    # Inicialização
    u_nm1 = u0(x_vals)  # u^{n-1}
    u_n = u_nm1 + dt * v0(x_vals)  # u^n (1º passo via Taylor)
    # Solução estacionária (reta entre as condições de contorno)
    sol_estacionaria = ua + (ub - ua) * (x_vals - a) / (b - a)
    resultados = [u_nm1.copy() + sol_estacionaria, u_n.copy() + sol_estacionaria]
    for t in range(1, n_passos):
        # (u^{n+1} - 2u^n + u^{n-1})/dt^2 = lambda^2 u_xx + f
        # => -lambda^2 u_xx + (1/dt^2)u^{n+1} = (2u^n - u^{n-1})/dt^2 + f
        # O termo fonte deve ser simbólico:
        if not isinstance(f, sp.Basic):
            raise TypeError(f"O parâmetro 'f' deve ser expressão simbólica do SymPy, recebido: {type(f)}")
        edp_params = {
            'p': -lamb**2,
            'q': 0,
            'r': 1/dt**2,
            'f': f
        }
        solver = solver_cls((a, b), n_pontos, condicoes_contorno)
        try:
            u_np1, _ = solver.resolver(edp_params)
        except TypeError as err:
            raise TypeError(f"Erro ao resolver EDP: {err}\nVerifique se a função fonte 'f' é simbólica.")
        # Soma a solução estacionária ao resultado dinâmico
        u_np1 = u_np1 + sol_estacionaria
        u_nm1, u_n = u_n, u_np1
        resultados.append(u_np1.copy())
    return x_vals, np.array(resultados)
