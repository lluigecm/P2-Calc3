import PySimpleGUI as sg
from PIL import Image
import ctypes

sg.theme('DarkBlue3')

class App:

    def __init__(self):
        self.selected_gt = None  # Variável para armazenar o GT selecionado

        self.layout = [
            [sg.Text('Selecione o Gerador de Tarefas para visualizar a resolução:')],
            [sg.Button('GT1'), sg.Button('GT2'), sg.Button('GT3')],
            [sg.Image('', key='-IMG-')],
            [sg.Button('', key='-RESOLUCAO-', visible=False)]
        ]

        self.window = sg.Window('Resolução Prova 2', self.layout, size=(500, 100), element_justification='center')

    def update_image(self, image_path, gt):
        self.selected_gt = gt  # Atualiza o GT selecionado

        image = Image.open(image_path)
        width, height = image.size

        self.window['-IMG-'].update(image_path)

        user32 = ctypes.windll.user32
        screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

        new_x = (screen_width - width) // 2
        new_y = (screen_height - (height + 100)) // 2

        self.window.TKroot.geometry(f'{width}x{height + 100}+{new_x}+{new_y}')

        # Update the "Resolução" button text and make it visible
        self.window['-RESOLUCAO-'].update(text=f'Resolução {gt}', visible=True)

    def run(self):
        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED:
                break

            if event == 'GT1':
                self.update_image("imgs/gt1.png", 'GT1')

            if event == 'GT2':
                self.update_image("imgs/gt2.png", 'GT2')

            if event == 'GT3':
                self.update_image("imgs/gt3.png", 'GT3')

            if event == '-RESOLUCAO-':
                if self.selected_gt == 'GT1':
                    print('TO DO GT1')

                if self.selected_gt == 'GT2':
                    print('TO DO GT2')

                if self.selected_gt == 'GT3':
                    print('TO DO GT3')

        self.window.close()