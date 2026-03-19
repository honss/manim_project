"""
Communication Complexity, NOF, and Behrend's Construction
12 scenes from the 15-minute script.
"""

import numpy as np
from manim import *


# -----------------------------------------------------------------------------
# Scene 1: Title and Motivation (1 min)
# -----------------------------------------------------------------------------
class IntroScene_1(Scene):
    """Scene 1: Title, subtitle, three players with numbers on foreheads."""
    def construct(self):
        title = Text(
            "Communication Complexity and\nArithmetic Progression–Free Sets",
            font_size=40,
            line_spacing=1.2,
        )
        subtitle = Text(
            "by Aidan Levy and Audrey Emis",
            font_size=28,
            color=GRAY,
        ).next_to(title, DOWN, buff=0.6)

        self.play(FadeIn(title))
        self.wait(1.1)
        self.play(FadeIn(subtitle))
        self.wait(1)

        # Remove subtitle when stick figures appear
        self.play(
            title.animate.to_edge(UP, buff=0.4).scale(0.7),
            FadeOut(subtitle),
        )

        # First: two stick figures (Alice and Bob) with arrows between them
        alice_two = self._stick_figure_no_number("Alice").move_to(2.5 * LEFT + 1.0 * DOWN).scale(0.95)
        bob_two = self._stick_figure_no_number("Bob").move_to(2.5 * RIGHT + 1.0 * DOWN).scale(0.95)
        arrow_alice_to_bob = Arrow(
            alice_two.get_right(), bob_two.get_left(),
            buff=0.25, color=YELLOW, max_tip_length_to_length_ratio=0.15,
        )
        arrow_bob_to_alice = Arrow(
            bob_two.get_left(), alice_two.get_right(),
            buff=0.25, color=YELLOW, max_tip_length_to_length_ratio=0.15,
        ).shift(0.3 * DOWN)

        self.play(FadeIn(alice_two), FadeIn(bob_two))
        self.wait(1)

        # Fade in X above Alice, Y above Bob
        head_alice = alice_two[0]
        head_bob = bob_two[0]
        num_x = MathTex(r"X", font_size=36).next_to(head_alice, UP, buff=0.12)
        num_y = MathTex(r"Y", font_size=36).next_to(head_bob, UP, buff=0.12)
        self.play(FadeIn(num_x), FadeIn(num_y))
        self.wait(1.1)

        self.play(GrowArrow(arrow_alice_to_bob))
        self.wait(1)
        self.play(GrowArrow(arrow_bob_to_alice))
        self.wait(1.1)

        # Cost of communication comes first
        two_figures = VGroup(alice_two, bob_two)
        bit_line = MathTex(r"x, y \in [1, N] \Rightarrow \log_2 N \text{ bits each}", font_size=28)
        share_line = MathTex(r"\text{To share a number: } O(\log_2 N) \text{ bits}", font_size=28)
        bit_line.next_to(two_figures, DOWN, buff=1.1)
        share_line.next_to(bit_line, DOWN, buff=0.25)

        self.play(FadeIn(bit_line), FadeIn(share_line))
        self.wait(1.5)

        # Now fade the two-party communication picture into checksum
        two_party_group = VGroup(
            alice_two, bob_two,
            num_x, num_y,
            arrow_alice_to_bob, arrow_bob_to_alice,
            bit_line, share_line,
        )

        checksum_title = Text("Checksum Function", font_size=34)
        checksum_title.move_to(UP * 0.15)

        checksum_eq = MathTex(
            r"\operatorname{CHECKSUM}(x,y)=1 \iff x+y=N",
            font_size=40
        ).next_to(checksum_title, DOWN, buff=0.5)

        checksum_note = Text(
            "Alice and Bob want to determine whether their inputs add to a target.",
            font_size=24,
            color=GRAY,
        ).next_to(checksum_eq, DOWN, buff=0.4)

        checksum_group = VGroup(checksum_title, checksum_eq, checksum_note)

        self.play(
            FadeOut(two_party_group, scale=0.9),
            FadeIn(checksum_group, shift=0.2 * UP),
            run_time=1.5,
        )
        self.wait(2)

        # Replace with three stick figures (Alice, Bob, Charlie) with numbers on foreheads
        self.play(FadeOut(checksum_group))

        names = ["Alice", "Bob", "Charlie"]
        numbers = ["X", "Y", "Z"]
        players = VGroup()
        for i in range(3):
            p = self._stick_figure(label=names[i], number=numbers[i])
            p.move_to(3 * (i - 1) * RIGHT)
            players.add(p)
        players.move_to(1.0 * DOWN).scale(0.95)

        self.play(LaggedStart(*[FadeIn(p) for p in players], lag_ratio=0.2))
        self.wait(2)

    def _stick_figure_no_number(self, label: str):
        """Stick figure with head, eyes, body, arms, legs, label below (no number on forehead)."""
        head = Circle(radius=0.22, color=WHITE)
        head.shift(UP * 0.35)
        eye_left = Dot(head.get_center() + 0.08 * LEFT + 0.02 * UP, color=BLACK, radius=0.04)
        eye_right = Dot(head.get_center() + 0.08 * RIGHT + 0.02 * UP, color=BLACK, radius=0.04)
        body_top = head.get_center() + 0.22 * DOWN
        body_bottom = body_top + DOWN * 0.45
        body = Line(body_top, body_bottom, color=WHITE)
        shoulder = body_top + DOWN * 0.12
        left_arm = Line(shoulder, shoulder + 0.35 * LEFT + 0.05 * UP, color=WHITE)
        right_arm = Line(shoulder, shoulder + 0.35 * RIGHT + 0.05 * UP, color=WHITE)
        left_leg = Line(body_bottom, body_bottom + 0.4 * DOWN + 0.18 * LEFT, color=WHITE)
        right_leg = Line(body_bottom, body_bottom + 0.4 * DOWN + 0.18 * RIGHT, color=WHITE)
        legs = VGroup(left_leg, right_leg)
        lbl = Text(label, font_size=20, color=GRAY).next_to(legs, DOWN, buff=0.08)
        return VGroup(head, eye_left, eye_right, body, left_arm, right_arm, left_leg, right_leg, lbl)

    def _stick_figure(self, label: str, number: int):
        """Stick figure with head, eyes, body, arms, legs, number on forehead, label below."""
        # Head and eyes
        head = Circle(radius=0.22, color=WHITE)
        head.shift(UP * 0.35)
        eye_left = Dot(head.get_center() + 0.08 * LEFT + 0.02 * UP, color=BLACK, radius=0.04)
        eye_right = Dot(head.get_center() + 0.08 * RIGHT + 0.02 * UP, color=BLACK, radius=0.04)
        # Body
        body_top = head.get_center() + 0.22 * DOWN
        body_bottom = body_top + DOWN * 0.45
        body = Line(body_top, body_bottom, color=WHITE)
        # Arms
        shoulder = body_top + DOWN * 0.12
        left_arm = Line(shoulder, shoulder + 0.35 * LEFT + 0.05 * UP, color=WHITE)
        right_arm = Line(shoulder, shoulder + 0.35 * RIGHT + 0.05 * UP, color=WHITE)
        # Legs
        left_leg = Line(body_bottom, body_bottom + 0.4 * DOWN + 0.18 * LEFT, color=WHITE)
        right_leg = Line(body_bottom, body_bottom + 0.4 * DOWN + 0.18 * RIGHT, color=WHITE)
        legs = VGroup(left_leg, right_leg)
        num = MathTex(str(number), font_size=32).next_to(head, UP, buff=0.12)
        lbl = Text(label, font_size=20, color=GRAY).next_to(legs, DOWN, buff=0.08)
        return VGroup(head, eye_left, eye_right, body, left_arm, right_arm, left_leg, right_leg, num, lbl)


# -----------------------------------------------------------------------------
# Scene 2: Three-party communication triangle


    """Alice, Bob, Charlie with X, Y, Z and arrows between every pair."""

