from manim import *
import math

# Format TikTok 9:16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 60
config.frame_width = 9
config.frame_height = 16

ORANGE = "#F7931A"
GREEN = "#39FF14"
RED = "#FF003C"
CYAN = "#00FFFF"
MAGENTA = "#FF00FF"
YELLOW = "#FFD700"

def create_clock(radius=0.5, color=WHITE):
    clock_group = VGroup()
    circle = Circle(radius=radius, color=color, stroke_width=3)
    center_dot = Dot(radius=0.05, color=color)
    hand = Line(ORIGIN, UP * (radius * 0.8), color=color, stroke_width=3)
    clock_group.add(circle, center_dot, hand)
    return clock_group

class TimeDilation(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # =====================================================
        # 0–4s — Grille spatiale et Trou Noir
        # =====================================================
        grid = NumberPlane(
            x_range=[-10, 10, 1],
            y_range=[-12, 12, 1],
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1, "stroke_opacity": 0.5},
            faded_line_ratio=1
        )
        self.play(Create(grid, lag_ratio=0.01), run_time=1.5)

        bh = Circle(radius=0.8, color=BLACK, fill_opacity=1, stroke_color=CYAN, stroke_width=2).move_to(DOWN * 2)
        bh_glow = Circle(radius=0.9, color=CYAN, fill_opacity=0.2, stroke_width=0).move_to(DOWN * 2)
        
        self.play(FadeIn(bh_glow), FadeIn(bh), run_time=0.8)
        
        intro_text = Text(
            "Time doesn't pass at the\nsame speed everywhere.",
            font_size=35, color=WHITE, line_spacing=1.2
        ).move_to(UP * 5)
        self.play(Write(intro_text), run_time=1.2)
        self.wait(1)
        self.play(FadeOut(intro_text), run_time=0.5)

        # =====================================================
        # 4–10s — Les deux horloges qui tournent
        # =====================================================
        clock_far = create_clock(0.5, CYAN).move_to(UP * 4)
        label_far = Text("FAR", font_size=25, color=CYAN).next_to(clock_far, UP)
        
        clock_close = create_clock(0.5, ORANGE).move_to(DOWN * 0.5)
        label_close = Text("CLOSE", font_size=25, color=ORANGE).next_to(clock_close, UP)

        self.play(FadeIn(clock_far), FadeIn(label_far), FadeIn(clock_close), FadeIn(label_close), run_time=0.8)

        # Animation des horloges (mains qui tournent)
        hand_far = clock_far[2]
        hand_close = clock_close[2]

        t_tracker = ValueTracker(0)

        # L'horloge éloignée tourne vite (facteur 1)
        hand_far.add_updater(lambda m: m.set_angle(PI/2 - t_tracker.get_value() * 3))
        # L'horloge proche tourne lentement (facteur 0.2)
        hand_close.add_updater(lambda m: m.set_angle(PI/2 - t_tracker.get_value() * 0.6))

        self.play(t_tracker.animate.set_value(TAU * 2), run_time=4, rate_func=linear)
        
        # Arrêt des updaters pour nettoyer
        hand_far.clear_updaters()
        hand_close.clear_updaters()

        self.play(FadeOut(VGroup(clock_far, label_far, clock_close, label_close)), run_time=0.4)

        # =====================================================
        # 10–18s — La Formule de Dilatation
        # =====================================================
        formula = MathTex(
            r"t =", r"\frac{t_0}{\sqrt{1 - \frac{2GM}{rc^2}}}",
            font_size=60, color=WHITE
        ).move_to(UP * 5)
        
        self.play(Write(formula[0]), run_time=0.5)
        self.play(Write(formula[1]), run_time=1.5)
        self.wait(0.5)

        # Extraction de r_s
        rs_formula = MathTex(
            r"r_s =", r"\frac{2GM}{c^2}",
            font_size=50, color=CYAN
        ).move_to(UP * 3)
        self.play(FadeIn(rs_formula, shift=UP), run_time=0.8)
        self.wait(0.5)

        rs_circle = DashedVMobject(Circle(radius=1.5, color=RED), num_dashes=30).move_to(DOWN * 2)
        rs_label = MathTex(r"r_s", font_size=30, color=RED).next_to(rs_circle, RIGHT)
        self.play(Create(rs_circle), FadeIn(rs_label), run_time=1)
        self.wait(1)

        self.play(FadeOut(VGroup(formula, rs_formula)), run_time=0.5)

        # =====================================================
        # 18–28s — Éloignement / Rapprochement de la caméra
        # =====================================================
        # On va créer une nouvelle horloge dont la vitesse dépend de sa distance `r`
        r_tracker = ValueTracker(3) # Distance par rapport au trou noir (centre DOWN*2)
        
        dynamic_clock = create_clock(0.6, YELLOW)
        d_hand = dynamic_clock[2]
        
        dynamic_clock.add_updater(lambda m: m.move_to(DOWN * 2 + UP * r_tracker.get_value()))
        
        global_time = ValueTracker(0)
        
        # t_speed = sqrt(1 - rs/r) avec rs=1.5
        def get_speed():
            r = max(r_tracker.get_value(), 1.501)
            return math.sqrt(1 - 1.5/r)

        # On triche un peu sur l'intégration du temps : on l'ajoute manuellement à chaque frame
        accumulated_angle = [PI/2]
        def update_hand(m, dt):
            speed = get_speed() * 4  # multiplicateur pour que ça tourne vite
            accumulated_angle[0] -= speed * dt
            m.set_angle(accumulated_angle[0])

        d_hand.add_updater(update_hand)
        
        self.play(FadeIn(dynamic_clock), run_time=0.5)
        
        # S'éloigne (r augmente, horloge accélère)
        self.play(r_tracker.animate.set_value(7), run_time=2.5)
        self.wait(1)
        
        # Se rapproche (r diminue, horloge ralentit énormément)
        self.play(r_tracker.animate.set_value(1.6), run_time=3)
        self.wait(1)
        
        d_hand.clear_updaters()
        dynamic_clock.clear_updaters()
        self.play(FadeOut(dynamic_clock), run_time=0.4)

        # =====================================================
        # 28–38s — Comparaison : Loin vs Près (désynchronisation)
        # =====================================================
        comp_title = Text("DESYNCHRONIZATION", font_size=40, color=ORANGE, weight=BOLD).move_to(UP * 6)
        self.play(FadeIn(comp_title, shift=DOWN), run_time=0.5)

        label_t0 = MathTex("t_0", font_size=40, color=CYAN).move_to(LEFT * 2 + UP * 4.5)
        label_t = MathTex("t > t_0", font_size=40, color=ORANGE).move_to(RIGHT * 2 + UP * 4.5)
        
        far_text = Text("FAR", font_size=25, color=CYAN).next_to(label_t0, UP)
        close_text = Text("CLOSE", font_size=25, color=ORANGE).next_to(label_t, UP)
        
        self.play(FadeIn(VGroup(label_t0, label_t, far_text, close_text)), run_time=0.5)
        
        # Timeline qui s'allonge plus vite pour l'un que pour l'autre
        line_far = Line(LEFT * 2 + UP * 4, LEFT * 2 + UP * 3.99, color=CYAN, stroke_width=6)
        line_close = Line(RIGHT * 2 + UP * 4, RIGHT * 2 + UP * 3.99, color=ORANGE, stroke_width=6)
        self.add(line_far, line_close)
        
        def update_line_far(m, dt):
            m.put_start_and_end_on(LEFT * 2 + UP * 4, m.get_end() + DOWN * 1.5 * dt)
            
        def update_line_close(m, dt):
            m.put_start_and_end_on(RIGHT * 2 + UP * 4, m.get_end() + DOWN * 0.3 * dt)

        line_far.add_updater(update_line_far)
        line_close.add_updater(update_line_close)
        
        self.wait(3)
        
        line_far.clear_updaters()
        line_close.clear_updaters()

        self.play(FadeOut(VGroup(comp_title, label_t0, label_t, far_text, close_text, line_far, line_close)), run_time=0.5)

        # =====================================================
        # 38–48s — r -> rs (limite)
        # =====================================================
        near_horizon = Text("Approaching the Event Horizon", font_size=35, color=RED).move_to(UP * 6)
        self.play(FadeIn(near_horizon), run_time=0.5)

        big_formula = MathTex(
            r"\sqrt{1 - \frac{r_s}{r}} \rightarrow 0",
            font_size=70, color=WHITE
        ).move_to(UP * 4)
        
        self.play(Write(big_formula), run_time=1.5)
        
        clock_freeze = create_clock(1, RED).move_to(DOWN * 2)
        
        self.play(FadeIn(clock_freeze), run_time=0.5)
        self.play(big_formula.animate.scale(1.5), clock_freeze.animate.scale(1.2), run_time=2)
        
        freeze_text = Text("Time freezes.", font_size=50, color=RED, weight=BOLD).move_to(UP * 1.5)
        self.play(FadeIn(freeze_text, scale=2), run_time=1)
        self.wait(1.5)

        self.play(FadeOut(VGroup(grid, bh, bh_glow, rs_circle, rs_label, near_horizon, big_formula, clock_freeze, freeze_text)), run_time=1)

        # =====================================================
        # OUTRO
        # =====================================================
        outro1 = Text("Space and time are not separated.", font_size=40, color=WHITE)
        outro2 = Text("SPACETIME", font_size=70, color=CYAN, weight=BOLD)
        
        self.play(Write(outro1), run_time=1.5)
        self.wait(1)
        self.play(ReplacementTransform(outro1, outro2), run_time=1)
        self.play(Flash(outro2, color=CYAN), run_time=0.5)
        self.wait(2)
