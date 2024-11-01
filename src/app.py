import PySimpleGUI as sg
from PIL import Image
import ctypes

sg.theme('DarkBlue3')


class App:

    def __init__(self):
        self.selected_gt = None

        self.layout = [[]
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


    def run(self):
        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED:
                break

        self.window.close()