class ThreePartyTriangleScene_2(Scene):
    """Alice, Bob, Charlie with X, Y, Z and arrows between every pair."""

    def construct(self):
        title = Text("Three-Party Communication", font_size=40)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        # Triangle layout
        alice = self._stick_figure("Alice", "X").move_to(3.2 * LEFT + 1.5 * DOWN)
        bob = self._stick_figure("Bob", "Y").move_to(3.2 * RIGHT + 1.5 * DOWN)
        charlie = self._stick_figure("Charlie", "Z").move_to(0.0 * RIGHT + 1.4 * UP)

        players = VGroup(alice, bob, charlie).scale(0.95)
        self.play(LaggedStart(*[FadeIn(p) for p in players], lag_ratio=0.2))
        self.wait(0.8)

        # Arrows for each pair, slightly offset so both directions are visible
        arrow_ab = Arrow(
            alice.get_right(), bob.get_left(),
            buff=0.35, color=YELLOW, max_tip_length_to_length_ratio=0.12,
        ).shift(0.16 * UP)

        arrow_ba = Arrow(
            bob.get_left(), alice.get_right(),
            buff=0.35, color=YELLOW, max_tip_length_to_length_ratio=0.12,
        ).shift(0.16 * DOWN)

        arrow_ac = CurvedArrow(
            alice.get_top() + 0.1 * UP,
            charlie.get_left() + 0.4 * UP,
            angle=0.4,
            color=YELLOW,
        )

        arrow_ca = CurvedArrow(
            charlie.get_left() + 0.5 * UP,
            alice.get_top() + 0.2 * UP,
            angle=0.4,
            color=YELLOW,
        )

        arrow_bc = CurvedArrow(
            bob.get_top() + 0.2 * UP,
            charlie.get_right() + 0.5 * UP,
            angle=0.4,
            color=YELLOW,
        )

        arrow_cb = CurvedArrow(
            charlie.get_right() + 0.4 * UP,
            bob.get_top() + 0.1 * UP,
            angle=0.4,
            color=YELLOW,
        )

        self.play(
            LaggedStart(
                GrowArrow(arrow_ab),
                GrowArrow(arrow_ba),
                Create(arrow_ac),
                Create(arrow_ca),
                Create(arrow_bc),
                Create(arrow_cb),
                lag_ratio=0.15,
            ),
            run_time=2.4,
        )
        self.wait(1)

        # Naive checksum communication cost
        triangle_group = VGroup(alice, bob, charlie)

        checksum_line = MathTex(
            r"\text{CHECKSUM still costs } O(\log_2 N) \text{ bits}",
            font_size=30,
        ).next_to(triangle_group, DOWN, buff=0.9)

        checksum_line2 = MathTex(
            r"\text{Each player can just reveal their number}",
            font_size=28,
        ).next_to(checksum_line, DOWN, buff=0.25)

        self.play(FadeIn(checksum_line), FadeIn(checksum_line2))
        self.wait(2)

        # Fade out communication arrows
        self.play(
            FadeOut(arrow_ab),
            FadeOut(arrow_ba),
            FadeOut(arrow_ac),
            FadeOut(arrow_ca),
            FadeOut(arrow_bc),
            FadeOut(arrow_cb),
        )
        self.wait(1)

        # Grab the XYZ labels
        x_label = alice[-2]
        y_label = bob[-2]
        z_label = charlie[-2]

        # Create tiny boxes around each variable
        box_x = SurroundingRectangle(x_label, buff=0.08, color=BLUE, stroke_width=3)
        box_y = SurroundingRectangle(y_label, buff=0.08, color=BLUE, stroke_width=3)
        box_z = SurroundingRectangle(z_label, buff=0.08, color=BLUE, stroke_width=3)

        self.play(
            Create(box_x),
            Create(box_y),
            Create(box_z),
        )
        self.wait(0.5)

        # Move XYZ onto the faces
        head_a = alice[0]
        head_b = bob[0]
        head_c = charlie[0]

        new_x = x_label.copy().move_to(head_a.get_center())
        new_y = y_label.copy().move_to(head_b.get_center())
        new_z = z_label.copy().move_to(head_c.get_center())

        new_box_x = SurroundingRectangle(new_x, buff=0.08, color=BLUE, stroke_width=3)
        new_box_y = SurroundingRectangle(new_y, buff=0.08, color=BLUE, stroke_width=3)
        new_box_z = SurroundingRectangle(new_z, buff=0.08, color=BLUE, stroke_width=3)

        # Background masks so head lines don't show through
        mask_x = BackgroundRectangle(new_x, color=BLACK, fill_opacity=1, buff=0.08)
        mask_y = BackgroundRectangle(new_y, color=BLACK, fill_opacity=1, buff=0.08)
        mask_z = BackgroundRectangle(new_z, color=BLACK, fill_opacity=1, buff=0.08)

        mask_x.set_z_index(1)
        mask_y.set_z_index(1)
        mask_z.set_z_index(1)

        new_x.set_z_index(2)
        new_y.set_z_index(2)
        new_z.set_z_index(2)

        new_box_x.set_z_index(3)
        new_box_y.set_z_index(3)
        new_box_z.set_z_index(3)

        self.add(mask_x, mask_y, mask_z)

        self.play(
            ReplacementTransform(x_label, new_x),
            ReplacementTransform(y_label, new_y),
            ReplacementTransform(z_label, new_z),
            ReplacementTransform(box_x, new_box_x),
            ReplacementTransform(box_y, new_box_y),
            ReplacementTransform(box_z, new_box_z),
        )

        self.bring_to_front(new_x, new_y, new_z, new_box_x, new_box_y, new_box_z)
        self.wait(1.5)

        # Transition to NOF explanation
        self.play(FadeOut(checksum_line), FadeOut(checksum_line2))

        title2 = Text("Number-On-Forehead (NOF) Communication", font_size=40)
        title2.to_edge(UP, buff=0.5)
        self.play(Transform(title, title2))

        nof_line = MathTex(
            r"\text{Each player sees everyone else's number, but not their own}",
            font_size=30,
        ).next_to(title, DOWN, buff=0.4)

        self.play(FadeIn(nof_line))
        self.wait(1)

        # Helper text at bottom
        sees_text = MathTex(r"\text{Alice sees } Y, Z", font_size=30)
        sees_text.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(sees_text))

        # Alice sees Y and Z, not X
        self.play(
            new_box_y.animate.set_color(GREEN),
            new_box_z.animate.set_color(GREEN),
            new_y.animate.set_color(GREEN),
            new_z.animate.set_color(GREEN),
            new_box_x.animate.set_stroke(opacity=0.25),
            new_x.animate.set_opacity(0.25),
        )
        self.wait(1.5)

        # Bob sees X and Z, not Y
        bob_text = MathTex(r"\text{Bob sees } X, Z", font_size=30).move_to(sees_text)
        self.play(
            Transform(sees_text, bob_text),
            new_box_x.animate.set_color(GREEN),
            new_box_z.animate.set_color(GREEN),
            new_x.animate.set_color(GREEN),
            new_z.animate.set_color(GREEN),
            new_box_y.animate.set_stroke(opacity=0.25),
            new_y.animate.set_opacity(0.25),
            new_box_x.animate.set_stroke(opacity=1),
            new_x.animate.set_opacity(1),
        )
        self.wait(1.5)

        # Charlie sees X and Y, not Z
        charlie_text = MathTex(r"\text{Charlie sees } X, Y", font_size=30).move_to(sees_text)
        self.play(
            Transform(sees_text, charlie_text),
            new_box_x.animate.set_color(GREEN),
            new_box_y.animate.set_color(GREEN),
            new_x.animate.set_color(GREEN),
            new_y.animate.set_color(GREEN),
            new_box_z.animate.set_stroke(opacity=0.25),
            new_z.animate.set_opacity(0.25),
            new_box_y.animate.set_stroke(opacity=1),
            new_y.animate.set_opacity(1),
        )
        self.wait(1.5)

        # Restore all to normal for next scene
        self.play(
            FadeOut(sees_text),
            FadeOut(nof_line),
            new_x.animate.set_color(WHITE).set_opacity(1),
            new_y.animate.set_color(WHITE).set_opacity(1),
            new_z.animate.set_color(WHITE).set_opacity(1),
            new_box_x.animate.set_color(BLUE).set_stroke(opacity=1),
            new_box_y.animate.set_color(BLUE).set_stroke(opacity=1),
            new_box_z.animate.set_color(BLUE).set_stroke(opacity=1),
        )
        self.wait(1)

        question_text = MathTex(r"\text{Using this, can we improve below} \log_2 N \text{ bits?}", font_size=30).move_to(sees_text)
        self.play(FadeIn(question_text))

    def _stick_figure(self, label: str, number: str):
        """Stick figure with head, eyes, body, arms, legs, number on forehead, label below."""
        head = Circle(radius=0.22, color=WHITE)
        head.shift(UP * 0.35)

        eye_left = Dot(head.get_center() + 0.08 * LEFT + 0.02 * UP, color=BLACK, radius=0.04)
        eye_right = Dot(head.get_center() + 0.08 * RIGHT + 0.02 * UP, color=BLACK, radius=0.04)

        body_top = head.get_center() + 0.22 * DOWN
        body_bottom = body_top + DOWN * 0.45
        body = Line(body_top, body_bottom, color=WHITE)

        shoulder = body_top + DOWN * 0.12
        left_arm = Line(shoulder, shoulder + 0.35 * LEFT + 0.05 * UP, color=WHITE)
        right_arm = Line(shoulder, shoulder + 0.35 * RIGHT + 0.05 * UP, color=WHITE)

        left_leg = Line(body_bottom, body_bottom + 0.4 * DOWN + 0.18 * LEFT, color=WHITE)
        right_leg = Line(body_bottom, body_bottom + 0.4 * DOWN + 0.18 * RIGHT, color=WHITE)
        legs = VGroup(left_leg, right_leg)

        num = MathTex(str(number), font_size=32).next_to(head, UP, buff=0.12)
        lbl = Text(label, font_size=20, color=GRAY).next_to(legs, DOWN, buff=0.08)

        return VGroup(head, eye_left, eye_right, body, left_arm, right_arm, left_leg, right_leg, num, lbl)

