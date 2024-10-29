import matplotlib.pyplot as plt
import numpy as np

from Plot_Util import plot_resolution


def GT3():
    resolution = './imgs/GT3-t1.png'
    fig = solve_eq()
    plot_resolution(resolution, fig)

def solve_eq():
    x, y, z = 1.5, 6, 4.5  # valores hipotéticos para ilustrar o gráfico

    # Definição da função f(x, y, z)
    def f(x, y, z):
        return 4 * x ** 2 + y ** 2 + 5 * z ** 2

    # Valor da superfície de nível
    c = f(x, y, z)

    # Preparando a malha para a superfície de nível de f
    x_vals = np.linspace(0, 3, 100)
    y_vals = np.linspace(0, 9, 100)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = np.sqrt((c - 4 * X ** 2 - Y ** 2) / 5)

    # Configuração do plano de vínculo x + y + z = 12
    x_plane_vals = np.linspace(0, 5, 50)
    y_plane_vals = np.linspace(0, 10, 50)
    X_plane, Y_plane = np.meshgrid(x_plane_vals, y_plane_vals)
    Z_plane = 12 - X_plane - Y_plane

    # Gradiente de f no ponto crítico
    grad_f = np.array([8 * x, 2 * y, 10 * z])

    # Plotagem
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plotando a superfície de nível de f
    ax.plot_surface(X, Y, Z, color='cyan', alpha=0.5, rstride=10, cstride=10, edgecolor='none', label='Superfície de nível de f')

    # Plotando o plano do vínculo
    ax.plot_surface(X_plane, Y_plane, Z_plane, color='lightgreen', alpha=0.5, rstride=10, cstride=10, edgecolor='none', label='Plano do vínculo')

    # Ponto crítico
    ax.scatter(x, y, z, color='red', s=100, label="Ponto Crítico")

    # Gradiente de f como um vetor
    ax.quiver(x, y, z, grad_f[0], grad_f[1], grad_f[2], color='blue', length=2, normalize=True, label="Gradiente de f")

    # Labels e legenda
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend()

    plt.title("Resolução da t2 do GT3")

    return fig
