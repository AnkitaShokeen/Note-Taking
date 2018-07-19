from tkinter import *
import pymysql as pm
from tkinter import messagebox

root = Tk()
root.title('Note Taking App')
root.geometry('550x600')

try:
    con = pm.connect(host='localhost', database='Ankita', user='root', password='Ankita@123')
    cursor = con.cursor()
    query = 'create table note_taking(title varchar(10) primary key,notes varchar(10000))'
    cursor.execute(query)

    # defining functions

    def add_notes():
        top1 = Toplevel()
        top1.title('Add Notes')
        top1.geometry('500x500')

        l2L = Label(top1, text='Enter Title')
        l2L.grid(row=0, column=0)
        e2 = Entry(top1, width=30, font=('times', 15))
        e2.grid(row=1, column=0)

        l3 = Label(top1, text='NOTES:',font="none 15 bold")
        l3.grid(row=2, column=0)

        s2 = Scrollbar(top1)
        s2.grid(row=3, column=2, rowspan=6)
        List_Box3 = Text(top1, height=15, width=50, bg='yellow', yscrollcommand=s2.set)
        s2.config(command=List_Box3.yview)
        List_Box3.grid(row=3, column=0, columnspan=3)

        def add_backend():
            try:
                if len(e2.get()) != 0:
                    if (len(List_Box3.get("1.0", "end-1c")) == 0):
                        temp = messagebox.askokcancel("Empty Notes", "No content found in %s note" % (e2.get()))
                        if temp:
                            cursor.execute("insert into note_taking values (%s,%s) ", (e2.get(), List_Box3.get("1.0", END)))
                            con.commit()
                            e2.delete(0, 'end')
                            List_Box3.delete("1.0", END)
                            messagebox.showinfo("Notes added", "Your Note are added successfully")

                        else:
                            sol = messagebox.askyesno("Confirmation", "Do you want to add again?")
                            if sol:
                                add_notes()

                    else:
                        cursor.execute("insert into note_taking values (%s,%s) ", (e2.get(), List_Box3.get("1.0", END)))
                        con.commit()
                        e2.delete(0, 'end')
                        List_Box3.delete("1.0", END)
                        l4 = Label(top1, text='Notes added successfully')
                        l4.grid(row=4, column=0)
                else:
                    messagebox.showinfo("TITLE not found!",
                                        "Please write TITLE to add notes")
            except Exception as e:
                messagebox.showinfo("Existing Title", "Note with title %s already exists, choose another. " % (e2.get()))

        b4 = Button(top1, text='ADD',font="none 15 bold", width=10,highlightbackground='green', command=add_backend)
        b4.grid(row=5, column=0,pady=10,sticky=W,padx=20)

        b5 = Button(top1, text='Exit',font="none 15 bold", width=10,highlightbackground='green', command=top1.destroy)
        b5.grid(row=5, column=1,pady=10,sticky=W)


    def list_notes():
        query1 = 'select title from note_taking order by title asc'
        rows_count = cursor.execute(query1)
        List_Box2.config(state=NORMAL)
        List_Box1.config(state=NORMAL)
        List_Box2.delete("1.0", END)
        List_Box1.delete("1.0", END)

        if rows_count > 0:
            List_Box1.insert(END, "NOTES ARE AS FOLLOWS:")
            data1 = cursor.fetchall()
            for row in data1:
                List_Box2.insert(END, row[0] + '\n')

        else:
            messagebox.showinfo("Sorry", "There are no notes.")
        List_Box2.config(state=DISABLED)


    def update_notes():
        top2 = Toplevel()
        top2.title('Update Notes')
        top2.geometry('700x600')

        l5 = Label(top2, text='Enter Title:')
        l5.grid(row=0,column=0)
        e3 = Entry(top2, width=30, font=('times', 15))
        e3.grid(row=1, column=0)

        l6 = Label(top2, text='NOTES:',font="none 15 bold",highlightbackground='green')
        l6.grid(row=2, column=0)

        s3 = Scrollbar(top2)
        s3.grid(row=3, column=1, rowspan=6)
        List_Box4 = Text(top2, height=15, width=65, bg='yellow',yscrollcommand=s3.set)
        s3.configure(command=List_Box4.yview)
        List_Box4.grid(row=3, column=0,columnspan=2)

        def update_backend():
            rows_count = cursor.execute("UPDATE note_taking SET notes=%s where title=%s",
                                        (List_Box4.get("1.0", END), e3.get()))
            con.commit()

            if rows_count > 0:
                l7 = Label(top2, text='successfully updated', width=50)
                l7.grid(row=6, column=0)
            else:
                l7 = Label(top2, text='No notes found with name %s' % (e3.get()), width=50)
                l7.grid(row=6, column=0)

            List_Box4.delete("1.0", END)
            e3.delete(0, 'end')

        b8 = Button(top2, text='Save Changes',font="none 15 bold",highlightbackground='green', width=15, command=update_backend)
        b8.grid(row=4, column=0,pady=10)

        def show_notes():
            rows_count = cursor.execute("select notes from note_taking where title=%s", (e3.get()))
            if rows_count > 0:
                data1 = cursor.fetchall()
                for row in data1:
                    List_Box4.insert(END, row[0])
            else:
                l7 = Label(top2, text='There are no existing notes titled %s' % (e3.get()), width=50)
                l7.grid(row=6, column=0)

        b10 = Button(top2, text='Show existing notes',font="none 15 bold", highlightbackground='green',command=show_notes)
        b10.grid(row=4, column=1,pady=5)

        b9 = Button(top2, text='Exit', font="none 15 bold",highlightbackground='green', width=15, command=top2.destroy)
        b9.grid(row=5, column=0,padx=150,pady=3,sticky=W)


    def delete_notes():
        top3 = Toplevel()
        top3.geometry('500x500')
        l8 = Label(top3, text="Enter title for notes you want to delete?")
        l8.grid(row=0, column=0)
        e4 = Entry(top3, width=30, font=('times', 15))
        e4.grid(row=1, column=0)

        def delete_backend():
            result = messagebox.askokcancel("Confirm", "Are you sure you want to delete?")
            if result:
                rows_count = cursor.execute(" DELETE from note_taking where title=%s", (e4.get()))
                con.commit()
                if rows_count > 0:
                    messagebox.showinfo("DELETED", "Notes  %s are deleted." % (e4.get()))
                else:
                    if(len(e4.get()) != 0):
                        messagebox.showinfo("Please Check", "There are no notes having title %s" % (e4.get()))
                    else:
                        messagebox.showinfo("Sorry", "There is no content to delete.")

        def deleteall_backend():
            result = messagebox.askokcancel("Confirm", "Are you sure you want to delete all notes ?")
            if result:
                rows_count = cursor.execute("DELETE from note_taking")
                con.commit()
                if rows_count > 0:
                    messagebox.showinfo("Deleted", "All Notes are deleted successfully")
                else:
                    messagebox.showinfo("Check", "No notes found.")

        b9 = Button(top3, text='DELETE', font="none 15 bold",highlightbackground='green',width=17, command=delete_backend)
        b9.grid(row=2, column=0)

        b11 = Button(top3, text='DELETE All',font="none 15 bold",highlightbackground='green', width=17, bg='red', command=deleteall_backend)
        b11.grid(row=2, column=1)


    def search_notes():
        if(len(e1.get()) == 0):
            messagebox.showinfo("OOPS!!", "Nothing to search")
        else:
            rows_count = cursor.execute("SELECT * from note_taking where title=%s", (e1.get()))
            List_Box2.config(state=NORMAL)
            List_Box1.config(state=NORMAL)
            List_Box2.delete('1.0', END)
            List_Box1.delete('1.0', END)
            e1.delete(0, 'end')
            if rows_count > 0:
                rs = cursor.fetchall()
                for row in rs:
                    List_Box2.insert(END, row[1])
                    if (len(List_Box2.get("1.0", "end-1c")) == 1):
                        messagebox.showinfo("EMPTY", row[0] + " is empty.")
                    else:
                        List_Box1.insert(END, "NOTES TITLE: " + row[0])

            else:
                messagebox.showinfo("ERROR", 'no results found')
            List_Box2.config(state=DISABLED)


    # defining Buttons and Labels

    AddB = Button(root, text='Add New Note>>', width=20, bg='red', highlightbackground='purple', command=add_notes)
    AddB.grid(row=0, column=0, padx=20, pady=17, sticky=W, ipady=2)

    ListB = Button(root, text='List All Notes', width=20, bg='red',
                   highlightbackground='purple',command=list_notes)
    ListB.grid(row=0, column=0, pady=17, padx=250, sticky=W, columnspan=5, ipady=2)

    l1L = Label(root, text="Search Notes", font='Times 15 bold')
    l1L.grid(row=1, column=0, padx=20, pady=5, sticky=W)

    search_text = StringVar()
    e1 = Entry(root, textvariable=search_text, width=40)
    e1.grid(row=2, column=0, sticky=W, padx=20, ipady=2)

    SearchB = Button(root, text='Search', width=10, bg='red', highlightbackground='green',command=search_notes)
    SearchB.grid(row=2, column=0, sticky=W, padx=400)

    l2L = Label(root, text="--Notes--", font='Times 15 bold')
    l2L.grid(row=3, column=0, pady=6, sticky=W, padx=200)

    List_Box1 = Text(root, height=2, width=68, bg='yellow', state='disabled')
    List_Box1.grid(row=4, column=0, sticky=W, padx=8)


    sb = Scrollbar(root)
    sb.grid(row=5, column=0, rowspan=6,sticky=W,padx=520)
    List_Box2 = Text(root, height=16, width=70,state=DISABLED, bg='yellow',yscrollcommand=sb.set)
    sb.configure(command=List_Box2.yview)
    List_Box2.grid(row=5,padx=2, column=0,sticky=W)


    l3L = Label(root, text="Edit Notes:", font='Times 15 bold', bg='pink')
    l3L.grid(row=6, column=0, pady=14, sticky=W, padx=200)

    UpdateB = Button(root, text='Update Notes', width=20, bg='red', highlightbackground='pink',command=update_notes)
    UpdateB.grid(row=7, column=0, pady=2, padx=20, sticky=W, columnspan=5, ipady=2)

    DeleteB = Button(root, text='Delete Notes', width=20, bg='red', highlightbackground='pink',command=delete_notes)
    DeleteB.grid(row=7, column=0, pady=2, padx=250, sticky=W, columnspan=5, ipady=2)

    exitB = Button(root, text="Exit", font="none 15 bold", command=root.destroy)
    exitB.grid(row=8, column=0, pady=14, sticky=W, padx=210)

    root.mainloop()

except pm.DatabaseError as e:
    if con:
        con.rollback()
        print("problem", e)

finally:
    cursor.close()
    con.close()