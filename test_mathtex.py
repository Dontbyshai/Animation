from manim import *

class TestMathTex(Scene):
    def construct(self):
        formula = MathTex("A=P(1+{r \\over n})^{nt}", substrings_to_isolate=["P", "r", "n", "t"], font_size=72)
        print("Length:", len(formula))
        self.play(FadeIn(formula))
        self.play(formula.get_parts_by_tex("P").animate.set_color(TEAL))
        self.wait(1)
