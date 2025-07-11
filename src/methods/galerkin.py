from .edp_solver_base import EDPSolver
import numpy as np
import sympy as sp
from scipy.integrate import quad
from numpy.linalg import solve


class Galerkin(EDPSolver):
    def __init__(self, dominio, n_pontos, condicoes_contorno):
        super().__init__(dominio, n_pontos, condicoes_contorno)
        self.dominio = dominio
        self.n_pontos = n_pontos
        self.condicoes_contorno = condicoes_contorno
        self.x = np.linspace(dominio[0], dominio[1], n_pontos)

    def resolver(self, edp_params):
        x = sp.Symbol('x')
        if not isinstance(edp_params['f'], sp.Basic):
            raise TypeError(f"O parâmetro 'f' deve ser expressão simbólica do SymPy, recebido: {type(edp_params['f'])}")

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
                phi_i = phi_base[i]
                phi_j = phi_base[j]

                dphi_i = sp.diff(phi_i, x)
                dphi_j = sp.diff(phi_j, x)

                integrand = (-edp_params['p'] * dphi_j * dphi_i +
                             edp_params['q'] * phi_j * dphi_i +
                             edp_params['r'] * phi_j * phi_i)

                func = sp.lambdify(x, integrand, 'numpy')
                try:
                    A[i, j], _ = quad(func, a, b)
                except:
                    A[i, j] = 0

            integrand_rhs = edp_params['f'] * phi_i
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
        x_vals = self.x
        resultado = np.zeros_like(x_vals)
        for i, c in enumerate(coef):
            phi_func = sp.lambdify(x, phi_base[i], 'numpy')
            try:
                resultado += c * phi_func(x_vals)
            except:
                pass

        #if self.condicoes_contorno['tipo'] == 'dirichlet':
        #    u_a, u_b = self.condicoes_contorno['valores']
        #    resultado += u_a + (u_b - u_a) * (x_vals - a) / (b - a)
        return resultado, coef
