from manim import *
import random

# Manim config pour format TikTok 9:16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 60
config.frame_width = 9
config.frame_height = 16

# Coordonnées de la frame:
# Y: -8 (bas) à +8 (haut)
# X: -4.5 (gauche) à +4.5 (droite)
# Zone de sécurité TikTok: garder entre Y=-6 et Y=+7, X=-3.8 et X=+3.8

ORANGE = "#F7931A"
GREEN = "#39FF14"
RED = "#FF003C"
CYAN = "#00FFFF"
MAGENTA = "#FF00FF"
YELLOW = "#FFD700"
MAX_W = 7.5  # Largeur max utile


class BitcoinMathTikTok(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # =====================================================
        # SCENE 1 — INTRO : Logo à gauche + Bitcoin à droite
        # =====================================================
        logo = ImageMobject("/Users/dontbyshai/Documents/Bitcoin animation/Bitcoin.svg.png")
        logo.scale_to_fit_width(3.5)
        logo.move_to(LEFT * 1.8 + UP * 2)

        btc_title = Text("Bitcoin", font_size=55, color=ORANGE, weight=BOLD)
        btc_title.move_to(RIGHT * 1.8 + UP * 2)

        self.play(FadeIn(logo, scale=0.3), FadeIn(btc_title, shift=RIGHT), run_time=0.8)
        self.wait(0.8)

        # Satoshi Nakamoto — 2008
        author = Text("Satoshi Nakamoto", font_size=45, color=WHITE, weight=BOLD)
        author.move_to(DOWN * 1)
        year = Text("2008", font_size=60, color=ORANGE, weight=BOLD)
        year.move_to(DOWN * 3)

        self.play(FadeIn(author, shift=UP), run_time=0.5)
        self.play(FadeIn(year, scale=1.5), run_time=0.5)
        self.wait(1)

        # Transition Sigma — plongeon dans les maths
        self.play(FadeOut(Group(logo, btc_title, author, year)), run_time=0.5)

        sigma = MathTex(r"\Sigma", font_size=300, color=CYAN)
        sigma.move_to(ORIGIN)
        self.play(FadeIn(sigma, scale=0.2), run_time=0.6)
        self.play(Wiggle(sigma, scale_value=1.15), run_time=0.8)
        self.wait(0.3)
        self.play(FadeOut(sigma), run_time=0.4)

        # =====================================================
        # SCENE 3 — ELLIPTIC CURVE CRYPTOGRAPHY
        # La base mathématique des signatures Bitcoin
        # =====================================================
        # Titre seul d'abord
        ec_title = Text("ELLIPTIC CURVE", font_size=55, color=CYAN, weight=BOLD)
        ec_title.move_to(UP * 6)
        self.play(FadeIn(ec_title, shift=DOWN), run_time=0.5)

        # Équation seule, bien grande, au centre
        ec_eq = MathTex(r"y^2 = x^3 + 7", font_size=70, color=ORANGE)
        ec_eq.move_to(UP * 3.5)
        self.play(Write(ec_eq), run_time=1)
        self.wait(0.8)

        # --- Coordonnées mathématiquement exactes ---
        # Courbe: y² = x³ + 7
        import math

        # G = (1, √8)
        gx = 1.0
        gy = math.sqrt(gx**3 + 7)  # = 2.8284

        # Tangente en G: pente m = 3x²/(2y)
        m_tang = (3 * gx**2) / (2 * gy)  # ≈ 0.5303

        # Point d'intersection de la tangente avec la courbe (3ème racine)
        # x₃ = m² − 2·x₁
        ix1 = m_tang**2 - 2 * gx  # ≈ -1.7188
        iy1 = m_tang * (ix1 - gx) + gy  # y sur la droite ≈ 1.386

        # 2G = réflexion = (ix1, -iy1)
        x_2g = ix1
        y_2g = -iy1  # ≈ -1.386

        # Sécante G → 2G: pente
        m_sec = (gy - y_2g) / (gx - x_2g)  # ≈ 1.550

        # Point d'intersection de la sécante avec la courbe (3ème racine)
        # x₃ = m² − x₁ − x₂
        ix2 = m_sec**2 - gx - x_2g  # ≈ 3.121
        iy2 = m_sec * (ix2 - gx) + gy  # y sur la droite ≈ 6.114

        # 3G = réflexion = (ix2, -iy2)
        x_3g = ix2
        y_3g = -iy2  # ≈ -6.114

        # Axes adaptés pour contenir tous les points
        axes = Axes(
            x_range=[-3, 4, 1],
            y_range=[-7, 7, 2],
            x_length=7,
            y_length=10,
            axis_config={"color": GRAY, "include_tip": False, "stroke_width": 1},
        ).move_to(DOWN * 1)

        curve_pos = axes.plot(lambda x: (max(x**3 + 7, 0))**0.5, x_range=[-1.912, 3.8], color=CYAN)
        curve_neg = axes.plot(lambda x: -(max(x**3 + 7, 0))**0.5, x_range=[-1.912, 3.8], color=CYAN)

        self.play(FadeOut(ec_eq), run_time=0.3)
        self.play(Create(axes), run_time=0.5)
        self.play(Create(curve_pos), Create(curve_neg), run_time=1.5)

        # Point G — exactement sur la courbe
        g_dot = Dot(axes.c2p(gx, gy), color=WHITE, radius=0.12)
        g_label = MathTex("G", font_size=40, color=WHITE).next_to(g_dot, UR, buff=0.15)
        self.play(FadeIn(g_dot, scale=2), Write(g_label), run_time=0.5)
        self.wait(0.5)

        # Tangente passant par G et l'intersection
        tang_x_start = gx + 1.5
        tang_y_start = m_tang * (tang_x_start - gx) + gy
        tang_x_end = ix1 - 0.8
        tang_y_end = m_tang * (tang_x_end - gx) + gy
        tang = Line(axes.c2p(tang_x_start, tang_y_start), axes.c2p(tang_x_end, tang_y_end), color=MAGENTA, stroke_width=2)
        self.play(Create(tang), run_time=0.8)

        # Intersection — exactement sur la courbe
        inter_dot = Dot(axes.c2p(ix1, iy1), color=MAGENTA, radius=0.08)
        self.play(FadeIn(inter_dot), run_time=0.3)

        # Réflexion verticale → 2G
        dash = DashedLine(axes.c2p(ix1, iy1), axes.c2p(x_2g, y_2g), color=WHITE, stroke_width=1.5)
        g2_dot = Dot(axes.c2p(x_2g, y_2g), color=YELLOW, radius=0.12)
        g2_label = MathTex("2G", font_size=40, color=YELLOW).next_to(g2_dot, DL, buff=0.15)
        self.play(Create(dash), FadeIn(g2_dot, scale=2), Write(g2_label), run_time=0.6)
        self.wait(0.8)

        # Nettoyer les constructions
        self.play(FadeOut(VGroup(tang, inter_dot, dash)), run_time=0.3)

        # Sécante passant par G et 2G
        sec_x_start = x_2g - 0.5
        sec_y_start = m_sec * (sec_x_start - gx) + gy
        sec_x_end = ix2 + 0.3
        sec_y_end = m_sec * (sec_x_end - gx) + gy
        sec = Line(axes.c2p(sec_x_start, sec_y_start), axes.c2p(sec_x_end, sec_y_end), color=YELLOW, stroke_width=2)
        self.play(Create(sec), run_time=0.8)

        # Intersection — exactement sur la courbe
        inter2_dot = Dot(axes.c2p(ix2, iy2), color=YELLOW, radius=0.08)
        self.play(FadeIn(inter2_dot), run_time=0.3)

        # Réflexion → 3G
        dash2 = DashedLine(axes.c2p(ix2, iy2), axes.c2p(x_3g, y_3g), color=WHITE, stroke_width=1.5)
        g3_dot = Dot(axes.c2p(x_3g, y_3g), color=GREEN, radius=0.12)
        g3_label = MathTex("3G", font_size=40, color=GREEN).next_to(g3_dot, DR, buff=0.15)
        self.play(Create(dash2), FadeIn(g3_dot, scale=2), Write(g3_label), run_time=0.6)
        self.wait(0.5)

        self.play(FadeOut(VGroup(sec, inter2_dot, dash2)), run_time=0.3)

        # Résultat final : Q = dG
        self.play(FadeOut(VGroup(g_dot, g_label, g2_dot, g2_label, g3_dot, g3_label, axes, curve_pos, curve_neg)), run_time=0.5)

        q_eq = MathTex(r"Q = d \cdot G", font_size=80, color=GREEN)
        q_eq.move_to(UP * 2)
        pub_label = Text("PUBLIC KEY", font_size=50, color=GREEN, weight=BOLD)
        pub_label.move_to(DOWN * 1)

        self.play(Write(q_eq), run_time=0.8)
        self.play(FadeIn(pub_label, scale=1.3), Flash(pub_label, color=GREEN, line_length=0.8), run_time=0.6)

        # Explication trapdoor
        easy = Text("d × G → Q  :  EASY", font_size=36, color=GREEN)
        easy.move_to(DOWN * 3.5)
        hard = Text("Q → d  :  IMPOSSIBLE", font_size=36, color=RED)
        hard.move_to(DOWN * 5)

        self.play(FadeIn(easy, shift=RIGHT), run_time=0.5)
        self.play(FadeIn(hard, shift=RIGHT), Wiggle(hard), run_time=0.8)
        self.wait(1.5)

        self.play(FadeOut(VGroup(ec_title, q_eq, pub_label, easy, hard)), run_time=0.5)

        # =====================================================
        # SCENE 4 — TIMESTAMP SERVER (Section 3)
        # =====================================================
        ts_title = Text("TIMESTAMP SERVER", font_size=50, color=ORANGE, weight=BOLD)
        ts_title.move_to(UP * 6)
        self.play(FadeIn(ts_title, shift=DOWN), run_time=0.5)

        # Blocs empilés
        def make_ts_block(label_text, y_pos):
            box = Rectangle(width=6, height=2, color=CYAN)
            box.move_to(UP * y_pos)
            items = Text(f"Block: {label_text}", font_size=24, color=WHITE).move_to(box.get_center() + UP * 0.3)
            hsh = Text("Hash(  )", font_size=22, color=GREEN).move_to(box.get_center() + DOWN * 0.3)
            return VGroup(box, items, hsh)

        b1 = make_ts_block("Item A, Item B ...", 3)
        b2 = make_ts_block("Item C, Item D ...", -0.5)

        self.play(Create(b1), run_time=0.5)
        self.wait(0.5)

        arr_ts = Arrow(b1.get_bottom(), b2.get_top(), color=WHITE)
        hash_link = Text("Hash includes\nprevious hash", font_size=20, color=MAGENTA).next_to(arr_ts, RIGHT, buff=0.3)

        self.play(GrowArrow(arr_ts), Write(hash_link), run_time=0.5)
        self.play(Create(b2), run_time=0.5)

        chain_text = Text("Each timestamp reinforces\nthe ones before it", font_size=28, color=WHITE)
        chain_text.move_to(DOWN * 4)
        self.play(Write(chain_text), run_time=1)
        self.wait(1.5)

        self.play(FadeOut(VGroup(ts_title, b1, b2, arr_ts, hash_link, chain_text)), run_time=0.5)

        # =====================================================
        # SCENE 5 — PROOF OF WORK (Section 4)
        # =====================================================
        pow_title = Text("PROOF OF WORK", font_size=55, color=ORANGE, weight=BOLD)
        pow_title.move_to(UP * 6)
        self.play(FadeIn(pow_title, scale=1.2), run_time=0.5)

        # Explication
        pow_explain = Text("Find a nonce so that\nSHA-256(Block + Nonce)\nstarts with zero bits", font_size=30, color=WHITE)
        pow_explain.move_to(UP * 3)
        self.play(Write(pow_explain), run_time=1.5)
        self.wait(0.5)
        self.play(FadeOut(pow_explain), run_time=0.3)

        # SHA-256 formula
        sha_formula = MathTex(r"\text{SHA-256}(\text{Block} \| \text{Nonce})", font_size=50, color=MAGENTA)
        sha_formula.move_to(UP * 3)
        self.play(Write(sha_formula), run_time=0.8)

        # Nonce counter + hash output
        nonce_label = Text("Nonce:", font_size=36, color=CYAN)
        nonce_label.move_to(LEFT * 2 + DOWN * 0)
        nonce_val = Integer(0, font_size=50, color=CYAN)
        nonce_val.next_to(nonce_label, RIGHT, buff=0.3)

        hash_label = Text("Hash:", font_size=30, color=WHITE)
        hash_label.move_to(LEFT * 2.5 + DOWN * 2)
        hash_val = Text("9f86d08188...", font_size=28, color=WHITE)
        hash_val.next_to(hash_label, RIGHT, buff=0.3)

        self.play(FadeIn(nonce_label), FadeIn(nonce_val), FadeIn(hash_label), FadeIn(hash_val))

        # Nonce spinning
        for i in range(1, 25):
            new_hash_str = "".join(random.choices("0123456789abcdef", k=12)) + "..."
            new_hash = Text(new_hash_str, font_size=28, color=WHITE)
            new_hash.next_to(hash_label, RIGHT, buff=0.3)
            self.play(
                nonce_val.animate.set_value(i * 127843),
                hash_val.animate.become(new_hash),
                run_time=0.04
            )

        # Found!
        zero_hash_str = "000000" + "".join(random.choices("0123456789abcdef", k=6)) + "..."
        zero_hash = Text(zero_hash_str, font_size=34, color=GREEN, weight=BOLD)
        zero_hash.next_to(hash_label, RIGHT, buff=0.3)
        self.play(
            nonce_val.animate.set_value(2847291),
            hash_val.animate.become(zero_hash),
            run_time=0.2
        )
        self.play(Flash(hash_val, color=GREEN, line_length=1.5), Wiggle(hash_val), run_time=0.8)

        found_text = Text("BLOCK MINED!", font_size=50, color=GREEN, weight=BOLD)
        found_text.move_to(DOWN * 5)
        self.play(FadeIn(found_text, scale=1.5), run_time=0.5)
        self.wait(1)

        self.play(FadeOut(VGroup(pow_title, sha_formula, nonce_label, nonce_val, hash_label, hash_val, found_text)), run_time=0.5)

        # =====================================================
        # SCENE 6 — SECTION 11 : CALCULATIONS (Attacker Probability)
        # Formules de Poisson et Gambler's Ruin
        # =====================================================
        calc_title = Text("CALCULATIONS", font_size=55, color=ORANGE, weight=BOLD)
        calc_title.move_to(UP * 6)
        self.play(FadeIn(calc_title, shift=DOWN), run_time=0.5)

        # Variables
        vars_text = MathTex(
            r"p = \text{honest node}", "\\\\",
            r"q = \text{attacker}", "\\\\",
            font_size=40, color=WHITE
        )
        vars_text.move_to(UP * 3)
        self.play(Write(vars_text), run_time=1)
        self.wait(1)

        # Gambler's Ruin formula
        self.play(FadeOut(vars_text), run_time=0.3)

        gr_label = Text("Gambler's Ruin", font_size=40, color=YELLOW)
        gr_label.move_to(UP * 4)
        self.play(FadeIn(gr_label), run_time=0.4)

        gr_formula = MathTex(
            r"q_z = \begin{cases} 1 & \text{if } p \leq q \\ (q/p)^z & \text{if } p > q \end{cases}",
            font_size=45, color=WHITE
        )
        gr_formula.move_to(UP * 1)
        self.play(Write(gr_formula), run_time=1.5)
        self.wait(1.5)

        # Explication
        gr_explain = Text("Probability an attacker\ncatches up from z blocks behind", font_size=26, color=CYAN)
        gr_explain.move_to(DOWN * 2)
        self.play(Write(gr_explain), run_time=1)
        self.wait(1)

        self.play(FadeOut(VGroup(gr_label, gr_formula, gr_explain)), run_time=0.5)

        # Poisson Distribution
        poisson_label = Text("Poisson Distribution", font_size=40, color=YELLOW)
        poisson_label.move_to(UP * 4)
        self.play(FadeIn(poisson_label), run_time=0.4)

        lambda_eq = MathTex(r"\lambda = z \cdot \frac{q}{p}", font_size=60, color=WHITE)
        lambda_eq.move_to(UP * 1.5)
        self.play(Write(lambda_eq), run_time=0.8)
        self.wait(0.8)

        poisson_formula = MathTex(
            r"\sum_{k=0}^{\infty} \frac{\lambda^k e^{-\lambda}}{k!} \cdot \begin{cases} (q/p)^{(z-k)} & \text{if } k \leq z \\ 1 & \text{if } k > z \end{cases}",
            font_size=35, color=WHITE
        )
        poisson_formula.move_to(DOWN * 2)
        self.play(Write(poisson_formula), run_time=2)
        self.wait(2)

        self.play(FadeOut(VGroup(calc_title, poisson_label, lambda_eq, poisson_formula)), run_time=0.5)

        # Résultats numériques (table du whitepaper)
        result_title = Text("RESULTS", font_size=50, color=ORANGE, weight=BOLD)
        result_title.move_to(UP * 6)
        self.play(FadeIn(result_title), run_time=0.4)

        q_label = MathTex(r"q = 0.1", font_size=45, color=CYAN)
        q_label.move_to(UP * 4)
        self.play(Write(q_label), run_time=0.5)

        results_data = [
            ("z=0", "P=1.0000000"),
            ("z=1", "P=0.2045873"),
            ("z=2", "P=0.0509779"),
            ("z=3", "P=0.0131722"),
            ("z=5", "P=0.0009137"),
            ("z=10", "P=0.0000012"),
        ]

        result_group = VGroup()
        for i, (z, p) in enumerate(results_data):
            line = Text(f"{z}    {p}", font_size=28, color=WHITE)
            line.move_to(UP * (2.5 - i * 1.0))
            result_group.add(line)

        for line in result_group:
            self.play(FadeIn(line, shift=LEFT), run_time=0.15)

        drop_text = Text("Probability drops\nEXPONENTIALLY", font_size=34, color=GREEN, weight=BOLD)
        drop_text.move_to(DOWN * 5)
        self.play(FadeIn(drop_text, scale=1.3), run_time=0.5)
        self.wait(1.5)

        self.play(FadeOut(VGroup(result_title, q_label, result_group, drop_text)), run_time=0.5)

        # =====================================================
        # SCENE 7 — BLOCKCHAIN (Chaîne de blocs avec Hash)
        # =====================================================
        bc_title = Text("BLOCKCHAIN", font_size=55, color=ORANGE, weight=BOLD)
        bc_title.move_to(UP * 6)
        self.play(FadeIn(bc_title), run_time=0.5)

        def make_block(bid, prev_h, cur_h, y_pos):
            box = Rectangle(width=6, height=2.2, color=ORANGE, stroke_width=2)
            box.move_to(UP * y_pos)
            t_id = Text(f"Block #{bid}", font_size=24, color=WHITE, weight=BOLD).move_to(box.get_top() + DOWN * 0.35)
            t_prev = Text(f"Prev: {prev_h}", font_size=20, color=CYAN).move_to(box.get_center())
            t_hash = Text(f"Hash: {cur_h}", font_size=20, color=GREEN).move_to(box.get_bottom() + UP * 0.35)
            return VGroup(box, t_id, t_prev, t_hash)

        bl1 = make_block(1, "0000...0", "8A4F...C2", 3)
        bl2 = make_block(2, "8A4F...C2", "9B2C...E7", -0.5)
        bl3 = make_block(3, "9B2C...E7", "4E1A...B3", -4)

        a1 = Arrow(bl1.get_bottom(), bl2.get_top(), color=WHITE)
        a2 = Arrow(bl2.get_bottom(), bl3.get_top(), color=WHITE)

        self.play(Create(bl1), run_time=0.5)
        self.play(GrowArrow(a1), run_time=0.3)
        self.play(Create(bl2), run_time=0.5)

        # Highlight hash link
        self.play(Indicate(bl1[3], color=RED, scale_factor=1.3), Indicate(bl2[2], color=RED, scale_factor=1.3), run_time=1)

        self.play(GrowArrow(a2), run_time=0.3)
        self.play(Create(bl3), run_time=0.5)
        self.play(Indicate(bl2[3], color=RED, scale_factor=1.3), Indicate(bl3[2], color=RED, scale_factor=1.3), run_time=1)

        locked = Text("IMMUTABLE CHAIN", font_size=40, color=RED, weight=BOLD)
        locked.move_to(DOWN * 7)
        self.play(FadeIn(locked, shift=UP), Flash(locked, color=RED), run_time=0.6)
        self.wait(1.5)

        self.play(FadeOut(VGroup(bc_title, bl1, bl2, bl3, a1, a2, locked)), run_time=0.5)

        # =====================================================
        # SCENE 8 — OUTRO : Logo Bitcoin final
        # =====================================================
        logo_final = ImageMobject("/Users/dontbyshai/Documents/Bitcoin animation/Bitcoin.svg.png")
        logo_final.scale_to_fit_width(6)
        logo_final.move_to(UP * 1)

        btc_text = Text("BITCOIN", font_size=90, weight=BOLD, color=ORANGE)
        btc_text.move_to(DOWN * 3.5)

        self.play(FadeIn(logo_final, scale=0.3), run_time=0.8)
        self.play(FadeIn(btc_text, scale=0.5), run_time=0.6)
        self.play(Flash(logo_final, color=ORANGE, line_length=2, num_lines=16), run_time=0.8)

        self.wait(2)
