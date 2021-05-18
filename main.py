import tkinter as tk
import tkinter.ttk as ttk
import time
import random
n = 100

class Person(object):
    # Constructor: creates a new person/agent
    def __init__(self, canvas, x, y, fill):
        # Calculate parameters for the oval/circle to be drawn
        r = 4 
        x0 = x-r
        y0 = y-r
        x1 = x+r
        y1 = y+r

        # Initialize the agents attributrs
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

    def check_cured(self, persons):
        for person in persons:
            c = ((self.x - person.x)**2 + (self.y - person.y)**2)**(1/2)
            if c < 10 and person.cured == True:
                self.cure()

    def infect(self):
        self.infected = True
        self.canvas.itemconfig(self.id, fill='red2')

    def doctor(self):
        self.cured = True
        self.immune = True
        self.canvas.itemconfig(self.id, fill='blue')


class App(object):
    def __init__(self, master, **kwargs):

        # Create the canvas on which the agents are drawn
        self.master = master
        self.canvas = tk.Canvas(self.master, width=800, height=800,background='gray12')
        self.canvas.pack()

        # Create a reset button for the simulation
        self.but_reset = ttk.Button(master, text = "Reset", command=self.init_sim)
        self.but_reset.pack(side=tk.BOTTOM)

        # Start / init the simulation
        self.init_sim()

        self.master.after(0, self.update)
        self.frame=0

    def update(self):

        # Update / move each agent
        for person in self.persons:
            person.move()
            person.check_infected(self.persons)

        # Count number of infected persons
        ni = 0
        for p in self.persons:
            if p.infected:
                ni += 1
        print("Number of infected persons:", ni)



        self.master.after(50, self.update)
        self.frame += 1


    # Start / init simulation (clear all agents and create new ones)
    def init_sim(self):
        self.canvas.delete('all')
        self.persons = []

        for i in range(n):
            x = random.randint(0,800)
            y = random.randint(0,800)
            p = Person(self.canvas, x, y, 'spring green')
            if random.uniform(0,1) < 0.05:
                p.infect()

            self.persons.append(p)

        for i in range(n):
            x = random.randint(0,800)
            y = random.randint(0,800)
            p = Person(self.canvas, x, y, 'spring green')
            if random.uniform(0,1) < 0.05:
                p.doctor()

            self.persons.append(p)

        self.canvas.pack()

        
# Create the Tkinter application and run it
root = tk.Tk()
app = App(root)
start=time.time()
root.mainloop()
end=time.time()
print("Frames:",app.frame)
print("Runtime:",end-start)
print("Framerate:", app.frame/(end-start))
