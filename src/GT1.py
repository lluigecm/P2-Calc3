from cProfile import label
from math import sqrt
from re import sub

import numpy as np
import sympy as sp
from matplotlib import pyplot as plt
from sympy import lambdify, symbols, diff, sympify

from src.Plot_Util import plot_resolution


class GT1():

    def __init__(self, function, point):
        self.function = sub(r'\^', '**', function)
        self.point = list(map(float, point))

        self.gradients = self.calc_gradient( self.function, point)
        self.duf = self.calc_duf(self.point, self.gradients)
        self.graph = self.solve(self.function, self.point)
        self.max_rate = sqrt(self.gradients[1][0] ** 2 + self.gradients[1][1] ** 2)

        self.solution_latex = (f'$D_u$f({self.point[0]}, {self.point[1]}) = ${self.duf:.3f}$\n'
                               f'Cresce mais rapidamente em direção de ({self.gradients[1][0]:.3f}, {self.gradients[1][1]:.3f})\n'
                               f'Taxa máxima de crescimento: {self.max_rate:.3f}')

        plot_resolution(self.solution_latex, self.graph)

    def calc_gradient(self, function, point):
        x, y = sp.symbols('x y')
        f = sp.sympify(function)

        gradient = [f.diff(x), f.diff(y)]
        gradient_on_point = [gradient[0].subs(x, point[0]).subs(y, point[1]), gradient[1].subs(x, point[0]).subs(y, point[1])]

        return gradient, gradient_on_point

    def calc_duf(self, point, gradients):
        uni = self.verify_vector_unit(point)
        gradient = gradients[1]

        duf = gradient[0] * uni[1] + gradient[1] * uni[0]

        return duf

    def verify_vector_unit(self, vector):
        magnitude = sqrt(sum([component ** 2 for component in vector]))

        if magnitude != 1:
            vector = [component / magnitude for component in vector]

        return vector

    # In src/GT1.py
    def solve(self, function, point):
        # Definindo as variáveis simbólicas
        x, y = symbols('x y')

        # Convertendo a função de string para expressão simbólica
        h = sympify(function)

        # Calculando o gradiente de h em relação a x e y
        grad_h_x = diff(h, x)
        grad_h_y = diff(h, y)
        gradiente_h = [grad_h_x, grad_h_y]

        # Avaliando o gradiente no ponto Q
        Qx, Qy = point
        gradiente_h_Q = [g.evalf(subs={x: Qx, y: Qy}) for g in gradiente_h]

        # Convertendo h(x, y) em uma função utilizável para o gráfico
        h_func = lambdify((x, y), h, 'numpy')

        # Gerando o espaço de valores para x e y para o gráfico
        x_vals = np.linspace(-2, 2, 100)
        y_vals = np.linspace(-2, 2, 100)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = h_func(X, Y)

        # Plotando o gráfico 3D de h(x, y)
        fig = plt.figure(figsize=(15, 10))  # Increase the figure size
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7, label='h(x, y)')

        # Gradiente de h em Q
        ax.quiver(Qx, Qy, h_func(Qx, Qy), gradiente_h_Q[0], gradiente_h_Q[1], 0, color='r',length = 0.25, label='∇h(Q)')

        # Ponto Q
        ax.scatter(Qx, Qy, h_func(Qx, Qy), color='r', s=100, label='Ponto Q')

        #Gradiente de h em (Q, h(Q))
        ax.quiver(Qx, Qy, h_func(Qx, Qy), gradiente_h_Q[0], gradiente_h_Q[1], h_func(Qx, Qy),length = 0.25, color='b', label='∇h(Q, h(Q))')

        # Configurações do gráfico
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('h(x, y)')
        ax.set_title('Gráfico da função h(x, y) e gradiente em Q')
        ax.legend()

        return fig