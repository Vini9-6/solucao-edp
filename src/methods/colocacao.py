import numpy as np
import sympy as sp
from scipy.integrate import quad
from numpy.linalg import solve


class MetodoColocacao:
    def __init__(self, dominio, n_pontos, condicoes_contorno):
        self.dominio = dominio
        self.n_pontos = n_pontos
        self.condicoes_contorno = condicoes_contorno
        self.x_col = np.linspace(dominio[0], dominio[1], n_pontos)[1:-1]
        self.n_col = len(self.x_col)
        self.phi_base = self._gerar_funcoes_base()

    def _gerar_funcoes_base(self):
        x = sp.Symbol('x')
        phi_base = []
        for i in range(1, self.n_col + 1):
            phi = sp.sin(
                i * sp.pi * (x - self.dominio[0]) / (self.dominio[1] - self.dominio[0]))
            phi_base.append(phi)
        return phi_base

    def resolver(self, edp_params):
        x = sp.Symbol('x')
        if not isinstance(edp_params['f'], sp.Basic):
            raise TypeError(f"O parâmetro 'f' deve ser expressão simbólica do SymPy, recebido: {type(edp_params['f'])}")

        a, b = self.dominio

        A = np.zeros((self.n_col, self.n_col))
        b_vec = np.zeros(self.n_col)

        for i, x_i in enumerate(self.x_col):
            for j in range(self.n_col):
                phi_j = self.phi_base[j]
                Lu_j = (edp_params['p'] * sp.diff(phi_j, x, 2) +
                        edp_params['q'] * sp.diff(phi_j, x) +
                        edp_params['r'] * phi_j)

                Lu_j_func = sp.lambdify(x, Lu_j, 'numpy')
                try:
                    A[i, j] = Lu_j_func(x_i)
                except:
                    A[i, j] = 0

            f_func = sp.lambdify(x, edp_params['f'], 'numpy')
            try:
                b_vec[i] = f_func(x_i)
            except:
                b_vec[i] = 0

        try:
            coef = solve(A, b_vec)
        except:
            coef = np.zeros(self.n_col)

        # Calcula a solução aproximada nos pontos do domínio
        x_vals = np.linspace(a, b, self.n_pontos)
        resultado = np.zeros_like(x_vals)
        for i, c in enumerate(coef):
            phi_func = sp.lambdify(x, self.phi_base[i], 'numpy')
            try:
                resultado += c * phi_func(x_vals)
            except:
                pass

        return resultado, coef
