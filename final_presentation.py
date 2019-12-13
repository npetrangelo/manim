#!/usr/bin/env python

from manim_util import *
from manimlib.imports import *

class ComplexNumbers(Scene):
    def construct(self):
        expressions = [
            TextMobject(*[c for c in "(a+bi)(c+di)"]),
            TextMobject(*[c for c in "a(c+di)+bi(c+di)"]),
            TextMobject(*[c for c in "ac+adi+bci+bidi"]),
            TextMobject(*[c for c in "ac+adi+bci-bd"]),
            TextMobject(*[c for c in "ac+(ad+bc)i-bd"]),
            TextMobject(*[c for c in "ac-bd+(ad+bc)i"]),
        ]

        distribution_top = TextMobject(*[c for c in "a(c+di)"])
        distribution_bottom = TextMobject(*[c for c in "bi(c+di)"])
        plus = TextMobject("+")
        VGroup(distribution_top, plus, distribution_bottom).arrange(DOWN)

        self.play(
            Write(expressions[0])
        )

        self.wait()

        self.play(
            FadeOut(expressions[0][0]),
            FadeOut(expressions[0][5]),
            *ReplacementMultiIndex(
                expressions[0],   (1, 6,7,8,9,10,11),
                distribution_top, (0, 1,2,3,4,5, 6),
            ),
            ReplacementTransform(expressions[0][2], plus),
            *ReplacementMultiIndex(
                expressions[0],      (3,4),
                distribution_bottom, (0,1),
            ),
            *ReplacementMultiIndex(
                expressions[0],      (6,7,8,9,10,11),
                distribution_bottom, (2,3,4,5,6, 7),copy_first=True
            ),
        )

        self.wait()

        self.play(
            *ReplacementMultiIndex(
                distribution_top, (0,1,2,3,4,5,6),
                expressions[1],   (0,1,2,3,4,5,6)
            ),
            ReplacementTransform(plus, expressions[1][7]),
            *ReplacementMultiIndex(
                distribution_bottom, (0,1, 2, 3, 4, 5, 6, 7),
                expressions[1],      (8,9,10,11,12,13,14,15)
            ),
        )

        self.wait()

        distribution1_top = TextMobject("a","c")
        distribution1_bottom = TextMobject("a","d","i")
        plus1 = TextMobject("+")
        VGroup(distribution1_top, plus1, distribution1_bottom).arrange(DOWN).to_edge(LEFT*0.5,12)

        distribution2_top = TextMobject("b","i","c")
        distribution2_bottom = TextMobject("b","i","d","i")
        plus2 = TextMobject("+")
        VGroup(distribution2_top, plus2, distribution2_bottom).arrange(DOWN).to_edge(RIGHT*0.5,12)

        self.play(
            FadeOut(expressions[1][1]),
            FadeOut(expressions[1][6]),
            FadeOut(expressions[1][10]),
            FadeOut(expressions[1][15]),

            *ReplacementMultiIndex(
                expressions[1], (0,2),
                distribution1_top,   (0,1)
            ),
            ReplacementTransform(expressions[1][0].copy(),distribution1_bottom[0]),
            ReplacementTransform(expressions[1][3],plus1),
            *ReplacementMultiIndex(
                expressions[1],       (4,5),
                distribution1_bottom, (1,2)
            ),

            *ReplacementMultiIndex(
                expressions[1], (8,9,11),
                distribution2_top,   (0,1,2)
            ),
            ReplacementTransform(expressions[1][12],plus2),
            *ReplacementMultiIndex(
                expressions[1],       (8,9),
                distribution2_bottom, (0,1),copy_first=True,
            ),
            *ReplacementMultiIndex(
                expressions[1],       (13,14),
                distribution2_bottom, (2,3)
            ),
        )

        self.wait()

        self.play(
            *ReplacementMultiIndex(
                distribution1_top, (0,1),
                expressions[2],    (0,1)
            ),
            ReplacementTransform(plus1,expressions[2][2]),
            *ReplacementMultiIndex(
                distribution1_bottom, (0,1,2),
                expressions[2],    (3,4,5)
            ),

            ReplacementTransform(expressions[1][7],expressions[2][6]),

            *ReplacementMultiIndex(
                distribution2_top, (0,1,2),
                expressions[2],    (7,9,8)
            ),
            ReplacementTransform(plus2,expressions[2][10]),
            *ReplacementMultiIndex(
                distribution2_bottom, (0,1,2,3),
                expressions[2],    (11,12,13,14)
            ),
        )

        self.wait()

        self.play(
            FadeOut(expressions[2][12]),
            FadeOut(expressions[2][14]),
            *ReplacementMultiIndex(
                expressions[2], (0,1,2,3,4,5,6,7,8,9,10,11,13),
                expressions[3], (0,1,2,3,4,5,6,7,8,9,10,11,12),
            )
        )

        self.wait()

        self.play(
            FadeOut(expressions[3][5]),
            FadeIn(expressions[4][3]),
            FadeIn(expressions[4][9]),
            *ReplacementMultiIndex(
                expressions[3], (0,1,2,3,4,5, 6,7,8,9, 10,11,12),
                expressions[4], (0,1,2,4,5,10,6,7,8,10,11,12,13)
            )
        )

        self.wait()

        self.play(
            *ReplacementMultiIndex(
                expressions[4], (0,1,2,3,4,5,6,7,8,9,10,11,12,13),
                expressions[5], (0,1,5,6,7,8,9,10,11,12,13,2,3,4),
            )
        )

        self.wait()
