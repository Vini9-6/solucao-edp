from .edp_solver_base import EDPSolver
import numpy as np
import sympy as sp
from scipy.integrate import quad
from numpy.linalg import solve


class RayleighRitz(EDPSolver):
    # ✅ 1. Inicialização
    def __init__(self, dominio, n_pontos, condicoes_contorno, funcoes_base=None):
        self.dominio = dominio
        self.n_pontos = n_pontos
        self.condicoes_contorno = condicoes_contorno
        self.x = np.linspace(dominio[0], dominio[1], n_pontos)
        self.h = (dominio[1] - dominio[0]) / (n_pontos - 1)
        self.n_base = max(3, n_pontos - 2)

        # Gera funções base senoidais se não forem fornecidas
        if funcoes_base is None:
            self.funcoes_base = self._gerar_funcoes_base_trigonometricas()
        else:
            self.funcoes_base = funcoes_base

    def _gerar_funcoes_base_trigonometricas(self):
        x = sp.Symbol('x')
        a, b = self.dominio
        funcoes = []
        for i in range(1, self.n_base + 1):
            phi = sp.sin(i * sp.pi * (x - a) / (b - a))
            funcoes.append(phi)
        return funcoes

    def resolver(self, edp_params):
        x = sp.Symbol('x')
        a, b = self.dominio

        # ✅ 2. Montagem da matriz de rigidez K
        K = np.zeros((self.n_base, self.n_base))
        F = np.zeros(self.n_base)

        for i in range(self.n_base):
            for j in range(self.n_base):
                phi_i = self.funcoes_base[i]
                phi_j = self.funcoes_base[j]

                dphi_i = sp.diff(phi_i, x)
                dphi_j = sp.diff(phi_j, x)

                integrand_k = (edp_params['p'] * dphi_i * dphi_j +
                               edp_params['q'] * dphi_i * phi_j +
                               edp_params['r'] * phi_i * phi_j)

                func_k = sp.lambdify(x, integrand_k, 'numpy')
                try:
                    K[i, j], _ = quad(func_k, a, b)
                except:
                    K[i, j] = 0

            # ✅ 3. Montagem do vetor de força F
            integrand_f = self.funcoes_base[i] * edp_params['f']
            func_f = sp.lambdify(x, integrand_f, 'numpy')
            try:
                F[i], _ = quad(func_f, a, b)
            except:
                F[i] = 0

        # ✅ 4. Resolução do sistema K * c = F
        try:
            coef = solve(K, F)
        except:
            coef = np.zeros(self.n_base)

        # ✅ 5. Construção da solução u_h(x)
        x_vals = self.x
        resultado = np.zeros_like(x_vals)
        for i, c in enumerate(coef):
            phi_func = sp.lambdify(x, self.funcoes_base[i], 'numpy')
            try:
                resultado += c * phi_func(x_vals)
            except:
                pass

        # ✅ 6. Ajuste das condições de contorno (Dirichlet)
        if self.condicoes_contorno['tipo'] == 'dirichlet':
            u_a, u_b = self.condicoes_contorno['valores']
            resultado += u_a + (u_b - u_a) * (x_vals - a) / (b - a)

        return resultado, coef
