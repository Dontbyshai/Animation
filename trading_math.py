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
DARK_RED = "#8B0000"


class TradingMath(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # =====================================================
        # 0–3s — HOOK : Portefeuille 100€ → -50% → 50€
        # =====================================================
        wallet_label = Text("PORTFOLIO", font_size=35, color=GRAY).move_to(UP * 5)
        amount = Text("100 €", font_size=120, color=WHITE, weight=BOLD).move_to(UP * 2)

        self.play(FadeIn(wallet_label), FadeIn(amount, scale=0.5), run_time=0.6)
        self.wait(0.4)

        # Flash rouge -50%
        loss = Text("-50%", font_size=150, color=RED, weight=BOLD).move_to(ORIGIN)
        self.play(FadeIn(loss, scale=3), Flash(loss, color=RED, line_length=2, num_lines=12), run_time=0.5)
        self.wait(0.3)

        # 100 → 50
        new_amount = Text("50 €", font_size=120, color=RED, weight=BOLD).move_to(UP * 2)
        self.play(
            ReplacementTransform(amount, new_amount),
            FadeOut(loss),
            run_time=0.6
        )

        hook_text = Text("You just lost half your money.", font_size=32, color=WHITE).move_to(DOWN * 2)
        self.play(FadeIn(hook_text, shift=UP), run_time=0.5)
        self.wait(0.8)

        self.play(FadeOut(VGroup(wallet_label, new_amount, hook_text)), run_time=0.4)

        # =====================================================
        # 3–8s — Combien pour revenir à 100€ ?
        # =====================================================
        big_50 = Text("50 €", font_size=140, color=RED, weight=BOLD).move_to(UP * 3)
        self.play(FadeIn(big_50, scale=0.5), run_time=0.5)

        question = Text("How much to get back\nto 100 € ?", font_size=36, color=WHITE).move_to(UP * 0.5)
        self.play(Write(question), run_time=1)
        self.wait(0.5)

        # Barre animée de 50 à 100
        self.play(FadeOut(question), run_time=0.3)

        bar_bg = Rectangle(width=4, height=0.8, color=GRAY, fill_opacity=0.2).move_to(DOWN * 0.5)
        bar_fill = Rectangle(width=2, height=0.8, color=RED, fill_opacity=0.8).move_to(bar_bg.get_left() + RIGHT * 1, aligned_edge=LEFT)
        label_50 = Text("50€", font_size=28, color=RED).next_to(bar_fill, LEFT, buff=0.3)
        label_100 = Text("100€", font_size=28, color=GREEN).next_to(bar_bg, RIGHT, buff=0.3)

        self.play(FadeIn(bar_bg), FadeIn(bar_fill), FadeIn(label_50), FadeIn(label_100), run_time=0.5)

        # Barre grandit de 50 à 100
        bar_full = Rectangle(width=4, height=0.8, color=GREEN, fill_opacity=0.8).move_to(bar_bg.get_left() + RIGHT * 2, aligned_edge=LEFT)
        plus_50 = Text("+50 €", font_size=50, color=GREEN, weight=BOLD).move_to(DOWN * 2.5)

        self.play(Transform(bar_fill, bar_full), run_time=1)
        self.play(FadeIn(plus_50, scale=1.3), run_time=0.4)

        # Le pourcentage qui apparaît
        pct = Text("+100%", font_size=100, color=GREEN, weight=BOLD).move_to(DOWN * 5)
        self.play(FadeIn(pct, scale=2), Flash(pct, color=GREEN, line_length=1.5), run_time=0.6)
        self.wait(1)

        self.play(FadeOut(VGroup(big_50, bar_bg, bar_fill, label_50, label_100, plus_50, pct)), run_time=0.4)

        # =====================================================
        # 8–15s — Deux colonnes PERTE / RÉCUPÉRATION
        # =====================================================
        col_loss_title = Text("LOSS", font_size=45, color=RED, weight=BOLD).move_to(LEFT * 2.2 + UP * 5)
        col_gain_title = Text("RECOVERY", font_size=45, color=GREEN, weight=BOLD).move_to(RIGHT * 2.2 + UP * 5)

        self.play(FadeIn(col_loss_title, shift=DOWN), FadeIn(col_gain_title, shift=DOWN), run_time=0.5)

        # Formule perte
        loss_formula = MathTex(r"100 \times (1 - 0.5) = 50", font_size=38, color=RED)
        loss_formula.move_to(LEFT * 2.2 + UP * 2.5)

        # Formule récupération
        gain_formula = MathTex(r"50 \times (1 + 1) = 100", font_size=38, color=GREEN)
        gain_formula.move_to(RIGHT * 2.2 + UP * 2.5)

        self.play(Write(loss_formula), run_time=1)
        self.play(Write(gain_formula), run_time=1)

        # Connexion visuelle entre les deux
        connect_line = Line(
            loss_formula.get_right() + RIGHT * 0.2,
            gain_formula.get_left() + LEFT * 0.2,
            color=YELLOW, stroke_width=3
        )
        connect_dot1 = Dot(loss_formula.get_right() + RIGHT * 0.2, color=YELLOW, radius=0.08)
        connect_dot2 = Dot(gain_formula.get_left() + LEFT * 0.2, color=YELLOW, radius=0.08)

        self.play(Create(connect_line), FadeIn(connect_dot1), FadeIn(connect_dot2), run_time=0.5)

        # 50 ↔ 50 mais les % sont différents
        diff_text = MathTex(r"-50\% \neq +50\%", font_size=55, color=YELLOW).move_to(DOWN * 1)
        self.play(Write(diff_text), run_time=0.8)
        self.wait(1.5)

        self.play(FadeOut(VGroup(col_loss_title, col_gain_title, loss_formula, gain_formula, connect_line, connect_dot1, connect_dot2, diff_text)), run_time=0.4)

        # =====================================================
        # 15–23s — CASCADE : -20% × 3 ≠ -60%
        # =====================================================
        cascade_title = Text("COMPOUNDING LOSSES", font_size=45, color=RED, weight=BOLD).move_to(UP * 6)
        self.play(FadeIn(cascade_title, shift=DOWN), run_time=0.5)

        # Cascade animée
        values = [100, 80, 64, 51.2]
        y_positions = [4, 2, 0, -2]
        cascade_texts = []
        arrows = []

        for i, (val, y) in enumerate(zip(values, y_positions)):
            color = WHITE if i == 0 else RED
            t = Text(f"{val}", font_size=60, color=color, weight=BOLD).move_to(UP * y)
            cascade_texts.append(t)

            if i == 0:
                self.play(FadeIn(t, scale=0.5), run_time=0.3)
            else:
                pct_label = Text("-20%", font_size=30, color=RED).move_to(UP * (y_positions[i-1] + y) / 2 + RIGHT * 2)
                arr = Arrow(
                    cascade_texts[i-1].get_bottom(),
                    t.get_top(),
                    color=RED, stroke_width=2
                )
                arrows.append(arr)
                self.play(GrowArrow(arr), FadeIn(pct_label), FadeIn(t, shift=DOWN), run_time=0.4)

        self.wait(0.5)

        # "Ce n'est PAS -60%"
        not_60 = Text("This is NOT -60%", font_size=40, color=YELLOW, weight=BOLD).move_to(DOWN * 4.5)
        self.play(FadeIn(not_60, shift=UP), run_time=0.5)
        self.wait(0.5)

        # Formule exacte
        self.play(FadeOut(not_60), run_time=0.3)
        compound_formula = MathTex(r"100 \times (0.8)^3 = 51.2", font_size=50, color=CYAN).move_to(DOWN * 4.5)
        self.play(Write(compound_formula), run_time=1)

        real_pct = Text("-48.8%", font_size=70, color=RED, weight=BOLD).move_to(DOWN * 6.5)
        self.play(FadeIn(real_pct, scale=1.5), Flash(real_pct, color=RED), run_time=0.5)
        self.wait(1)

        # Cleanup
        all_cascade = VGroup(cascade_title, compound_formula, real_pct, *cascade_texts, *arrows)
        # Also fade out any remaining pct_labels (they're not tracked, use self.clear approach)
        self.play(FadeOut(all_cascade), run_time=0.4)
        self.clear()

        # =====================================================
        # 23–32s — INVERSE : gains composés + courbe exponentielle
        # =====================================================
        gains_title = Text("COMPOUNDING GAINS", font_size=45, color=GREEN, weight=BOLD).move_to(UP * 6)
        self.play(FadeIn(gains_title, shift=DOWN), run_time=0.5)

        gain_values = [100, 120, 144, 172.8]
        g_y_positions = [4, 2, 0, -2]
        gain_texts = []
        gain_arrows = []

        for i, (val, y) in enumerate(zip(gain_values, g_y_positions)):
            color = WHITE if i == 0 else GREEN
            t = Text(f"{val}", font_size=60, color=color, weight=BOLD).move_to(UP * y)
            gain_texts.append(t)

            if i == 0:
                self.play(FadeIn(t, scale=0.5), run_time=0.3)
            else:
                pct_label = Text("+20%", font_size=30, color=GREEN).move_to(UP * (g_y_positions[i-1] + y) / 2 + RIGHT * 2)
                arr = Arrow(
                    gain_texts[i-1].get_bottom(),
                    t.get_top(),
                    color=GREEN, stroke_width=2
                )
                gain_arrows.append(arr)
                self.play(GrowArrow(arr), FadeIn(pct_label), FadeIn(t, shift=DOWN), run_time=0.4)

        gain_formula = MathTex(r"100 \times (1.2)^3 = 172.8", font_size=50, color=CYAN).move_to(DOWN * 4.5)
        self.play(Write(gain_formula), run_time=1)
        self.wait(0.5)

        # Transition vers la courbe
        all_gains = VGroup(gains_title, gain_formula, *gain_texts, *gain_arrows)
        self.play(FadeOut(all_gains), run_time=0.4)
        self.clear()

        # Courbe exponentielle
        exp_title = Text("EXPONENTIAL GROWTH", font_size=42, color=GREEN, weight=BOLD).move_to(UP * 6)
        self.play(FadeIn(exp_title), run_time=0.4)

        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 700, 100],
            x_length=7,
            y_length=9,
            axis_config={"color": GRAY, "include_tip": False, "stroke_width": 1},
        ).move_to(DOWN * 0.5)

        x_label = Text("Periods", font_size=24, color=GRAY).next_to(axes, DOWN, buff=0.3)
        y_label = Text("Value", font_size=24, color=GRAY).next_to(axes, LEFT, buff=0.3).rotate(PI/2)

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=0.5)

        exp_curve = axes.plot(lambda x: 100 * (1.2)**x, x_range=[0, 10], color=GREEN, stroke_width=3)
        self.play(Create(exp_curve), run_time=2)

        # Point final
        end_dot = Dot(axes.c2p(10, 100 * 1.2**10), color=GREEN, radius=0.12)
        end_val = Text(f"{100 * 1.2**10:.0f}€", font_size=30, color=GREEN).next_to(end_dot, UR, buff=0.15)
        self.play(FadeIn(end_dot), FadeIn(end_val), run_time=0.4)
        self.wait(1)

        self.play(FadeOut(VGroup(exp_title, axes, x_label, y_label, exp_curve, end_dot, end_val)), run_time=0.5)

        # =====================================================
        # 32–40s — La formule du produit composé
        # =====================================================
        text1 = Text("In trading,", font_size=42, color=WHITE).move_to(UP * 4)
        text2 = Text("percentages don't add up.", font_size=42, color=WHITE).move_to(UP * 2.5)
        text3 = Text("They compound.", font_size=50, color=ORANGE, weight=BOLD).move_to(UP * 0.5)

        self.play(FadeIn(text1, shift=RIGHT), run_time=0.5)
        self.play(FadeIn(text2, shift=RIGHT), run_time=0.5)
        self.play(FadeIn(text3, scale=1.3), run_time=0.6)
        self.wait(1)

        self.play(FadeOut(VGroup(text1, text2, text3)), run_time=0.4)

        # La grande formule
        product_formula = MathTex(
            r"V_n = V_0 \prod_{i=1}^{n} (1 + r_i)",
            font_size=55, color=CYAN
        ).move_to(ORIGIN)

        self.play(Write(product_formula), run_time=2)
        self.wait(0.5)

        # Zoom sur la formule (scale up)
        self.play(product_formula.animate.scale(1.4).move_to(UP * 1), run_time=1)
        self.wait(1.5)

        self.play(FadeOut(product_formula), run_time=0.5)

        # =====================================================
        # 40–45s — OUTRO
        # =====================================================
        outro1 = MathTex(r"-50\%", font_size=80, color=RED).move_to(LEFT * 2 + UP * 2)
        neq = MathTex(r"\neq", font_size=80, color=WHITE).move_to(UP * 2)
        outro2 = MathTex(r"+50\%", font_size=80, color=GREEN).move_to(RIGHT * 2 + UP * 2)

        self.play(Write(outro1), Write(neq), Write(outro2), run_time=0.8)

        outro_text = Text("to get back to where you started.", font_size=30, color=GRAY).move_to(DOWN * 1)
        self.play(FadeIn(outro_text, shift=UP), run_time=0.5)

        self.wait(2)
