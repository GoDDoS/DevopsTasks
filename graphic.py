from db import *
from tkinter import *

root = Tk()
root.title("Personal anime list")
ii = 0
gg = 0
ttl = ""


def add():
    str = ('type', 'released_date', 'end_date', 'producer_name', 'rating', 'studio')
    quest = ('When did you see it?', 'Rate it!', 'Type the best character')
    array = {}
    info_array = {}

    def user_add(event):
        global gg
        question.delete(1.0, END)
        question.insert(END, quest[gg])
        question.grid(row=0, column=0)
        but.config(text="OK")
        text.delete(1.0, END)
        text.grid(row=0, column=1)
        but.grid(row=0, column=2)
        but.bind("<Button-1>", read_info)

    def read_info(event):
        global gg
        global ttl
        info_array[gg] = text.get(1.0, END)
        gg += 1
        if gg == 3:
            add_personal_list(ttl, info_array[1], info_array[0], info_array[2])
            return
        question.delete(1.0, END)
        string = quest[gg]
        question.insert(END, string)
        question.grid(row=0, column=0)
        text.delete(1.0, END)
        text.grid(row=0, column=1)
        but.grid(row=0, column=2)

    def output(event):
        global ttl
        ttl = text.get("1.0", END)
        if check_anime_in_DB(ttl) == 0:
            string = "Sorry, we can't find the anime in the DB.\n"
            string += "Please, give us info about it"
            question.insert(END, string)
            question.grid(row=0, column=0)
            but.config(text="OK")
            but.grid(row=0, column=1)
            but.bind("<Button-1>", questions)
        else:
            user_add(event)

    def questions(event):
        global ii
        question.delete(1.0, END)
        string = 'Type '
        string += str[ii]
        string += " of the anime (type '-' if you don't know)"
        question.insert(END, string)
        question.grid(row=0, column=0)
        text.delete(1.0, END)
        text.grid(row=0, column=1)
        but.grid(row=0, column=2)
        but.bind("<Button-1>", read)

    def read(event):
        global ii
        global ttl
        array[ii] = text.get(1.0, END)
        if array[ii] == '-':
            array[ii] = 'DEFAULT'
        ii += 1
        # print(ii)
        if ii == 6:
            add_anime(ttl, array[0], array[1], array[2], array[3], array[4], array[5])
            user_add()
            return
        question.delete(1.0, END)
        string = 'Type '
        string += str[ii]
        string += " of the anime (type '-' if you don't know)"
        question.insert(END, string)
        question.grid(row=0, column=0)
        text.delete(1.0, END)
        text.grid(row=0, column=1)
        but.grid(row=0, column=2)

    # fra.config(bg="Red")
    text = Text(fra, width=45, height=10, wrap=WORD)
    but = Button(fra, width=45, height=10, text="Find it!")
    question = Text(fra, width=45, height=10, wrap=WORD)
    text.grid(row=0, column=0)
    but.grid(row=0, column=1)
    but.bind("<Button-1>", output)


def print_table(anm):
    text = []
    for i, token in enumerate(anm):
        text.append([0] * len(token))
        for j, word in enumerate(token):
            text[i][j] = Text(fra, wrap=WORD, width=10, height=2.5)
            text[i][j].insert(END, anm[i][j])
            text[i][j].grid(row=i, column=j)


def find_by_title():
    def find_title(event):
        but.grid_remove()
        s = text.get(1.0, END)
        text.grid_remove()
        print_table(find_anime_by_title(s))
    text = Text(fra, width=45, height=10, wrap=WORD)
    but = Button(fra, width=45, height=10, text="Search!")
    text.grid(row=0, column=0)
    but.grid(row=0, column=1)
    but.bind("<Button-1>", find_title)


def find_by_tag():
    def find_tag(event):
        but.grid_remove()
        s = text.get(1.0, END)
        text.grid_remove()
        print_table(find_anime_by_tag(s))
    text = Text(fra, width=45, height=10, wrap=WORD)
    but = Button(fra, width=45, height=10, text="Search!")
    text.grid(row=0, column=0)
    but.grid(row=0, column=1)
    but.bind("<Button-1>", find_tag)


def top():
    def show_top(event):
        but.grid_remove()
        print_table(top_anime())
    but = Button(fra, width=45, height=10, text="Show!")
    but.grid(row=0, column=1)
    but.bind("<Button-1>", show_top)


def find_by_name():
    def find_name(event):
        but.grid_remove()
        s = text.get(1.0, END)
        text.grid_remove()
        print_table(find_ch_by_name(s))
    text = Text(fra, width=45, height=10, wrap=WORD)
    but = Button(fra, width=45, height=10, text="Search!")
    text.grid(row=0, column=0)
    but.grid(row=0, column=1)
    but.bind("<Button-1>", find_name)


def inf_seiyuu():
    def find_seiyuu(event):
        but.grid_remove()
        s = text.get(1.0, END)
        text.grid_remove()
        print_table(inf_by_seiyuu(s))
    text = Text(fra, width=45, height=10, wrap=WORD)
    but = Button(fra, width=45, height=10, text="Search!")
    text.grid(row=0, column=0)
    but.grid(row=0, column=1)
    but.bind("<Button-1>", find_seiyuu)


def personal_list():
    def show_list(event):
        but.grid_remove()
        print_table(my_list())
    but = Button(fra, width=45, height=10, text="Show!")
    but.grid(row=0, column=1)
    but.bind("<Button-1>", show_list)

fra = Frame(root, width=700, height=500, bg="Black")
fra.pack()

m = Menu(root)
root.config(menu=m)

cm = Menu(m)
dm = Menu(cm)
em = Menu(dm)
m.add_cascade(label="Choose option", menu=cm)
cm.add_command(label="Add anime to your list", command=add)
cm.add_cascade(label="Find...", menu=dm)
dm.add_cascade(label="anime by...", menu=em)
em.add_command(label="title", command=find_by_title)
em.add_command(label="tag", command=find_by_tag)
dm.add_command(label="character", command=find_by_name)
dm.add_command(label="seiyuu", command=inf_seiyuu)
#dm.add_command(label="producer", command=find_producer)
cm.add_command(label="Show top", command=top)
cm.add_command(label="Show my list", command=personal_list)
cm.add_command(label="Clear my list", command=clear_list)
#cm.add_command(label="Show tags", command=tags)


root.mainloop()