# -----------------------------------------------------------------------------
# Scene 3: Introduction to 3-AP-Free Sets
# -----------------------------------------------------------------------------
class ThreeAPFreeIntroScene_3(Scene):
    """Introduce 3-term arithmetic progressions and 3-AP-free sets on a number line."""

    def construct(self):
        title = Text("3-AP-Free Sets", font_size=42)
        title.to_edge(UP, buff=0.45)

        subtitle = MathTex(
            r"\text{A 3-term arithmetic progression is } a,\, a+d,\, a+2d",
            font_size=32,
        ).next_to(title, DOWN, buff=0.3)

        self.play(FadeIn(title), FadeIn(subtitle))
        self.wait(1)

        # Number line
        number_line = NumberLine(
            x_range=[1, 12, 1],
            length=10,
            include_numbers=True,
            include_tip=False,
            font_size=28,
        )
        number_line.shift(0.4 * DOWN)

        self.play(Create(number_line))
        self.wait(0.6)

        # ------------------------------------------------------------------
        # Part 1: A set that is NOT 3-AP-free
        # ------------------------------------------------------------------
        bad_label = Text("Not 3-AP-free", font_size=30, color=RED)
        bad_label.next_to(number_line, UP, buff=0.5)

        bad_set_tex = MathTex(
            r"S=\{2,4,6,9\}",
            font_size=34,
            color=RED,
        ).next_to(number_line, DOWN, buff=0.8)

        self.play(FadeIn(bad_label), FadeIn(bad_set_tex))
        self.wait(0.5)

        bad_points_vals = [2, 4, 6, 9]
        bad_points = VGroup(*[
            Dot(number_line.n2p(x), radius=0.10, color=RED)
            for x in bad_points_vals
        ])

        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in bad_points], lag_ratio=0.18))
        self.wait(0.8)

        # Highlight the progression 2,4,6
        ap_points = VGroup(*[
            Dot(number_line.n2p(x), radius=0.13, color=YELLOW)
            for x in [2, 4, 6]
        ])
        ap_line = Line(
            number_line.n2p(2), number_line.n2p(6),
            color=YELLOW, stroke_width=6
        )
        ap_brace = Brace(ap_line, DOWN, color=YELLOW)
        ap_text = MathTex(
            r"2,4,6 \quad (\text{equal spacing})",
            font_size=30,
            color=YELLOW,
        ).next_to(ap_brace, DOWN, buff=0.2)

        mid_arrows = VGroup(
            Arrow(number_line.n2p(2) + 0.22 * UP, number_line.n2p(4) + 0.22 * UP, buff=0.05, color=YELLOW),
            Arrow(number_line.n2p(4) + 0.22 * UP, number_line.n2p(6) + 0.22 * UP, buff=0.05, color=YELLOW),
        )

        self.play(
            FadeIn(ap_points),
            Create(ap_line),
            GrowArrow(mid_arrows[0]),
            GrowArrow(mid_arrows[1]),
        )
        self.play(GrowFromCenter(ap_brace), FadeIn(ap_text))
        self.wait(1.8)

        cross = Cross(bad_label, stroke_color=RED, stroke_width=8)
        self.play(Create(cross))
        self.wait(0.8)

        # Fade out bad example
        self.play(
            FadeOut(bad_label),
            FadeOut(bad_set_tex),
            FadeOut(bad_points),
            FadeOut(ap_points),
            FadeOut(ap_line),
            FadeOut(mid_arrows),
            FadeOut(ap_brace),
            FadeOut(ap_text),
            FadeOut(cross),
        )
        self.wait(0.4)

        # ------------------------------------------------------------------
        # Part 2: A set that IS 3-AP-free
        # ------------------------------------------------------------------
        good_label = Text("3-AP-free", font_size=30, color=GREEN)
        good_label.next_to(number_line, UP, buff=0.5)

        good_set_tex = MathTex(
            r"T=\{1,2,4,8,11\}",
            font_size=34,
            color=GREEN,
        ).next_to(number_line, DOWN, buff=0.8)

        self.play(FadeIn(good_label), FadeIn(good_set_tex))
        self.wait(0.5)

        good_points_vals = [1, 2, 4, 8, 11]
        good_points = VGroup(*[
            Dot(number_line.n2p(x), radius=0.10, color=GREEN)
            for x in good_points_vals
        ])

        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in good_points], lag_ratio=0.15))
        self.wait(1)

        # Check a few tempting triples and reject them
        trial1 = VGroup(
            Circle(radius=0.18, color=BLUE).move_to(number_line.n2p(1)),
            Circle(radius=0.18, color=BLUE).move_to(number_line.n2p(2)),
            Circle(radius=0.18, color=BLUE).move_to(number_line.n2p(4)),
        )
        trial1_text = MathTex(
            r"1,2,4 \text{ is not equally spaced}",
            font_size=28,
            color=BLUE,
        ).next_to(good_set_tex, DOWN, buff=0.35)

        self.play(Create(trial1), FadeIn(trial1_text))
        self.wait(1)
        self.play(FadeOut(trial1), FadeOut(trial1_text))

        trial2 = VGroup(
            Circle(radius=0.18, color=BLUE).move_to(number_line.n2p(2)),
            Circle(radius=0.18, color=BLUE).move_to(number_line.n2p(4)),
            Circle(radius=0.18, color=BLUE).move_to(number_line.n2p(8)),
        )
        trial2_text = MathTex(
            r"2,4,8 \text{ is not equally spaced either}",
            font_size=28,
            color=BLUE,
        ).next_to(good_set_tex, DOWN, buff=0.35)

        self.play(Create(trial2), FadeIn(trial2_text))
        self.wait(1)
        self.play(FadeOut(trial2), FadeOut(trial2_text))

        # Final statement
        good_box = SurroundingRectangle(good_set_tex, color=GREEN, buff=0.18, stroke_width=3)
        final_text = MathTex(
            r"\text{No three chosen points form } a,\,a+d,\,a+2d",
            font_size=30,
            color=GREEN,
        ).next_to(good_set_tex, DOWN, buff=0.35)

        self.play(Create(good_box), FadeIn(final_text))
        self.wait(2)

        # Optional transition emphasis
        sparkle_group = VGroup(*[
            Star(n=5, outer_radius=0.08, inner_radius=0.04, color=YELLOW)
            .move_to(number_line.n2p(x) + 0.28 * UP)
            for x in good_points_vals
        ])
        self.play(LaggedStart(*[FadeIn(s, scale=0.3) for s in sparkle_group], lag_ratio=0.08))
        self.wait(1.2)

        # Clean ending
        self.play(
            FadeOut(good_label),
            FadeOut(good_set_tex),
            FadeOut(good_points),
            FadeOut(good_box),
            FadeOut(final_text),
            FadeOut(sparkle_group),
            FadeOut(number_line),
            FadeOut(title),
            FadeOut(subtitle),
        )


