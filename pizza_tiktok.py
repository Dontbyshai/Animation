from manim import *
import numpy as np

# Format TikTok 9:16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 60
config.frame_width = 9
config.frame_height = 16

class PizzaTikTok(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#000000"

        # Tonalités 
        YELLOW = "#FFD700"
        ORANGE = "#F7931A"
        RED = "#FF003C"
        WHITE = "#FFFFFF"

        # =====================================================
        # SCENE 1 : LE MOT PIZZA ET LA TRANSFORMATION MATHÉMATIQUE
        # =====================================================
        # Font size adapté au standard de ton projet (environ 75-85)
        pizza_text = Tex(r"\textbf{PIZZA}", font_size=85)
        self.play(Write(pizza_text))
        self.wait(1)

        # On sépare en parties PI, Z, Z, A
        pizza_parts = MathTex(r"\text{PI}", "Z", "Z", "A", font_size=85)
        self.play(TransformMatchingShapes(pizza_text, pizza_parts))
        self.wait(0.5)

        # P, I -> \pi | Z -> z | Z -> z | A -> a
        math_parts = MathTex(r"\pi", "z", "z", "a", font_size=85)
        self.play(
            Transform(pizza_parts[0], math_parts[0]),
            Transform(pizza_parts[1], math_parts[1]),
            Transform(pizza_parts[2], math_parts[2]),
            Transform(pizza_parts[3], math_parts[3]),
        )
        self.wait(0.8)

        # z et z fusionnent en z²
        z2_formula = MathTex(r"\pi", "z^2", "a", font_size=85)
        self.play(
            Transform(pizza_parts[0], z2_formula[0]),
            Transform(pizza_parts[1], z2_formula[1]),
            Transform(pizza_parts[2], z2_formula[1]),
            Transform(pizza_parts[3], z2_formula[2]),
        )
        self.wait(1)

        # L'équation monte en haut
        final_formula = MathTex(r"\text{PIZZA} = \pi z^2 a", font_size=65)
        final_formula.to_edge(UP, buff=2)
        
        self.play(TransformMatchingShapes(pizza_parts, final_formula))
        self.wait(0.5)

        # =====================================================
        # SCENE 2 : LE CYLINDRE (LA VRAIE PIZZA EN 3D)
        # =====================================================
        # Volume d'un cylindre
        volume_formula = MathTex(r"V = \pi r^2 h", font_size=65)
        volume_formula.next_to(final_formula, DOWN, buff=1.5)
        self.play(Write(volume_formula))
        self.wait(1)

        # Mouvement de caméra pour la 3D
        self.move_camera(phi=65 * DEGREES, theta=-60 * DEGREES, run_time=1.5)

        # Création de la pizza en 3D
        # La pâte (Cylindre marron/orange)
        crust = Cylinder(radius=2.5, height=0.4, color="#C27A30", resolution=(24, 24))
        # Le fromage (Cercle ou cylindre fin au-dessus)
        cheese = Cylinder(radius=2.3, height=0.41, color=YELLOW, resolution=(24, 24))
        
        # Quelques pepperonis
        pepperonis = VGroup()
        for pos in [(1, 1), (-1, 1.5), (-1.2, -1), (0.5, -1.8), (0, 0)]:
            pep = Cylinder(radius=0.3, height=0.42, color=RED, resolution=(12, 12))
            pep.move_to([pos[0], pos[1], 0])
            pepperonis.add(pep)
        
        pizza_3d = VGroup(crust, cheese, pepperonis)
        pizza_3d.shift(DOWN * 2)

        self.play(FadeIn(pizza_3d))
        self.wait(0.5)

        # Rotation lente de la pizza pour admirer la 3D
        self.play(Rotate(pizza_3d, angle=PI/2, axis=OUT), run_time=3)
        self.wait(0.5)

        # On se remet face à l'écran pour les dernières explications
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, run_time=1.5)
        
        # Note: Après move_camera à phi=0, la pizza apparaitra vue de dessus (comme un cercle 2D)
        # On trace le rayon r=z et la hauteur h=a
        center_2d = pizza_3d.get_center()
        right_edge_2d = center_2d + RIGHT * 2.5
        
        r_line = Line(center_2d, right_edge_2d, color=WHITE)
        r_label = MathTex("r = z", font_size=55).next_to(r_line, UP, buff=0.1)
        
        self.play(Create(r_line), Write(r_label))
        self.wait(0.5)

        # Remplacement dans la formule du volume
        volume_z_a = MathTex("V =", r"\pi", "z^2", "a", font_size=65).move_to(volume_formula)
        self.play(TransformMatchingShapes(volume_formula, volume_z_a))
        self.wait(1)

        # Zoom énorme sur z^2
        self.play(
            volume_z_a[2].animate.scale(3).set_color(YELLOW),
            run_time=1.5
        )
        self.wait(0.5)

        # Mind blown
        mind_blown_text = Text("🤯", font_size=90, font="Apple Color Emoji")
        mind_blown_text.next_to(pizza_3d, DOWN, buff=1)
        
        self.play(FadeIn(mind_blown_text, shift=UP))
        self.wait(3)

