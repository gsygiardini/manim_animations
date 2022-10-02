from manimlib.imports import *
from scipy.integrate import odeint
import numpy as np


class vanDerPolPhaseSpace (Scene):
    #sempre colocar o construct como self
    CONFIG = {
        "tMax": 300,      #Time of the animation (it is divided by the velocity factor)
        "dt":0,      #dt Used in the differential equation solution
        "velFactor":1, #Animation Speed
        "m":1,           #Particle's mass
        "epsilon":5,   #Dampening constant
        "omega0":1,      #Harmonic oscillator frequency
        "omegaD":2.465,      #Force oscillation frequency
        "F":5,           #Force value
        "xIni":10,      #Initial value for x
        "yIni":0.0,      #Initial value for y = dx/dt
        "scale":0.5,     #Scale of the "simulation"
        "radius":0.1,    #Radius of the ball in the animation
}



    def construct (self):
        #Animated object "allocation"
        dot = self.get_particle(self.radius)
        self.dt = 1/self.camera.frame_rate

        #Differential equation
        def f(r,t):
            m = self.m
            epsilon = self.epsilon
            omega0 = self.omega0
            omegaD = self.omegaD
            F = self.F

            return(r[1],(1/m)*(epsilon * (1.0 - r[0]*r[0])*r[1] - m*omega0*omega0*r[0] + F*np.cos(omegaD*t)))

        #Solving differential equation
        y0=[self.xIni,self.yIni]

        t = np.linspace(1,self.tMax,self.tMax*int(1/self.dt)*10)
        _aux = odeint(f,y0,t)

        print(len(t))

        x = _aux[:,0]
        xDot = []

        #Euler derivative for dx/dt
        for i in range(0,len(x)-1):
            xDot.append((x[i+1]-x[i])/self.dt)

        x = np.delete(x,len(x)-1)

        dot.xSol = x
        dot.ySol = xDot

        #Update the particle's postion in animation
        dot.add_updater(self.update)

        #Trace path of the particle
        path = self.get_traced_path(dot)

        #self.add(axes)

        #Add particle and its path
        self.add(dot)
        self.add(path)

        self.dot = dot
        self.path = path

        #"Simulation" run time
        # self.wait(int(1/dt)/self.velFactor-1)
        #print(self.tMax/self.velFactor-10)

        runTime = self.tMax/self.velFactor

        self.wait(runTime-1)



    def update (self,dot,dt):
        dot.i = dot.i + 1*self.velFactor

        dot.x = dot.xSol[int(dot.i)]*self.scale
        dot.y = dot.ySol[int(dot.i)]*self.scale

        xMax = np.amax(dot.xSol)
        yMax = np.amax(dot.ySol)
        xyScale = xMax/yMax

        dot.center = np.array([float(dot.x),float(dot.y)*xyScale,0])
        dot.move_to(dot.center)

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

    def get_particle(self, rad):
        dot = Dot(radius=rad)
        dot.set_fill(YELLOW, 1)

        dot.x = self.xIni
        dot.y = self.yIni
        dot.i = 0

        dot.xSol = [0]
        dot.ySol = [0]

        dot.center = np.array([dot.x,dot.y])

        return dot


class vanDerPolvsTime (Scene):
    #sempre colocar o construct como self
    CONFIG = {
        "tMax": 40,      #Time of the animation (it is divided by the velocity factor)
        "dt":0.001,      #dt Used in the differential equation solution
        "velFactor":3,  #Animation Speed
        "m":1,           #Particle's mass
        "epsilon":0.3,     #Dampening constant
        "omega0":1,      #Harmonic oscillator frequency
        "omegaD":1,      #Force oscillation frequency
        "F":1,           #Force value
        "xIni":0.5,      #Initial value for x
        "yIni":0.0,      #Initial value for y = dx/dt
        "scale":0.08,     #Scale of the "simulation"
        "radius":0.1,    #Radius of the ball in the animation
        "origin":4*LEFT,
}



    def construct (self):
        #Animated object "allocation"
        dot = self.get_particle(self.radius)

        #Differential equation
        def f(r,t):
            m = self.m
            epsilon = self.epsilon
            omega0 = self.omega0
            omegaD = self.omegaD
            F = self.F

            return(r[1],(1/m)*(epsilon * (1.0 - r[0]*r[0])*r[1] - m*omega0*omega0*r[0] + F*np.cos(omegaD*t)))

        #Solving differential equation
        y0=[self.yIni,self.xIni]

        t = np.linspace(1,self.tMax,int(1/self.dt))
        _aux = odeint(f,y0,t)

        print(len(t))

        x = _aux[:,0]

        dot.xSol = t
        dot.ySol = x

        #Update the particle's postion in animation
        dot.add_updater(self.update)

        #Trace path of the particle
        path = self.get_traced_path(dot)

        #self.add(axes)

        #Add particle and its path
        self.add(dot)
        self.add(path)

        self.dot = dot
        self.path = path

        #"Simulation" run time
        # self.wait(int(1/dt)/self.velFactor-1)
        #print(self.tMax/self.velFactor-10)

        runTime = (1/(self.dt*self.camera.frame_rate)-1)/self.velFactor

        self.wait(runTime-1)



    def update (self,dot,dt):
        dot.i = dot.i + 1*self.velFactor

        dot.x = dot.xSol[int(dot.i)]*self.scale
        dot.y = dot.ySol[int(dot.i)]*self.scale

        xMax = np.amax(dot.xSol)
        yMax = np.amax(dot.ySol)
        xyScale = xMax/yMax

        dot.center = np.array([float(dot.x),float(dot.y)*xyScale,0])
        dot.move_to(dot.center + self.origin)

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

    def get_particle(self, rad):
        dot = Dot(radius=rad)
        dot.set_fill(YELLOW, 1)

        dot.x = self.xIni
        dot.y = self.yIni
        dot.i = 0

        dot.xSol = [0]
        dot.ySol = [0]

        dot.center = np.array([dot.x,dot.y])

        return dot