# -----------------------------------------------------------------------------
# Scene 4: Why 3-AP means x + y = 2z
# -----------------------------------------------------------------------------
class ThreeAPEquationScene_4(Scene):
    """Show that in a 3-AP, the middle term is the average of the endpoints."""

    def construct(self):
        # Start clean
        self.clear()

        title = Text("What Does a 3-Term Progression Mean?", font_size=40)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title))
        self.wait(0.6)

        intro = MathTex(
            r"\text{Suppose we order the numbers as } X < Z < Y",
            font_size=34,
        ).next_to(title, DOWN, buff=0.45)
        self.play(FadeIn(intro))
        self.wait(1)

        # Number line
        number_line = NumberLine(
            x_range=[0, 10, 1],
            length=10,
            include_tip=False,
            include_numbers=False,
        ).shift(0.6 * DOWN)

        self.play(Create(number_line))
        self.wait(0.4)

        # Example positions
        x_pos = 2
        z_pos = 5
        y_pos = 8

        x_dot = Dot(number_line.n2p(x_pos), radius=0.11, color=BLUE)
        z_dot = Dot(number_line.n2p(z_pos), radius=0.11, color=GREEN)
        y_dot = Dot(number_line.n2p(y_pos), radius=0.11, color=BLUE)

        x_lbl = MathTex("x", font_size=34, color=BLUE).next_to(x_dot, DOWN, buff=0.18)
        z_lbl = MathTex("z", font_size=34, color=GREEN).next_to(z_dot, DOWN, buff=0.18)
        y_lbl = MathTex("y", font_size=34, color=BLUE).next_to(y_dot, DOWN, buff=0.18)

        self.play(
            LaggedStart(
                FadeIn(x_dot), FadeIn(x_lbl),
                FadeIn(z_dot), FadeIn(z_lbl),
                FadeIn(y_dot), FadeIn(y_lbl),
                lag_ratio=0.12,
            )
        )
        self.wait(0.8)

        # Show equal spacing
        left_seg = Line(number_line.n2p(x_pos), number_line.n2p(z_pos), color=YELLOW, stroke_width=6)
        right_seg = Line(number_line.n2p(z_pos), number_line.n2p(y_pos), color=YELLOW, stroke_width=6)

        d_left = Brace(left_seg, UP, buff=0.08, color=YELLOW)
        d_right = Brace(right_seg, UP, buff=0.08, color=YELLOW)

        d_left_lbl = MathTex("d", font_size=30, color=YELLOW).next_to(d_left, UP, buff=0.08)
        d_right_lbl = MathTex("d", font_size=30, color=YELLOW).next_to(d_right, UP, buff=0.08)

        self.play(Create(left_seg), Create(right_seg))
        self.play(
            GrowFromCenter(d_left),
            GrowFromCenter(d_right),
            FadeIn(d_left_lbl),
            FadeIn(d_right_lbl),
        )
        self.wait(1)

        eq1 = MathTex(
            r"d = z - x = y - z",
            font_size=38,
        ).next_to(number_line, DOWN, buff=1.0)

        self.play(Write(eq1))
        self.wait(1.2)

        # Emphasize z as midpoint / average
        midpoint_text = Text("So z sits exactly halfway between x and y", font_size=28, color=GRAY)
        midpoint_text.next_to(eq1, DOWN, buff=0.35)

        midpoint_arrow_left = Arrow(
            z_dot.get_top() + 0.15 * UP,
            z_dot.get_top() + 0.01 * UP,
            buff=0.02,
            color=GREEN,
            max_tip_length_to_length_ratio=0.25,
        )
        midpoint_circle = Circle(radius=0.22, color=GREEN, stroke_width=3).move_to(z_dot)

        self.play(FadeIn(midpoint_text), GrowArrow(midpoint_arrow_left), Create(midpoint_circle))
        self.wait(1.4)

        # Algebra derivation
        eq2 = MathTex(
            r"z - x = y - z",
            font_size=38,
        ).move_to(eq1)

        eq3 = MathTex(
            r"2z = x + y",
            font_size=42,
            color=GREEN,
        ).move_to(eq1)

        self.play(Transform(eq1, eq2))
        self.wait(0.9)
        self.play(Transform(eq1, eq3))
        self.wait(1.2)

        avg_text = Text("The middle term is the average of the two endpoints.", font_size=28)
        avg_text.next_to(eq1, DOWN, buff=0.35)

        avg_eq = MathTex(
            r"z = \frac{x+y}{2}",
            font_size=40,
            color=GREEN,
        ).next_to(avg_text, DOWN, buff=0.28)

        self.play(FadeOut(midpoint_text), FadeIn(avg_text), Write(avg_eq))
        self.wait(1.5)

        # Final summary box
        summary_box = SurroundingRectangle(VGroup(eq1, avg_eq), color=GREEN, buff=0.2, stroke_width=3)
        self.play(Create(summary_box))
        self.wait(2)
