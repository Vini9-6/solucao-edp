from tkinter import Tk, Frame, Label, Entry, Button, Text, Scrollbar, messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("EDP Solver")
        self.master.geometry("1200x800")

        self.create_widgets()

    def create_widgets(self):
        # Frame de configuração
        self.config_frame = Frame(self.master)
        self.config_frame.pack(side="top", fill="x", padx=10, pady=10)

        Label(self.config_frame, text="p(x):").grid(row=0, column=0, sticky='w')
        self.entry_p = Entry(self.config_frame, width=20)
        self.entry_p.grid(row=0, column=1)

        Label(self.config_frame, text="q(x):").grid(row=1, column=0, sticky='w')
        self.entry_q = Entry(self.config_frame, width=20)
        self.entry_q.grid(row=1, column=1)

        Label(self.config_frame, text="r(x):").grid(row=2, column=0, sticky='w')
        self.entry_r = Entry(self.config_frame, width=20)
        self.entry_r.grid(row=2, column=1)

        Label(self.config_frame, text="f(x):").grid(row=3, column=0, sticky='w')
        self.entry_f = Entry(self.config_frame, width=20)
        self.entry_f.grid(row=3, column=1)

        Label(self.config_frame, text="a:").grid(row=4, column=0, sticky='w')
        self.entry_a = Entry(self.config_frame, width=20)
        self.entry_a.grid(row=4, column=1)

        Label(self.config_frame, text="b:").grid(row=5, column=0, sticky='w')
        self.entry_b = Entry(self.config_frame, width=20)
        self.entry_b.grid(row=5, column=1)

        Label(self.config_frame, text="u(a):").grid(row=6, column=0, sticky='w')
        self.entry_ua = Entry(self.config_frame, width=20)
        self.entry_ua.grid(row=6, column=1)

        Label(self.config_frame, text="u(b):").grid(row=7, column=0, sticky='w')
        self.entry_ub = Entry(self.config_frame, width=20)
        self.entry_ub.grid(row=7, column=1)

        Button(self.config_frame, text="Resolver EDP", command=self.solve_edp).grid(row=8, columnspan=2, pady=10)

        # Frame de resultados
        self.result_frame = Frame(self.master)
        self.result_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        self.result_text = Text(self.result_frame, height=15)
        self.result_text.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(self.result_frame, command=self.result_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.result_text.config(yscrollcommand=scrollbar.set)

        # Frame de gráfico
        self.graph_frame = Frame(self.master)
        self.graph_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def solve_edp(self):
        # Aqui você chamaria a lógica para resolver a EDP
        # e atualizar a área de resultados e o gráfico.
        messagebox.showinfo("Info", "Função de resolução não implementada.")

if __name__ == "__main__":
    root = Tk()
    app = MainWindow(root)
    root.mainloop()