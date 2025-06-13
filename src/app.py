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

class EDPSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EDP Solver")
        self.root.geometry("1200x800")
        
        self.resultados = {}
        self.figura = None
        self.canvas = None
        
        self.create_interface()
        
    def create_interface(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.frame_config = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_config, text="Configuração")
        
        self.frame_resultados = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_resultados, text="Resultados")
        
        self.frame_relatorio = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_relatorio, text="Relatório")
        
        self.create_config_frame()
        self.create_results_frame()
        self.create_report_frame()
        
    def create_config_frame(self):
        # Frame for configuration inputs
        config_frame = ttk.LabelFrame(self.frame_config, text="Configurações da EDP", padding=10)
        config_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(config_frame, text="p(x):").grid(row=0, column=0, sticky='w')
        self.entry_p = ttk.Entry(config_frame)
        self.entry_p.grid(row=0, column=1, padx=5)
        
        ttk.Label(config_frame, text="q(x):").grid(row=1, column=0, sticky='w')
        self.entry_q = ttk.Entry(config_frame)
        self.entry_q.grid(row=1, column=1, padx=5)
        
        ttk.Label(config_frame, text="r(x):").grid(row=2, column=0, sticky='w')
        self.entry_r = ttk.Entry(config_frame)
        self.entry_r.grid(row=2, column=1, padx=5)
        
        ttk.Label(config_frame, text="f(x):").grid(row=3, column=0, sticky='w')
        self.entry_f = ttk.Entry(config_frame)
        self.entry_f.grid(row=3, column=1, padx=5)
        
        ttk.Label(config_frame, text="Domínio [a, b]:").grid(row=4, column=0, sticky='w')
        self.entry_a = ttk.Entry(config_frame)
        self.entry_a.grid(row=4, column=1, padx=5)
        self.entry_b = ttk.Entry(config_frame)
        self.entry_b.grid(row=4, column=2, padx=5)
        
        ttk.Label(config_frame, text="Condições de Contorno:").grid(row=5, column=0, sticky='w')
        self.entry_ua = ttk.Entry(config_frame)
        self.entry_ua.grid(row=5, column=1, padx=5)
        self.entry_ub = ttk.Entry(config_frame)
        self.entry_ub.grid(row=5, column=2, padx=5)
        
        ttk.Label(config_frame, text="Número de Pontos:").grid(row=6, column=0, sticky='w')
        self.entry_n_pontos = ttk.Entry(config_frame)
        self.entry_n_pontos.grid(row=6, column=1, padx=5)
        
        ttk.Button(config_frame, text="Resolver EDP", command=self.solve_edp).grid(row=7, column=0, columnspan=3, pady=10)
        
    def create_results_frame(self):
        self.results_text = scrolledtext.ScrolledText(self.frame_resultados, height=15)
        self.results_text.pack(fill='both', expand=True, padx=10, pady=10)
        
    def create_report_frame(self):
        self.report_text = scrolledtext.ScrolledText(self.frame_relatorio, height=15)
        self.report_text.pack(fill='both', expand=True, padx=10, pady=10)
        
    def solve_edp(self):
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
            
            edp_params = {'p': p, 'q': q, 'r': r, 'f': f}
            condicoes_contorno = {'tipo': 'dirichlet', 'valores': (ua, ub)}
            
            self.resultados = {}
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
                self.resultados[name] = {'solution': solution, 'coefficients': coefficients}
            
            self.display_results()
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def display_results(self):
        self.results_text.delete(1.0, tk.END)
        for name, result in self.resultados.items():
            self.results_text.insert(tk.END, f"{name}:\n")
            self.results_text.insert(tk.END, f"  Coeficientes: {result['coefficients']}\n")
            self.results_text.insert(tk.END, "\n")
        
        self.notebook.select(self.frame_resultados)

if __name__ == "__main__":
    root = tk.Tk()
    app = EDPSolverApp(root)
    root.mainloop()