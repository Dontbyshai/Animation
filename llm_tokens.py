from manim import *
import numpy as np

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

class LLMNextWord(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # =====================================================
        # 0–3s — HOOK : "Comment une IA sait quel mot..."
        # =====================================================
        question = Text(
            "How does an AI know\nwhat word comes next?",
            font_size=35, color=WHITE, line_spacing=1.2
        ).move_to(UP * 4)
        
        self.play(Write(question), run_time=1.2)
        
        sentence = Text("Le Bitcoin est", font_size=50, color=ORANGE, weight=BOLD).move_to(ORIGIN)
        cursor = Line(UP*0.4, DOWN*0.4, color=WHITE, stroke_width=4).next_to(sentence, RIGHT, buff=0.1)
        
        self.play(FadeIn(sentence, shift=UP), run_time=0.6)
        
        # Cursor blinking
        for _ in range(3):
            self.play(FadeIn(cursor), run_time=0.2)
            self.play(FadeOut(cursor), run_time=0.2)

        self.play(FadeOut(question), run_time=0.3)

        # =====================================================
        # 3–10s — Tokens et Nombres
        # =====================================================
        # Le | Bitcoin | est
        t1 = Text("Le", font_size=50, color=ORANGE, weight=BOLD)
        bar1 = Text("|", font_size=50, color=CYAN)
        t2 = Text("Bitcoin", font_size=50, color=ORANGE, weight=BOLD)
        bar2 = Text("|", font_size=50, color=CYAN)
        t3 = Text("est", font_size=50, color=ORANGE, weight=BOLD)
        
        token_group = VGroup(t1, bar1, t2, bar2, t3).arrange(RIGHT, buff=0.3).move_to(ORIGIN)
        
        self.play(ReplacementTransform(sentence, VGroup(t1, t2, t3)), FadeIn(bar1), FadeIn(bar2), run_time=0.8)
        
        token_title = Text("TOKENS", font_size=40, color=CYAN, weight=BOLD).move_to(UP * 2)
        self.play(FadeIn(token_title, shift=DOWN), run_time=0.5)
        self.wait(0.5)
        
        # Devenir des nombres
        n1 = Text("142", font_size=50, color=GREEN)
        n2 = Text("9341", font_size=50, color=GREEN)
        n3 = Text("76", font_size=50, color=GREEN)
        
        num_group = VGroup(n1, bar1.copy(), n2, bar2.copy(), n3).arrange(RIGHT, buff=0.4).move_to(ORIGIN)
        
        self.play(
            ReplacementTransform(t1, num_group[0]),
            ReplacementTransform(t2, num_group[2]),
            ReplacementTransform(t3, num_group[4]),
            run_time=0.8
        )
        self.wait(1)

        self.play(FadeOut(VGroup(token_title, bar1, bar2, num_group[1], num_group[3])), run_time=0.4)

        # =====================================================
        # 10–17s — Vecteurs et Espace Latent (Embeddings)
        # =====================================================
        vec_formula = MathTex(r"\vec{x} \in \mathbb{R}^n", font_size=55, color=YELLOW).move_to(UP * 4)
        
        # Transformation des nombres en vecteurs (colonnes)
        v1 = Matrix([[0.12], [-0.5], ["\vdots"], [0.8]], v_buff=0.4, left_bracket="[", right_bracket="]").scale(0.6)
        v2 = Matrix([[-0.9], [0.3], ["\vdots"], [0.1]], v_buff=0.4, left_bracket="[", right_bracket="]").scale(0.6)
        v3 = Matrix([[0.4], [0.7], ["\vdots"], [-0.2]], v_buff=0.4, left_bracket="[", right_bracket="]").scale(0.6)
        
        vec_group = VGroup(v1, v2, v3).arrange(RIGHT, buff=1.5).move_to(UP * 1)
        
        self.play(Write(vec_formula), run_time=0.6)
        self.play(
            ReplacementTransform(num_group[0], v1),
            ReplacementTransform(num_group[2], v2),
            ReplacementTransform(num_group[4], v3),
            run_time=1
        )
        self.wait(0.5)

        # Espace 2D/3D avec pleins de points
        self.play(FadeOut(VGroup(vec_formula, vec_group)), run_time=0.4)
        
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=6, y_length=6,
            axis_config={"color": GRAY, "stroke_opacity": 0.5}
        ).move_to(DOWN * 1)
        
        np.random.seed(42)
        dots = VGroup()
        for _ in range(40):
            x = np.random.uniform(-3, 3)
            y = np.random.uniform(-3, 3)
            dots.add(Dot(axes.c2p(x, y), color=BLUE_B, radius=0.06))
            
        # Nos 3 tokens spécifiques (plus gros et colorés)
        main_dots = VGroup(
            Dot(axes.c2p(-1.5, 2), color=ORANGE, radius=0.1),
            Dot(axes.c2p(0.5, 1.5), color=GREEN, radius=0.1),
            Dot(axes.c2p(2, -1), color=MAGENTA, radius=0.1)
        )
        
        self.play(Create(axes), FadeIn(dots), FadeIn(main_dots), run_time=1)
        
        # Relier les vecteurs proches
        lines = VGroup()
        for d1 in main_dots:
            for d2 in dots:
                if np.linalg.norm(d1.get_center() - d2.get_center()) < 1.5:
                    lines.add(Line(d1.get_center(), d2.get_center(), color=YELLOW, stroke_width=1, stroke_opacity=0.4))
                    
        self.play(Create(lines, lag_ratio=0.05), run_time=1.5)
        self.wait(0.8)
        
        self.play(FadeOut(VGroup(axes, dots, main_dots, lines)), run_time=0.5)

        # =====================================================
        # 17–25s — Q, K, V et Attention
        # =====================================================
        qkv = MathTex("Q,", "K,", "V", font_size=70, color=CYAN).move_to(UP * 5)
        self.play(Write(qkv), run_time=0.8)
        
        attention = MathTex(r"\text{Attention}(Q, K, V)", font_size=55, color=ORANGE).move_to(UP * 3.5)
        self.play(FadeIn(attention, shift=UP), run_time=0.6)

        # Réseaux de tokens (3 cercles)
        t_nodes = VGroup(
            Circle(radius=0.5, color=WHITE).move_to(LEFT * 2.5 + DOWN * 1),
            Circle(radius=0.5, color=WHITE).move_to(ORIGIN + DOWN * 1),
            Circle(radius=0.5, color=WHITE).move_to(RIGHT * 2.5 + DOWN * 1)
        )
        t_labels = VGroup(
            Text("Le", font_size=30).move_to(t_nodes[0]),
            Text("Bitcoin", font_size=30).move_to(t_nodes[1]),
            Text("est", font_size=30).move_to(t_nodes[2])
        )
        
        self.play(FadeIn(t_nodes), FadeIn(t_labels), run_time=0.5)

        # Connexions lumineuses d'épaisseurs différentes
        conn1 = Line(t_nodes[0].get_right(), t_nodes[1].get_left(), color=YELLOW, stroke_width=2)
        conn2 = Line(t_nodes[1].get_right(), t_nodes[2].get_left(), color=YELLOW, stroke_width=6)
        conn3 = CurvedArrow(t_nodes[0].get_top(), t_nodes[2].get_top(), color=YELLOW, stroke_width=1).shift(UP*0.2)
        
        self.play(Create(conn1), Create(conn2), Create(conn3), run_time=1.2)
        self.wait(1)

        self.play(FadeOut(VGroup(qkv, attention, t_nodes, t_labels, conn1, conn2, conn3)), run_time=0.5)

        # =====================================================
        # 25–34s — Matrice d'Attention
        # =====================================================
        matrix_title = Text("ATTENTION MATRIX", font_size=40, color=GREEN, weight=BOLD).move_to(UP * 5)
        self.play(FadeIn(matrix_title, shift=DOWN), run_time=0.4)
        
        # Dessiner une matrice 3x3 avec des carrés
        grid = VGroup()
        for i in range(3):
            for j in range(3):
                rect = Rectangle(width=1.5, height=1.5, stroke_color=WHITE, fill_color=CYAN, fill_opacity=0.1)
                rect.move_to(RIGHT * (j*1.5 - 1.5) + DOWN * (i*1.5 - 1.5))
                
                val = np.random.uniform(0.1, 0.9)
                num = Text(f"{val:.1f}", font_size=35, color=WHITE).move_to(rect.get_center())
                
                grid.add(VGroup(rect, num))
                
        grid.move_to(ORIGIN)
        self.play(LaggedStart(*[FadeIn(g, scale=0.5) for g in grid], lag_ratio=0.05), run_time=1)
        
        # Changer l'intensité (fill_opacity)
        animations = []
        for g in grid:
            rect, num = g[0], g[1]
            new_val = np.random.uniform(0.1, 0.9)
            animations.append(rect.animate.set_fill(opacity=new_val))
            animations.append(num.animate.become(Text(f"{new_val:.1f}", font_size=35, color=WHITE).move_to(rect.get_center())))
            
        self.play(*animations, run_time=1.5)
        self.wait(1)
        
        self.play(FadeOut(VGroup(matrix_title, grid)), run_time=0.5)

        # =====================================================
        # 34–42s — Scores du prochain token
        # =====================================================
        scores_title = Text("NEXT TOKEN SCORES", font_size=40, color=ORANGE, weight=BOLD).move_to(UP * 6)
        self.play(FadeIn(scores_title, shift=DOWN), run_time=0.4)

        words_data = [
            ("monde", 0.04),
            ("orange", 0.01),
            ("minage", 0.12),
            ("fonctionne", 0.61),
            ("blockchain", 0.22)
        ]
        
        bar_group = VGroup()
        for i, (word, score) in enumerate(words_data):
            w_text = Text(word, font_size=30, color=WHITE).move_to(LEFT * 3 + UP * (4 - i * 1.5))
            
            # Bare de progression
            bg_bar = Rectangle(width=5, height=0.6, color=GRAY, fill_opacity=0.2).next_to(w_text, RIGHT, buff=0.5).align_to(w_text, DOWN).shift(UP*0.1)
            
            bar_color = GREEN if word == "fonctionne" else CYAN
            fill_bar = Rectangle(width=5 * score, height=0.6, color=bar_color, fill_opacity=0.8)
            fill_bar.next_to(bg_bar.get_left(), RIGHT, buff=0).align_to(bg_bar, DOWN)
            
            s_text = Text(f"{score:.2f}", font_size=25, color=WHITE).next_to(bg_bar, RIGHT, buff=0.3)
            
            bar_group.add(VGroup(w_text, bg_bar, fill_bar, s_text))
            
        self.play(LaggedStart(*[FadeIn(g, shift=LEFT) for g in bar_group], lag_ratio=0.1), run_time=1.5)

        # =====================================================
        # 42–50s — Softmax + Choix du mot
        # =====================================================
        softmax = MathTex(
            r"P_i = \frac{e^{z_i}}{\sum_j e^{z_j}}",
            font_size=55, color=YELLOW
        ).move_to(DOWN * 5)
        
        self.play(Write(softmax), run_time=1.2)
        
        # La barre de fonctionne monte fortement (highlight)
        func_bar = bar_group[3]
        self.play(
            func_bar.animate.scale(1.1).set_color(GREEN),
            Flash(func_bar, color=GREEN),
            run_time=0.8
        )
        self.wait(1)

        self.play(FadeOut(VGroup(scores_title, bar_group, softmax)), run_time=0.5)

        # =====================================================
        # FIN — Recommencer
        # =====================================================
        final_sentence = Text("Le Bitcoin est fonctionne", font_size=45, color=ORANGE, weight=BOLD).move_to(UP * 2)
        self.play(FadeIn(final_sentence, scale=0.5), run_time=0.6)
        self.wait(0.5)
        
        # Éclatement (dispersion)
        self.play(
            final_sentence[0:2].animate.shift(LEFT * 5 + UP * 2).set_opacity(0),
            final_sentence[2:9].animate.shift(LEFT * 2 + DOWN * 5).set_opacity(0),
            final_sentence[9:12].animate.shift(RIGHT * 3 + UP * 4).set_opacity(0),
            final_sentence[12:].animate.shift(RIGHT * 6 + DOWN * 2).set_opacity(0),
            run_time=0.8
        )
        
        # "Le Bitcoin est ..."
        restart = Text("Le Bitcoin est ...", font_size=50, color=CYAN, weight=BOLD).move_to(UP * 2)
        self.play(FadeIn(restart), run_time=0.5)
        
        outro_text = Text(
            "An AI doesn't 'guess' the word.\nIt calculates a probability distribution.",
            font_size=32, color=WHITE, line_spacing=1.2
        ).move_to(DOWN * 1)
        
        self.play(Write(outro_text), run_time=1.5)
        self.wait(2)
