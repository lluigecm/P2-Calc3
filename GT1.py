import matplotlib.pyplot as plt
import numpy as np

from Plot_Util import plot3_resolution


def GT1():
    resolution_p1= 'imgs/GT1-t1-p1.png'
    resolution_p2 = 'imgs/GT1-t1-p2.png'
    resolution2 = 'imgs/GT1-t2.png'
    fig = solve_eq()
    plot3_resolution(resolution_p1, resolution_p2, resolution2, fig)

def solve_eq():
    x_vals = np.linspace(-2, 2, 50)
    y_vals = np.linspace(-2, 2, 50)
    X, Y = np.meshgrid(x_vals, y_vals)

    # Calcular Z diretamente usando a expressão de h(x, y)
    Z = X ** 2 + (1 / 4) * Y ** 2 + 2

    # Ponto Q e cálculo de h(Q) diretamente
    Q_x, Q_y = 1, 2
    h_Q = Q_x ** 2 + (1 / 4) * Q_y ** 2 + 2

    # Calcular o gradiente de h no ponto Q = (1, 2)
    grad_Q_x = 2 * Q_x
    grad_Q_y = (1 / 2) * Q_y

    # Configuração do gráfico 3D
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.6, edgecolor='none', label= 'h(x, y)')

    # Plotar o ponto Q e o ponto (Q, h(Q))
    ax.scatter(Q_x, Q_y, h_Q, color='red', s=50, label='Ponto(Q, h(Q))')

    # Adicionar o vetor gradiente no ponto Q
    ax.quiver(Q_x, Q_y, h_Q, grad_Q_x, grad_Q_y, 0, color='blue', length=0.5, normalize=True,
              label='Gradiente de h em Q')

    # Configuração dos eixos e título
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title('Resolução da t3 do GT1')
    ax.legend()

    return fig