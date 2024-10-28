import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

# --- Funções para a superfície e o plano tangente ---
def superficie_S(x, y):
    """Calcula z para a superfície S: 3x^2 + 12y^2 + 4z^2 = 48."""
    return np.sqrt((48 - 3 * x ** 2 - 12 * y ** 2) / 4)

def plano_tangente(x, y):
    """Calcula z para o plano tangente: 12x + 24y + 8√6z = 96."""
    return (96 - 12 * x - 24 * y) / (8 * np.sqrt(6))

# --- Configuração da janela Tkinter ---
root = tk.Tk()
root.title("Resolução GT2")
root.geometry("1200x600")

# --- Função para criar o gráfico 3D ---
def criar_grafico_3d(fig):
    ax = fig.add_subplot(111, projection='3d')

    # Geração da grade de pontos
    x = np.linspace(-4, 4, 50)
    y = np.linspace(-4, 4, 50)
    X, Y = np.meshgrid(x, y)
    Z_superficie = superficie_S(X, Y)
    Z_plano = plano_tangente(X, Y)

    # Plotando a superfície e o plano tangente
    ax.plot_surface(X, Y, Z_superficie, color='lightblue', alpha=0.5)
    ax.plot_surface(X, Y, Z_plano, color='lightgreen', alpha=0.7)

    # Plotando o ponto M(2, 1, √6)
    M = (2, 1, np.sqrt(6))
    ax.scatter(*M, color='red', s=50)

    # Configuração dos eixos
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(r"$\mathbf{Resolução\ da\ t2\ do\ GT2}$: "
                 'Superfície S e Plano Tangente no Ponto M', fontsize=9)

# --- Função para criar o texto explicativo em LaTeX ---
def criar_texto_latex(fig):
    ax = fig.add_subplot(111)
    ax.axis("off")  # Desativa os eixos para exibir apenas o texto

    # Blocos de texto em LaTeX
    text_blocks = [
        r"$\mathbf{Resolução\ da\ t1\ do\ GT2:}$",
        r"Vamos resolver o problema de determinar a equação do plano tangente",
        r"à superfície S no ponto M(2, 1, √6) e também calcular o gradiente nesse ponto.",
        r"A superfície S é dada pela equação implícita:",
        r"$3x^2 + 12y^2 + 4z^2 = 48$",
        r"Podemos reescrever esta equação como:",
        r"$F(x, y, z) = 3x^2 + 12y^2 + 4z^2 - 48 = 0$",
        r"O gradiente de F(x, y, z) é dado por:",
        r"$\nabla F = \left( \frac{\partial F}{\partial x}, \frac{\partial F}{\partial y}, \frac{\partial F}{\partial z} \right)$",
        r"Vamos calcular as derivadas parciais de F(x, y, z):",
        r"$\frac{\partial F}{\partial x} = 6x$, $\frac{\partial F}{\partial y} = 24y$, $\frac{\partial F}{\partial z} = 8z$",
        r"Portanto, o gradiente de F(x, y, z) é:",
        r"$\nabla F(x, y, z) = (6x, 24y, 8z)$",
        r"$Substituímos:\ x = 2, y = 1, z = \sqrt{6}:$",
        r"$\nabla F(2, 1, \sqrt{6}) = (12, 24, 8\sqrt{6})$",
        r"A equação do plano tangente é:",
        r"$12(x - 2) + 24(y - 1) + 8\sqrt{6}(z - \sqrt{6}) = 0$",
        r"Distribuindo:",
        r"$12x + 24y + 8\sqrt{6}z = 96$",
        r"Simplificando:",
        r"$x + 2y + \frac{2\sqrt{6}}{3}z = 8$"
    ]

    # Adicionar os blocos de texto com espaçamento vertical ajustado
    y_position = 0.95
    font_size = 8
    for block in text_blocks:
        ax.text(0.05, y_position, block, ha='left', va='top', fontsize=font_size)
        y_position -= 0.05

# --- Criação das figuras ---
fig_latex = Figure(figsize=(6, 6))
criar_texto_latex(fig_latex)

fig_3d = Figure(figsize=(6, 6))
criar_grafico_3d(fig_3d)

# --- Interface gráfica ---
frame_main = tk.Frame(root)
frame_main.pack(fill=tk.BOTH, expand=True)

# Frame para o texto à esquerda
frame_left = tk.Frame(frame_main)
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

canvas_latex = FigureCanvasTkAgg(fig_latex, master=frame_left)
canvas_latex.draw()
canvas_latex.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Frame para o gráfico à direita
frame_right = tk.Frame(frame_main)
frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

canvas_3d = FigureCanvasTkAgg(fig_3d, master=frame_right)
canvas_3d.draw()
canvas_3d.get_tk_widget().pack(fill=tk.BOTH, expand=True)

root.mainloop()
