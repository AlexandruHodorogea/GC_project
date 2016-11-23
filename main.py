import tkinter
import turtle


root = tkinter.Tk()

state = 1
completeDrawing = False

stateLabel = tkinter.StringVar()
stateLabel.set("Desenati poligonul (Click)")

frame = tkinter.Frame(bg = "white")
tkinter.Label(frame, textvariable=stateLabel, bg='grey', fg='white').pack(fill='x')


canvas = tkinter.Canvas(frame, width=500, height=500)
canvas.pack()

frame.pack(fill='both', expand=True)



t = turtle.RawTurtle(canvas)
t.speed(6)
t.hideturtle()
tPV = turtle.RawTurtle(canvas)
tPV.color("#468499")    # #B5CDD6 suprafata vizibila
tPV.hideturtle()
tPV.speed(10)

vert = []
viewPoint = (-1, -1)


def onClick(ev):
	global state
	global vert
	if state == 1 and not completeDrawing:
		print("State 1: ", ev.x, ev.y)

		if len(vert) == 0:
			t.penup()
			t.goto(ev.x - canvas.winfo_width()//2, canvas.winfo_height()//2 - ev.y)
			t.pendown()
		else:
			t.goto(ev.x - canvas.winfo_width()//2, canvas.winfo_height()//2 - ev.y)

		if len(vert) <= 2:
			vert.append((ev.x, ev.y))
		else:
			AB = (vert[-1][0] - vert[-2][0], vert[-1][0] - vert[-2][0])
			BC = (ev.x - vert[-1][0], ev.y - vert[-1][0])
			if AB[0]*BC[1] != AB[1]*BC[0]:
				vert.append((ev.x, ev.y))


	if state == 3:
		tPV.clear()
		tPV.penup()
		tPV.goto(ev.x - canvas.winfo_width()//2 - 1, canvas.winfo_height()//2 - ev.y - 1)
		tPV.pendown()
		tPV.begin_fill()
		tPV.circle(2)
		tPV.end_fill()
		tPV.penup()



canvas.bind("<Button>", onClick)


def comDesen():
	stateLabel.set("Desenati poligonul (Click)")
	global state
	global completeDrawing
	state = 1
	if completeDrawing:
		answer = tkinter.messagebox.askquestion("Vechiul desen va fi sters", "Doriti sa stergeti desenul actual?")
		if answer == "yes":
			vert[:] = []
			t.clear()
			tPV.clear()
			viewPoint = (-1, -1)
			completeDrawing = False

def comIncheie():
	global state
	global vert
	global completeDrawing
	t.goto(vert[0][0] - canvas.winfo_width()//2, canvas.winfo_height()//2 - vert[0][1])
	completeDrawing = True
	print(vert)
	state = 0

def comTriang():
	stateLabel.set("Poligonul este triangulat")
	global state
	state = 0

def comArie():
	stateLabel.set("Setati punct")
	global state
	state = 3



butDesen = tkinter.Button(frame, text = "Desenati", command = comDesen)
butDesen.pack(fill='x')
butIncheie = tkinter.Button(frame, text = "Incheiati desenul", command = comIncheie)
butIncheie.pack(fill='x')
butTriang = tkinter.Button(frame, text = "Triangulare", command = comTriang)
butTriang.pack(fill='x')
butArie = tkinter.Button(frame, text = "Arie vizibila (Setati un punct)", command = comArie)
butArie.pack(fill='x')





root.mainloop()