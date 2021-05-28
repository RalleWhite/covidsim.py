import tkinter as tk
import tkinter.ttk as ttk
import time
import random
import matplotlib.pyplot as plt
n = 100

class Person(object):
    # Constructor: skaber ny agent
    def __init__(self, canvas, x, y, fill):
        # Parametre for cirklen der skal tegnes
        r = 4 
        x0 = x-r
        y0 = y-r
        x1 = x+r
        y1 = y+r

        # Definere agenternes attributer
        self.x = x
        self.y = y
        self.infected = False

        self.canvas = canvas
        self.id = canvas.create_oval(x0,y0,x1,y1, fill=fill, outline='')


    def move(self):
        x1, y1, x2, y2 = self.canvas.bbox(self.id)
        dx = random.choice([-5, 5])
        dy = random.choice([-5, 5])


        self.canvas.move(self.id, dx, dy)
        self.x = self.x + dx
        self.y = self.y + dy


    def check_infected(self, persons):
        for person in persons:
            d = ((self.x - person.x)**2 + (self.y - person.y)**2)**(1/2)
            if d < 10 and person.infected == True:
                self.infect()
    # Smitte funktion
    def infect(self):
        self.infected = True # Sætter attribut til smittet
        self.canvas.itemconfig(self.id, fill='red2') # Sætter farve attributen til rød

class App(object):
    def __init__(self, master, **kwargs):

        # Laver interfacet hvor agenterne er
        self.master = master
        self.canvas = tk.Canvas(self.master, width=800, height=800,background='gray12')
        self.canvas.pack()

        # Genstart knap
        self.but_reset = ttk.Button(master, text = "Reset", command=self.init_sim)
        self.but_reset.pack(side=tk.BOTTOM)

        # Knap til at vise graf
        self.but_graph = ttk.Button(master, text = "Show Graph", command=self.plot)
        self.but_graph.pack(side=tk.BOTTOM)

        # Starter simulationen
        self.init_sim()

        self.smittede = []

        self.master.after(0, self.update)
        self.frame=0

    def update(self):

        # Kører funktionerne der opdatere agenternes placering og status
        for person in self.persons:
            person.move()
            person.check_infected(self.persons)

        # Tæller antal smittede i konsol
        ni = 0
        for p in self.persons:
            if p.infected:
                ni += 1
        print("Number of infected persons:", ni)
        self.smittede.append(ni)



        self.master.after(75, self.update) # hvert 75. millisekund køre den update frame koden
        self.frame += 1 # tilføjer næste frame


    # (gen)Starter simulationen (fjerner alle agenter og skaber nye)
    def init_sim(self):
        self.canvas.delete('all')
        self.persons = []

        for i in range(n):
            x = random.randint(0,800) # Placerer hver agent på tilfældigt x koordinat
            y = random.randint(0,800) # Placerer hver agent på tilfældigt y koordinat
            p = Person(self.canvas, x, y, 'spring green') # Sætter farven på de raske (nye agenter)
            if random.uniform(0,1) < 0.05: # Fra start af er 5% smittede
                p.infect()

            self.persons.append(p)

        self.canvas.pack()

    # Skaber en graf med antal smittede
    def plot(self):
        plt.plot(self.smittede)
        plt.show()

# Create the Tkinter application and run it
root = tk.Tk()
app = App(root)
start=time.time()
root.mainloop()
end=time.time()
print("Frames:",app.frame)
print("Runtime:",end-start)
print("Framerate:", app.frame/(end-start))
