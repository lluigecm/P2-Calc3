import PySimpleGUI as sg

from src.GT1 import GT1
from src.GT2 import GT2
from src.GT3 import GT3

sg.theme('DarkBlue3')

class App:

    def __init__(self):

        self.layout = [
            [sg.Text('Selecione uma tarefa abaixo:', size=(25, 1), justification='center')],
            [sg.Button('GT1', key='-GT1-'), sg.Button('GT2', key='-GT2-'), sg.Button('GT3', key='-GT3-')],
            [sg.Text('', key='-ACT-')],
            [sg.Button('Calcular', key='-CALC-', visible=False, )]
        ]

        self.window = sg.Window('Resolução Prova 2', self.layout, size=(500, 175), element_justification='center')

        self.run()

    def update_layout(self, window : sg.Window, gt : str):

        if gt == 'GT1':
            for key in ['-INPUT1-', '-INPUT2-', '-TITLE-']:
                if key in window.AllKeysDict:
                    window[key].ParentRowFrame.pack_forget()
                    del window.AllKeysDict[key]

            # Add new input fields
            input_layout = [
                [sg.Text('Gradiente e Derivadas Direcionais:', justification='center', key='-TITLE-')],
                [sg.Text('h(x,y):          '), sg.Input(key='-INPUT1-')],
                [sg.Text('Ponto Q(x,y):'), sg.Input(key='-INPUT2-')]
            ]

            window.extend_layout(window['-ACT-'], input_layout)
            window['-ACT-'].update('')
            window['-CALC-'].update(visible=True)
        elif gt == 'GT3':
            for key in ['-INPUT1-', '-INPUT2-', '-TITLE-']:
                if key in window.AllKeysDict:
                    window[key].ParentRowFrame.pack_forget()
                    del window.AllKeysDict[key]

            # Add new input fields
            input_layout = [
                [sg.Text('Multiplicadores de Lagrange:', justification='center', key='-TITLE-')],
                [sg.Text('f(x,y,z) =   '), sg.Input(key='-INPUT1-')],
                [sg.Text('Vinculo = 0:    '), sg.Input(key='-INPUT2-')]
            ]

            window.extend_layout(window['-ACT-'], input_layout)
            window['-ACT-'].update('')
            window['-CALC-'].update(visible=True)

    def run(self):
        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED:
                break

            if event == '-GT1-':
                self.selected_gt = 'GT1'
                self.update_layout(self.window, 'GT1')

            if event == '-GT2-':
                GT2().run()

            if event == '-GT3-':
                self.selected_gt = 'GT3'
                self.update_layout(self.window, 'GT3')

            if event == '-CALC-':
                if self.selected_gt == 'GT1':
                    gt1 = GT1(values['-INPUT1-'], list(values['-INPUT2-'].split(',')))
                if self.selected_gt == 'GT3':
                    gt3 = GT3(values['-INPUT1-'], values['-INPUT2-'])

        self.window.close()