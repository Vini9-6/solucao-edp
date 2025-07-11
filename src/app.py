import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp
from datetime import datetime
from methods.rayleigh_ritz import RayleighRitz
from methods.galerkin import Galerkin
from methods.colocacao import MetodoColocacao
from methods.momentos import MetodoMomentos
from methods.subdominios import MetodoSubdominios
from methods.minimos_quadrados import MetodoMinimosQuadrados

# Classe principal da aplicação


class EDPSolverApp:
    def __init__(self, root):
        # Inicializa a janela principal
        self.root = root
        self.root.title("EDP Solver")
        self.root.geometry("1200x800")

        self.resultados = {}  # Armazena os resultados dos métodos
        self.figura = None    # Figura do matplotlib para gráficos
        self.canvas = None    # Canvas do matplotlib na interface

        self.create_interface()  # Monta a interface gráfica

    def create_interface(self):
        # Cria as abas principais da interface
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.frame_config = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_config, text="Configuração")

        self.frame_resultados = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_resultados, text="Resultados")

        self.frame_relatorio = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_relatorio, text="Relatório")

        self.frame_ajuda = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_ajuda, text="Ajuda")

        # Cria os conteúdos de cada aba
        self.create_config_frame()
        self.create_results_frame()
        self.create_report_frame()
        self.create_help_frame()

    def create_config_frame(self):
        # Frame para entrada dos parâmetros da EDP
        fonte = ("Arial", 20)  # Fonte maior para melhor visualização
        config_frame = ttk.LabelFrame(
            self.frame_config, text="Configurações da EDP", padding=10)
        config_frame.pack(fill='x', padx=10, pady=10)

        # Tooltips explicativos para cada campo, incluindo temporais
        tooltips = {
            'p(x)': 'Coeficiente de u"(x) na EDP. Exemplo: 1, x, exp(x)',
            'q(x)': 'Coeficiente de u\'(x) na EDP. Exemplo: 0, x**2',
            'r(x)': 'Coeficiente de u(x) na EDP. Exemplo: 0, 2',
            'f(x)': 'Função do lado direito. Exemplo: sin(pi*x), x**2',
            'Domínio [a, b]': 'Extremos do domínio. Exemplo: 0 e 1',
            'Condições de Contorno': 'Valores de u(a) e u(b). Exemplo: 0 e 0',
            'Número de Pontos': 'Quantidade de pontos de discretização. Exemplo: 20',
            'u(x,0)': 'Condição inicial. Exemplo para Calor: 3*sin(2*pi*x/1). Para Onda: sin(pi*x)',
            'v(x,0)': 'Velocidade inicial (apenas Onda). Exemplo: 0',
            'dt': 'Passo de tempo Δt. Exemplo: 0.01',
            'tmax': 'Tempo máximo T_max. Exemplo: 1.0'
        }

        def add_tooltip(widget, text):
            # Função para adicionar tooltip (dica) a um widget
            def on_enter(event):
                self.tooltip = tk.Toplevel(widget)
                self.tooltip.wm_overrideredirect(True)
                x = widget.winfo_rootx() + 50
                y = widget.winfo_rooty() + 30
                self.tooltip.wm_geometry(f"+{x}+{y}")
                label = tk.Label(self.tooltip, text=text, background="#ffffe0",
                                 relief='solid', borderwidth=1, font=("Arial", 12))
                label.pack()

            def on_leave(event):
                if hasattr(self, 'tooltip'):
                    self.tooltip.destroy()
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

        # Adiciona seleção do tipo de equação no topo do frame de configuração
        label_tipo_equacao = ttk.Label(config_frame, text="Tipo de Equação:", font=fonte)
        label_tipo_equacao.grid(row=0, column=0, sticky='w')
        self.edp_var = ttk.Combobox(config_frame, values=[
            "Poisson",
            "Calor",
            "Onda",
            "Helmholtz"
        ], state="readonly", width=18, font=fonte)
        self.edp_var.current(0)
        self.edp_var.grid(row=0, column=1, padx=5)

        # Criação dos campos de entrada e tooltips
        label_p = ttk.Label(config_frame, text="Coeficiente p(x):", font=fonte)
        label_p.grid(row=1, column=0, sticky='w')
        self.entry_p = ttk.Entry(config_frame, font=fonte)
        self.entry_p.grid(row=1, column=1, padx=5)
        add_tooltip(label_p, tooltips['p(x)'])
        add_tooltip(self.entry_p, tooltips['p(x)'])

        label_q = ttk.Label(config_frame, text="Coeficiente q(x):", font=fonte)
        label_q.grid(row=2, column=0, sticky='w')
        self.entry_q = ttk.Entry(config_frame, font=fonte)
        self.entry_q.grid(row=2, column=1, padx=5)
        add_tooltip(label_q, tooltips['q(x)'])
        add_tooltip(self.entry_q, tooltips['q(x)'])

        label_r = ttk.Label(config_frame, text="Coeficiente r(x):", font=fonte)
        label_r.grid(row=3, column=0, sticky='w')
        self.entry_r = ttk.Entry(config_frame, font=fonte)
        self.entry_r.grid(row=3, column=1, padx=5)
        add_tooltip(label_r, tooltips['r(x)'])
        add_tooltip(self.entry_r, tooltips['r(x)'])

        label_f = ttk.Label(config_frame, text="Termo fonte f(x):", font=fonte)
        label_f.grid(row=4, column=0, sticky='w')
        self.entry_f = ttk.Entry(config_frame, font=fonte)
        self.entry_f.grid(row=4, column=1, padx=5)
        add_tooltip(label_f, tooltips['f(x)'])
        add_tooltip(self.entry_f, tooltips['f(x)'])

        label_dom = ttk.Label(config_frame, text="Domínio espacial [a, b]:", font=fonte)
        label_dom.grid(row=5, column=0, sticky='w')
        self.entry_a = ttk.Entry(config_frame, font=fonte)
        self.entry_a.grid(row=5, column=1, padx=5)
        self.entry_b = ttk.Entry(config_frame, font=fonte)
        self.entry_b.grid(row=5, column=2, padx=5)
        add_tooltip(label_dom, tooltips['Domínio [a, b]'])
        add_tooltip(self.entry_a, tooltips['Domínio [a, b]'])
        add_tooltip(self.entry_b, tooltips['Domínio [a, b]'])

        label_cc = ttk.Label(
            config_frame, text="Cond. de contorno u(a), u(b):", font=fonte)
        label_cc.grid(row=6, column=0, sticky='w')
        self.entry_ua = ttk.Entry(config_frame, font=fonte)
        self.entry_ua.grid(row=6, column=1, padx=5)
        self.entry_ub = ttk.Entry(config_frame, font=fonte)
        self.entry_ub.grid(row=6, column=2, padx=5)
        add_tooltip(label_cc, tooltips['Condições de Contorno'])
        add_tooltip(self.entry_ua, tooltips['Condições de Contorno'])
        add_tooltip(self.entry_ub, tooltips['Condições de Contorno'])

        label_np = ttk.Label(
            config_frame, text="Nº de pontos (N):", font=fonte)
        label_np.grid(row=7, column=0, sticky='w')
        self.entry_n_pontos = ttk.Entry(config_frame, font=fonte)
        self.entry_n_pontos.grid(row=7, column=1, padx=5)
        add_tooltip(label_np, tooltips['Número de Pontos'])
        add_tooltip(self.entry_n_pontos, tooltips['Número de Pontos'])

        # Campos extras para EDPs temporais
        self.label_u0 = ttk.Label(config_frame, text="Condição inicial u(x,0):", font=fonte)
        self.entry_u0 = ttk.Entry(config_frame, font=fonte)
        add_tooltip(self.label_u0, tooltips['u(x,0)'])
        add_tooltip(self.entry_u0, tooltips['u(x,0)'])
        self.label_v0 = ttk.Label(config_frame, text="Velocidade inicial v(x,0):", font=fonte)
        self.entry_v0 = ttk.Entry(config_frame, font=fonte)
        add_tooltip(self.label_v0, tooltips['v(x,0)'])
        add_tooltip(self.entry_v0, tooltips['v(x,0)'])
        # Campos extras para Δt e T_max, se existirem
        if not hasattr(self, 'entry_dt'):
            self.label_dt = ttk.Label(config_frame, text="Passo de tempo Δt:", font=fonte)
            self.entry_dt = ttk.Entry(config_frame, font=fonte)
            self.label_dt.grid(row=12, column=0, sticky='w')
            self.entry_dt.grid(row=12, column=1, padx=5)
            add_tooltip(self.label_dt, tooltips['dt'])
            add_tooltip(self.entry_dt, tooltips['dt'])
        if not hasattr(self, 'entry_tmax'):
            self.label_tmax = ttk.Label(config_frame, text="Tempo máximo T_max:", font=fonte)
            self.entry_tmax = ttk.Entry(config_frame, font=fonte)
            self.label_tmax.grid(row=13, column=0, sticky='w')
            self.entry_tmax.grid(row=13, column=1, padx=5)
            add_tooltip(self.label_tmax, tooltips['tmax'])
            add_tooltip(self.entry_tmax, tooltips['tmax'])
        # Esconde inicialmente
        self.label_u0.grid_remove()
        self.entry_u0.grid_remove()
        self.label_v0.grid_remove()
        self.entry_v0.grid_remove()
        # Bind para atualizar campos ao trocar o tipo de equação
        self.edp_var.bind("<<ComboboxSelected>>", self.on_edp_change)

        # Exibição simbólica da equação
        self.equation_fig = plt.Figure(figsize=(8, 1.2), dpi=100)
        self.equation_ax = self.equation_fig.add_subplot(111)
        self.equation_ax.axis('off')
        self.equation_canvas = FigureCanvasTkAgg(self.equation_fig, master=config_frame)
        self.equation_canvas.get_tk_widget().grid(row=0, column=3, rowspan=3, padx=20, pady=5, sticky='n')
        self.update_equation_display()

        # Botão para resolver a EDP
        ttk.Button(config_frame, text="Resolver", command=self.solve_edp, style="Big.TButton").grid(
            row=8, column=0, columnspan=3, pady=10)

        # Botão de exemplo
        ttk.Button(config_frame, text="PreencherExemplo", command=self.preencher_exemplo, style="Big.TButton").grid(
            row=8, column=3, padx=10, pady=10)

        # Estilo para botão maior
        style = ttk.Style()
        style.configure("Big.TButton", font=fonte)

        # Informações de autoria e local no rodapé
        self.label_autoria = ttk.Label(self.frame_config, text="São Luís, MA\n2025\ndesenvolvido por Vinicius Oliveira e Luys Arthur", font=("Arial", 9), anchor='center', justify='center')
        self.label_autoria.pack(side='bottom', pady=(20, 5))

    def create_results_frame(self):
        # Frame para exibir os resultados numéricos dos métodos
        self.results_text = scrolledtext.ScrolledText(
            self.frame_resultados, height=15)
        self.results_text.pack(fill='both', expand=True, padx=10, pady=10)

    def create_report_frame(self):
        # Frame para exibir o relatório e exportar PDF
        self.report_text = scrolledtext.ScrolledText(
            self.frame_relatorio, height=15)
        self.report_text.pack(fill='both', expand=True, padx=10, pady=10)
        ttk.Button(self.frame_relatorio, text="Exportar PDF",
                   command=self.export_report_pdf, style="Big.TButton").pack(pady=10)

    def create_help_frame(self):
        # Aba de ajuda com instruções e dicas
        help_text = scrolledtext.ScrolledText(
            self.frame_ajuda, height=30, font=("Arial", 14))
        help_text.pack(fill='both', expand=True, padx=10, pady=10)
        help_text.insert(tk.END, """
🎉 Bem-vindo ao EDP Solver! 🎉

Este programa foi desenvolvido para fins educacionais.

""")
        help_text.insert(tk.END, """
O que são EDPs?
Equações Diferenciais Parciais (EDPs) são equações matemáticas que envolvem derivadas parciais de uma função desconhecida de duas ou mais variáveis independentes. Elas modelam fenômenos físicos como calor, difusão, vibração de membranas, eletromagnetismo, entre outros.

Sobre os campos de entrada:
- p(x,y), q(x,y), r(x,y): coeficientes da EDP. Podem ser constantes ou funções de x e y.
- f(x,y): termo fonte ou função do lado direito da EDP.
- Domínio [a, b] x [c, d]: limites do retângulo onde a solução será calculada. Exemplo: 0   1 
- Condições de contorno (u(a,y), u(b,y), u(x,c), u(x,d)): valores da solução nas bordas do domínio. Exemplo: 0   0 
- Número de pontos (x, y): quantidade de pontos de discretização em cada direção. Exemplo: 10  

O que digitar em cada campo?
- Nos campos de coeficientes e f(x,y):
  - Aceite expressões simbólicas do sympy, como: x, y, x**2, y**2, sin(pi*x), exp(x*y), x+y, etc.
  - Operadores permitidos: +, -, *, /, ** (potência)
  - Constantes permitidas: pi, E, exp, sqrt, etc.
  - Não use letras diferentes de x e y (exceto constantes do sympy).
- Nos campos de domínio, condições de contorno e número de pontos:
  - Aceite apenas números reais (ex: 0, 1, -2.5, 3.14) ou inteiros (para número de pontos).

Exemplo completo de preenchimento:
  p(x,y): 1
  q(x,y): 1
  r(x,y): 0
  f(x,y): sin(pi*x)
  Domínio: 0   1 
  Condições de contorno: 0   0
  Número de pontos: 10 

Como usar:
1. Preencha os campos da aba Configuração com os parâmetros da EDP.
2. Clique em 'Resolver EDP'.
3. Veja os resultados, relatórios e mapas de calor nas abas correspondentes.

Dicas:
- O número de pontos afeta a precisão e o tempo de cálculo. Para testes rápidos, use valores menores.
- As condições de contorno são aplicadas nas quatro bordas do domínio retangular.
- O relatório pode ser exportado em PDF, incluindo o gráfico.
- O sistema é voltado para EDPs lineares de segunda ordem em domínios retangulares.

Sobre os resultados:
- Os coeficientes são os pesos das funções base na solução aproximada.
- O erro RMS mostra a diferença entre as soluções dos métodos.


Última atualização: 27/06/2025
""")
        help_text.config(state='disabled')
        help_text.insert(tk.END, """

---
Licença: MIT
Desenvolvido por Vinicius Oliveira e Luys Arthur.
""")

    def validate_inputs(self):
        # Valida todos os campos de entrada da interface
        campos = [
            (self.entry_p, 'p(x)'),
            (self.entry_q, 'q(x)'),
            (self.entry_r, 'r(x)'),
            (self.entry_f, 'f(x)'),
            (self.entry_a, 'Domínio a'),
            (self.entry_b, 'Domínio b'),
            (self.entry_ua, 'u(a)'),
            (self.entry_ub, 'u(b)'),
            (self.entry_n_pontos, 'Número de Pontos')
        ]
        for campo, nome in campos:
            if not campo.get().strip():
                messagebox.showerror(
                    'Erro de entrada', f'O campo "{nome}" deve ser preenchido.')
                return False
        # Validação de tipos e valores numéricos
        try:
            a = float(self.entry_a.get())
            b = float(self.entry_b.get())
            if a >= b:
                messagebox.showerror(
                    'Erro de entrada', 'O valor de "a" deve ser menor que "b" no domínio.')
                return False
        except ValueError:
            messagebox.showerror(
                'Erro de entrada', 'Os valores do domínio devem ser números reais.')
            return False
        try:
            n_pontos = int(self.entry_n_pontos.get())
            if n_pontos < 4:
                messagebox.showerror(
                    'Erro de entrada', 'O número de pontos deve ser pelo menos 4 para garantir precisão.')
                return False
        except ValueError:
            messagebox.showerror(
                'Erro de entrada', 'O número de pontos deve ser um número inteiro.')
            return False
        try:
            float(self.entry_ua.get())
            float(self.entry_ub.get())
        except ValueError:
            messagebox.showerror(
                'Erro de entrada', 'As condições de contorno devem ser números reais.')
            return False
        # Validação de expressões sympy
        try:
            sp.sympify(self.entry_p.get())
            sp.sympify(self.entry_q.get())
            sp.sympify(self.entry_r.get())
            sp.sympify(self.entry_f.get())
        except Exception:
            messagebox.showerror(
                'Erro de entrada', 'p(x), q(x), r(x) e f(x) devem ser expressões válidas do sympy.')
            return False
        return True

    def solve_edp(self):
        # Função utilitária para converter expressões para float de forma robusta
        def safe_float(expr, default):
            try:
                val = sp.sympify(expr).evalf()
                if hasattr(val, 'is_real') and not val.is_real:
                    return default
                return float(val)
            except Exception:
                return default

        # Executa a resolução da EDP usando todos os métodos numéricos
        if not self.validate_inputs():
            return
        # Adiciona indicador de processamento
        progress = tk.Toplevel(self.root)
        progress.title('Processando...')
        progress.geometry('350x80')
        label = tk.Label(
            progress, text='Resolvendo EDP, aguarde...', font=("Arial", 16))
        label.pack(pady=10)
        pb = ttk.Progressbar(progress, mode='indeterminate', length=300)
        pb.pack(pady=5)
        pb.start(10)
        self.root.update_idletasks()
        try:
            tipo = self.edp_var.get()
            a = float(self.entry_a.get())
            b = float(self.entry_b.get())
            ua = float(self.entry_ua.get())
            ub = float(self.entry_ub.get())
            n_pontos = int(self.entry_n_pontos.get())
            self.resultados = {}
            if tipo == "Onda":
                from time_solvers import onda_1d
                f_expr = self.entry_f.get()
                if not isinstance(f_expr, str):
                    messagebox.showerror("Erro", "O termo fonte f(x) deve ser uma expressão simbólica (ex: 0, sin(pi*x)). Não use arrays NumPy.")
                    pb.stop()
                    progress.destroy()
                    return
                u0_expr = self.entry_u0.get()
                v0_expr = self.entry_v0.get()
                dt = safe_float(self.entry_dt.get() if hasattr(self, 'entry_dt') else '', 0.01)
                tmax = safe_float(self.entry_tmax.get() if hasattr(self, 'entry_tmax') else '', 1.0)
                if dt <= 0:
                    messagebox.showerror("Erro", "O valor de Δt deve ser um número real positivo.")
                    pb.stop()
                    progress.destroy()
                    return
                if tmax <= 0:
                    messagebox.showerror("Erro", "O valor de T_max deve ser um número real positivo.")
                    pb.stop()
                    progress.destroy()
                    return
                try:
                    n_passos = int(tmax / dt)
                    if n_passos < 1:
                        n_passos = 1
                except Exception:
                    n_passos = 100
                for metodo in [
                    'Rayleigh-Ritz', 'Galerkin', 'Colocação', 'Momentos', 'Subdomínios', 'Mínimos Quadrados']:
                    x_vals, resultados = onda_1d.solve_onda_1d(
                        f_expr, u0_expr, v0_expr, a, b, ua, ub, n_pontos, dt, n_passos, metodo=metodo)
                    sol_final = resultados[-1]
                    info = f"máx: {np.max(sol_final):.4g}, mín: {np.min(sol_final):.4g}"
                    self.resultados[metodo] = {
                        'solution': sol_final,
                        'coefficients': info
                    }
                self.display_results()
                self.display_report()
            elif tipo == "Calor":
                from time_solvers import calor_1d
                f_expr = self.entry_f.get()
                u0_expr = self.entry_u0.get()
                dt = safe_float(self.entry_dt.get() if hasattr(self, 'entry_dt') else '', 0.01)
                tmax = safe_float(self.entry_tmax.get() if hasattr(self, 'entry_tmax') else '', 1.0)
                if dt <= 0:
                    messagebox.showerror("Erro", "O valor de Δt deve ser um número real positivo.")
                    pb.stop()
                    progress.destroy()
                    return
                if tmax <= 0:
                    messagebox.showerror("Erro", "O valor de T_max deve ser um número real positivo.")
                    pb.stop()
                    progress.destroy()
                    return
                try:
                    n_passos = int(tmax / dt)
                    if n_passos < 1:
                        n_passos = 1
                except Exception:
                    n_passos = 100
                for metodo in [
                    'Rayleigh-Ritz', 'Galerkin', 'Colocação', 'Momentos', 'Subdomínios', 'Mínimos Quadrados']:
                    x_vals, resultados = calor_1d.solve_calor_1d(
                        f_expr, u0_expr, a, b, ua, ub, n_pontos, dt, n_passos, metodo=metodo)
                    sol_final = resultados[-1]
                    info = f"máx: {np.max(sol_final):.4g}, mín: {np.min(sol_final):.4g}"
                    self.resultados[metodo] = {
                        'solution': sol_final,
                        'coefficients': info
                    }
                self.display_results()
                self.display_report()
            else:
                # Poisson e Helmholtz (estacionárias)
                p = sp.sympify(self.entry_p.get())
                q = sp.sympify(self.entry_q.get())
                r = sp.sympify(self.entry_r.get())
                f = sp.sympify(self.entry_f.get())
                edp_params = {'p': p, 'q': q, 'r': r, 'f': f}
                condicoes_contorno = {'tipo': 'dirichlet', 'valores': (ua, ub)}
                methods = {
                    'Rayleigh-Ritz': RayleighRitz,
                    'Galerkin': Galerkin,
                    'Colocação': MetodoColocacao,
                    'Momentos': MetodoMomentos,
                    'Subdomínios': MetodoSubdominios,
                    'Mínimos Quadrados': MetodoMinimosQuadrados
                }
                for name, method in methods.items():
                    solver = method((a, b), n_pontos, condicoes_contorno)
                    solution, coefficients = solver.resolver(edp_params)
                    self.resultados[name] = {
                        'solution': solution, 'coefficients': coefficients}
                self.display_results()
                self.display_report()
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            pb.stop()
            progress.destroy()

    def display_results(self):
        # Exibe os coeficientes dos métodos na aba de resultados
        self.results_text.delete(1.0, tk.END)
        for name, result in self.resultados.items():
            self.results_text.insert(tk.END, f"{name}:\n")
            self.results_text.insert(
                tk.END, f"  Coeficientes: {result['coefficients']}\n")
            self.results_text.insert(tk.END, "\n")

        self.notebook.select(self.frame_resultados)

    def display_report(self):
        # Gera o relatório completo, incluindo comparação e gráfico
        self.report_text.delete(1.0, tk.END)
        tipo = self.edp_var.get() if hasattr(self, 'edp_var') else ''
        self.report_text.insert(
            tk.END, f'Relatório de Métodos Numéricos para EDP ({tipo})\n')
        self.report_text.insert(tk.END, '-'*50 + '\n')
        # Exibe coeficientes de cada método
        for name, result in self.resultados.items():
            self.report_text.insert(tk.END, f"{name}:\n")
            self.report_text.insert(
                tk.END, f"  Coeficientes: {result['coefficients']}\n\n")
        # Comparação dos resultados (erro RMS)
        self.report_text.insert(tk.END, '\nComparação entre métodos:\n')
        self.report_text.insert(tk.END, '-'*50 + '\n')
        nomes = list(self.resultados.keys())
        for i in range(len(nomes)):
            for j in range(i+1, len(nomes)):
                sol1 = self.resultados[nomes[i]]['solution']
                sol2 = self.resultados[nomes[j]]['solution']
                try:
                    arr1 = np.array(sol1, dtype=float)
                    arr2 = np.array(sol2, dtype=float)
                    rms = np.sqrt(np.mean((arr1 - arr2)**2))
                    self.report_text.insert(
                        tk.END, f"RMS({nomes[i]} vs {nomes[j]}): {rms:.4e}\n")
                except Exception:
                    self.report_text.insert(
                        tk.END, f"Não foi possível comparar {nomes[i]} e {nomes[j]}\n")
        self.report_text.insert(tk.END, '\n')

        # Gráfico comparativo das soluções com cores e marcadores
        cores = ['#1f77b4', '#ff7f0e', '#2ca02c',
                 '#d62728', '#9467bd', '#8c564b']
        marcadores = ['o', 's', '^', 'D', 'v', 'P']
        if self.figura:
            self.figura.clf()
        else:
            self.figura = plt.Figure(figsize=(6, 4), dpi=100)
        ax = self.figura.add_subplot(111)
        x_plot = None
        for idx, (name, result) in enumerate(self.resultados.items()):
            sol = result['solution']
            try:
                arr = np.array(sol, dtype=float)
                if x_plot is None:
                    x_plot = np.linspace(float(self.entry_a.get()), float(
                        self.entry_b.get()), len(arr))
                cor = cores[idx % len(cores)]
                marcador = marcadores[idx % len(marcadores)]
                ax.plot(x_plot, arr, label=name, color=cor,
                        marker=marcador, markevery=max(1, len(arr)//10))
            except Exception:
                continue
        ax.set_title('Comparação das Soluções Aproximadas')
        ax.set_xlabel('x')
        ax.set_ylabel('u(x)')
        ax.legend(loc='center left', bbox_to_anchor=(
            1, 0.5))  # Legenda na lateral direita
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(
            self.figura, master=self.frame_relatorio)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

    def export_report_pdf(self):
        # Exporta o relatório e o gráfico para um arquivo PDF
        import tempfile
        from fpdf import FPDF
        import os
        # Cria PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        # Adiciona texto do relatório
        texto = self.report_text.get(1.0, tk.END)
        for line in texto.splitlines():
            pdf.cell(0, 10, line, ln=1)
        # Salva gráfico como imagem temporária
        img_path = os.path.join(tempfile.gettempdir(), "edp_grafico.png")
        self.figura.savefig(img_path)
        pdf.image(img_path, x=10, y=None, w=180)
        # Salva PDF
        save_path = tk.filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")],
            title="Salvar relatório em PDF")
        if save_path:
            pdf.output(save_path)
            messagebox.showinfo(
                "Exportação", f"Relatório exportado para {save_path}")
        try:
            os.remove(img_path)
        except Exception:
            pass

    def on_edp_change(self, event=None):
        tipo = self.edp_var.get()
        self.update_equation_display()
        # Esconde extras
        self.label_u0.grid_remove()
        self.entry_u0.grid_remove()
        self.label_v0.grid_remove()
        self.entry_v0.grid_remove()
        if tipo == "Calor":
            self.label_u0.grid(row=10, column=0, sticky='w')
            self.entry_u0.grid(row=10, column=1, padx=5)
        elif tipo == "Onda":
            self.label_u0.grid(row=10, column=0, sticky='w')
            self.entry_u0.grid(row=10, column=1, padx=5)
            self.label_v0.grid(row=11, column=0, sticky='w')
            self.entry_v0.grid(row=11, column=1, padx=5)

    def update_equation_display(self):
        tipo = self.edp_var.get() if hasattr(self, 'edp_var') else 'Poisson'
        eq_latex = {
            'Poisson': r"-\dfrac{d^2u}{dx^2} = f(x)",
            'Calor': r"\dfrac{\partial u}{\partial t} = \dfrac{\partial^2 u}{\partial x^2}",
            'Onda': r"\dfrac{\partial^2 u}{\partial t^2} = \dfrac{\partial^2 u}{\partial x^2}",
            'Helmholtz': r"-\dfrac{d^2u}{dx^2} + k^2 u = f(x)"
        }.get(tipo, r"-\dfrac{d^2u}{dx^2} = f(x)")
        self.equation_ax.clear()
        self.equation_ax.axis('off')
        self.equation_ax.text(0.5, 0.5, f"${eq_latex}$", fontsize=32, ha='center', va='center')
        self.equation_canvas.draw()

    def preencher_exemplo(self):
        tipo = self.edp_var.get()
        if tipo == "Poisson":
            self.entry_p.delete(0, 'end'); self.entry_p.insert(0, '1')
            self.entry_q.delete(0, 'end'); self.entry_q.insert(0, '0')
            self.entry_r.delete(0, 'end'); self.entry_r.insert(0, '0')
            self.entry_f.delete(0, 'end'); self.entry_f.insert(0, 'sin(pi*x)')
            self.entry_a.delete(0, 'end'); self.entry_a.insert(0, '0')
            self.entry_b.delete(0, 'end'); self.entry_b.insert(0, '1')
            self.entry_ua.delete(0, 'end'); self.entry_ua.insert(0, '0')
            self.entry_ub.delete(0, 'end'); self.entry_ub.insert(0, '0')
            self.entry_n_pontos.delete(0, 'end'); self.entry_n_pontos.insert(0, '10')
        elif tipo == "Calor":
            L = 1
            self.entry_p.delete(0, 'end'); self.entry_p.insert(0, '1')
            self.entry_q.delete(0, 'end'); self.entry_q.insert(0, '0')
            self.entry_r.delete(0, 'end'); self.entry_r.insert(0, '0')
            self.entry_f.delete(0, 'end'); self.entry_f.insert(0, '0')
            self.entry_a.delete(0, 'end'); self.entry_a.insert(0, '0')
            self.entry_b.delete(0, 'end'); self.entry_b.insert(0, str(L))
            self.entry_ua.delete(0, 'end'); self.entry_ua.insert(0, '0')
            self.entry_ub.delete(0, 'end'); self.entry_ub.insert(0, '0')
            self.entry_n_pontos.delete(0, 'end'); self.entry_n_pontos.insert(0, '20')
            self.entry_u0.delete(0, 'end'); self.entry_u0.insert(0, f'3*sin(2*pi*x/{L})')
            if hasattr(self, 'entry_dt'):
                self.entry_dt.delete(0, 'end'); self.entry_dt.insert(0, '0.01')
            if hasattr(self, 'entry_tmax'):
                self.entry_tmax.delete(0, 'end'); self.entry_tmax.insert(0, '1')
        elif tipo == "Onda":
            self.entry_p.delete(0, 'end'); self.entry_p.insert(0, '1')
            self.entry_q.delete(0, 'end'); self.entry_q.insert(0, '0')
            self.entry_r.delete(0, 'end'); self.entry_r.insert(0, '0')
            self.entry_f.delete(0, 'end'); self.entry_f.insert(0, '0')
            self.entry_a.delete(0, 'end'); self.entry_a.insert(0, '0')
            self.entry_b.delete(0, 'end'); self.entry_b.insert(0, '1')
            self.entry_ua.delete(0, 'end'); self.entry_ua.insert(0, '0')
            self.entry_ub.delete(0, 'end'); self.entry_ub.insert(0, '4')
            self.entry_n_pontos.delete(0, 'end'); self.entry_n_pontos.insert(0, '20')
            # Condições iniciais não nulas para propagação de onda
            self.entry_u0.delete(0, 'end'); self.entry_u0.insert(0, 'sin(pi*x)')
            self.entry_v0.delete(0, 'end'); self.entry_v0.insert(0, '0')
            # Se existirem campos para dt e T_max, preencha também
            if hasattr(self, 'entry_dt'):
                self.entry_dt.delete(0, 'end'); self.entry_dt.insert(0, '0.01')
            if hasattr(self, 'entry_tmax'):
                self.entry_tmax.delete(0, 'end'); self.entry_tmax.insert(0, '1')
        elif tipo == "Helmholtz":
            self.entry_p.delete(0, 'end'); self.entry_p.insert(0, '1')
            self.entry_q.delete(0, 'end'); self.entry_q.insert(0, '0')
            self.entry_r.delete(0, 'end'); self.entry_r.insert(0, '10')
            self.entry_f.delete(0, 'end'); self.entry_f.insert(0, 'sin(pi*x)')
            self.entry_a.delete(0, 'end'); self.entry_a.insert(0, '0')
            self.entry_b.delete(0, 'end'); self.entry_b.insert(0, '1')
            self.entry_ua.delete(0, 'end'); self.entry_ua.insert(0, '0')
            self.entry_ub.delete(0, 'end'); self.entry_ub.insert(0, '0')
            self.entry_n_pontos.delete(0, 'end'); self.entry_n_pontos.insert(0, '10')


# Bloco principal para rodar a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = EDPSolverApp(root)
    root.mainloop()

# Após calcular resultado, garantir que a solução estacionária (reta) seja somada ao resultado dinâmico
# Isso deve ser feito dentro do loop de solve_onda_1d, após cada passo
# Edite o arquivo 'src/time_solvers/onda_1d.py' para garantir isso
