import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import subplots


def plot_resolution(resolution, fig):
    layout = [
        [sg.Canvas(key='canvas', expand_x=False, expand_y=False),
         sg.Canvas(key='canvas2', expand_x=True, expand_y=True)]
    ]

    font_size = max(15 - len(resolution) // 20, 13 )

    figura, ax = subplots()
    ax.text(0.5, 0.5, resolution, fontsize=font_size, ha='center', va='center')
    ax.axis('off')

    window = sg.Window(' Resoluçaõ GT1', layout, location=(0,0), finalize=True, auto_size_text=False, element_justification='center', size=(1200,800), background_color='white')  # Increase the window size

    #Conecta o canvasdo matplotlib com a janela
    canvas_elem = window['canvas']
    canvas = FigureCanvasTkAgg(figura, canvas_elem.TKCanvas)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=False)

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