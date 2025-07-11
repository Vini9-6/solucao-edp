from tkinter import Tk, Frame, Label, Entry, Button, Text, Scrollbar, messagebox, ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp
from methods.rayleigh_ritz import RayleighRitz
from methods.galerkin import Galerkin
from methods.colocacao import MetodoColocacao
from methods.momentos import MetodoMomentos
from methods.subdominios import MetodoSubdominios
from methods.minimos_quadrados import MetodoMinimosQuadrados

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("EDP Solver")
        self.master.geometry("1200x800") 
        self.create_interface()

    def create_interface(self):
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.frame_config = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_config, text="Configuração")
        self.frame_resultados = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_resultados, text="Resultados")
        self.frame_relatorio = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_relatorio, text="Relatório")
        self.frame_ajuda = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_ajuda, text="Ajuda")

        self.create_config_frame()
        self.create_results_frame()
        self.create_report_frame()
        self.create_help_frame()

    def create_config_frame(self):
        fonte = ("Arial", 16)
        config_frame = ttk.LabelFrame(self.frame_config, text="Configurações da EDP", padding=10)
        config_frame.pack(fill='x', padx=10, pady=10)

        Label(config_frame, text="Tipo de Equação:", font=fonte).grid(row=0, column=0, sticky='w')
        self.edp_var = ttk.Combobox(config_frame, values=[
            "Poisson",
            "Calor",
            "Onda",
            "Helmholtz"
        ], state="readonly", width=18, font=fonte)
        self.edp_var.current(0)
        self.edp_var.grid(row=0, column=1, padx=5)

        Label(config_frame, text="p(x):", font=fonte).grid(row=1, column=0, sticky='w')
        self.entry_p = ttk.Entry(config_frame, font=fonte)
        self.entry_p.grid(row=1, column=1, padx=5)
        Label(config_frame, text="q(x):", font=fonte).grid(row=2, column=0, sticky='w')
        self.entry_q = ttk.Entry(config_frame, font=fonte)
        self.entry_q.grid(row=2, column=1, padx=5)
        Label(config_frame, text="r(x):", font=fonte).grid(row=3, column=0, sticky='w')
        self.entry_r = ttk.Entry(config_frame, font=fonte)
        self.entry_r.grid(row=3, column=1, padx=5)
        Label(config_frame, text="f(x):", font=fonte).grid(row=4, column=0, sticky='w')
        self.entry_f = ttk.Entry(config_frame, font=fonte)
        self.entry_f.grid(row=4, column=1, padx=5)
        Label(config_frame, text="a:", font=fonte).grid(row=5, column=0, sticky='w')
        self.entry_a = ttk.Entry(config_frame, font=fonte)
        self.entry_a.grid(row=5, column=1, padx=5)
        Label(config_frame, text="b:", font=fonte).grid(row=6, column=0, sticky='w')
        self.entry_b = ttk.Entry(config_frame, font=fonte)
        self.entry_b.grid(row=6, column=1, padx=5)
        Label(config_frame, text="u(a):", font=fonte).grid(row=7, column=0, sticky='w')
        self.entry_ua = ttk.Entry(config_frame, font=fonte)
        self.entry_ua.grid(row=7, column=1, padx=5)
        Label(config_frame, text="u(b):", font=fonte).grid(row=8, column=0, sticky='w')
        self.entry_ub = ttk.Entry(config_frame, font=fonte)
        self.entry_ub.grid(row=8, column=1, padx=5)
        Label(config_frame, text="Nº Pontos:", font=fonte).grid(row=9, column=0, sticky='w')
        self.entry_n_pontos = ttk.Entry(config_frame, font=fonte)
        self.entry_n_pontos.grid(row=9, column=1, padx=5)
        Label(config_frame, text="Δt:", font=fonte).grid(row=10, column=0, sticky='w')
        self.entry_dt = ttk.Entry(config_frame, font=fonte)
        self.entry_dt.insert(0, "0.01")
        self.entry_dt.grid(row=10, column=1, padx=5)
        Label(config_frame, text="T_max:", font=fonte).grid(row=11, column=0, sticky='w')
        self.entry_tmax = ttk.Entry(config_frame, font=fonte)
        self.entry_tmax.insert(0, "1.0")
        self.entry_tmax.grid(row=11, column=1, padx=5)
        Button(config_frame, text="Resolver EDP", font=fonte, command=self.solve_edp).grid(row=12, column=0, columnspan=2, pady=10)

    def create_results_frame(self):
        self.results_text = Text(self.frame_resultados, height=15, font=("Arial", 14))
        self.results_text.pack(fill='both', expand=True, padx=10, pady=10)
        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame_resultados)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

    def create_report_frame(self):
        self.report_text = Text(self.frame_relatorio, height=15, font=("Arial", 14))
        self.report_text.pack(fill='both', expand=True, padx=10, pady=10)
        Button(self.frame_relatorio, text="Exportar PDF", command=self.export_report_pdf, font=("Arial", 14)).pack(pady=10)

    def create_help_frame(self):
        help_text = Text(self.frame_ajuda, height=30, font=("Arial", 14))
        help_text.pack(fill='both', expand=True, padx=10, pady=10)
        help_text.insert('end', "Ajuda: Instruções e exemplos de uso...\n")
        help_text.config(state='disabled')

    def solve_edp(self):
        edp_tipo = self.edp_var.get()
        try:
            p = sp.sympify(self.entry_p.get())
            q = sp.sympify(self.entry_q.get())
            r = sp.sympify(self.entry_r.get())
            f = sp.sympify(self.entry_f.get())
            a = float(self.entry_a.get())
            b = float(self.entry_b.get())
            ua = float(self.entry_ua.get())
            ub = float(self.entry_ub.get())
            n_pontos = int(self.entry_n_pontos.get())
            dt = float(self.entry_dt.get())
            t_max = float(self.entry_tmax.get())
            edp_params = {'p': p, 'q': q, 'r': r, 'f': f}
            condicoes_contorno = {'tipo': 'dirichlet', 'valores': (ua, ub)}
            self.results_text.delete(1.0, 'end')
            self.figure.clf()
            if edp_tipo == "Poisson":
                methods = {
                    'Rayleigh-Ritz': RayleighRitz,
                    'Galerkin': Galerkin,
                    'Colocação': MetodoColocacao,
                    'Momentos': MetodoMomentos,
                    'Subdomínios': MetodoSubdominios,
                    'Mínimos Quadrados': MetodoMinimosQuadrados
                }
                x_plot = np.linspace(a, b, n_pontos)
                for name, method in methods.items():
                    solver = method((a, b), n_pontos, condicoes_contorno)
                    sol, coef = solver.resolver(edp_params)
                    self.results_text.insert('end', f"{name}:\nCoeficientes: {coef}\n\n")
                    ax = self.figure.gca()
                    ax.plot(x_plot, sol, label=name)
                ax.set_title('Solução da Equação de Poisson')
                ax.set_xlabel('x')
                ax.set_ylabel('u(x)')
                ax.legend()
                self.canvas.draw()
                self.notebook.select(self.frame_resultados)
            elif edp_tipo == "Calor":
                from time_solvers.calor_1d import solve_calor_1d
                u0_expr = self.entry_ua.get()  # ou campo extra
                n_passos = int(t_max / dt)
                metodo = 'Rayleigh-Ritz'
                x_vals, resultados = solve_calor_1d(self.entry_f.get(), u0_expr, a, b, ua, ub, n_pontos, dt, n_passos, metodo)
                self.results_text.insert('end', f"Solução final (t={n_passos*dt}):\n{resultados[-1]}\n")
                ax = self.figure.gca()
                ax.plot(x_vals, resultados[-1], label=f't={n_passos*dt:.2f}')
                ax.set_title('Solução da Equação do Calor (t final)')
                ax.set_xlabel('x')
                ax.set_ylabel('u(x, t)')
                ax.legend()
                self.canvas.draw()
                self.notebook.select(self.frame_resultados)
            elif edp_tipo == "Onda":
                from time_solvers.onda_1d import solve_onda_1d
                # Parâmetros fixos conforme solicitado
                a = 0.0
                b = 1.0
                ua = 0.0
                ub = 4.0
                u0_expr = "0"
                v0_expr = "0"
                try:
                    n_pontos = int(self.entry_n_pontos.get())
                except:
                    n_pontos = 20
                try:
                    dt = float(self.entry_dt.get())
                except:
                    dt = 0.01
                try:
                    t_max = float(self.entry_tmax.get())
                except:
                    t_max = 1.0
                n_passos = int(t_max // dt)
                metodo = 'Rayleigh-Ritz'
                lamb = 4.0
                x_vals, resultados = solve_onda_1d("0", u0_expr, v0_expr, a, b, ua, ub, n_pontos, dt, n_passos, metodo, lamb)
                self.results_text.insert('end', f"Solução final (t={n_passos*dt}):\n{resultados[-1]}\n")
                ax = self.figure.gca()
                ax.plot(x_vals, resultados[-1], label=f't={n_passos*dt:.2f}')
                ax.set_title('Solução da Equação da Onda (t final)')
                ax.set_xlabel('x')
                ax.set_ylabel('u(x, t)')
                ax.legend()
                self.canvas.draw()
                self.notebook.select(self.frame_resultados)
            elif edp_tipo == "Helmholtz":
                methods = {
                    'Rayleigh-Ritz': RayleighRitz,
                    'Galerkin': Galerkin,
                    'Colocação': MetodoColocacao,
                    'Momentos': MetodoMomentos,
                    'Subdomínios': MetodoSubdominios,
                    'Mínimos Quadrados': MetodoMinimosQuadrados
                }
                x_plot = np.linspace(a, b, n_pontos)
                for name, method in methods.items():
                    solver = method((a, b), n_pontos, condicoes_contorno)
                    sol, coef = solver.resolver(edp_params)
                    self.results_text.insert('end', f"{name}:\nCoeficientes: {coef}\n\n")
                    ax = self.figure.gca()
                    ax.plot(x_plot, sol, label=name)
                ax.set_title('Solução da Equação de Helmholtz')
                ax.set_xlabel('x')
                ax.set_ylabel('u(x)')
                ax.legend()
                self.canvas.draw()
                self.notebook.select(self.frame_resultados)
            else:
                messagebox.showinfo("Info", f"Tipo de EDP não reconhecido: {edp_tipo}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def export_report_pdf(self):
        try:
            from fpdf import FPDF
            import tempfile, os
            texto = self.report_text.get(1.0, 'end')
            img_path = os.path.join(tempfile.gettempdir(), "edp_grafico.png")
            self.figure.savefig(img_path)
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for line in texto.splitlines():
                pdf.cell(0, 10, line, ln=1)
            pdf.image(img_path, x=10, y=None, w=180)
            from tkinter import filedialog
            save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")],
                title="Salvar relatório em PDF")
            if save_path:
                pdf.output(save_path)
                messagebox.showinfo("Exportação", f"Relatório exportado para {save_path}")
            try:
                os.remove(img_path)
            except Exception:
                pass
        except Exception as e:
            messagebox.showerror("Erro ao exportar PDF", str(e))

if __name__ == "__main__":
    root = Tk()
    app = MainWindow(root)
    root.mainloop()