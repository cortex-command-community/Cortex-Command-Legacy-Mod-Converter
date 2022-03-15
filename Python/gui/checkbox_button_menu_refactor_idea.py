import PySimpleGUI as sg

def find_sub_menu(widget, position):
    length = widget.index("end")+1
    for i in range(length):
        label = widget.entrycget(i, 'label')
        sub_menu = widget.nametowidget(widget.entrycget(i, 'menu'))
        if label == position[0]:
            if len(position) == 1:
                return sub_menu
            else:
                return find_sub_menu(sub_menu, position[1:])

def insert_menu_checkbutton(menu, position, indexes, labels):
    widget = menu.Widget
    sub_menu = find_sub_menu(widget, position)
    if sub_menu:
        for index, label in zip(indexes, labels):
            var = sg.tk.BooleanVar()
            sub_menu.insert_checkbutton(index, label=label, variable=var,
                command=lambda label=label, var=var: menu._MenuItemChosenCallback(f'{label} {var.get()}'))
    else:
        print("Postion not found !")

sg.theme("DarkBlue3")
sg.set_options(font=("Courier New", 20))

menu_def = [['&File', ['&Open', '&Save', '&Properties', 'E&xit']]]

layout = [
    [sg.Menu(menu_def, key='-MENU-')],
    [sg.Button("Add Checkbox in Menu")],
]
window = sg.Window('Title', layout, finalize=True)
variables = []
while True:

    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == "Add Checkbox in Menu":

        menu = window['-MENU-']

        position = ("File",)
        indexes = (0, 2, 4)
        labels = ("Confirmation", "Alarm", "Status")
        insert_menu_checkbutton(menu, position, indexes, labels)

    print(event, values)

window.close()