# -----------------------------------------------------------------------------
# Scene: Geometry behind Behrend's construction
# -----------------------------------------------------------------------------
class BehrendGeometryScene_5(Scene):
    """Explain why spheres contain no nontrivial 3-term arithmetic progressions."""

    def construct(self):
        title = Text("Geometry Behind Behrend's Construction", font_size=40)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title))
        self.wait(0.5)

        # ------------------------------------------------------------------
        # Part 1: 2D circle intuition
        # ------------------------------------------------------------------
        part1 = Text("Start with the 2D unit circle", font_size=30)
        part1.next_to(title, DOWN, buff=0.35)
        self.play(FadeIn(part1))

        plane = NumberPlane(
            x_range=[-1.5, 1.5, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=5,
            y_length=5,
            background_line_style={"stroke_opacity": 0.25},
        ).shift(3.2 * LEFT + 0.6 * DOWN)

        circle = Circle(radius=1.6, color=BLUE).move_to(plane.get_origin())

        circle_label = MathTex(
            r"x_1^2 + x_2^2 = 1",
            font_size=30,
            color=BLUE,
        ).next_to(plane, DOWN, buff=0.25)

        self.play(Create(plane), Create(circle), FadeIn(circle_label))
        self.wait(0.7)

        # Two points on circle and midpoint inside
        p1 = plane.c2p(-0.8, 0.6)
        p2 = plane.c2p(0.8, 0.6)
        midpoint = (p1 + p2) / 2

        dot1 = Dot(p1, color=YELLOW, radius=0.08)
        dot2 = Dot(p2, color=YELLOW, radius=0.08)
        mid_dot = Dot(midpoint, color=RED, radius=0.08)

        secant = Line(p1, p2, color=YELLOW, stroke_width=5)

        dot1_label = MathTex("x", font_size=28, color=YELLOW).next_to(dot1, UP + LEFT, buff=0.08)
        dot2_label = MathTex("y", font_size=28, color=YELLOW).next_to(dot2, UP + RIGHT, buff=0.08)
        mid_label = MathTex(r"\frac{x+y}{2}", font_size=28, color=RED).next_to(mid_dot, DOWN, buff=0.12)

        self.play(
            FadeIn(dot1), FadeIn(dot2),
            FadeIn(dot1_label), FadeIn(dot2_label),
            Create(secant),
        )
        self.wait(0.6)
        self.play(FadeIn(mid_dot), FadeIn(mid_label))
        self.wait(0.8)

        circle_text1 = Text(
            "If x and y are distinct points on the circle,",
            font_size=24,
        ).move_to(3.3 * RIGHT + 1.6 * DOWN)

        circle_text2 = Text(
            "their midpoint lies inside the circle.",
            font_size=24,
            color=RED,
        ).next_to(circle_text1, DOWN, buff=0.18)

        circle_text3 = MathTex(
            r"\Rightarrow \frac{x+y}{2} \notin S_2",
            font_size=30,
            color=RED,
        ).next_to(circle_text2, DOWN, buff=0.25)

        self.play(FadeIn(circle_text1), FadeIn(circle_text2), FadeIn(circle_text3))
        self.wait(1.2)

        circle_text4 = MathTex(
            r"\text{So } S_2 \text{ contains no 3 distinct points in arithmetic progression.}",
            font_size=28,
            color=GREEN,
        ).next_to(circle_text3, DOWN, buff=0.3)

        self.play(FadeIn(circle_text4))

        self.wait(1)
        self.play(FadeOut(circle_text1), FadeOut(circle_text2), FadeOut(circle_text3), FadeOut(circle_text4))

        # ------------------------------------------------------------------
        # Part 2: Generalize to d dimensions
        # ------------------------------------------------------------------
        left_group = VGroup(
            plane, circle, circle_label,
            dot1, dot2, mid_dot, secant,
            dot1_label, dot2_label, mid_label
        )

        self.play(
            left_group.animate.scale(0.8).to_edge(LEFT, buff=0.5),
        )
        self.wait(0.4)

        part2 = Text("Generalize to any dimension", font_size=30)
        part2.next_to(left_group, RIGHT, buff=1.0).shift(1.3 * UP)

        sphere_def = MathTex(
            r"S_d = \{(x_1,\dots,x_d): x_1^2+\dots+x_d^2=1\}",
            font_size=30,
        ).next_to(part2, DOWN, buff=0.3)

        sphere_note = Text(
            "This is the d-dimensional unit sphere.",
            font_size=24,
            color=GRAY,
        ).next_to(sphere_def, DOWN, buff=0.18)

        coord_cap = MathTex(
            r"x_i \in \{1,2,\dots,k\}",
            font_size=32,
            color=BLUE,
        ).next_to(sphere_note, DOWN, buff=0.3).shift(LEFT * 0.4)

        coord_note = Text(
            "So each input is capped at k in every coordinate.",
            font_size=24,
            color=GRAY,
        ).next_to(coord_cap, DOWN, buff=0.18)

        self.play(FadeIn(part2), Write(sphere_def), FadeIn(sphere_note))
        self.wait(0.8)
        self.play(Write(coord_cap), FadeIn(coord_note))
        self.wait(1.2)

        # Clear some text before adding more, to save space
        self.play(
            FadeOut(sphere_note),
            FadeOut(coord_note),
            FadeOut(coord_cap),
        )

        gen_text1 = Text(
            "The same midpoint argument still works.",
            font_size=24,
        ).next_to(coord_cap, DOWN, buff=0.3)

        gen_text2 = MathTex(
            r"\text{If } x,z,y \in S_d \text{ form a 3-AP, then } z=\frac{x+y}{2}.",
            font_size=28,
        ).next_to(gen_text1, DOWN, buff=0.2)

        self.play(FadeIn(gen_text1), FadeIn(gen_text2))
        self.wait(1.1)

        # Clear again before the geometric conclusion
        self.play(FadeOut(gen_text1), FadeOut(gen_text2))

        gen_text3 = Text(
            "A line can intersect a sphere in at most two points.",
            font_size=26,
            color=RED,
        ).next_to(coord_cap, DOWN, buff=0.32)

        gen_text4 = MathTex(
            r"\Rightarrow S_d \text{ contains no 3 distinct collinear points}",
            font_size=28,
            color=GREEN,
        ).next_to(gen_text3, DOWN, buff=0.22)

        gen_text5 = MathTex(
            r"\Rightarrow S_d \text{ contains no nontrivial 3-term arithmetic progression.}",
            font_size=30,
            color=GREEN,
        ).next_to(gen_text4, DOWN, buff=0.22)

        self.play(FadeIn(gen_text3))
        self.wait(0.8)
        self.play(FadeIn(gen_text4), FadeIn(gen_text5))
        self.wait(2)

        # ------------------------------------------------------------------
        # Generalize radius and compute size of S
        # ------------------------------------------------------------------

        unit_circle_text = VGroup(part1, gen_text3, gen_text4, gen_text5)
        two_figures = VGroup(part2, sphere_def)
        self.play(FadeOut(left_group), FadeOut(unit_circle_text), two_figures.animate.next_to(title, DOWN, buff=0.35))
        self.wait(0.5)
        
        part2_new = Text("Generalize to any radius", font_size=30)
        part2_new.move_to(part2)

        sphere_def_new = MathTex(
            r"S_d = \{(x_1,\dots,x_d): x_1^2+\dots+x_d^2=R\}",
            font_size=30,
        )
        sphere_def_new.move_to(sphere_def)

        self.play(Transform(part2, part2_new), TransformMatchingShapes(sphere_def, sphere_def_new))
        self.wait(3)

        S_R_length_question = MathTex(
            r"\text{How big is } |S_R|?",
            font_size=40,
            color=WHITE,
        ).next_to(sphere_def_new, DOWN, buff=0.5)

        self.play(FadeIn(S_R_length_question))
        self.wait(3)

        claim = MathTex(
            r"\exists \space R \le k^2d \text{ such that } |S_R| \ge \frac {k^d} {k^2d}",
            font_size=35,
            color=RED,
        ).next_to(S_R_length_question, DOWN, buff=0.3)  

        self.play(FadeIn(claim))
        self.wait(11) 

        averaging_argument = MathTex(
            r"\text{Averaging Argument } \rightarrow \text{ at least one shell containing average number of points = }\frac {\text{\# of points}} {\text {\# of shells}}",
            font_size=30,
            color=WHITE,
        ).next_to(claim, DOWN, buff=0.25)

        self.play(FadeIn(averaging_argument))
        self.wait(15)

        big_claim = VGroup(claim, averaging_argument)

        self.play(FadeOut(part2), FadeOut(sphere_def_new), FadeOut(S_R_length_question), big_claim.animate.next_to(title, DOWN, buff=0.3))

        num_points = MathTex(
            r"x \in [k]^d \rightarrow \text{ There are } k^d \text{ points}",
            font_size=30,
            color=RED,
        ).next_to(big_claim, DOWN, buff=0.3)     

        self.play(FadeIn(num_points))
        self.wait(5)

        num_shells = MathTex(
            r"\text{Number of possible values of } R \text{ corresponds to number of shells}",
            font_size=30,
            color=WHITE,
        ).next_to(num_points, DOWN, buff=0.3)     

        self.play(FadeIn(num_shells))
        self.wait(4)    

        num_shells_eq = MathTex(
            r"R = \sum_{i = 1}^{d} x_i^2 \le d*k^2",
            font_size=30,
            color=WHITE,
        ).next_to(num_shells, DOWN, buff=0.3)   

        num_shells_eq_explanation = MathTex(
            r"\text{The max value of } x_i \text{ is } k \rightarrow \text{The max value of } \sum_{i = 1}^{d} x_i^2 \text{ is } d*k^2",
            font_size=30,
            color=RED,
        ).next_to(num_shells_eq, DOWN, buff=0.3)    

        self.play(FadeIn(num_shells_eq), FadeIn(num_shells_eq_explanation))
        self.wait(11.5)  

        self.play(Indicate(claim)) 
        self.wait(2) 

# -----------------------------------------------------------------------------
# Scene: Mapping Vector to Integer
# -----------------------------------------------------------------------------
class MappingScene_6(Scene):
    """Explain mapping vectors to integers"""

    def construct(self):
        title = Text("Mapping Vectors to Integers", font_size=40)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title))
        self.wait(0.5)

        goal = MathTex(
            r"\text{Goal: Find a mapping } f: S_R \rightarrow \mathbb{Z}",
            font_size=30,
            color=RED,
        ).next_to(title, DOWN, buff=0.3) 

        self.play(FadeIn(goal))
        self.wait(10)

        simplify_0 = MathTex(
            r"x \in \{0,1\}^d",
            font_size=30,
            color=RED,
        )

        summation_0 = MathTex(
            r"f(x) = \sum_{i=1}^{d}x_i*2^{i-1}",
            font_size=30,
            color=RED,
        ).next_to(simplify_0, RIGHT, buff=0.5)

        binary_info = VGroup(simplify_0, summation_0).next_to(goal, DOWN, buff=0.3) 

        self.play(FadeIn(binary_info))
        self.wait(14)

        example_0 = MathTex(
            r"x = \{x_4, x_3, x_2, x_1\}",
            font_size=25,
            color=WHITE,
        ).next_to(binary_info, DOWN, buff=0.5)

        self.play(FadeIn(example_0))
        self.wait(1)

        example_1 = MathTex(
            r"x = \{1, 1, 0, 1\}",
            font_size=25,
            color=WHITE,
        )
        example_1.move_to(example_0)

        self.play(Transform(example_0, example_1))
        self.wait(1)

        binary_eq_0 = MathTex(
            r"f(x) = \sum_{i=1}^{d}x_i*2^{i-1}",
            font_size=30,
            color=RED,
        ).next_to(simplify_0, RIGHT, buff=0.5)

        self.play(FadeIn(binary_eq_0))

        binary_eq_1 = MathTex(
            r"f(x) = \sum_{i=1}^{d}x_i*2^{i-1}",
            font_size=30,
            color=RED,
        ).next_to(example_1, DOWN, buff=0.3)

        self.play(Transform(binary_eq_0, binary_eq_1))
        self.wait(1)

        binary_eq_2 = MathTex(
            r"f(x) = x_4*2^3 + x_3*2^2 +x_2*2^1 + x_1*2^0",
            font_size=30,
            color=RED,
        )

        self.play(Transform(binary_eq_0, binary_eq_2))
        self.wait(1)

        binary_eq_3 = MathTex(
            r"f(x) = 1*8 + 1*4 + 0*2 + 1*1",
            font_size=30,
            color=RED,
        ).move_to(binary_eq_1)

        self.play(Transform(binary_eq_0, binary_eq_3))
        self.wait(1)

        binary_eq_4 = MathTex(
            r"f(x) = 13",
            font_size=30,
            color=RED,
        ).move_to(binary_eq_2)

        self.play(Transform(binary_eq_0, binary_eq_4))
        self.wait(2)

        self.play(FadeOut(example_0), FadeOut(binary_eq_0))

        simplify_1 = MathTex(
            r"x \in \{0,k\}^d",
            font_size=30,
            color=RED,
        ).move_to(simplify_0)

        summation_1 = MathTex(
            r"f(x) = \sum_{i=1}^{d}x_i*", r"(2k+1)", r"^{i-1}",
            font_size=30,
            color=RED,
        ).move_to(summation_0)

        self.play(Transform(simplify_0, simplify_1.shift(0.3 * LEFT)), Transform(summation_0, summation_1.shift(0.5 * RIGHT)))
        self.wait(7)

        self.play(Indicate(summation_1[1]))
        self.wait(3)

        red_group = VGroup(simplify_0, summation_0)

        three_ap_eq_0 = MathTex(
            r"x+y=2z",
            font_size=30,
            color=WHITE,
        ).next_to(red_group, DOWN, buff=0.5)

        self.play(FadeIn(three_ap_eq_0))
        self.wait(2)

        three_ap_eq_1 = MathTex(
            r"f(x)+f(y)=2*f(z)",
            font_size=30,
            color=WHITE,
        ).move_to(three_ap_eq_0)

        self.play(Transform(three_ap_eq_0, three_ap_eq_1))
        self.wait(1)

        left_side_0 = MathTex(
            r"f(x)+f(y)", r"2*f(z)",
            font_size=30,
            color=WHITE,
        ).move_to(three_ap_eq_0)

        left_side_1 = MathTex(
            r"f(x)+f(y)",
            font_size=30,
            color=WHITE,
        ).next_to(three_ap_eq_0, DOWN, buff=0.5)

        self.play(TransformMatchingShapes(left_side_0[0], left_side_1))
        self.wait(1)

        left_side_2 = MathTex(
            r"f(x) +f(y) = \sum_{i=1}^{d}", r"(x_i+y_i)", r"*", r"(2k+1)", r"^{i-1}",
            font_size=30,
            color=WHITE,
        ).move_to(left_side_1)

        self.play(Transform(left_side_1, left_side_2))
        self.wait(2)

        self.play(Indicate(left_side_2[1]))
        self.wait(5)

        self.play(Indicate(left_side_2[3]))
        self.wait(2)  

        right_side_1 = MathTex(
            r"2*f(z)",
            font_size=30,
            color=WHITE,
        ).next_to(left_side_1, DOWN, buff=0.5)

        self.play(TransformMatchingShapes(left_side_0[1], right_side_1))
        self.wait(1)

        right_side_2 = MathTex(
            r"2*f(z)= \sum_{i=1}^{d}", r"(2*z_i)", r"*", r"(2k+1)", r"^{i-1}",
            font_size=30,
            color=WHITE,
        ).move_to(right_side_1)

        self.play(Transform(right_side_1, right_side_2))
        self.wait(3)

        self.play(Indicate(right_side_2[1]))
        self.wait(2)

        self.play(Indicate(right_side_2[3]))
        self.wait(2) 

        conclusion = Text(
            "No carry over!",
            font_size=40,
            color=YELLOW,
        ).next_to(right_side_1, DOWN, buff=0.5)  

        self.play(FadeIn(conclusion))
        self.wait(2)

