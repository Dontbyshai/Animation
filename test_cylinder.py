from manim import *

class TestCylinder(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)
        
        # Manim Cylinder
        pizza_base = Cylinder(radius=2.5, height=0.5, color="#D2691E")
        
        # Top cheese cap (Circle)
        # Cylinder default direction is along the Z axis (OUT) in Manim? Let's verify.
        # If it's along Z, its center is ORIGIN, ranging from -height/2 to height/2 along Z
        cheese = Circle(radius=2.3, color="#FFD700", fill_opacity=1, stroke_width=0)
        cheese.shift(OUT * 0.251)
        
        # Add pepperoni
        pepperoni = Circle(radius=0.3, color="#DC143C", fill_opacity=1, stroke_width=0)
        pepperoni.move_to([1, 1, 0.252])
        
        self.play(FadeIn(pizza_base), FadeIn(cheese), FadeIn(pepperoni))
        self.wait(1)
        
        self.move_camera(phi=45 * DEGREES, theta=-45 * DEGREES, run_time=2)
        self.wait(1)
