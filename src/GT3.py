import re
import numpy as np
import sympy as sp
from matplotlib import pyplot as plt

from src.Plot_Util import plot_resolution


class GT3():

    def __init__(self, function, constraint):
        x, y, z, λ= sp.symbols('x y z λ')

        self.function = sp.sympify(re.sub('\^','**',function))
        self.constraint = sp.sympify(constraint)

        self.extremes = self.lagrange_extremes(self.function, self.constraint)

        self.plot = self.solve_eq(self.function, self.constraint)

        self.solution_latex = (f'Extremos da função: $({sp.sympify(self.extremes[0][x])}, {sp.sympify(self.extremes[0][y])}, {sp.sympify(self.extremes[0][z])})$')

        plot_resolution(self.solution_latex, self.plot)

    def lagrange_extremes(self, func, constraint):
        x, y, z, λ = sp.symbols('x y z λ')

        f = func

        g = constraint

        grad_f = [sp.diff(f, var) for var in (x, y, z)]
        grad_g = [sp.diff(g, var) for var in (x, y, z)]

        # Sistema de equações dos multiplicadores de Lagrange
        equations = [
                        grad_f[i] - λ * grad_g[i] for i in range(3)
                    ] + [g]  # Inclui o vínculo g = 0

        # Resolvendo o sistema de equações
        solutions = sp.solve(equations, (x, y, z, λ), dict=True)

        return solutions

    def solve_eq(self, func, constraint):
        x, y, z, λ = sp.symbols('x y z λ')

        # Gradiente da função f
        grad_f = [sp.diff(func, var) for var in (x, y, z)]

        # Gradiente da função g
        grad_g = [sp.diff(constraint, var) for var in (x, y, z)]

        # Sistema de equações dos multiplicadores de Lagrange
        equations = [
                        grad_f[i] - λ * grad_g[i] for i in range(3)
                    ] + [constraint]

        # Resolvendo o sistema de equações
        solutions = sp.solve(equations, (x, y, z, λ), dict=True)

        # Obtendo o primeiro ponto crítico (x, y, z)
        if solutions:
            px, py, pz = solutions[0][x], solutions[0][y], solutions[0][z]
            point = (float(px), float(py), float(pz))
        else:
            print("Nenhuma solução encontrada.")
            return

        # Passo 2: Representação Gráfica

        # Convertendo para funções numéricas
        f_lambdified = sp.lambdify((x, y, z), func, 'numpy')
        g_lambdified = sp.lambdify((x, y, z), constraint, 'numpy')

        # Definindo a região de plotagem
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Ponto extremo obtido
        ax.scatter(point[0], point[1], point[2], color='red', s=50, label='Ponto extremo')

        # Superfície do vínculo
        X, Y = np.linspace(point[0] - 5, point[0] + 5, 50), np.linspace(point[1] - 5, point[1] + 5, 50)
        X, Y = np.meshgrid(X, Y)
        Z = g_lambdified(X, Y, np.zeros_like(X))  # Usando a função lambdificada para calcular Z
        ax.plot_surface(X, Y, Z, alpha=0.5, color='cyan', label='Vínculo')

        # Superfície de nível de f
        level_value = f_lambdified(point[0], point[1], point[2])
        Z_f = (level_value - f_lambdified(X, Y, np.zeros_like(X))) / 5  # Reescrevendo f em função de Z
        ax.plot_surface(X, Y, Z_f, alpha=0.3, color='orange', label='Nível de f')

        # Gradiente de f no ponto
        grad_f_at_point = np.array(
            [sp.diff(func, var).subs({x: point[0], y: point[1], z: point[2]}) for var in (x, y, z)], dtype=float)
        ax.quiver(point[0], point[1], point[2], *grad_f_at_point, color='purple', length=0.35, label='Gradiente de f')

        # Configurações do gráfico
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.legend()
        ax.set_title('Multiplicadores de Lagrange')

        return fig