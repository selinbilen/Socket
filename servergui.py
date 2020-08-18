from tkinter import *
from math import *
from __main__ import *

main = Tk()
main.title('SERVER')

ct =[]

def save():
    h = host.get()
    p = port.get()
    q = quiz.get()
    ct.append(h)
    ct.append(p)
    ct.append(q)
    #print ct
    from server import server
    server()

"""
def server():
    from server import server
    server()
"""

main.geometry('350x300')
main.configure(bg='#33464b')
Label(main,bg='#33464b',font='Helvetica 18 bold', text = "SERVER INFORMATIONS").grid(row=0, column=1)
Label(main,bg='#33464b', text = "HOST:").grid(row=1, column=0)
Label(main, bg='#33464b',text = "PORT:").grid(row=3, column=0)
Label(main,bg='#33464b', text = "Quiz Name:").grid(row=5, column=0)

host = Entry(main)
port = Entry(main)
quiz = Entry(main)

host.grid(row=1, column=1)
port.grid(row=3, column=1)
quiz.grid(row=5, column=1)

Button(main, text='EXIT', command=main.destroy).grid(row=9, column=1)
Button(main,text='Run the Server', command=save).grid(row=7, column=1)
#Button(main,text='Run the Server', command=server).grid(row=8, column=1)

mainloop()
