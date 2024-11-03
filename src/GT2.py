import tkinter as tk
from sympy import symbols, diff, Eq, solve, lambdify, simplify
from sympy.parsing.sympy_parser import parse_expr
from sympy.printing.pretty import pretty  # Importando para exibir raiz quadrada
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

# Definindo as variáveis
x, y, z = symbols('x y z')

class GT2():

    @staticmethod
    def run():
        # Configurando interface com Tkinter
        root = tk.Tk()
        root.title("GT2")

        # Campo para entrada da função
        tk.Label(root, text="Superfície S(x, y, z) = 0:").grid(row=0, column=0, sticky="w")
        entrada_funcao = tk.Entry(root, width=40)
        entrada_funcao.grid(row=0, column=1, columnspan=3)

        # Campos para entrada das coordenadas do ponto M
        tk.Label(root, text="Ponto M(x, y, z):").grid(row=1, column=0, sticky="w")
        tk.Label(root, text="x:").grid(row=1, column=1)
        entrada_x = tk.Entry(root, width=10)
        entrada_x.grid(row=1, column=2)

        tk.Label(root, text="y:").grid(row=2, column=1)
        entrada_y = tk.Entry(root, width=10)
        entrada_y.grid(row=2, column=2)

        tk.Label(root, text="z:").grid(row=3, column=1)
        entrada_z = tk.Entry(root, width=10)
        entrada_z.grid(row=3, column=2)

        # Botão para calcular
        botao_calcular = tk.Button(root, text="Calcular", command=lambda: GT2.calcular(entrada_funcao, entrada_x, entrada_y, entrada_z, ax, canvas, resultado_texto))
        botao_calcular.grid(row=4, column=1, columnspan=2)

        # Área de texto para exibir os resultados de texto
        resultado_texto = tk.Text(root, width=60, height=8)
        resultado_texto.grid(row=5, column=0, columnspan=4)

        # Canvas para exibir o gráfico
        fig = plt.figure(figsize=(7, 5))
        ax = fig.add_subplot(111, projection='3d')
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().grid(row=6, column=0, columnspan=4)

        root.mainloop()

    @staticmethod
    def calcular(entrada_funcao, entrada_x, entrada_y, entrada_z, ax, canvas, resultado_texto):
        funcao = entrada_funcao.get()

        try:
            # Convertendo a função e coordenadas usando parse_expr
            superficie = parse_expr(funcao)
            ponto_x = parse_expr(entrada_x.get())
            ponto_y = parse_expr(entrada_y.get())
            ponto_z = parse_expr(entrada_z.get())
        except Exception as e:
            ax.clear()
            ax.text(0.1, 0.5, 0.5, f"Erro na entrada: {e}", fontsize=12, color="red")
            canvas.draw()
            return

        # Resolvendo a equação da superfície para z
        try:
            solucao_z = solve(Eq(superficie, 0), z)
            funcao_z = solucao_z[0]  # Seleciona a primeira solução (em caso de múltiplas raízes)
            superf_func = lambdify((x, y), funcao_z, 'numpy')
        except Exception as e:
            ax.clear()
            ax.text(0.1, 0.5, 0.5, f"Erro ao resolver a superfície: {e}", fontsize=12, color="red")
            canvas.draw()
            return

        # Calculando gradientes parciais simbolicamente
        gradiente_x = diff(superficie, x)
        gradiente_y = diff(superficie, y)
        gradiente_z = diff(superficie, z)

        # Avaliando o gradiente no ponto M simbolicamente (mantendo raízes e frações)
        grad_x = gradiente_x.subs({x: ponto_x, y: ponto_y, z: ponto_z})
        grad_y = gradiente_y.subs({x: ponto_x, y: ponto_y, z: ponto_z})
        grad_z = gradiente_z.subs({x: ponto_x, y: ponto_y, z: ponto_z})

        # Construindo o plano tangente com a expressão exata
        plano_tangente_expr = grad_x * (x - ponto_x) + grad_y * (y - ponto_y) + grad_z * (z - ponto_z)
        plano_tangente_completo = Eq(simplify(plano_tangente_expr), 0)

        # Exibindo os resultados na área de texto com o formato de raiz quadrada
        resultado_texto.delete("1.0", tk.END)
        resultado_texto.insert(tk.END, f"Gradiente: ({pretty(grad_x)}, {pretty(grad_y)}, {pretty(grad_z)})\n")
        resultado_texto.insert(tk.END, f"Equação do Plano Tangente:\n {pretty(plano_tangente_completo)}\n")

        # Limpando e preparando para renderizar o gráfico
        ax.clear()

        # Configuração de limites e plano 3D
        limite = 5
        x_vals = np.linspace(float(ponto_x.evalf() - limite), float(ponto_x.evalf() + limite), 50)
        y_vals = np.linspace(float(ponto_y.evalf() - limite), float(ponto_y.evalf() + limite), 50)
        X, Y = np.meshgrid(x_vals, y_vals)

        # Calculando valores de Z para a superfície e verificando complexidade
        try:
            Z_superficie = np.array(superf_func(X, Y), dtype=float)
            if np.iscomplexobj(Z_superficie):
                raise ValueError("Erro: A superfície contém valores complexos.")
        except (TypeError, ValueError) as e:
            ax.clear()
            ax.text(0.1, 0.5, 0.5, str(e), fontsize=12, color="red")
            canvas.draw()
            return

        # Calculando valores de Z para o plano tangente
        if grad_z != 0:
            Z_plano = ponto_z + (grad_x * (X - ponto_x.evalf()) + grad_y * (Y - ponto_y.evalf())) / -grad_z
            if np.iscomplexobj(Z_plano):
                ax.clear()
                ax.text(0.1, 0.5, 0.5, "Erro: O plano tangente contém valores complexos.", fontsize=12, color="red")
                canvas.draw()
                return
        else:
            Z_plano = np.full_like(X, np.nan)  # Em caso de plano paralelo ao eixo Z

        # Plotando a superfície e o plano tangente com legendas
        ax.plot_surface(X, Y, Z_superficie, color='lightblue', alpha=0.5, edgecolor='none', label="Superfície")
        ax.plot_surface(X, Y, Z_plano, color='orange', alpha=0.5, edgecolor='none', label="Plano Tangente")

        # Adicionando o ponto M e os vetores do gradiente
        ax.scatter([float(ponto_x.evalf())], [float(ponto_y.evalf())], [float(ponto_z.evalf())], color='red', s=50,
                   label="Ponto M")
        ax.quiver(float(ponto_x.evalf()), float(ponto_y.evalf()), float(ponto_z.evalf()), float(grad_x.evalf()),
                  float(grad_y.evalf()), float(grad_z.evalf()), color="green", length=1, normalize=True, label="Gradiente")

        # Configurações de visualização e legendas
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.legend()
        ax.set_title("Superfície, Plano Tangente e Gradiente")
        canvas.draw()