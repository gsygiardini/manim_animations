#Importando a biblioteca do Manim
from manimlib.imports import *

#Cria a classe no Manim, que será utilizada para compilar o vídeo no manim.
#A classe é utilizada para escolher qual vídeo será compilado, pois é possível criar vários scripts
#de vídeo em um mesmo arquivo.py
#Na compilação, ficará: manim -p arquivo.py classe
#p é a opção de play
#arquivo é o arquivo que foi escrito em python
#e classe é o nome da classe abaixo
gridSpc = 0.5
intervalTime = 5
inBetweenTime = 1.5
t=intervalTime
tInt = inBetweenTime

class ex8 (ThreeDScene):
    CONFIG = {
        "coef":2,
        "buff":0.6,
    }

    #sempre colocar o construct como self
    def construct (self):
        axes = ThreeDAxes(x_length=([-2,2,0.5]),y_range=([-2,2,0.5]),z_range=([-2,2,0.5]))
        self.set_camera_orientation(phi=60 * DEGREES, theta=30 * DEGREES)

        # xaxis = TexMobject("x").move_to(np.array([5,0,0]))
        # yaxis = TexMobject("y").move_to(np.array([0,5,0]))
        # zaxis = TexMobject("z").move_to(np.array([0,0,2]))
        # self.add(xaxis,yaxis,zaxis)

        x = TexMobject("x = a \\, cosh\\left(\\frac{y-b}{a}\\right)").scale(0.75)
        self.add_fixed_orientation_mobjects(x)
        self.play(Write(x))
        x.generate_target()
        x.target.shift(5*DOWN + 2*LEFT)
        self.play(MoveToTarget(x))
        self.wait(2)


        graph = axes.get_parametric_curve(
            lambda t: np.array([0,self.coef*np.cosh(t/self.coef),t]), t_min=-3, t_max=3, color=WHITE)

        self.play(ShowCreation(axes),run_time=2)
        self.play(ShowCreation(graph),run_time=5)
        self.wait(5)

        self.move_camera(phi=65*DEGREES,theta=0*DEGREES)
        self.wait()

        arrow_a = Arrow(start=np.array([0,-0.2,0]),end=np.array([0,self.coef+0.2,0]),color=YELLOW)
        self.play(ShowCreation(arrow_a),run_time=2)
        self.wait()

        a = TexMobject("a")
        self.add_fixed_orientation_mobjects(a)

        arrow_a.add_updater(lambda d: d.set_length(graph.get_center()[1]-self.coef+self.buff))
        arrow_a.add_updater(lambda d: d.move_to(np.array([0,0,0]) + np.array([0,(graph.get_center()[1]-self.coef+self.buff)/2,0])))
        a.add_updater(lambda d: d.next_to(arrow_a,np.array([0,0,1])))
        self.add(a)

        p = ValueTracker(2)

        graph.add_updater(
            lambda m: m.become(
                axes.get_parametric_curve(
                    lambda t: np.array([0,p.get_value()*np.cosh(t/p.get_value()),t]), t_min=-3, t_max=3, color=WHITE)
            )
        )

        self.add(graph)
        self.wait()
        self.play(
            ApplyMethod(p.increment_value,3.5),
            run_time=4,
        )

        self.play(
            ApplyMethod(p.increment_value,-3.5),
            run_time=4,
        )

        # self.play(
        #     graph.move_to,np.array([0,self.coef,0]),
        #     rate_func=there_and_back,
        #     run_time=5
        # )
        #

        # line_b = Line(start=np.array([0,0,0]), end=np.array([0,0,3]), color=RED,buff=0)
        # tri_b = Triangle(color=RED,fill_opacity=1).move_to(line_b.get_center()).scale(0.05)
        # self.add_fixed_orientation_mobjects(tri_b)

        b = TexMobject("b").move_to(np.array([3,1,1]))
        self.add_fixed_orientation_mobjects(b)

        b.add_updater(lambda d: d.move_to(np.array([-1,-1,(graph.get_center()[2]+0.5)/2])))

        # line_b.add_updater(lambda d: d.set_length(graph.get_center()[2]+0.1))
        # line_b.add_updater(lambda d: d.move_to(np.array([0,0,(graph.get_center()[2]+0.5)/2 - 0.2])))
        # tri_b.add_updater(lambda d: d.move_to(np.array([0,0,graph.get_center()[2]])))
        #
        # arrow_b = VGroup(line_b,tri_b)

        self.add(b)
        # self.play(ShowCreation(arrow_b))

        # self.play(
        #     graph.shift,np.array([0,0,self.coef]),
        #     rate_func=there_and_back,
        #     run_time=5
        # )
        self.play(FadeOut(a),FadeOut(arrow_a))

        p = ValueTracker(1)

        graph.add_updater(
            lambda m: m.become(
                axes.get_parametric_curve(
                    lambda t: np.array([0,self.coef*np.cosh((t-p.get_value())/self.coef),t]), t_min=-3, t_max=3, color=WHITE)
            )
        )

        self.add(graph)
        self.wait()
        self.play(
            ApplyMethod(p.increment_value,1),
            run_time=4,
        )

        self.play(
            ApplyMethod(p.increment_value,-1.999),
            run_time=4,
        )

        # self.remove(tri_b,line_b,arrow_a)
        # self.remove(arrow_a)

        b.generate_target()
        b.target.shift(np.array([2,-2,0]))
        self.play(MoveToTarget(b))

        _aux = TexMobject("b = 0").move_to(b.get_center())
        self.add_fixed_orientation_mobjects(_aux)
        self.remove(b)
        self.add(_aux)

        self.wait(5)
        self.remove(a,_aux)

        self.move_camera(phi=60*DEGREES,theta=30*DEGREES)
        self.wait()

        surface = ParametricSurface(
            lambda u, v: axes.c2p(self.coef*np.cosh(v/self.coef)*np.cos(u), self.coef*np.cosh(v/self.coef)*np.sin(u),v),
            u_min=PI/2,
            u_max=5 * (PI/2),
            v_min=-1,
            v_max=1,
            checkerboard_colors=[BLACK,WHITE]
        )

        group = VGroup(surface)

        self.add(axes)
        self.play(ShowCreation(group),run_time=5)

        self.wait(5)

        self.remove(group,graph,x)

        self.move_camera(phi=65*DEGREES,theta=0*DEGREES)
        self.wait()

        degLine1 = Line(start=np.array([0,self.coef,3]), end=np.array([0,0,3]),color=RED)
        degLine2 = Line(start=np.array([0,0,3]), end=np.array([0,0,-3]),color=RED)
        degLine3 = Line(start=np.array([0,0,-3]), end=np.array([0,self.coef,-3]),color=RED)

        self.play(ShowCreation(degLine1))
        self.play(ShowCreation(degLine2))
        self.play(ShowCreation(degLine3))

        self.move_camera(phi=60*DEGREES,theta=30*DEGREES)
        self.wait()

        disk1 = ParametricSurface(
        lambda u, v: axes.c2p(self.coef*v*np.cos(u), self.coef*v*np.sin(u),3),
            u_min=PI/2,
            u_max=5 * (PI/2),
            v_min=0,
            v_max=1,
            checkerboard_colors=[BLACK,WHITE]
        )

        disk2 = ParametricSurface(
        lambda u, v: axes.c2p(self.coef*v*np.cos(u), self.coef*v*np.sin(u),-3),
            u_min=PI/2,
            u_max=5 * (PI/2),
            v_min=0,
            v_max=1,
            checkerboard_colors=[BLACK,WHITE]
        )

        self.play(ShowCreation(disk1),ShowCreation(disk2))

        self.wait(10)
