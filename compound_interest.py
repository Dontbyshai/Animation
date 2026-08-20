from manim import *
import math

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9.0
config.frame_height = 16.0

class CompoundInterest(MovingCameraScene):
    def construct(self):
        # ==========================================
        # 0-3s
        # ==========================================
        # Formula: A=P\Big(1+\frac{r}{n}\Big)^{nt}
        # A(0) =(1) P(2) \Big((3) 1(4) +(5) r(6) \frac_bar(7) n(8) \Big)(9) n(10) t(11)
        formula = MathTex("A=P\\Big(1+\\frac{r}{n}\\Big)^{nt}", font_size=80)
        
        self.play(FadeIn(formula), run_time=1)
        
        self.play(
            formula[0][2].animate.set_color(TEAL),
            formula[0][6].animate.set_color(TEAL),
            formula[0][8].animate.set_color(TEAL),
            formula[0][10].animate.set_color(TEAL),
            formula[0][11].animate.set_color(TEAL),
            run_time=1
        )
        
        # Camera zoom on exponent
        self.play(
            self.camera.frame.animate.scale(0.5).move_to(formula[0][10:12]),
            run_time=1
        )
        
        # ==========================================
        # 3-7s
        # ==========================================
        self.play(self.camera.frame.animate.scale(2).move_to(ORIGIN), run_time=0.5)
        
        formula_sub = MathTex("A", "=", "1000", "\\Big(1+", "0.05", "\\Big)^", "1", font_size=80)
        formula_sub[2].set_color(TEAL)
        formula_sub[4].set_color(TEAL)
        formula_sub[6].set_color(TEAL)
        
        self.play(Transform(formula, formula_sub), run_time=1)
        self.wait(0.5)
        
        result_1 = MathTex("A", "=", "1050", font_size=80)
        result_1[2].set_color(YELLOW)
        
        self.play(Transform(formula, result_1), run_time=1)
        
        # 1000 euros appear as coins (dots) - vertical grid for portrait
        dots = VGroup(*[Dot(radius=0.1, color=YELLOW) for _ in range(50)])
        dots.arrange_in_grid(rows=10, cols=5, buff=0.15)
        dots.next_to(result_1, DOWN, buff=1.5)
        self.play(Create(dots), run_time=1)
        
        # ==========================================
        # 7-12s
        # ==========================================
        calc_1 = MathTex("1050", "(1.05)", "=", "1102.50", font_size=60)
        calc_1[0].set_color(YELLOW)
        calc_1[1].set_color(YELLOW)
        
        self.play(FadeOut(dots), Transform(formula, calc_1), run_time=1)
        
        # Chart - fit to portrait width
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[1000, 1300, 50],
            x_length=7,
            y_length=6,
            axis_config={"include_numbers": False},
        ).to_edge(DOWN, buff=1)
        
        bar_1050 = Rectangle(width=0.6, height=axes.c2p(1, 1050)[1] - axes.c2p(1, 1000)[1], color=BLUE, fill_opacity=0.8)
        bar_1050.move_to(axes.c2p(1, 1000), aligned_edge=DOWN)
        
        self.play(Create(axes), GrowFromEdge(bar_1050, DOWN), formula.animate.to_edge(UP, buff=2), run_time=1)
        
        calc_2 = MathTex("1102.50", "(1.05)", "=", "1157.63", font_size=60).to_edge(UP, buff=2)
        calc_2[0].set_color(YELLOW)
        calc_2[1].set_color(YELLOW)
        
        bar_1102 = Rectangle(width=0.6, height=axes.c2p(2, 1102.5)[1] - axes.c2p(2, 1000)[1], color=BLUE, fill_opacity=0.8)
        bar_1102.move_to(axes.c2p(2, 1000), aligned_edge=DOWN)
        
        self.play(Transform(formula, calc_2), GrowFromEdge(bar_1102, DOWN), run_time=1)
        
        calc_3 = MathTex("1157.63", "(1.05)", "=", "1215.51", font_size=60).to_edge(UP, buff=2)
        calc_3[0].set_color(YELLOW)
        calc_3[1].set_color(YELLOW)
        
        bar_1157 = Rectangle(width=0.6, height=axes.c2p(3, 1157.63)[1] - axes.c2p(3, 1000)[1], color=BLUE, fill_opacity=0.8)
        bar_1157.move_to(axes.c2p(3, 1000), aligned_edge=DOWN)
        
        self.play(Transform(formula, calc_3), GrowFromEdge(bar_1157, DOWN), run_time=1)
        
        # ==========================================
        # 12-18s
        # ==========================================
        self.play(FadeOut(formula), FadeOut(bar_1050), FadeOut(bar_1102), FadeOut(bar_1157), run_time=1)
        
        seq_text = MathTex("1000 \\rightarrow 1050 \\rightarrow 1102.5", "\\\\", "\\rightarrow 1157.6 \\rightarrow 1215.5", "\\\\", "\\rightarrow 1276.3...").scale(0.9).to_edge(UP, buff=1.5)
        self.play(Write(seq_text), run_time=1)
        
        # Draw curve
        curve = axes.plot(lambda x: 1000 * (1.05)**x, color=YELLOW, x_range=[0, 6])
        
        time_tracker = ValueTracker(0)
        time_label = always_redraw(lambda: Text(f"{int(time_tracker.get_value())} ans", font_size=36).next_to(axes.c2p(time_tracker.get_value(), 1000 * (1.05)**time_tracker.get_value()), UP))
        
        self.play(Create(curve), run_time=2)
        self.play(time_tracker.animate.set_value(5), FadeIn(time_label), run_time=2)
        
        # ==========================================
        # 18-24s
        # ==========================================
        self.play(FadeOut(seq_text), FadeOut(axes), FadeOut(curve), FadeOut(time_label), run_time=1)
        
        formula2 = MathTex("A", "=", "P", "(1+", "r", ")^", "t", font_size=80)
        self.play(Write(formula2), run_time=1)
        self.play(formula2.animate.to_edge(UP, buff=1), run_time=0.5)
        
        # Stacked comparison for 9:16
        simple_title = Text("Intérêt simple", font_size=48, color=RED).shift(UP*3)
        simple_calc = MathTex("1000(1+0.05\\times10)", font_size=48).next_to(simple_title, DOWN, buff=0.5)
        simple_res = MathTex("=1500", font_size=60, color=RED).next_to(simple_calc, DOWN, buff=0.5)
        
        compound_title = Text("Intérêt composé", font_size=48, color=GREEN).shift(DOWN*1.5)
        comp_calc = MathTex("1000(1.05)^{10}", font_size=48).next_to(compound_title, DOWN, buff=0.5)
        comp_res = MathTex("=1628.89", font_size=60, color=GREEN).next_to(comp_calc, DOWN, buff=0.5)
        
        self.play(Write(simple_title), Write(compound_title), run_time=1)
        self.play(Write(simple_calc), Write(comp_calc), run_time=1)
        self.play(Write(simple_res), Write(comp_res), run_time=1)
        
        # ==========================================
        # 24-31s
        # ==========================================
        self.play(
            FadeOut(formula2), FadeOut(simple_calc), FadeOut(comp_calc),
            simple_title.animate.scale(0.6).to_edge(UL, buff=1).shift(DOWN*0.5),
            simple_res.animate.scale(0.6).next_to(simple_title, RIGHT, buff=0.5).to_edge(UR, buff=1).shift(DOWN*0.5),
            compound_title.animate.scale(0.6).next_to(simple_title, DOWN, buff=0.5).to_edge(UL, buff=1),
            comp_res.animate.scale(0.6).next_to(compound_title, RIGHT, buff=0.5).to_edge(UR, buff=1),
            run_time=1
        )
        
        comp_axes = Axes(
            x_range=[0, 30, 5],
            y_range=[1000, 4500, 500],
            x_length=7.5,
            y_length=8,
            axis_config={"include_numbers": False},
        ).to_edge(DOWN, buff=1)
        
        simple_curve = comp_axes.plot(lambda x: 1000 * (1 + 0.05 * x), color=RED, x_range=[0, 30])
        comp_curve = comp_axes.plot(lambda x: 1000 * (1.05)**x, color=GREEN, x_range=[0, 30])
        
        self.play(Create(comp_axes), run_time=1)
        self.play(Create(simple_curve), Create(comp_curve), run_time=2)
        
        diff_box = MathTex("\\boxed{1628.89 - 1500 = 128.89}", font_size=48).shift(UP*1.5)
        self.play(Write(diff_box), run_time=1)
        
        particles = VGroup(*[Dot(radius=0.06, color=GREEN) for _ in range(30)])
        particles.arrange_in_grid(rows=3, cols=10, buff=0.15)
        particles.move_to(diff_box.get_center())
        
        self.play(FadeOut(diff_box), FadeIn(particles), run_time=0.5)
        
        self.play(
            AnimationGroup(
                *[p.animate.move_to(comp_axes.c2p(10, 1628.89)) for p in particles],
                lag_ratio=0.05
            ),
            run_time=1.5
        )
        self.play(FadeOut(particles), run_time=0.5)
        
        # ==========================================
        # 31-38s
        # ==========================================
        self.play(
            FadeOut(comp_axes), FadeOut(simple_curve), FadeOut(comp_curve),
            FadeOut(simple_title), FadeOut(simple_res), FadeOut(compound_title), FadeOut(comp_res),
            run_time=1
        )
        
        mech_seq = MathTex("1000", "\\rightarrow", "1050", "\\rightarrow", "1102.50", "\\rightarrow", "1157.63", font_size=60).shift(UP*3)
        self.play(Write(mech_seq), run_time=1)
        
        cycle = VGroup(
            Text("Capital", font_size=48, color=BLUE),
            MathTex("\\downarrow").scale(1.5),
            Text("Intérêt", font_size=48, color=YELLOW),
            MathTex("\\downarrow").scale(1.5),
            Text("Capital", font_size=48, color=BLUE),
            MathTex("\\downarrow").scale(1.5),
            Text("Intérêt", font_size=48, color=YELLOW)
        ).arrange(DOWN, buff=0.8).shift(DOWN*1)
        
        self.play(Write(cycle), run_time=2)
        self.wait(1)
        
        # ==========================================
        # 38-45s
        # ==========================================
        self.play(FadeOut(mech_seq), FadeOut(cycle), run_time=1)
        
        formula3 = MathTex("A", "=", "P", "(1+", "r", ")^", "t", font_size=90)
        self.play(Write(formula3), run_time=1)
        
        t_tracker = ValueTracker(1)
        t_val = always_redraw(lambda: MathTex(f"t={int(t_tracker.get_value())}", font_size=72).next_to(formula3, DOWN*1.5))
        final_val = always_redraw(lambda: MathTex(f"A={int(1000*(1.05)**t_tracker.get_value())}", font_size=72, color=GREEN).next_to(t_val, DOWN))
        
        self.play(FadeIn(t_val), FadeIn(final_val), run_time=1)
        
        self.play(
            formula3.animate.to_edge(UP, buff=1.5),
            run_time=0.5
        )
        
        exp_axes = Axes(
            x_range=[0, 30, 5],
            y_range=[1000, 4500, 500],
            x_length=7.5,
            y_length=7,
            axis_config={"include_numbers": False},
        ).to_edge(DOWN, buff=1)
        
        exp_curve = always_redraw(lambda: exp_axes.plot(lambda x: 1000 * (1.05)**x, x_range=[0, max(0.1, t_tracker.get_value())], color=GREEN))
        
        self.play(FadeIn(exp_axes), FadeIn(exp_curve), run_time=1)
        
        self.play(t_tracker.animate.set_value(30), run_time=3, rate_func=rate_functions.ease_in_out_sine)
        
        # ==========================================
        # 45-50s
        # ==========================================
        self.play(
            FadeOut(exp_axes), FadeOut(exp_curve), FadeOut(t_val), FadeOut(final_val),
            run_time=1
        )
        
        self.play(formula3.animate.move_to(UP*1.5), run_time=0.5)
        
        boxed_formula = MathTex("\\boxed{A = P(1+r)^t}", font_size=90).move_to(UP*1.5)
        self.play(Transform(formula3, boxed_formula), run_time=1)
        
        quote = Tex("\\boxed{\\text{Le temps transforme une}}", "\\\\", "\\boxed{\\text{petite différence en}}", "\\\\", "\\boxed{\\text{énorme différence.}}", font_size=48).next_to(formula3, DOWN*2)
        self.play(Write(quote), run_time=2)
        
        self.wait(1)
        self.play(FadeOut(formula3), FadeOut(quote), run_time=2)
