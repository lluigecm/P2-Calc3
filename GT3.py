import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

from Plot_Util import plot_resolution


def GT3():
    resolution = 'imgs/resolutionGT3.png'
    fig = solve_eq()
    plot_resolution(resolution, fig)

def solve_eq():
    x, y, z, lambd = sp.symbols('x y z lambda')

    f = 4 * x**2 + y**2 + 5 * z**2
    g = x + y + z - 12

    L = f - lambd * g

    # Derivadas parciais de L em relação a x, y, z, e lambda
    dL_dx = sp.diff(L, x)
    dL_dy = sp.diff(L, y)
    dL_dz = sp.diff(L, z)
    dL_dlambd = sp.diff(L, lambd)

    # Sistema de equações para resolver
    equations = [
        dL_dx,
        dL_dy,
        dL_dz,
        dL_dlambd
    ]

    # Solucionando o sistema
    solution = sp.solve(equations, (x, y, z, lambd))

    # Extraindo a solução
    x_val = solution[x]
    y_val = solution[y]
    z_val = solution[z]

    # Cálculo do valor da função f no ponto encontrado
    f_val = f.subs({x: x_val, y: y_val, z: z_val})

    x_num = float(x_val)
    y_num = float(y_val)
    z_num = float(z_val)
    f_num = float(f_val)

    # Cria o gráfico
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Plano de restrição: x + y + z = 12
    xx, yy = np.meshgrid(np.linspace(0, 10, 30), np.linspace(0, 10, 30))
    zz = 12 - xx - yy
    ax.plot_surface(xx, yy, zz, color='cyan', alpha=0.5, rstride=100, cstride=100, label = "Vinculo")

    # Superfície de nível de f: f(x, y, z) = f_num
    z_vals = np.linspace(0, 5, 100)
    x_vals = np.linspace(0, 5, 100)
    X, Z = np.meshgrid(x_vals, z_vals)
    Y = np.sqrt(np.maximum(f_num - 4 * X ** 2 - 5 * Z ** 2, 0))  # Ensure non-negative values for sqrt
    Y = np.real(Y)  # Remover valores imaginários
    ax.plot_surface(X, Y, Z, color='orange', alpha=0.3, label = "Superfície de nível de f")

    # Pontos de interesse
    ax.scatter(x_num, y_num, z_num, color='red', s=50, label="Ponto crítico (x, y, z)")
    ax.quiver(x_num, y_num, z_num, 8 * x_num, 2 * y_num, 10 * z_num, color='black', length=0.5, normalize=True,
              label="Gradiente de f")

    # Configurações de plotagem
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend()
    plt.title("Resolução da t2 do GT3")


    return fig
