from .edp_solver_base import EDPSolver
import numpy as np
import sympy as sp
from scipy.integrate import quad
from numpy.linalg import solve


class MetodoMinimosQuadrados(EDPSolver):
    def resolver(self, edp_params):
        x = sp.Symbol('x')
        a, b = self.dominio

        n_base = max(3, self.n_pontos - 2)
        phi_base = []
        for i in range(1, n_base + 1):
            phi = sp.sin(i * sp.pi * (x - a) / (b - a))
            phi_base.append(phi)

        A = np.zeros((n_base, n_base))
        b_vec = np.zeros(n_base)

        for i in range(n_base):
            for j in range(n_base):
                phi_j = phi_base[j]
                Lu_j = (edp_params['p'] * sp.diff(phi_j, x, 2) +
                        edp_params['q'] * sp.diff(phi_j, x) +
                        edp_params['r'] * phi_j)

                integrand = Lu_j * (edp_params['p'] * sp.diff(phi_base[i], x, 2) +
                                    edp_params['q'] * sp.diff(phi_base[i], x) +
                                    edp_params['r'] * phi_base[i])

                func = sp.lambdify(x, integrand, 'numpy')
                try:
                    A[i, j], _ = quad(func, a, b)
                except:
                    A[i, j] = 0

            integrand_rhs = edp_params['f'] * (edp_params['p'] * sp.diff(phi_base[i], x, 2) +
                                               edp_params['q'] * sp.diff(phi_base[i], x) +
                                               edp_params['r'] * phi_base[i])
            func_rhs = sp.lambdify(x, integrand_rhs, 'numpy')
            try:
                b_vec[i], _ = quad(func_rhs, a, b)
            except:
                b_vec[i] = 0

        try:
            coef = solve(A, b_vec)
        except:
            coef = np.zeros(n_base)

        # Calcula a solução aproximada nos pontos do domínio
        x_vals = np.linspace(a, b, self.n_pontos)
        resultado = np.zeros_like(x_vals)
        for i, c in enumerate(coef):
            phi_func = sp.lambdify(x, phi_base[i], 'numpy')
            try:
                resultado += c * phi_func(x_vals)
            except:
                pass

        if self.condicoes_contorno['tipo'] == 'dirichlet':
            u_a, u_b = self.condicoes_contorno['valores']
            resultado += u_a + (u_b - u_a) * (x_vals - a) / (b - a)

        return resultado, coef
