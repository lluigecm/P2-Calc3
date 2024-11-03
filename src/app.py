import PySimpleGUI as sg
from PIL import Image
import ctypes

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

        self.window = sg.Window('Resolução Prova 2', self.layout, size=(500, 150), element_justification='center')

        self.run()

    def update_layout(self, window : sg.Window, gt : str):

        if gt == 'GT1':
            for key in ['-INPUT1-', '-INPUT2-']:
                if key in window.AllKeysDict:
                    window[key].ParentRowFrame.pack_forget()
                    del window.AllKeysDict[key]

            # Add new input fields
            input_layout = [
                [sg.Text('h(x,y):          '), sg.Input(key='-INPUT1-')],
                [sg.Text('Ponto Q(x,y):'), sg.Input(key='-INPUT2-')]
            ]

            window.extend_layout(window['-ACT-'], input_layout)
            window['-ACT-'].update('')
            window['-CALC-'].update(visible=True)
        elif gt == 'GT2':
            for key in ['-INPUT1-', '-INPUT2-', '-INPUT3-']:
                if key in window.AllKeysDict:
                    window[key].ParentRowFrame.pack_forget()
                    del window.AllKeysDict[key]

            # Add new input fields
            input_layout = [
                [sg.Text('Função da Superfície: '), sg.Input(key='-INPUT1-')],
                [sg.Text('Ponto M(x,y,z):          '), sg.Input(key='-INPUT2-')]
            ]

            window.extend_layout(window['-ACT-'], input_layout)
            window['-ACT-'].update('')
            window['-CALC-'].update(visible=True)
        else:
            for key in ['-INPUT1-', '-INPUT2-']:
                if key in window.AllKeysDict:
                    window[key].ParentRowFrame.pack_forget()
                    del window.AllKeysDict[key]

            # Add new input fields
            input_layout = [
                [sg.Text('f(x,y,z) =   '), sg.Input(key='-INPUT1-')],
                [sg.Text('Vinculo:    '), sg.Input(key='-INPUT2-')]
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
                self.selected_gt = 'GT2'
                self.update_layout(self.window, 'GT2')

            if event == '-GT3-':
                self.selected_gt = 'GT3'
                self.update_layout(self.window, 'GT3')

            if event == '-CALC-':
                if self.selected_gt == 'GT1':
                    gt1 = GT1(values['-INPUT1-'], list(values['-INPUT2-'].split(',')))
                if self.selected_gt == 'GT2':
                    gt2 = GT2(values['-INPUT1-'], list(values['-INPUT2-'].split(',')))
                if self.selected_gt == 'GT3':
                    gt3 = GT3(values['-INPUT1-'], list(values['-INPUT2-'].split(',')))

        self.window.close()