# -----------------------------------------------------------------------------
# Scene: S_R Arithmetic
# -----------------------------------------------------------------------------
class S_RArithmeticScene_7(Scene):
    """Explain S_R Arithmetic"""

    def construct(self):
        title = MathTex(r"|S_R| \text{ in terms of } N", font_size=40)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title))
        self.wait(0.5)

        # Number line
        number_line = NumberLine(
            x_range=[1, 11, 1],
            length=10,
            include_numbers=False,
            include_tip=False,
            font_size=28,
        ).next_to(title, DOWN, buff=0.5)

        label_1 = MathTex("0").next_to(number_line.n2p(1), DOWN)
        label_2 = MathTex("1").next_to(number_line.n2p(2), DOWN)
        label_3 = MathTex("2").next_to(number_line.n2p(3), DOWN)
        label_end = MathTex("N = (2k+1)^d").next_to(number_line.n2p(11), DOWN)

        dot_1 = Dot(number_line.n2p(1), radius=0.10, color=RED)
        dot_end = Dot(number_line.n2p(11), radius=0.10, color=RED)

        self.play(FadeIn(number_line), FadeIn(label_1), FadeIn(label_2), FadeIn(label_3), FadeIn(label_end), FadeIn(dot_1), FadeIn(dot_end))
        self.wait(3)

        S_R_length = MathTex(
            r"\exists \space R \le k^2d \text{ such that } |S_R| \ge \frac {k^d} {k^2d}",
            font_size=35,
            color=RED,
        ).next_to(number_line, DOWN, buff=1) 

        self.play(FadeIn(S_R_length))
        self.wait(5)

        question = MathTex(
            r"\text{How to represent } k^d \text{ in terms of } N \text{?}",
            font_size=30,
            color=WHITE,
        ).next_to(S_R_length, DOWN, buff=0.5)

        self.play(FadeIn(question))
        self.wait(3)

        eq = MathTex(
            r"k^d \approx \frac 1 {2^d} * N^d",
            font_size=30,
            color=WHITE,
        ).next_to(question, DOWN, buff=0.5)

        self.play(FadeIn(eq))
        self.wait(3)

        eq_0 = MathTex(
            r"k^d \approx \frac 1 {2^d} * N^d",
            font_size=30,
            color=WHITE,
        ).move_to(eq)

        eq_1 = MathTex(
            r"k^d \approx \frac 1 {2^d} * N^d",
            font_size=30,
            color=WHITE,
        ).next_to(eq, DOWN, buff=0.5)

        self.play(Transform(eq_0, eq_1))
        self.wait(2)

        eq_2 = MathTex(
            r"k^d \approx \frac 1 {2^d} * (2k+1)^d",
            font_size=30,
            color=WHITE,
        ).move_to(eq_0)

        self.play(Transform(eq_0, eq_2))
        self.wait(1)

        eq_3 = MathTex(
            r"k^d \approx \frac 1 {2^d} * 2^d * k^d",
            font_size=30,
            color=WHITE,
        ).move_to(eq_0)

        self.play(Transform(eq_0, eq_3))
        self.wait(1)

        eq_4 = MathTex(
            r"k^d \approx k^d",
            font_size=30,
            color=WHITE,
        ).move_to(eq_0)

        self.play(Transform(eq_0, eq_4))
        self.wait(1)

        self.play(FadeOut(question), FadeOut(eq_0), eq.animate.shift(1 * UP))
        self.wait(2)

        plug_in_0 = MathTex(
            r"\exists \space R \le k^2d \text{ such that }", r"|S_R| \ge \frac {k^d} {k^2d}",
            font_size=35,
            color=RED,
        ).move_to(S_R_length) 

        plug_in_1 = MathTex(
            r"|S_R| \ge \frac {k^d} {k^2d}",
            font_size=35,
            color=RED,
        ).next_to(eq, DOWN, buff=0.5) 

        self.play(Transform(plug_in_0[1], plug_in_1))
        self.wait(3)

        plug_in_2 = MathTex(
            r"|S_R| \ge \frac 1 {2^d}*N*\frac {1} {k^2d}",
            font_size=35,
            color=RED,
        ).move_to(plug_in_0[1]) 

        self.play(Transform(plug_in_0[1], plug_in_2))
        self.wait(2)

        plug_in_3 = MathTex(
            r"|S_R| \ge \frac {N} {2^dk^2d}",
            font_size=35,
            color=RED,
        ).move_to(plug_in_0[1]) 

        self.play(Transform(plug_in_0[1], plug_in_3))
        self.wait(5)

        solution = MathTex(
            r"\text{Optimizing } k,d \rightarrow 2k+1 = 2^{\sqrt{\log N}}, d = \sqrt{\log N} \rightarrow", r"|S_R| \ge \frac N {2^{c*\sqrt{\log N}}}",
            font_size=35,
            color=YELLOW,
        ).next_to(plug_in_0[1], DOWN, buff=0.5)

        self.play(FadeIn(solution))
        self.wait(8)

        self.play(Indicate(solution[1]))
        self.wait(2)

