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

        # Tooltips explicativos para cada campo
        tooltips = {
            'p(x)': 'Coeficiente de u"(x) na EDP. Ex: 1, x, exp(x)',
            'q(x)': 'Coeficiente de u\'(x) na EDP. Ex: 0, x**2',
            'r(x)': 'Coeficiente de u(x) na EDP. Ex: 0, 2',
            'f(x)': 'Função do lado direito. Ex: sin(pi*x), x**2',
            'Domínio [a, b]': 'Extremos do domínio. Ex: 0 e 1',
            'Condições de Contorno': 'Valores de u(a) e u(b)',
            'Número de Pontos': 'Quantidade de pontos de discretização'
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

        # Criação dos campos de entrada e tooltips
        label_p = ttk.Label(config_frame, text="p(x):", font=fonte)
        label_p.grid(row=0, column=0, sticky='w')
        self.entry_p = ttk.Entry(config_frame, font=fonte)
        self.entry_p.grid(row=0, column=1, padx=5)
        add_tooltip(label_p, tooltips['p(x)'])
        add_tooltip(self.entry_p, tooltips['p(x)'])

        label_q = ttk.Label(config_frame, text="q(x):", font=fonte)
        label_q.grid(row=1, column=0, sticky='w')
        self.entry_q = ttk.Entry(config_frame, font=fonte)
        self.entry_q.grid(row=1, column=1, padx=5)
        add_tooltip(label_q, tooltips['q(x)'])
        add_tooltip(self.entry_q, tooltips['q(x)'])

        label_r = ttk.Label(config_frame, text="r(x):", font=fonte)
        label_r.grid(row=2, column=0, sticky='w')
        self.entry_r = ttk.Entry(config_frame, font=fonte)
        self.entry_r.grid(row=2, column=1, padx=5)
        add_tooltip(label_r, tooltips['r(x)'])
        add_tooltip(self.entry_r, tooltips['r(x)'])

        label_f = ttk.Label(config_frame, text="f(x):", font=fonte)
        label_f.grid(row=3, column=0, sticky='w')
        self.entry_f = ttk.Entry(config_frame, font=fonte)
        self.entry_f.grid(row=3, column=1, padx=5)
        add_tooltip(label_f, tooltips['f(x)'])
        add_tooltip(self.entry_f, tooltips['f(x)'])

        label_dom = ttk.Label(config_frame, text="Domínio [a, b]:", font=fonte)
        label_dom.grid(row=4, column=0, sticky='w')
        self.entry_a = ttk.Entry(config_frame, font=fonte)
        self.entry_a.grid(row=4, column=1, padx=5)
        self.entry_b = ttk.Entry(config_frame, font=fonte)
        self.entry_b.grid(row=4, column=2, padx=5)
        add_tooltip(label_dom, tooltips['Domínio [a, b]'])
        add_tooltip(self.entry_a, tooltips['Domínio [a, b]'])
        add_tooltip(self.entry_b, tooltips['Domínio [a, b]'])

        label_cc = ttk.Label(
            config_frame, text="Condições de Contorno:", font=fonte)
        label_cc.grid(row=5, column=0, sticky='w')
        self.entry_ua = ttk.Entry(config_frame, font=fonte)
        self.entry_ua.grid(row=5, column=1, padx=5)
        self.entry_ub = ttk.Entry(config_frame, font=fonte)
        self.entry_ub.grid(row=5, column=2, padx=5)
        add_tooltip(label_cc, tooltips['Condições de Contorno'])
        add_tooltip(self.entry_ua, tooltips['Condições de Contorno'])
        add_tooltip(self.entry_ub, tooltips['Condições de Contorno'])

        label_np = ttk.Label(
            config_frame, text="Número de Pontos:", font=fonte)
        label_np.grid(row=6, column=0, sticky='w')
        self.entry_n_pontos = ttk.Entry(config_frame, font=fonte)
        self.entry_n_pontos.grid(row=6, column=1, padx=5)
        add_tooltip(label_np, tooltips['Número de Pontos'])
        add_tooltip(self.entry_n_pontos, tooltips['Número de Pontos'])

        # Botão para resolver a EDP
        ttk.Button(config_frame, text="Resolver EDP", command=self.solve_edp, style="Big.TButton").grid(
            row=7, column=0, columnspan=3, pady=10)

        # Estilo para botão maior
        style = ttk.Style()
        style.configure("Big.TButton", font=fonte)

        # Botão para alternar tema claro/escuro
        self.theme = 'light'

        def toggle_theme():
            # Alterna entre tema claro e escuro
            if self.theme == 'light':
                self.root.tk_setPalette(
                    background='#222', foreground='#fff', activeBackground='#444', activeForeground='#fff')
                style.configure('.', background='#222', foreground='#fff')
                style.configure('TLabel', background='#222', foreground='#fff')
                style.configure(
                    'TEntry', fieldbackground='#333', foreground='#fff')
                style.configure('TFrame', background='#222')
                self.theme = 'dark'
            else:
                self.root.tk_setPalette(
                    background='#f0f0f0', foreground='#000', activeBackground='#ececec', activeForeground='#000')
                style.configure('.', background='#f0f0f0', foreground='#000')
                style.configure('TLabel', background='#f0f0f0',
                                foreground='#000')
                style.configure(
                    'TEntry', fieldbackground='#fff', foreground='#000')
                style.configure('TFrame', background='#f0f0f0')
                self.theme = 'light'
        ttk.Button(config_frame, text="Alternar Tema Claro/Escuro", command=toggle_theme,
                   style="Big.TButton").grid(row=8, column=0, columnspan=3, pady=10)
        # Botão para visualizar a equação simbólica
        ttk.Button(config_frame, text="Visualizar Equação", command=self.display_equation,
                   style="Big.TButton").grid(row=9, column=0, columnspan=3, pady=10)

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
Bem-vindo ao EDP Solver!

Este sistema resolve EDPs unidimensionais de segunda ordem usando diversos métodos numéricos.

Como usar:
1. Preencha os campos da aba Configuração com os parâmetros da EDP.
2. Clique em 'Resolver EDP'.
3. Veja os resultados, relatórios e gráficos nas abas correspondentes.

Exemplo de entrada:
  p(x): 1
  q(x): 0
  r(x): 0
  f(x): sin(pi*x)
  Domínio: 0   1
  Condições de contorno: 0   0
  Número de pontos: 10

Métodos implementados:
- Rayleigh-Ritz
- Galerkin
- Colocação
- Momentos
- Subdomínios
- Mínimos Quadrados

Dicas:
- Use funções do sympy em f(x), p(x), q(x), r(x) (ex: sin(pi*x), exp(x), x**2).
- O número de pontos afeta a precisão e o tempo de cálculo.
- Para comparar com solução analítica, insira a expressão correta e compare os gráficos.

Sobre os resultados:
- Os coeficientes são os pesos das funções base na solução aproximada.
- O erro RMS mostra a diferença entre as soluções dos métodos.
- O gráfico compara visualmente as soluções.

Última atualização: 12/06/2025
""")
        help_text.config(state='disabled')

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
            # Lê e converte os parâmetros da interface
            p = sp.sympify(self.entry_p.get())
            q = sp.sympify(self.entry_q.get())
            r = sp.sympify(self.entry_r.get())
            f = sp.sympify(self.entry_f.get())
            a = float(self.entry_a.get())
            b = float(self.entry_b.get())
            ua = float(self.entry_ua.get())
            ub = float(self.entry_ub.get())
            n_pontos = int(self.entry_n_pontos.get())

            edp_params = {'p': p, 'q': q, 'r': r, 'f': f}
            condicoes_contorno = {'tipo': 'dirichlet', 'valores': (ua, ub)}

            self.resultados = {}
            # Dicionário de métodos numéricos disponíveis
            methods = {
                'Rayleigh-Ritz': RayleighRitz,
                'Galerkin': Galerkin,
                'Colocação': MetodoColocacao,
                'Momentos': MetodoMomentos,
                'Subdomínios': MetodoSubdominios,
                'Mínimos Quadrados': MetodoMinimosQuadrados
            }

            # Executa cada método e armazena os resultados
            for name, method in methods.items():
                solver = method((a, b), n_pontos, condicoes_contorno)
                solution, coefficients = solver.resolver(edp_params)
                self.resultados[name] = {
                    'solution': solution, 'coefficients': coefficients}

            self.display_results()
            self.display_report()  # Preenche o relatório
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
        self.report_text.insert(
            tk.END, 'Relatório de Métodos Numéricos para EDP\n')
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

    def display_equation(self):
        # Monta e exibe a equação simbólica da EDP baseada nos parâmetros do usuário
        try:
            x = sp.Symbol('x')
            p = sp.sympify(self.entry_p.get())
            q = sp.sympify(self.entry_q.get())
            r = sp.sympify(self.entry_r.get())
            f = sp.sympify(self.entry_f.get())
            eq = sp.Eq(p*sp.Derivative('u(x)', x, 2) + q *
                       sp.Derivative('u(x)', x) + r*sp.Symbol('u(x)'), f)
            eq_str = sp.latex(eq)
            # Exibe em um widget de texto ou label
            if hasattr(self, 'equation_label'):
                self.equation_label.config(
                    text=f"Equação montada: $${eq_str}$$")
            else:
                self.equation_label = tk.Label(self.frame_config, text=f"Equação montada: $${eq_str}$$", font=(
                    "Arial", 16), anchor='w', justify='left')
                self.equation_label.pack(
                    fill='x', padx=10, pady=10, after=self.frame_config.winfo_children()[-1])
        except Exception:
            if hasattr(self, 'equation_label'):
                self.equation_label.config(
                    text="Equação inválida. Corrija os parâmetros.")

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


# Bloco principal para rodar a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = EDPSolverApp(root)
    root.mainloop()
