#!/usr/bin/env python

from helpers import *

from mobject.tex_mobject import TexMobject
from mobject import Mobject
from mobject.image_mobject import ImageMobject
from mobject.vectorized_mobject import *
from mobject.svg_mobject import *
from mobject.tex_mobject import *

from scene import Scene
from camera import Camera

from animation.animation import Animation
from animation.transform import *
from animation.simple_animations import *
from animation.playground import *

from topics.geometry import *
from topics.objects import *
from topics.characters import *
from topics.functions import *
from topics.number_line import *
from topics.combinatorics import *
from topics.three_dimensions import *

from topics.three_dimensions import *

class CarrotDrive(Scene):
    def construct(self):
        tankbot = TankBot()
        self.play(ShowCreation(tankbot))