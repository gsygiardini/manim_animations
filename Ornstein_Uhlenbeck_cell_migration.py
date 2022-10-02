from manimlib.imports import *
from csv import *
from math import pi as pi
from random import random
from numpy.random import normal

import numpy as np
import math
import csv


class velocityRelaxationGraph(GraphScene):
    CONFIG = {
        "y_max": 20,
        "y_min": 0,
        "x_max": 10,
        "x_min": -10,
        "y_tick_frequency": 5,
        "x_tick_frequency": 0.5,
        "axes_color": WHITE,
        "y_labeled_nums": range(0,20,10),
        "x_labeled_nums": range(-10,10,5),
        "x_label_decimal": 1,
        "y_label_decimal": 3,
        "y_label_direction": RIGHT,
        "x_label_direction": UP,
    }

    def construct(self):
        self.setup_axes(animate=True)
        graph = self.get_graph(lambda x : x**2, color = GREEN, x_min=-4, x_max=4)
        self.play(ShowCreation(graph),run_time=2)
        self.wait()

class ourModel(Scene):
    CONFIG = {
        "wait_time": 60,
        "L": 3,  # Box in [-L, L] x [-L, L]

        "gamma": 1,
        "q": 0.1,
        "k": 0.04405,
        "g": 10,

        "r": 0.2,
        "v0": 10,
        "theta0": 2*PI*(random()-0.5),
        "random_seed": 2,

        "counter": 0,
        "file": open("data.csv", "w"),
    }

    def construct(self):
        self.add_title()
        self.simulation()
        self.wait(self.wait_time)

    def add_title(self):
        square = Square(side_length=2 * self.L)
        self.add(square)

    def simulation(self):
        k = self.k
        q = self.q
        g = self.g
        gamma = self.gamma
        theta = self.theta0
        v = self.v0

        r = self.r

        L = self.L

        big_particle = self.get_particle(q, g, gamma, k, v, theta, r, L)
        big_particle.set_fill(YELLOW, 1)

        all_particles = VGroup(big_particle)
        all_particles.add_updater(self.update_particles)

        path = self.get_traced_path(big_particle)

        self.add(all_particles)
        self.add(path)

        self.particles = all_particles
        self.big_particle = big_particle
        self.path = path

    def get_particle(self, q, g, gamma, k, v, theta, r, L):
        dot = Dot(radius=r)
        dot.set_fill(WHITE, 0.7)
        dot.q = q
        dot.radius = r
        dot.g = g
        dot.gamma = gamma
        dot.k = k
        dot.v = v
        dot.angle = theta
        dot.v2Avg = 0

        dot.center = np.array([0,0,0])

        return dot

    def get_traced_path(self, particle):
        path = VMobject()
        path.set_stroke(BLUE, 3)
        path.start_new_path(particle.get_center())

        buff = 0.02

        def update_path(path):
            new_point = particle.get_center()
            if get_norm(new_point - path.get_last_point()) > buff:
                path.add_line_to(new_point)

        path.add_updater(update_path)
        return path

    def update_particles(self, particles, dt):
        DT = 0.1*dt
        buff = self.L*0.1
        for p1 in particles:
            etapar = math.sqrt(p1.g) * math.sqrt(DT) * normal()
            dtheta = math.sqrt(2*p1.k) * math.sqrt(DT) * normal()

            if (math.sqrt((p1.center[0])**2) >= self.L-buff):
                px = -math.cos(p1.angle)
                py = math.sin(p1.angle)

            else:
                if (math.sqrt((p1.center[1])**2) >= self.L-buff):
                    py = -math.sin(p1.angle)
                    px = math.cos(p1.angle)

                else:
                    px = math.cos(p1.angle)
                    py = math.sin(p1.angle)

            # if (math.sqrt((p1.center[0])**2) >= self.L-buff or math.sqrt((p1.center[1])**2) >= self.L-buff):
            #     p1.v = -p1.v

            p1.angle = math.atan2(py,px)

            p1.angle = p1.angle + dtheta

            px = math.cos(p1.angle)
            py = math.sin(p1.angle)

            nx = py
            ny = -px

            p1.v = ((1 - p1.gamma * DT) * p1.v + etapar) * math.cos(dtheta)

            dx = (p1.v + etapar) * px * DT + math.sqrt(p1.q) * dtheta * nx
            dy = (p1.v + etapar) * py * DT + math.sqrt(p1.q) * dtheta * ny

            p1.center = p1.center + np.array([dx,dy,0])

            # self.file.write(p1.v)
            oldCounter = self.counter
            self.counter = self.counter + 1
            p1.v2Avg = (p1.v2Avg*oldCounter)/self.counter  + p1.v * p1.v / self.counter

            print(self.counter,";",p1.v2Avg, file=self.file)
            # print(self.counter,p1.v2Avg, file=self.file)

        for p in particles:
            p.move_to(p.center)
        return particles

