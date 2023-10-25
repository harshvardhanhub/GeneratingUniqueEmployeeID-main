from tkinter import *
from tkcalendar import DateEntry
from  datetime import date
from pymysql import *
def genempid(nm,jd,dept):
    empid=list(jd.split("-"))[-1]
    cur.execute("select dept_ID,sub_dept_ID from sub_departments where sub_dept_name='"+dept+"';")
    ans=cur.fetchall()
    for i in ans:
        for j in i:
            empid+=str(j)
    cur.execute("select count(*) from Employees where dept_id=(select dept_Id from sub_departments where Sub_Dept_Name='"+dept+"');")
    for i in cur.fetchall():
        for j in i:
            dt=str(j+1)
    jd="-".join(list(jd.split("-"))[::-1])
    empid+="".join(["0" for i in range(3-len(dt))])+str(dt)
    if mimeType.get()=='1':
        empid+="E"
    else:
        empid+="M"
    cur.execute("select count(*) from Employees;")
    for i in cur.fetchall():
        for j in i:
            tot=str(j+1)
    empid+="".join(["0" for i in range(4-len(tot))])+str(tot)
    l6=Label(top,text=empid,relief=RAISED,font=('Helvetica',20),fg="darkblue",bg="white",bd=0).place(x=330,y=400)
    cur.execute("insert into Employees(ID,Name,Joining_Date,Dept_Id,sub_dept_id) values('"+empid+"','"+nm+"','"+jd+"','"+empid[4:6]+"','"+empid[6:7]+"');")
    conn.commit()
def submit():
    name=name_var.get()
    join_date=cal_var.get()
    dept=clicked.get()
    genempid(name,join_date,dept)

conn=connect(host="localhost",user="root",database="GenEmpID",password="root")
cur=conn.cursor()
top=Tk()
top.title("EmpIDGen")
title=Label(top,text="GENERATING UNIQUE EMPLOYEE ID",relief=RAISED,font=('Helvetica', 30, 'bold'),fg="red",bd=0,bg="yellow")
title.pack()
top.geometry("900x500")
l1=Label(top,text="Enter Your Name:",relief=RAISED,font=('Helvetica',20),fg="black",bg="yellow",bd=0).place(x=20,y=70)
top.configure(bg='yellow')
name_var=StringVar()
cal_var=StringVar()
dept_var=StringVar()
mimeType=StringVar()
nm=Entry(top,textvariable = name_var, font=('calibre',10,'normal')).place(x=250,y=80)
l2=Label(top,text="Enter Joining Date:",relief=RAISED,font=('Helvetica',20),fg="black",bg="yellow",bd=0).place(x=20,y=120)
cal = DateEntry(top, width= 16, background= "magenta3", foreground= "white",bd=2,textvariable = cal_var,date_pattern="dd-mm-yyyy").place(x=270,y=130)
l3=Label(top,text="Select Department:",relief=RAISED,font=('Helvetica',20),fg="black",bg="yellow",bd=0).place(x=20,y=170)
cur.execute("select sub_dept_name from Sub_Departments;")
get_dept=cur.fetchall()
options=[]
for i in get_dept:
    for j in i:
        options.append(j)
clicked = StringVar()
clicked.set("Research and Development")
drop = OptionMenu( top , clicked , *options).place(x=270,y=170)
l4=Label(top,text="Choose a Post:",relief=RAISED,font=('Helvetica',20),fg="black",bg="yellow",bd=0).place(x=20,y=220)
values = {"Employee" : "1",
        "Manager" : "2"}
for (text, value) in values.items():
    Radiobutton(top, text = text,
        value = value,bg="lightgreen",variable=mimeType).place(x=220,y=220+(int(value)-1)*30)
l5=Label(top,text="Generated Employee ID=",relief=RAISED,font=('Helvetica',20),fg="black",bg="yellow",bd=0).place(x=20,y=400)

b=Button(top,text="Submit",command=submit,bg="red",bd=2).place(x=250,y=300)
top.mainloop()
