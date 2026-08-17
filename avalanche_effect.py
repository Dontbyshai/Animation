from manim import *
import hashlib

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

def get_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

class AvalancheEffect(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # =====================================================
        # 0–3s — HOOK : bitcoin -> Bitcoin
        # =====================================================
        word1 = Text("bitcoin", font_size=90, color=WHITE).move_to(ORIGIN)
        self.play(FadeIn(word1, shift=UP), run_time=0.6)
        self.wait(0.5)
        
        word2 = Text("Bitcoin", font_size=90, color=ORANGE).move_to(ORIGIN)
        # Highlight just the first letter change by transforming
        self.play(Transform(word1, word2), run_time=0.5)
        
        hook_text = Text("Just one character.", font_size=35, color=GRAY).move_to(DOWN * 2)
        self.play(FadeIn(hook_text, shift=UP), run_time=0.5)
        self.wait(0.8)

        # =====================================================
        # 3–8s — Envoi dans SHA256(x)
        # =====================================================
        self.play(FadeOut(hook_text), word1.animate.scale(0.5).move_to(UP * 5), run_time=0.5)
        
        box = Rectangle(width=4, height=2, color=CYAN, stroke_width=4).move_to(UP * 2)
        box_text = Text("SHA256(x)", font_size=40, color=CYAN, weight=BOLD).move_to(box.get_center())
        
        self.play(Create(box), Write(box_text), run_time=0.8)
        
        # Flux de données (particules descendantes)
        stream = VGroup()
        for i in range(5):
            dot = Dot(color=ORANGE, radius=0.08).move_to(UP * 4.5 + RIGHT * (i*0.4 - 0.8))
            stream.add(dot)
            
        self.play(LaggedStart(*[d.animate.move_to(UP * 2.5 + RIGHT * (i*0.4 - 0.8)) for i, d in enumerate(stream)], lag_ratio=0.1), run_time=0.6)
        self.play(FadeOut(stream), run_time=0.2)

        # =====================================================
        # 8–15s — Hash 1 et Hash 2
        # =====================================================
        self.play(FadeOut(box), FadeOut(box_text), FadeOut(word1), run_time=0.4)
        
        hash1_str = get_hash("bitcoin")
        hash2_str = get_hash("Bitcoin")
        
        # Lignes défilantes type "matrix"
        matrix_group = VGroup()
        for _ in range(10):
            t = Text("".join(__import__('random').choices("0123456789abcdef", k=64)), font_size=18, color=GREEN).move_to(ORIGIN)
            matrix_group.add(t)
            
        self.play(LaggedStart(*[FadeIn(t, run_time=0.1) for t in matrix_group], lag_ratio=0.1), run_time=1)
        self.play(FadeOut(matrix_group), run_time=0.2)
        
        # Affichage propre des deux hash
        t_b1 = Text("bitcoin", font_size=35, color=WHITE).move_to(UP * 4 + LEFT * 2)
        t_b2 = Text("Bitcoin", font_size=35, color=ORANGE).move_to(UP * 2 + LEFT * 2)
        
        h1 = Text(hash1_str[:32] + "\n" + hash1_str[32:], font_size=20, color=CYAN).move_to(UP * 4 + RIGHT * 1)
        h2 = Text(hash2_str[:32] + "\n" + hash2_str[32:], font_size=20, color=RED).move_to(UP * 2 + RIGHT * 1)
        
        self.play(FadeIn(t_b1), FadeIn(t_b2), run_time=0.4)
        self.play(Write(h1), run_time=0.8)
        self.play(Write(h2), run_time=0.8)
        self.wait(0.8)

        # =====================================================
        # 15–23s — Conversion en bits
        # =====================================================
        self.play(FadeOut(t_b1), FadeOut(t_b2), run_time=0.3)
        
        def hex_to_bin(h):
            return bin(int(h, 16))[2:].zfill(256)
            
        bin1 = hex_to_bin(hash1_str)
        bin2 = hex_to_bin(hash2_str)
        
        # On affiche juste les 64 premiers bits pour que ça soit lisible
        b1_disp = bin1[:64]
        b2_disp = bin2[:64]
        
        # On va créer des VGroup de caractères pour pouvoir colorer ceux qui diffèrent
        b1_group = VGroup(*[Text(c, font_size=22, color=WHITE) for c in b1_disp]).arrange(RIGHT, buff=0.05).move_to(UP * 4)
        b2_group = VGroup(*[Text(c, font_size=22, color=WHITE) for c in b2_disp]).arrange(RIGHT, buff=0.05).move_to(UP * 2)
        
        self.play(ReplacementTransform(h1, b1_group), ReplacementTransform(h2, b2_group), run_time=1)
        
        # Colorer les bits différents en cyan
        diff_anims = []
        diff_count = 0
        for i in range(64):
            if b1_disp[i] != b2_disp[i]:
                diff_count += 1
                diff_anims.append(b1_group[i].animate.set_color(CYAN))
                diff_anims.append(b2_group[i].animate.set_color(CYAN))
                
        self.play(*diff_anims, run_time=1.5)
        self.wait(1)

        # =====================================================
        # 23–31s — Distance de Hamming + Jauge
        # =====================================================
        self.play(FadeOut(b1_group), FadeOut(b2_group), run_time=0.4)
        
        hamming = MathTex(r"d_H(H_1, H_2)", font_size=60, color=YELLOW).move_to(UP * 4)
        self.play(Write(hamming), run_time=0.8)
        
        # Jauge 0 -> 128 -> 256
        gauge_bg = Rectangle(width=6, height=0.8, color=GRAY, fill_opacity=0.2).move_to(UP * 1)
        
        label_0 = Text("0", font_size=24, color=WHITE).next_to(gauge_bg, DOWN, aligned_edge=LEFT)
        label_256 = Text("256", font_size=24, color=WHITE).next_to(gauge_bg, DOWN, aligned_edge=RIGHT)
        
        self.play(FadeIn(gauge_bg), FadeIn(label_0), FadeIn(label_256), run_time=0.5)
        
        tracker = ValueTracker(0)
        
        # Le nombre de bits différents sur les 256 complets
        total_diff = sum(1 for a, b in zip(bin1, bin2) if a != b)
        
        gauge_fill = always_redraw(lambda: Rectangle(
            width=6 * (tracker.get_value() / 256), 
            height=0.8, color=CYAN, fill_opacity=0.8
        ).move_to(gauge_bg.get_left() + RIGHT * (6 * (tracker.get_value() / 256) / 2), aligned_edge=ORIGIN))
        
        val_text = always_redraw(lambda: Text(
            f"{int(tracker.get_value())} bits changed", font_size=40, color=CYAN
        ).move_to(DOWN * 1))
        
        self.add(gauge_fill, val_text)
        
        self.play(tracker.animate.set_value(total_diff), run_time=2)
        
        avg_text = Text(f"(Average is 128)", font_size=25, color=GRAY).next_to(val_text, DOWN)
        self.play(FadeIn(avg_text), run_time=0.5)
        self.wait(1.5)

        self.play(FadeOut(VGroup(hamming, gauge_bg, gauge_fill, label_0, label_256, val_text, avg_text)), run_time=0.5)

        # =====================================================
        # 31–39s — Exemples multiples
        # =====================================================
        words = ["bitcoin", "Bitcoin", "bitcoin!", "bitcoin?", "bitcoin123"]
        ex_group = VGroup()
        
        for i, w in enumerate(words):
            w_text = Text(w, font_size=30, color=ORANGE).move_to(LEFT * 2.5 + UP * (5 - i * 2))
            h_str = get_hash(w)
            h_text = Text(h_str[:20] + "...", font_size=22, color=WHITE).move_to(RIGHT * 1 + UP * (5 - i * 2))
            ex_group.add(VGroup(w_text, h_text))
            
        self.play(LaggedStart(*[FadeIn(g, shift=RIGHT) for g in ex_group], lag_ratio=0.15), run_time=1.5)
        self.wait(1.5)
        
        self.play(FadeOut(ex_group), run_time=0.5)

        # =====================================================
        # 39–45s — OUTRO (Effet avalanche)
        # =====================================================
        outro_title = Text("This is the Avalanche Effect.", font_size=40, color=CYAN, weight=BOLD).move_to(UP * 2)
        
        formula = MathTex(
            r"\text{small modification} \rightarrow \text{HUGE change}",
            font_size=45, color=WHITE
        ).move_to(DOWN * 1)
        
        self.play(Write(outro_title), run_time=0.8)
        self.play(FadeIn(formula, shift=UP), run_time=0.8)
        
        # Flash the "HUGE" part by changing color of the mathTex parts
        self.play(formula[0][-10:].animate.set_color(RED), run_time=0.5)
        
        self.wait(2)
