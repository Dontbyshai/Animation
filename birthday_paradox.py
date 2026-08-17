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


class BirthdayParadox(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # =====================================================
        # 0–3s — HOOK : 23 silhouettes + question
        # =====================================================
        # 23 petits cercles comme silhouettes
        silhouettes = VGroup()
        for i in range(23):
            row = i // 8
            col = i % 8
            dot = Circle(radius=0.2, color=CYAN, fill_opacity=0.6, stroke_width=1)
            dot.move_to(LEFT * 2.8 + RIGHT * col * 0.8 + UP * 4 - DOWN * row * 0.9)
            silhouettes.add(dot)

        self.play(LaggedStart(*[FadeIn(s, scale=0.3) for s in silhouettes], lag_ratio=0.02), run_time=0.8)

        question = Text(
            "How many people for a 50%\nchance two share a birthday?",
            font_size=30, color=WHITE
        ).move_to(DOWN * 0.5)
        self.play(Write(question), run_time=1.2)
        self.wait(0.3)

        self.play(FadeOut(question), FadeOut(silhouettes), run_time=0.3)

        big_23 = Text("23", font_size=250, color=CYAN, weight=BOLD).move_to(ORIGIN)
        self.play(FadeIn(big_23, scale=0.2), Flash(big_23, color=CYAN, line_length=2, num_lines=12), run_time=0.6)
        self.wait(0.8)
        self.play(FadeOut(big_23), run_time=0.3)

        # =====================================================
        # 3–10s — 23 personnes sur un cercle + paires
        # =====================================================
        # Cercle de 23 points
        circle_dots = VGroup()
        circle_labels = VGroup()
        radius = 3.5
        center = DOWN * 1

        for i in range(23):
            angle = i * TAU / 23 + PI / 2
            pos = center + radius * np.array([math.cos(angle), math.sin(angle), 0])
            dot = Dot(pos, color=CYAN, radius=0.12)
            circle_dots.add(dot)

        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in circle_dots], lag_ratio=0.03), run_time=1)

        # Montrer quelques dates
        sample_dates = ["Jan 5", "Mar 12", "Jul 8", "Nov 23", "Feb 14"]
        date_labels = VGroup()
        for i, date in enumerate(sample_dates):
            label = Text(date, font_size=16, color=WHITE).next_to(circle_dots[i], UP, buff=0.15)
            date_labels.add(label)

        self.play(LaggedStart(*[FadeIn(l) for l in date_labels], lag_ratio=0.1), run_time=0.6)
        self.wait(0.3)
        self.play(FadeOut(date_labels), run_time=0.2)

        # Montrer les connexions d'une personne
        person_lines = VGroup()
        for j in range(1, 23):
            line = Line(circle_dots[0].get_center(), circle_dots[j].get_center(), color=ORANGE, stroke_width=1, stroke_opacity=0.5)
            person_lines.add(line)

        pair_text = Text("1 person → 22 comparisons", font_size=30, color=ORANGE).move_to(UP * 6)
        self.play(FadeIn(pair_text), LaggedStart(*[Create(l) for l in person_lines], lag_ratio=0.03), run_time=1)
        self.wait(0.8)

        self.play(FadeOut(person_lines), FadeOut(pair_text), run_time=0.3)

        # =====================================================
        # 10–18s — Formule P(aucune correspondance)
        # =====================================================
        self.play(FadeOut(circle_dots), run_time=0.3)

        formula_title = Text("P(no match)", font_size=45, color=RED, weight=BOLD).move_to(UP * 6)
        self.play(FadeIn(formula_title, shift=DOWN), run_time=0.4)

        # Fractions qui apparaissent une par une
        fracs = []
        frac_strs = [
            r"\frac{365}{365}",
            r"\cdot \frac{364}{365}",
            r"\cdot \frac{363}{365}",
            r"\cdot \frac{362}{365}",
            r"\cdots",
            r"\cdot \frac{343}{365}",
        ]

        # Ligne 1
        line1 = MathTex(
            r"\frac{365}{365}", r"\cdot", r"\frac{364}{365}", r"\cdot", r"\frac{363}{365}",
            font_size=42, color=WHITE
        ).move_to(UP * 3)

        # Ligne 2
        line2 = MathTex(
            r"\cdot", r"\frac{362}{365}", r"\cdots", r"\frac{343}{365}",
            font_size=42, color=WHITE
        ).move_to(UP * 1)

        self.play(Write(line1), run_time=1.5)
        self.play(Write(line2), run_time=1)

        # Probabilité qui diminue
        prob_result = MathTex(r"= 0.4927...", font_size=55, color=RED).move_to(DOWN * 1.5)
        self.play(Write(prob_result), run_time=0.8)

        pct_49 = Text("49.3%", font_size=70, color=RED, weight=BOLD).move_to(DOWN * 4)
        self.play(FadeIn(pct_49, scale=1.3), run_time=0.5)
        self.wait(1)

        self.play(FadeOut(VGroup(formula_title, line1, line2, prob_result, pct_49)), run_time=0.4)

        # =====================================================
        # 18–26s — Jauge + P(au moins une)
        # =====================================================
        comp_title = Text("P(at least one match)", font_size=40, color=GREEN, weight=BOLD).move_to(UP * 5)
        self.play(FadeIn(comp_title, shift=DOWN), run_time=0.4)

        comp_formula = MathTex(
            r"P(\text{match}) = 1 - P(\text{no match})",
            font_size=40, color=WHITE
        ).move_to(UP * 2.5)
        self.play(Write(comp_formula), run_time=1)

        # Jauge horizontale
        gauge_bg = Rectangle(width=7, height=1, color=GRAY, fill_opacity=0.15, stroke_width=1).move_to(DOWN * 0.5)
        gauge_fill = Rectangle(width=7 * 0.507, height=1, color=GREEN, fill_opacity=0.7, stroke_width=0)
        gauge_fill.move_to(gauge_bg.get_left() + RIGHT * (7 * 0.507 / 2), aligned_edge=ORIGIN)
        gauge_fill.align_to(gauge_bg, LEFT)

        label_0 = Text("0%", font_size=24, color=GRAY).next_to(gauge_bg, LEFT, buff=0.2)
        label_100 = Text("100%", font_size=24, color=GRAY).next_to(gauge_bg, RIGHT, buff=0.2)

        self.play(FadeIn(gauge_bg), FadeIn(label_0), FadeIn(label_100), run_time=0.3)

        # Animer le remplissage
        gauge_fill_anim = Rectangle(width=0.01, height=1, color=GREEN, fill_opacity=0.7, stroke_width=0)
        gauge_fill_anim.align_to(gauge_bg, LEFT)
        self.add(gauge_fill_anim)

        self.play(gauge_fill_anim.animate.become(gauge_fill), run_time=1.5)

        # Résultat
        result_pct = Text("50.7%", font_size=90, color=GREEN, weight=BOLD).move_to(DOWN * 3.5)
        self.play(FadeIn(result_pct, scale=1.5), Flash(result_pct, color=GREEN, line_length=1.5), run_time=0.6)
        self.wait(1.2)

        self.play(FadeOut(VGroup(comp_title, comp_formula, gauge_bg, gauge_fill_anim, label_0, label_100, result_pct)), run_time=0.4)

        # =====================================================
        # 26–35s — 253 paires explosent
        # =====================================================
        pairs_title = Text("POSSIBLE PAIRS", font_size=45, color=ORANGE, weight=BOLD).move_to(UP * 6)
        self.play(FadeIn(pairs_title, shift=DOWN), run_time=0.4)

        # Formule combinaison
        comb_formula = MathTex(r"\binom{23}{2} = 253", font_size=60, color=ORANGE).move_to(UP * 3.5)
        self.play(Write(comb_formula), run_time=0.8)

        # Recréer le cercle de 23 personnes
        circle_dots2 = VGroup()
        radius2 = 2.8
        center2 = DOWN * 2

        for i in range(23):
            angle = i * TAU / 23 + PI / 2
            pos = center2 + radius2 * np.array([math.cos(angle), math.sin(angle), 0])
            dot = Dot(pos, color=CYAN, radius=0.08)
            circle_dots2.add(dot)

        self.play(LaggedStart(*[FadeIn(d) for d in circle_dots2], lag_ratio=0.02), run_time=0.5)

        # 253 connexions
        all_lines = VGroup()
        for i in range(23):
            for j in range(i + 1, 23):
                line = Line(
                    circle_dots2[i].get_center(),
                    circle_dots2[j].get_center(),
                    color=ORANGE, stroke_width=0.5, stroke_opacity=0.3
                )
                all_lines.add(line)

        self.play(LaggedStart(*[Create(l) for l in all_lines], lag_ratio=0.005), run_time=2.5)

        pairs_count = Text("253 pairs!", font_size=50, color=ORANGE, weight=BOLD).move_to(DOWN * 6.5)
        self.play(FadeIn(pairs_count, scale=1.3), run_time=0.4)
        self.wait(1)

        self.play(FadeOut(VGroup(pairs_title, comb_formula, circle_dots2, all_lines, pairs_count)), run_time=0.5)

        # =====================================================
        # 35–45s — Probabilité qui monte avec n
        # =====================================================
        growth_title = Text("AS n GROWS...", font_size=45, color=CYAN, weight=BOLD).move_to(UP * 6)
        self.play(FadeIn(growth_title, shift=DOWN), run_time=0.4)

        # Tableau n → P
        data = [
            (10, "11.7%"),
            (20, "41.1%"),
            (23, "50.7%"),
            (30, "70.6%"),
            (50, "97.0%"),
            (70, "99.9%"),
        ]

        table_entries = VGroup()
        for i, (n, p) in enumerate(data):
            n_text = Text(f"n = {n}", font_size=32, color=CYAN).move_to(LEFT * 2 + UP * (3.5 - i * 1.3))
            p_text = Text(p, font_size=32, color=GREEN, weight=BOLD).move_to(RIGHT * 2 + UP * (3.5 - i * 1.3))
            row = VGroup(n_text, p_text)
            table_entries.add(row)

        for row in table_entries:
            self.play(FadeIn(row, shift=LEFT), run_time=0.25)

        self.wait(0.8)

        # Highlight n=23
        highlight = SurroundingRectangle(table_entries[2], color=YELLOW, buff=0.15)
        self.play(Create(highlight), run_time=0.4)
        self.wait(0.5)

        self.play(FadeOut(VGroup(growth_title, table_entries, highlight)), run_time=0.4)

        # Message final
        msg1 = Text("It's not the number of people.", font_size=36, color=WHITE).move_to(UP * 2)
        msg2 = Text("It's the number of PAIRS.", font_size=40, color=ORANGE, weight=BOLD).move_to(DOWN * 0.5)

        self.play(FadeIn(msg1, shift=RIGHT), run_time=0.6)
        self.play(FadeIn(msg2, scale=1.3), run_time=0.6)
        self.wait(0.8)

        self.play(FadeOut(VGroup(msg1, msg2)), run_time=0.4)

        # Formule finale
        final_formula = MathTex(
            r"\binom{n}{2} = \frac{n(n-1)}{2}",
            font_size=60, color=CYAN
        ).move_to(ORIGIN)

        self.play(Write(final_formula), run_time=1.5)
        self.play(final_formula.animate.scale(1.3), run_time=0.8)
        self.wait(1.5)

        self.play(FadeOut(final_formula), run_time=0.5)
        self.wait(0.5)