# -----------------------------------------------------------------------------
# Scene: Explain Coloring
# -----------------------------------------------------------------------------
class ColoringScene_8(Scene):
    """Explain Coloring"""

    def construct(self):
        title = MathTex(r"3\text{AP-Free Coloring}", font_size=40)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title))
        self.wait(0.5)

        # Number line
        number_line = NumberLine(
            x_range=[1, 11, 1],
            length=10,
            include_numbers=False,
            include_tip=False,
            font_size=28,
        ).next_to(title, DOWN, buff=1)

        dot_1_white = Dot(number_line.n2p(2), radius=0.20, color=WHITE)
        dot_2_white = Dot(number_line.n2p(4), radius=0.20, color=WHITE)
        dot_3_white = Dot(number_line.n2p(6), radius=0.20, color=WHITE)
        dot_4_white = Dot(number_line.n2p(9), radius=0.20, color=WHITE)

        self.play(FadeIn(number_line), FadeIn(dot_1_white), FadeIn(dot_2_white), FadeIn(dot_3_white), FadeIn(dot_4_white))
        self.wait(2)

        dot_1 = Dot(number_line.n2p(2), radius=0.20, color=YELLOW)
        dot_2 = Dot(number_line.n2p(4), radius=0.20, color=RED)
        dot_3 = Dot(number_line.n2p(6), radius=0.20, color=YELLOW)
        dot_4 = Dot(number_line.n2p(9), radius=0.20, color=BLUE)

        self.play(FadeIn(dot_1))
        self.play(FadeIn(dot_2))
        self.play(FadeIn(dot_3))
        self.play(FadeIn(dot_4))

        goal_0 = MathTex(
            r"\text{Goal: Find a coloring }", r"\chi: \{1, ..., N\} \rightarrow [\text{colors}]",
            font_size=30,
            color=WHITE,
        ).next_to(number_line, DOWN, buff=1) 

        self.play(FadeIn(goal_0))
        self.wait(5)

        goal_1 = MathTex(
            r"\text{such that there is no }", r"\text{monochromatic 3AP}",
            font_size=30,
            color=WHITE,
        ).next_to(goal_0, DOWN, buff=0.3) 

        self.play(FadeIn(goal_1))
        self.wait(3)
        self.play(Indicate(goal_1[1]))
        self.wait(2)

        goal_2 = MathTex(
            r"\nexists \text{ } a, b, c \text{ such that } a+b = 2c \text{ and } \chi(a) = \chi(b) = \chi(c)",
            font_size=30,
            color=YELLOW,
        ).next_to(goal_1, DOWN, buff=0.3) 

        self.play(FadeIn(goal_2), FadeOut(dot_2_white))
        self.wait(6)

        self.play(Indicate(dot_2))
        self.wait(1)

        dot_2_3AP = Dot(number_line.n2p(4), radius=0.20, color=YELLOW)        
        self.play(FadeIn(dot_2_3AP), FadeOut(dot_1_white), FadeOut(dot_3_white))
        self.wait(4)

        self.play(Indicate(dot_1), Indicate(dot_2_3AP), Indicate(dot_3))
        self.wait(2)

        fade = VGroup(number_line, dot_1, dot_2, dot_3, dot_4, dot_2_3AP, dot_4_white, goal_0[0], goal_1, goal_2)
        self.play(goal_0[1].animate.next_to(title, DOWN, buff=0.5), FadeOut(fade))
        self.wait(1)

        behrend = MathTex(
            r"|S_R| \ge \frac N {2^{c*\sqrt{\log N}}}",
            font_size=30,
            color=YELLOW,
        ).next_to(goal_0[1], LEFT, buff=0.7) 

        self.play(FadeIn(behrend))
        self.wait(3)

        behrend_coloring = MathTex(
            r"\chi: \{1, ..., N\} \rightarrow [2^{c*\sqrt{\log N}}]",
            font_size=30,
            color=WHITE,
        ).move_to(goal_0[1])

        self.play(TransformMatchingShapes(goal_0[1], behrend_coloring))     
        self.wait(4)

        self.play(FadeOut(behrend_coloring), FadeOut(behrend))
        self.wait(2)

