from .edp_solver_base import EDPSolver
import numpy as np
import sympy as sp
from scipy.integrate import quad
from numpy.linalg import solve


class MetodoSubdominios(EDPSolver):
    def resolver(self, edp_params):
        x = sp.Symbol('x')
        if not isinstance(edp_params['f'], sp.Basic):
            raise TypeError(f"O parâmetro 'f' deve ser expressão simbólica do SymPy, recebido: {type(edp_params['f'])}")

        a, b = self.dominio

        n_sub = max(3, self.n_pontos - 2)
        subdominios = np.linspace(a, b, n_sub + 1)
        phi_base = []

        for i in range(1, n_sub + 1):
            phi = sp.Piecewise(
                (1, (x >= subdominios[i-1]) & (x <= subdominios[i])),
                (0, True)
            )
            phi_base.append(phi)

        A = np.zeros((n_sub, n_sub))
        b_vec = np.zeros(n_sub)

        for i in range(n_sub):
            for j in range(n_sub):
                phi_j = phi_base[j]
                Lu_j = (edp_params['p'] * sp.diff(phi_j, x, 2) +
                        edp_params['q'] * sp.diff(phi_j, x) +
                        edp_params['r'] * phi_j)

                integrand = phi_base[i] * Lu_j
                func = sp.lambdify(x, integrand, 'numpy')
                try:
                    A[i, j], _ = quad(func, a, b)
                except:
                    A[i, j] = 0

            integrand_rhs = phi_base[i] * edp_params['f']
            func_rhs = sp.lambdify(x, integrand_rhs, 'numpy')
            try:
                b_vec[i], _ = quad(func_rhs, a, b)
            except:
                b_vec[i] = 0

        try:
            coef = solve(A, b_vec)
        except:
            coef = np.zeros(n_sub)

        # Calcula a solução aproximada nos pontos do domínio
        x_vals = np.linspace(a, b, self.n_pontos)
        resultado = np.zeros_like(x_vals)
        for i, c in enumerate(coef):
            phi_func = sp.lambdify(x, phi_base[i], 'numpy')
            try:
                resultado += c * phi_func(x_vals)
            except:
                pass

        return resultado, coef