class vanDerPolRandomParticles (Scene):
    #sempre colocar o construct como self
    CONFIG = {
        "tMax": 100,     #Time of the animation (it is divided by the velocity factor)
        "nPart":5,      #Number of particles
        "dt":0.001,      #dt Used in the differential equation solution
        "velFactor":5, #Animation Speed
        "m":1,           #Particle's mass
        "epsilon":5,   #Dampening constant
        "omega0":1,      #Harmonic oscillator frequency
        "omegaD":2.465,      #Force oscillation frequency
        "F":5,           #Force value
        "xIni":10,       #Initial value for x
        "yIni":0.0,      #Initial value for y = dx/dt
        "scale":0.5,     #Scale of the "simulation"
        "radius":0.1,    #Radius of the ball in the animation
}



    def construct (self):
        #Animated object "allocation"
        dot = []
        path = []
        for i in range(0,self.nPart):
            dot.append(self.get_particle(self.radius))
            path.append([])

        #Differential equation
        def f(r,t):
            m = self.m
            epsilon = self.epsilon
            omega0 = self.omega0
            omegaD = self.omegaD
            F = self.F

            return(r[1],(1/m)*(epsilon * (1.0 - r[0]*r[0])*r[1] - m*omega0*omega0*r[0] + F*np.cos(omegaD*t)))

        x = [0]*self.nPart
        xDot = [[]]*self.nPart
        #Solving differential equation
        for i in range(0,self.nPart-1):
            xIni = 5*np.random.rand()
            yIni = 5*np.random.rand()
            y0=[xIni,yIni]

            t = np.linspace(1,self.tMax,int(1/self.dt)*self.tMax)
            _aux = odeint(f,y0,t)

            x[i] = _aux[:,0]

            #Euler derivative for dx/dt
            for j in range(0,len(x[i])-1):
                xDot[i].append((x[i][j+1]-x[i][j])/self.dt)

            x[i] = np.delete(x[i],len(x[i])-1)

            dot[i].xSol = x[i]
            dot[i].ySol = xDot[i]

            #Update the particle's postion in animation
            dot[i].add_updater(self.update)

            #Add particles
            self.add(dot[i])

        for i in dot:
            path = TracedPath(i.get_center,dissipating_time=0.1, stroke_opacity=[0, 0.5])
            self.add(path)

        #"Simulation" run time
        runTime = (self.tMax/(self.dt*self.camera.frame_rate)-1)/self.velFactor

        self.wait(runTime-1)



    def update (self,dot,dt):
        dot.i = dot.i + 1*self.velFactor

        dot.x = dot.xSol[int(dot.i)]*self.scale
        dot.y = dot.ySol[int(dot.i)]*self.scale

        xMax = np.amax(dot.xSol)
        yMax = np.amax(dot.ySol)
        xyScale = xMax/yMax

        dot.center = np.array([float(dot.x),float(dot.y)*xyScale,0])
        dot.move_to(dot.center)

        # dot.path = TracedPath(dot.get_center, dissipating_time=1, stroke_opacity=[0, 1])

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

    def get_particle(self, rad):
        dot = Dot(radius=rad)
        dot.set_fill(random_color(), 1)

        # dot.path =

        dot.x = self.xIni
        dot.y = self.yIni
        dot.i = 0

        dot.xSol = [0]
        dot.ySol = [0]

        dot.center = np.array([dot.x,dot.y])

        return dot
