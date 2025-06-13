class EDPSolver:
    def __init__(self, dominio, n_pontos, condicoes_contorno):
        self.dominio = dominio
        self.n_pontos = n_pontos
        self.condicoes_contorno = condicoes_contorno

    def resolver(self, edp_params):
        raise NotImplementedError("O método resolver deve ser implementado nas subclasses.")