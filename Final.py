
import math
from turtle import *
from tkinter import *
G = 6.67428e-11
import sys
# Assumed scale: 100 pixels = 1AU.
AU = (149.6e6 * 1000)     # 149.6 million km, in meters.
SCALE = 100 / AU
class Body(Turtle):
    """Subclass of Turtle representing a gravitationally-acting body.

    Extra attributes:
    mass : mass in kg
    vx, vy: x, y velocities in m/s
    px, py: x, y positions in m
    """

    name = 'Body'
    mass = None
    vx = vy = 0.0
    px = py = 0.0

    def attraction(self, other):
        """(Body): (fx, fy)

        Returns the force exerted upon this body by the other body.
        """
        # Report an error if the other object is the same as this one.
        if self is other:
            raise ValueError("Attraction of object %r to itself requested"
                             % self.name)

        # Compute the distance of the other body.
        sx, sy = self.px, self.py
        ox, oy = other.px, other.py
        dx = (ox-sx)
        dy = (oy-sy)
        d = math.sqrt(dx**2 + dy**2)


        # Report an error if the distance is zero; otherwise we'll
        # get a ZeroDivisionError exception further down.
        if d == 0:
            raise ValueError("Collision between objects %r and %r"
                             % (self.name, other.name))

        # Compute the force of attraction
        f = G * self.mass * other.mass / (d**2)

        # Compute the direction of the force.
        theta = math.atan2(dy, dx)
        fx = math.cos(theta) * f
        fy = math.sin(theta) * f
        return fx, fy

def update_info(step, bodies):
    """(int, [Body])

    Displays information about the status of the simulation.
    """
    print('Step #{}'.format(step))
    for body in bodies:
        s = '{:<8}  Pos.={:>6.2f} {:>6.2f} Vel.={:>10.3f} {:>10.3f}'.format(
            body.name, body.px/AU, body.py/AU, body.vx, body.vy)
        print(s)
    print()

def loop(bodies):
    """([Body])

    Never returns; loops through the simulation, updating the
    positions of all the provided bodies.
    """
    timestep = 24*3600*5  # Five days

    for body in bodies:
        body.penup()
        body.hideturtle()

    step = 1
    while True:
        update_info(step, bodies)
        step += 1

        force = {}
        for body in bodies:
            # Add up all of the forces exerted on 'body'.
            total_fx = total_fy = 0.0
            for other in bodies:
                # Don't calculate the body's attraction to itself
                if body is other:
                    continue
                fx, fy = body.attraction(other)
                total_fx += fx
                total_fy += fy

            # Record the total force exerted.
            force[body] = (total_fx, total_fy)

        # Update velocities based upon on the force.
        for body in bodies:
            x = 1
            fx, fy = force[body]
            body.vx += fx / body.mass * timestep
            body.vy += fy / body.mass * timestep

            body.px += body.vx * timestep
            body.py += body.vy * timestep
            body.goto(body.px*SCALE, body.py*SCALE)
            body.dot(3)


def main():
    print("Do you want to create a new solarsystem? ")
    a = input()
    if (a == "yes" or a == "Yes"):
        print("How many bodies are there? ")
        numer = input()
        numer = int(numer)
        plants = []
        for i in range(numer):
            print("What is the body's name? ")
            name = input()
            print("What is its mass (in kg)? ")
            mass = input()
            mass = float(mass)
            print("What is the mass's exponent? ")
            power = input()
            power = int(power)
            print("What color is it? ")
            pencolor = input()
            print("Where is it positioned (in AU)? ")
            position = input()
            position = float(position)
            print("What is its velocity (in km/sec)? ")
            velocity = input()
            velocity = float(velocity)
            obj_i = Body()
            obj_i.name = name
            obj_i.mass = (mass*pow(10,power))
            obj_i.pencolor(pencolor)
            obj_i.px = ((float(position)*AU))
            obj_i.vx = (float(velocity) *1000)
            plants.append(obj_i)
        bgcolor("black")
        loop(plants)
    else:
        bgcolor("black")

        sun = Body()
        sun.name = 'Sun'
        sun.mass = 1.98892 * 10**30
        sun.pencolor('yellow')

        mercury = Body()
        mercury.name = 'Mercury'
        mercury.mass = .33011*10**24
        mercury.pencolor('blue')
        mercury.px = .387*AU
        mercury.vy = 47.36 *1000

        earth = Body()
        earth.name = 'Earth'
        earth.mass = 5.9742 * 10**24       # mass in kg
        earth.px = 1*AU                    # distance from center
        earth.vy = 29.783 * 1000            # 29.783 km/sec
        earth.pencolor('green')

        # http://nssdc.gsfc.nasa.gov/planetary/factsheet
        #look this link up for planetary bodies
        venus = Body()
        venus.name = 'Venus'
        venus.mass = 4.8685 * 10**24
        venus.px = 0.723 * AU
        venus.vy = 35.02 * 1000
        venus.pencolor('pink')

        mars = Body()
        mars.name = 'Mars'
        mars.mass = .64171 *10**24
        mars.px = 1.52366 *AU
        mars.vy = 24.07*1000
        mars.pencolor('red')

        loop([sun, mercury, mars, earth, venus])

if __name__ == '__main__':
    main()
