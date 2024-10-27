import PySimpleGUI as sg
import ctypes
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def plot_resolution(resolution, fig):
    # Abra um pop up maximizado dividido em duas partes iguais
    layout = [
        [sg.Image(resolution, key='canvas'), sg.Canvas(key='canvas2', expand_x=True, expand_y=True)],
    ]

    user32 = ctypes.windll.user32
    screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    window = sg.Window('Resolução GT3', layout, location=(0,0) ,finalize=True, auto_size_text=True, element_justification='center', size=(screen_width, screen_height), background_color='white')

    #Fundo de resolution seja branco
    window['canvas'].Widget.config(bg='white')

    # Exibe o gráfico interativo
    canvas_elem2 = window['canvas2']
    canvas2 = FigureCanvasTkAgg(fig, canvas_elem2.TKCanvas)
    canvas2.draw()
    canvas2.get_tk_widget().pack(fill='both', expand=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == '-CLOSE-':
            break

    window.close()

def plot3_resolution(resolution_p1, resolution_p2, resolution2, fig):
    # Abra um pop up maximizado dividido em duas partes iguais
    layout = [
        [sg.Image(resolution_p1, key='canvas', pad=(0,0)), sg.Image(resolution2, key='canvas2', pad=(0,0))],
        [sg.Image(resolution_p2, key='canvas3', pad=(90,0)), sg.Canvas(key='canvas4', expand_x=True, expand_y=True, pad=(0,0))]
    ]

    user32 = ctypes.windll.user32
    screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    window = sg.Window('Resolução GT3', layout, location=(0,0), finalize=True, auto_size_text=True, element_justification='center', size=(screen_width, screen_height), background_color='white')

    # Fundo de resolution seja branco
    window['canvas'].Widget.config(bg='white')
    window['canvas2'].Widget.config(bg='white')
    window['canvas3'].Widget.config(bg='white')


    # Exibe o gráfico interativo
    canvas_elem4 = window['canvas4']
    canvas4 = FigureCanvasTkAgg(fig, canvas_elem4.TKCanvas)
    canvas4.draw()
    canvas4.get_tk_widget().pack(fill='both', expand=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == '-CLOSE-':
            break

    window.close()