class explicacao(Scene):
    CONFIG = {
        "size": 2,
        "iMax": 5,#math.ceil(10*random()),
        "runTime": 0.3,
        "angle": PI/5,
        "cellCenter": np.array([-3,-2,0]),
        "velVec": np.array([1.5*2,0,0]),
        "polVec": np.array([2,0,0]),
        "perpVec": np.array([0, -2, 0]),
        "gamma": 0.1,
        "langEq": 0,
        "perpEq": 0,
        "counter": 0,
        "start": 0,
        "end": 0,
        "perpColor": YELLOW,
        "polColor": GREEN,
        "cellContourColor": WHITE,
        "cellColor": BLUE,
        "velColor": RED,
        "rectWidth": 14,
        "rectHeight": 7,
    }

    def construct(self):
        angle = self.angle
        runTime = self.runTime
        iMax = self.iMax
        self.langEq = self.cellCenter + (1 - self.gamma) * self.velVec + self.polVec
        self.perpEq = self.perpVec
        # self.cellNewCenter = np.array([2*math.cos(angle),2*math.sin(angle),0])
        self.cellNewCenter = get_norm(self.langEq)*np.array([math.cos(angle),math.sin(angle),0]) + get_norm(self.perpEq) * np.array([math.sin(angle), - math.cos(angle),0])

        # self.addBox()

        cell = Ellipse(width=self.size, color=self.cellContourColor)
        cell.set_fill(color=self.cellColor, opacity=0.5)
        # vel = Arrow(cell.get_center() + np.array([-0.28,0,0]), cell.get_center() + np.array([1.5*self.size,0,0]), color=self.velColor)
        # pol = Arrow(cell.get_center() + np.array([-0.28,0,0]), cell.get_center() + np.array([self.size,0,0]), color=self.polColor)
        vel = Arrow(cell.get_center(), cell.get_center() + self.velVec, color=self.velColor)
        pol = Arrow(cell.get_center(), cell.get_center() + self.polVec, color=self.polColor)
        perp = Arrow(cell.get_center() , cell.get_center() + self.perpVec, color=self.perpColor)

        cell.move_to(self.cellCenter)
        vel.move_to(self.cellCenter + np.array([0.75*self.size,0,0]))
        pol.move_to(self.cellCenter + np.array([self.size/2,0,0]))
        perp.move_to(cell.get_center() + np.array([0,-0.38 * self.size, 0]))

        for i in range(0, iMax):
            self.play(Rotate(cell, 2*((-1)**i)*angle, about_point=self.cellCenter,run_time=runTime), Rotate(vel, 2*((-1)**i)*angle, about_point=self.cellCenter,run_time=runTime), Rotate(pol, 2*((-1)**i)*angle, about_point=self.cellCenter,run_time=runTime))
            perp.rotate(2*((-1)**i)*angle, about_point=self.cellCenter)

        if iMax%2==0:
            self.play(Rotate(cell, angle, about_point=self.cellCenter,run_time=1), Rotate(vel, angle, about_point=self.cellCenter,run_time=1), Rotate(pol, angle, about_point=self.cellCenter,run_time=1))
            perp.rotate(angle, about_point=self.cellCenter)
        else:
            self.play(Rotate(cell, -angle, about_point=self.cellCenter,run_time=1), Rotate(vel, -angle, about_point=self.cellCenter,run_time=1), Rotate(pol, -angle, about_point=self.cellCenter,run_time=1))
            perp.rotate(-angle, about_point=self.cellCenter)

        self.add(perp)

        path = Line(self.cellCenter,self.cellNewCenter,color=BLUE)

        self.start = cell.get_center()
        self.end = cell.get_center()

        velName = TexMobject("\\vec{v}_{\\parallel}", color=self.velColor)
        polName = TexMobject("\\vec{\\xi}_{\\parallel}", color=self.polColor)
        perpName = TexMobject("\\vec{\\xi}_{\\perp}", color=self.perpColor)

        self.add(velName)
        self.add(polName)
        self.add(perpName)

        def updateVel(obj):
            obj.next_to(vel,RIGHT + UP)
        def updatePol(obj):
            obj.next_to(pol,UP)
        def updatePerp(obj):
            obj.next_to(perp,LEFT)

        velName.add_updater(updateVel)
        polName.add_updater(updatePol)
        perpName.add_updater(updatePerp)

        perp.add_updater(self.updateArrowsPerp)
        self.wait(5)

        perp.remove_updater(self.updateArrowsPerp)
        pol.add_updater(self.updateArrowsPol)
        self.wait(4)

        pol.remove_updater(self.updateArrowsPol)

        self.play(cell.move_to,self.cellNewCenter, pol.move_to,self.cellNewCenter + 0.5 * np.array([self.size * math.cos(angle), self.size * math.sin(angle), 0]), perp.move_to,self.cellNewCenter + 0.5 * np.array([self.size * math.sin(angle), - self.size * math.cos(angle), 0]), vel.move_to,self.cellNewCenter + 0.75 * np.array([self.size * math.cos(angle), self.size * math.sin(angle), 0]), ShowCreation(path))

        self.wait(5)

    def updateArrowsPerp(self, obj, dt):
        self.counter = self.counter + (PI)*dt
        # print(math.cos(self.counter))
        newArrow = Arrow(self.start, np.array([self.end[0] - self.size * math.cos(self.counter) * math.sin(self.angle) ,self.end[1] + self.size * math.cos(self.counter) * math.cos(self.angle),self.end[2]]), color=self.perpColor)
        # newArrow = Arrow(self.start, self.end)
        obj.become(newArrow)

    def updateArrowsPol(self, obj, dt):
        self.counter = self.counter + (PI)*dt
        # print(math.cos(self.counter))
        newArrow = Arrow(self.start, np.array([self.end[0] - 1.2 * self.size * math.cos(self.counter) * math.cos(self.angle) ,self.end[1] - 1.2 * self.size * math.cos(self.counter) * math.sin(self.angle),self.end[2]]), color=self.polColor)
        # newArrow = Arrow(self.start, self.end)
        obj.become(newArrow)

    def addBox(self):
        rectangle = Rectangle(width=self.rectWidth,height=self.rectHeight)
        self.add(rectangle)


    # def update_pol(self, obj, dt):
    #     # angle = 2*PI*random()
    #     angle = self.angle
    #     iMax = self.iMax
    #
    #         # Rotate(obj, ((-1)**(i+1))* 2*angle, run_time=1)
    #         obj.rotate(((-1)**(i)) * 2*angle, about_point=np.array([0,0,0]))
    #         iFinal = i
    #     if iFinal%2==0 :
    #         # Rotate(obj, angle, run_time=1)
    #         obj.rotate(angle, about_point=np.array([0,0,0]))
    #     else:
    #         # Rotate(obj, -angle, run_time=1)
    #         obj.rotate(-angle, about_point=np.array([0,0,0]))