# -----------------------------------------------------------------------------
# Scene: A, B, C Arithmetic
# -----------------------------------------------------------------------------
class ABCArithmeticScene_9(Scene):
    """Explain A, B, C Arithmetic"""

    def construct(self):
        title = MathTex(r"3\text{AP-Free Coloring}", font_size=40)
        title.to_edge(UP, buff=0.4)
        self.add(title)

        # Number line
        number_line = NumberLine(
            x_range=[0, 10, 1],
            length=10,
            include_tip=False,
            include_numbers=False,
        ).next_to(title, DOWN, buff=1)

        self.play(Create(number_line))
        self.wait(0.4)

        # Example positions
        a_pos = 2
        b_pos = 5
        c_pos = 8

        a_dot = Dot(number_line.n2p(a_pos), radius=0.11, color=BLUE)
        b_dot = Dot(number_line.n2p(b_pos), radius=0.11, color=BLUE)
        c_dot = Dot(number_line.n2p(c_pos), radius=0.11, color=BLUE)

        a_lbl = MathTex("A", font_size=34, color=BLUE).next_to(a_dot, DOWN, buff=0.18)
        b_lbl = MathTex("B", font_size=34, color=BLUE).next_to(b_dot, DOWN, buff=0.18)
        c_lbl = MathTex("C", font_size=34, color=BLUE).next_to(c_dot, DOWN, buff=0.18)

        self.play(
            LaggedStart(
                FadeIn(a_dot), FadeIn(a_lbl),
                FadeIn(b_dot), FadeIn(b_lbl),
                FadeIn(c_dot), FadeIn(c_lbl),
                lag_ratio=0.12,
            )
        )
        self.wait(0.8)

        # Show equal spacing
        left_seg = Line(number_line.n2p(a_pos), number_line.n2p(b_pos), color=YELLOW, stroke_width=6)
        right_seg = Line(number_line.n2p(b_pos), number_line.n2p(c_pos), color=YELLOW, stroke_width=6)

        d_left = Brace(left_seg, UP, buff=0.08, color=YELLOW)
        d_right = Brace(right_seg, UP, buff=0.08, color=YELLOW)

        d_left_lbl = MathTex("d", font_size=30, color=YELLOW).next_to(d_left, UP, buff=0.08)
        d_right_lbl = MathTex("d", font_size=30, color=YELLOW).next_to(d_right, UP, buff=0.08)

        self.play(Create(left_seg), Create(right_seg))
        self.play(
            GrowFromCenter(d_left),
            GrowFromCenter(d_right),
            FadeIn(d_left_lbl),
            FadeIn(d_right_lbl),
        )
        self.wait(1)

        d_equal_0 = MathTex(
            r"\text{Still monochromatic } 3AP \text{-free if } d = 0",
            font_size=30,
            color=YELLOW
        ).next_to(number_line, DOWN, buff=1)

        self.play(FadeIn(d_equal_0))
        self.wait(3)

        checksum_eq = MathTex(
            r"\operatorname{CHECKSUM}(x,y,z)=1 \iff x+y+z=N",
            font_size=30
        ).next_to(d_equal_0, DOWN, buff=0.5)

        self.play(FadeIn(checksum_eq))
        self.wait(5)

        d_0 = MathTex(
            r"\operatorname{CHECKSUM}(x,y,z)=1 \iff ", r"x+y+z=N",
            font_size=30
        ).move_to(checksum_eq)

        d_1 = MathTex(
            r"x+y+z=N",
            font_size=30
        ).next_to(checksum_eq, DOWN, buff=0.5)

        self.play(TransformMatchingShapes(d_0[1], d_1))

        d_2 = MathTex(
            r"x+y+z-N=0",
            font_size=30
        ).move_to(d_1)

        self.play(TransformMatchingShapes(d_1, d_2))
        self.wait(2)

        d_3 = MathTex(
            r"d=x+y+z-N=0",
            font_size=30
        ).move_to(d_1)

        self.play(TransformMatchingShapes(d_2, d_3))
        self.wait(2)

        self.play(d_3.animate.next_to(number_line, DOWN, buff=1), FadeOut(d_equal_0), FadeOut(checksum_eq))
        self.wait(0.7)

        a_0 = MathTex(
            r"A",
            font_size=34,
            color=BLUE
        ).next_to(d_3, DOWN, buff=0.7)

        b_0 = MathTex(
            r"B",
            font_size=34,
            color=BLUE
        ).next_to(a_0, DOWN, buff=0.5)

        c_0 = MathTex(
            r"C",
            font_size=34,
            color=BLUE
        ).next_to(b_0, DOWN, buff=0.5)

        self.play(
            LaggedStart(
                FadeIn(a_0),
                FadeIn(b_0),
                FadeIn(c_0),
                lag_ratio=0.12,
            )
        )
        self.wait(2)

        a_1 = MathTex(
            r"A: -y-2z",
            font_size=34,
            color=BLUE
        ).move_to(a_0)

        self.play(TransformMatchingShapes(a_0, a_1))
        self.wait(7)

        self.play(Indicate(a_dot), Indicate(a_lbl))
        self.wait(1)

        b_1 = MathTex(
            r"B: (-y-2z)",
            font_size=34,
            color=BLUE
        ).move_to(b_0)

        self.play(TransformMatchingShapes(b_0, b_1))
        self.wait(1.5)

        self.play(Indicate(d_left), Indicate(d_left_lbl))
        self.wait(1)

        b_2 = MathTex(
            r"B: (-y-2z)+d",
            font_size=34,
            color=BLUE
        ).move_to(b_1)

        self.play(TransformMatchingShapes(b_1, b_2))
        self.wait(1.5)

        self.play(Indicate(d_3))
        self.wait(1)

        b_3 = MathTex(
            r"B: (-y-2z)+x+y+z-N",
            font_size=34,
            color=BLUE
        ).move_to(b_2)

        self.play(TransformMatchingShapes(b_2, b_3))
        self.wait(1.5)

        b_4 = MathTex(
            r"B: x-z-N",
            font_size=34,
            color=BLUE
        ).move_to(b_3)

        self.play(TransformMatchingShapes(b_3, b_4))
        self.wait(5)

        self.play(Indicate(a_dot), Indicate(a_lbl))
        self.wait(1)

        c_1 = MathTex(
            r"C: (-y-2z)",
            font_size=34,
            color=BLUE
        ).move_to(c_0)

        self.play(TransformMatchingShapes(c_0, c_1))
        self.wait(1.5)

        self.play(Indicate(d_left), Indicate(d_left_lbl), Indicate(d_right), Indicate(d_right_lbl))
        self.wait(1)

        c_2 = MathTex(
            r"C: (-y-2z)+2d",
            font_size=34,
            color=BLUE
        ).move_to(c_1)

        self.play(TransformMatchingShapes(c_1, c_2))
        self.wait(1.5)

        self.play(Indicate(d_3))
        self.wait(1)

        c_3 = MathTex(
            r"C: (-y-2z)+2x+2y+2z-2N",
            font_size=34,
            color=BLUE
        ).move_to(c_2)

        self.play(TransformMatchingShapes(c_2, c_3))
        self.wait(1.5)

        c_4 = MathTex(
            r"C: 2x+y-2N",
            font_size=34,
            color=BLUE
        ).move_to(c_3)

        self.play(TransformMatchingShapes(c_3, c_4))
        self.wait(4)

        a_5 = MathTex(
            r"A: 3N-y-2z",
            font_size=34,
            color=BLUE
        ).move_to(a_1)

        b_5 = MathTex(
            r"B: 2N+x-z",
            font_size=34,
            color=BLUE
        ).move_to(b_4)

        c_5 = MathTex(
            r"C: N+2x+y",
            font_size=34,
            color=BLUE
        ).move_to(c_4)

        self.play(TransformMatchingShapes(a_1, a_5), TransformMatchingShapes(b_4, b_5), TransformMatchingShapes(c_4, c_5))
        self.wait(3)

        a_6 = MathTex(
            r"\chi(A)= \chi(3N-y-2z)",
            font_size=34,
            color=BLUE
        ).move_to(a_5)

        b_6 = MathTex(
            r"\chi(B)= \chi(2N+x-z)",
            font_size=34,
            color=BLUE
        ).move_to(b_5)

        c_6 = MathTex(
            r"\chi(C)= \chi(N+2x+y)",
            font_size=34,
            color=BLUE
        ).move_to(c_5)

        self.play(TransformMatchingShapes(a_5, a_6), TransformMatchingShapes(b_5, b_6), TransformMatchingShapes(c_5, c_6))
        self.wait(2)

        conclusion = MathTex(
            r"\text{Notice that each coloring relies on only two variables}",
            font_size=40,
            color=WHITE
        ).next_to(c_6, DOWN, buff=0.5)

        self.play(FadeIn(conclusion))
        self.wait(3)
        self.play(Indicate(a_6))
        self.wait(1.5)
        self.play(Indicate(b_6))
        self.wait(1.5)
        self.play(Indicate(c_6))
        self.wait(2)

# -----------------------------------------------------------------------------
# Scene: CSUM and 3AP
# -----------------------------------------------------------------------------
class CSUM3APScene_10(Scene):
    """Explain relation between CSUM and 3AP"""

    def construct(self):
        title = MathTex(r"\text{How is } CSUM \text{ related to } 3AP \text{ ?}", font_size=40)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title))
        self.wait(2.5)

        behrend_coloring = MathTex(
            r"\chi: \{1, ..., N\} \rightarrow [2^{c*\sqrt{\log N}}]",
            font_size=30,
            color=YELLOW,
        ).next_to(title, DOWN, 0.5)

        self.play(FadeIn(behrend_coloring))
        self.wait(1)

        color_cc = MathTex(
            r"\text{Since we only send the color} \rightarrow O(\sqrt{\log N})",
            font_size=30,
            color=YELLOW,
        ).next_to(behrend_coloring, DOWN, 0.5) 

        self.play(FadeIn(color_cc))
        self.wait(6)   

        csum_ex_0 = MathTex(
            r"\text{If colors are the same, } CSUM = 1",
            font_size=30,
            color=WHITE,
        ).next_to(color_cc, DOWN, 0.5) 

        self.play(FadeIn(csum_ex_0))
        self.wait(2) 

        csum_ex_1 = MathTex(
            r"\rightarrow A, B, C \text{ same color and ``form a 3AP'' but coloring says this is impossible}",
            font_size=30,
            color=WHITE,
        ).next_to(csum_ex_0, DOWN, 0.5) 

        self.play(FadeIn(csum_ex_1))
        self.wait(6)

        csum_ex_2 = MathTex(
            r"\rightarrow A, B, C \text{ form a trivial 3AP where } d=0 \text{, meaning } d=x+y+z-N=0",
            font_size=30,
            color=WHITE,
        ).next_to(csum_ex_1, DOWN, 0.5) 

        self.play(FadeIn(csum_ex_2))
        self.wait(12)  
        self.play(FadeOut(csum_ex_0), FadeOut(csum_ex_1), FadeOut(csum_ex_2))

        csum_ex_3 = MathTex(
            r"\text{If colors are different, } CSUM = 0",
            font_size=30,
            color=WHITE,
        ).next_to(color_cc, DOWN, 0.5) 

        self.play(FadeIn(csum_ex_3))
        self.wait(2)

        csum_ex_4 = MathTex(
            r"\rightarrow \text{ Some non-trivial 3AP exists where } d \ne 0 \text{ so colors cannot be the same}",
            font_size=30,
            color=WHITE,
        ).next_to(csum_ex_3, DOWN, 0.5) 

        self.play(FadeIn(csum_ex_4))
        self.wait(6)