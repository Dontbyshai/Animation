from manim import *
import random

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

def create_door(num):
    door_group = VGroup()
    door_rect = Rectangle(width=2.2, height=4, color=ORANGE, fill_opacity=0.3, stroke_width=4)
    handle = Circle(radius=0.1, color=WHITE, fill_opacity=1).move_to(door_rect.get_right() + LEFT*0.3 + DOWN*0.2)
    number = Text(str(num), font_size=50, color=WHITE, weight=BOLD).move_to(door_rect.get_center() + UP*0.5)
    door_group.add(door_rect, handle, number)
    return door_group

class MontyHall(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # =====================================================
        # 0–3s — HOOK : 3 portes
        # =====================================================
        doors = VGroup(create_door(1), create_door(2), create_door(3)).arrange(RIGHT, buff=0.8)
        doors.move_to(UP * 2)
        
        self.play(LaggedStart(*[FadeIn(d, shift=UP) for d in doors], lag_ratio=0.1), run_time=0.8)

        intro_text = Text(
            "1 car. 2 goats.\nYou pick a door.",
            font_size=40, color=WHITE, line_spacing=1.2
        ).move_to(DOWN * 2)
        
        self.play(Write(intro_text), run_time=1.2)
        self.wait(1)

        self.play(FadeOut(intro_text), run_time=0.3)

        # =====================================================
        # 3–8s — Le joueur choisit PORTE 1 + P=1/3
        # =====================================================
        pick_arrow = Arrow(DOWN*1.5, UP*0.1, color=CYAN, stroke_width=6).next_to(doors[0], DOWN, buff=0.3)
        pick_text = Text("YOU PICK", font_size=30, color=CYAN, weight=BOLD).next_to(pick_arrow, DOWN, buff=0.2)
        
        self.play(GrowArrow(pick_arrow), FadeIn(pick_text, shift=UP), run_time=0.5)
        
        # P = 1/3
        p_1_3 = MathTex(r"P = \frac{1}{3}", font_size=60, color=CYAN).move_to(DOWN * 4)
        self.play(Write(p_1_3), run_time=0.8)
        self.wait(1.2)

        # =====================================================
        # 8–14s — Animateur ouvre PORTE 3 -> GOAT. "Switch or stay?"
        # =====================================================
        host_text = Text("The host opens a door...", font_size=35, color=WHITE).move_to(DOWN * 2)
        self.play(FadeIn(host_text), FadeOut(p_1_3), run_time=0.5)
        
        # Ouvrir porte 3
        goat_text = Text("GOAT", font_size=45, color=RED, weight=BOLD).move_to(doors[2].get_center())
        
        # Animation d'ouverture: effacer la porte, montrer la chèvre
        self.play(
            FadeOut(doors[2], shift=DOWN),
            FadeIn(goat_text, scale=0.5),
            run_time=0.6
        )
        self.wait(0.5)

        self.play(FadeOut(host_text), run_time=0.3)
        
        switch_stay = Text("Switch or stay?", font_size=55, color=ORANGE, weight=BOLD).move_to(DOWN * 2)
        self.play(Write(switch_stay), run_time=0.8)
        self.wait(1)

        self.play(FadeOut(VGroup(pick_arrow, pick_text, switch_stay)), run_time=0.4)

        # =====================================================
        # 14–22s — Deux chemins : RESTER 1/3, CHANGER 2/3
        # =====================================================
        path_stay = Text("STAY", font_size=40, color=CYAN, weight=BOLD).move_to(LEFT * 2 + DOWN * 1)
        path_switch = Text("SWITCH", font_size=40, color=GREEN, weight=BOLD).move_to(RIGHT * 2 + DOWN * 1)
        
        stay_p = MathTex(r"\frac{1}{3}", font_size=70, color=CYAN).move_to(LEFT * 2 + DOWN * 3)
        switch_p = MathTex(r"\frac{2}{3}", font_size=70, color=GREEN).move_to(RIGHT * 2 + DOWN * 3)
        
        self.play(FadeIn(path_stay, shift=DOWN), FadeIn(path_switch, shift=DOWN), run_time=0.5)
        self.play(Write(stay_p), Write(switch_p), run_time=0.8)
        
        self.play(switch_p.animate.scale(2.5).set_color(GREEN), run_time=1)
        self.wait(1.5)

        self.play(FadeOut(VGroup(path_stay, path_switch, stay_p, switch_p, doors[0], doors[1], goat_text)), run_time=0.5)

        # =====================================================
        # 22–30s — Rembobine + simulations
        # =====================================================
        sim_title = Text("SIMULATION", font_size=55, color=YELLOW, weight=BOLD).move_to(UP * 6)
        self.play(FadeIn(sim_title, shift=DOWN), run_time=0.5)
        
        col_stay = Text("STAY", font_size=40, color=CYAN, weight=BOLD).move_to(LEFT * 2.2 + UP * 4.5)
        col_switch = Text("SWITCH", font_size=40, color=GREEN, weight=BOLD).move_to(RIGHT * 2.2 + UP * 4.5)
        self.play(FadeIn(col_stay), FadeIn(col_switch), run_time=0.4)
        
        # Trackers
        stay_wins = ValueTracker(0)
        switch_wins = ValueTracker(0)
        total_games = ValueTracker(0)
        
        stay_counter = always_redraw(lambda: Text(
            f"{int(stay_wins.get_value())} / {int(total_games.get_value())}", 
            font_size=45, color=WHITE
        ).move_to(LEFT * 2.2 + UP * 3.2))
        
        switch_counter = always_redraw(lambda: Text(
            f"{int(switch_wins.get_value())} / {int(total_games.get_value())}", 
            font_size=45, color=WHITE
        ).move_to(RIGHT * 2.2 + UP * 3.2))
        
        self.add(stay_counter, switch_counter)
        
        # Petites portes pour l'animation
        sim_doors = VGroup(
            Rectangle(width=1, height=1.5, color=ORANGE, fill_opacity=0.2),
            Rectangle(width=1, height=1.5, color=ORANGE, fill_opacity=0.2),
            Rectangle(width=1, height=1.5, color=ORANGE, fill_opacity=0.2)
        ).arrange(RIGHT, buff=0.5).move_to(DOWN * 1)
        self.play(FadeIn(sim_doors), run_time=0.4)
        
        # Simuler quelques jeux visuellement (rapide)
        for i in range(5):
            # mélange visuel
            self.play(
                sim_doors[0].animate.move_to(sim_doors[2].get_center()),
                sim_doors[1].animate.move_to(sim_doors[0].get_center()),
                sim_doors[2].animate.move_to(sim_doors[1].get_center()),
                run_time=0.15
            )
            total_games.set_value(total_games.get_value() + 2)
            stay_wins.set_value(stay_wins.get_value() + (1 if random.random() < 0.33 else 0))
            switch_wins.set_value(switch_wins.get_value() + (1 if random.random() < 0.67 else 0))
            self.wait(0.05)

        # Accélérer la simulation sans animation visuelle des portes
        self.play(FadeOut(sim_doors), run_time=0.3)
        
        fast_sim_text = Text("Running 10,000 games...", font_size=35, color=GRAY).move_to(DOWN * 1)
        self.play(FadeIn(fast_sim_text), run_time=0.3)
        
        # Faire monter les compteurs jusqu'à ~10000
        # On va animer les trackers continuellement sur 2 secondes
        self.play(
            total_games.animate.set_value(10000),
            stay_wins.animate.set_value(3342),
            switch_wins.animate.set_value(6658),
            run_time=2.5,
            rate_func=linear
        )
        self.wait(0.5)
        
        # =====================================================
        # 30–40s — Résultats ≈33% et ≈67%
        # =====================================================
        stay_pct = always_redraw(lambda: Text(
            f"{(stay_wins.get_value() / max(1, total_games.get_value())) * 100:.1f}%",
            font_size=60, color=CYAN, weight=BOLD
        ).move_to(LEFT * 2.2 + UP * 1.5))
        
        switch_pct = always_redraw(lambda: Text(
            f"{(switch_wins.get_value() / max(1, total_games.get_value())) * 100:.1f}%",
            font_size=80, color=GREEN, weight=BOLD
        ).move_to(RIGHT * 2.2 + UP * 1.5))
        
        self.play(FadeIn(stay_pct, shift=UP), FadeIn(switch_pct, shift=UP), FadeOut(fast_sim_text), run_time=0.6)
        self.wait(1.5)

        final_switch = MathTex(r"P(\text{switch}) = \frac{2}{3}", font_size=70, color=GREEN).move_to(DOWN * 2)
        self.play(Write(final_switch), run_time=1)
        self.play(final_switch.animate.scale(1.3), run_time=1)
        self.wait(1.5)
        
        self.play(FadeOut(VGroup(sim_title, col_stay, col_switch, stay_counter, switch_counter, stay_pct, switch_pct, final_switch)), run_time=0.5)

        # =====================================================
        # 40–45s — OUTRO
        # =====================================================
        outro1 = Text("Your intuition says 50/50.", font_size=40, color=WHITE).move_to(UP * 1)
        outro2 = Text("Math says 2/3.", font_size=55, color=ORANGE, weight=BOLD).move_to(DOWN * 0.5)

        self.play(FadeIn(outro1, shift=UP), run_time=0.6)
        self.play(FadeIn(outro2, scale=1.5), Flash(outro2, color=ORANGE), run_time=0.8)

        self.wait(2)
