import tkinter
import turtle


# canvas-ul are originea in stanga sus, turtle-ul are originea la misjloc


vert = []             # vectorul de puncte
viewPoint = (-1, -1)  # punctul din care porneste aria vizibila


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
tErr = turtle.RawTurtle(canvas)
tErr.color("red")
tErr.hideturtle()
tErr.speed(8)


def testOr(p, q, r):    # pozitia lui r fata de pq
	return q[0]*r[1] + p[0]*q[1] + p[1]*r[0] - q[0]*p[1] - r[0]*q[1] - r[1]*p[0]

def seIntersecteaza(A, B, C, D):
	AB = (B[0] - A[0], B[1] - A[1])
	CD = (D[0] - C[0], D[1] - C[1])

	if(testOr(A, B, C)*testOr(A, B, D) < 0 and testOr(C, D, A)*testOr(C, D, B) < 0):
		return True                                                                       # daca sunt in parti diferite
	else:
		return False                                                                      # daca sunt de aceeasi parte sau exista un punct pe dreapta



def onClick(ev):
	global state
	global vert
	if state == 1 and not completeDrawing:
		currentPoint = (ev.x - canvas.winfo_width()//2, canvas.winfo_height()//2 - ev.y)
		print("State 1: ", currentPoint)

		if len(vert) == 0:
			vert.append(currentPoint)
			t.penup()
			t.goto(currentPoint)
			t.pendown()
		else:
			ok = True;   # folosit pentru intersectii (Daca e True => poate sa adauge o noua muchie)
			
			for i in range(1, len(vert)):                                                       # verifica intersectia ultimului segment posibil adaugat cu celelalte muchii deja adaugate
				if seIntersecteaza(currentPoint, vert[-1], vert[i], vert[i-1]):
					ok = False
					print("Intersectie!!")

			if ok:
				t.goto(currentPoint)
				if len(vert) <= 2:
					vert.append(currentPoint)
				else:
					AB = (vert[-1][0] - vert[-2][0], vert[-1][1] - vert[-2][1])
					BC = (currentPoint[0] - vert[-1][0], currentPoint[1] - vert[-1][1])
					if AB[0]*BC[1] == AB[1]*BC[0]:                                              #verifica daca ulimele 3 puncte sunt coliniare
						vert.pop()
					vert.append(currentPoint)

			else:
				tErr.penup()
				tErr.goto(vert[-1])
				tErr.pendown()
				tErr.goto(currentPoint)
				tErr.penup()
				tErr.clear()
			


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
	#if completeDrawing:
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

	ok = True
	for i in range(1, len(vert)):                                                       # verifica intersectia ultimului segment posibil adaugat cu celelalte muchii deja adaugate
		if seIntersecteaza(vert[0], vert[-1], vert[i], vert[i-1]):
			ok = False
			print("Intersectie!!")

	if ok:
		t.goto(vert[0][0], vert[0][1])
		completeDrawing = True
		print(vert)
		state = 0
	else:
		tErr.penup()
		tErr.goto(vert[-1])
		tErr.pendown()
		tErr.goto(vert[0])
		tErr.penup()
		tErr.clear()

	

def comTriang():
	stateLabel.set("Poligonul este triangulat")
	global state
	state = 0

def comArie():
	stateLabel.set("Setati punct")
	global state
	state = 3



butDesen = tkinter.Button(frame, text = "Stergeti plansa", command = comDesen)
butDesen.pack(fill='x')
butIncheie = tkinter.Button(frame, text = "Incheiati desenul", command = comIncheie)
butIncheie.pack(fill='x')
butTriang = tkinter.Button(frame, text = "Triangulare", command = comTriang)
butTriang.pack(fill='x')
butArie = tkinter.Button(frame, text = "Arie vizibila (Setati un punct)", command = comArie)
butArie.pack(fill='x')





root.mainloop()