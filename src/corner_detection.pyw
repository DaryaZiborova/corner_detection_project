import cornerslib as cl
import PIL
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import ttk
import os

methods = ["Shi-Tomasi", "Moravec", "SUSAN", "Harris","FAST"]
functions = [cl.shi_tomasi_corner, cl.moravec_corner, cl.susan_corner, cl.harris_corner, cl.FAST_corner]
def showDetectedCorners():
    reviewLb['text'] = ''

    if combobox.get() in methods and os.path.exists(pathLb['text']):
        output = functions[methods.index(combobox.get())](pathLb['text'])
        str = '''        Время выполнения: {} сек
        Найденные ключевые точки: {}
        Предел: {}
        Окружение: '''.format(output[4], output[1],output[3])

        if methods.index(combobox.get()) == 1:
            str += output[2]+' прилежащих пикселя'

        elif methods.index(combobox.get()) == 2:
            str += 'пиксели в радиусе '+output[2]+'px'

        else:
            str += output[2]+'x'+output[2]+' пикселей'
        reviewLb['text'] = str

        plt.figure("Detected corners")
        plt.imshow(output[0]), plt.show()

def browse():
    try:
        image = tk.filedialog.askopenfilename()

        pathLb['text'] = image
        pathLb['foreground'] = 'black'
    except FileNotFoundError:
        pass
    except PIL.UnidentifiedImageError:
        pass

def fill_the_table():
    table = tk.Toplevel(root)
    table.geometry('1000x350')
    table.transient(root)
    table.title('review')

    headings = ['Метод', 'Кол-во найденных точек', 'Окружение', 'Предел', 'Время выполнения, сек']
    columns = ['method', 'points', 'neighborhood', 'threshold', 'runtime']

    reviewTbl = ttk.Treeview(table, columns=columns, show="headings")
    reviewTbl.pack(fill='both', expand=1)

    for i in range(0, 5):
        reviewTbl.heading(i, text=headings[i])

    output = []
    for i in range(0, 5):
        output.append(list(functions[i](pathLb['text'])))
        output[i][0] = methods[i]
        if i == 1:
            output[i][2] = output[i][2]+' прилежащих пикселя'
        elif i == 2:
            output[i][2] = 'пиксели в радиусе '+output[i][2]+'px'
        else:
            output[i][2] = output[i][2]+'x'+output[i][2]+' пикселей'
        output[i] = tuple(output[i])

    for method in output:
        reviewTbl.insert("", 'end', values=method)


def showReview():
    if os.path.exists(pathLb['text']):
        fill_the_table()


root = tk.Tk()
root.geometry('500x350')
root.title("Corner detection")

combobox = ttk.Combobox(values=methods, state='readonly')
combobox.pack(anchor='center', pady=160)
combobox.set("Выберите метод")

pathLb = tk.Label(text='Ваш путь',background='lightgrey',anchor='w',foreground='grey')
pathLb.place(rely=0.3,relx=0.4,relheight=0.07,relwidth=0.5)

browseBtn = tk.Button(text='Выбрать изображение',command=browse,background='white',relief='groove')
browseBtn.place(rely=0.3,relx=0.1,relheight=0.07,relwidth=0.27)

reviewLb = tk.Label(justify='left')
reviewLb.place(rely=0.75, relx=0.15, relwidth=0.7)

findCornersBtn = tk.Button(text='Обнаружить углы',command=showDetectedCorners,background='white',relief='groove')
findCornersBtn.place(rely=0.6,relx=0.35,relwidth=0.3,relheight=0.1)

reviewBtn = tk.Button(text='Показать отчет для выбранного изображения',command=showReview,background='white',relief='groove')
reviewBtn.place(rely=0.05,relx=0.41,relheight=0.07,relwidth=0.55)

root.mainloop()
