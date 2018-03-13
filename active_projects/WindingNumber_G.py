from helpers import *

from mobject.tex_mobject import TexMobject
from mobject import Mobject
from mobject.image_mobject import ImageMobject
from mobject.vectorized_mobject import *

from animation.animation import Animation
from animation.transform import *
from animation.simple_animations import *
from animation.compositions import *
from animation.playground import *
from animation.continual_animation import *
from topics.geometry import *
from topics.characters import *
from topics.functions import *
from topics.fractals import *
from topics.number_line import *
from topics.combinatorics import *
from topics.numerals import *
from topics.three_dimensions import *
from topics.objects import *
from topics.probability import *
from topics.complex_numbers import *
from scene import Scene
from scene.reconfigurable_scene import ReconfigurableScene
from scene.zoomed_scene import *
from scene.moving_camera_scene import *
from camera import *
from mobject.svg_mobject import *
from mobject.tex_mobject import *
from topics.graph_scene import *

from active_projects.WindingNumber import *

class AltTeacherStudentsScene(TeacherStudentsScene):
    def setup(self):
        TeacherStudentsScene.setup(self)
        self.teacher.set_color(YELLOW_E)

###############


class IntroSceneWrapper(PiCreatureScene):
    CONFIG = {
        "default_pi_creature_kwargs" : {
            "color" : YELLOW_E,
            "flip_at_start" : False,
            "height" : 2,
        },
        "default_pi_creature_start_corner" : DOWN+LEFT,
    }
    def construct(self):
        self.introduce_two_words()
        self.describe_main_topic()
        self.describe_meta_topic()

    def introduce_two_words(self):
        morty = self.pi_creature
        rect = ScreenRectangle(height = 5)
        rect.to_corner(UP+RIGHT)
        self.add(rect)

        h_line = Line(LEFT, RIGHT).scale(2)
        h_line.to_corner(UP+LEFT)
        h_line.shift(0.5*DOWN)

        main_topic, meta_topic = topics = VGroup(
            TextMobject("Main topic"),
            TextMobject("Meta topic"),
        )
        topics.next_to(morty, UP)
        topics.shift_onto_screen()

        self.play(
            morty.change, "raise_left_hand",
            FadeInFromDown(main_topic)
        )
        self.wait()
        self.play(
            morty.change, "raise_right_hand",
            main_topic.next_to, meta_topic.get_top(), UP, MED_SMALL_BUFF,
            FadeInFromDown(meta_topic)
        )
        self.wait()
        self.play(
            morty.change, "happy",
            main_topic.next_to, h_line, UP,
            meta_topic.set_fill, {"opacity" : 0.2},
        )
        self.play(ShowCreation(h_line))
        self.wait()

        self.set_variables_as_attrs(h_line, main_topic, meta_topic)

    def describe_main_topic(self):
        h_line = self.h_line
        morty = self.pi_creature
        main_topic = self.main_topic
        meta_topic = self.meta_topic

        solver = TextMobject("2d equation solver")
        solver.match_width(h_line)
        solver.next_to(h_line, DOWN)
        rainbow_solver1 = solver.copy()
        rainbow_solver2 = solver.copy()
        colors = ["RED", "ORANGE", "YELLOW", "GREEN", BLUE, "PURPLE", PINK]
        rainbow_solver1.gradient_highlight(*colors)
        rainbow_solver2.gradient_highlight(*reversed(colors))


        xy_equation = TexMobject("""
            \\left[\\begin{array}{c}
                ye^x \\\\
                \\sin(|xy|)
            \\end{array}\\right] = 
            \\left[\\begin{array}{c}
                y^2 \\\\
                3y
            \\end{array}\\right]
        """)
        # xy_equation.highlight_by_tex_to_color_map({
        #     "x" : BLUE,
        #     "y" : YELLOW
        # })
        xy_equation.scale(0.8)
        xy_equation.next_to(solver, DOWN, MED_LARGE_BUFF)

        z_equation = TexMobject("z", "^5", "+", "z", "+", "1", "=", "0")
        z_equation.highlight_by_tex("z", GREEN)
        z_equation.move_to(xy_equation, UP)

        zeta = TexMobject("\\zeta(s) = 0")
        zeta[2].highlight(GREEN)
        zeta.next_to(z_equation, DOWN, MED_LARGE_BUFF)

        self.play(Write(solver))
        self.play(
            LaggedStart(FadeIn, xy_equation, run_time = 1),
            morty.change, "pondering"
        )
        self.wait(2)
        self.play(
            FadeOut(xy_equation),
            FadeIn(z_equation)
        )
        self.wait()
        self.play(Write(zeta))
        self.wait()
        solver.save_state()
        for rainbow_solver in rainbow_solver1, rainbow_solver2:
            self.play(Transform(
                solver, rainbow_solver,
                run_time = 2,
                submobject_mode = "lagged_start"
            ))
        self.play(solver.restore)
        self.wait()

        self.play(LaggedStart(
            FadeOut, VGroup(solver, z_equation, zeta)
        ))
        self.play(
            main_topic.move_to, meta_topic,
            main_topic.set_fill, {"opacity" : 0.2},
            meta_topic.move_to, main_topic,
            meta_topic.set_fill, {"opacity" : 1},
            morty.change, "hesitant",
            path_arc = TAU/8,
        )

    def describe_meta_topic(self):
        h_line = self.h_line
        morty = self.pi_creature

        words = TextMobject("Seek constructs which \\\\ compose nicely")
        words.scale(0.7)
        words.next_to(h_line, DOWN)

        self.play(Write(words))
        self.play(morty.change, "happy")
        self.wait(3)

class Introduce1DFunctionCase(Scene):
    CONFIG = {
        "search_range_rect_height" : 0.15,
        "arrow_opacity" : 1,
        "show_dotted_line_to_f" : True,
        "arrow_config": {
            "max_stem_width_to_tip_width_ratio" : 0.5,
            "max_tip_length_to_length_ratio" : 0.5,
        },
        "show_midpoint_value" : True,
    }
    def construct(self):
        self.show_axes_one_at_a_time()
        self.show_two_graphs()
        self.transition_to_sqrt_2_case()
        self.show_example_binary_search()

    def show_axes_one_at_a_time(self):
        axes = Axes(
            x_min = -1, x_max = 3.2,
            x_axis_config = {
                "unit_size" : 3,
                "tick_frequency" : 0.25,
                "numbers_with_elongated_ticks" : range(-1, 4)
            },
            y_min = -2, y_max = 4.5,
        )
        axes.to_corner(DOWN+LEFT)
        axes.x_axis.add_numbers(*range(-1, 4))
        axes.y_axis.label_direction = LEFT
        axes.y_axis.add_numbers(-1, *range(1, 5))

        inputs = TextMobject("Inputs")
        inputs.next_to(axes.x_axis, UP, aligned_edge = RIGHT)

        outputs = TextMobject("Outputs")
        outputs.next_to(axes.y_axis, UP, SMALL_BUFF)

        self.play(
            ShowCreation(axes.x_axis),
            Write(inputs)
        )
        self.wait()
        self.play(
            ShowCreation(axes.y_axis),
            FadeOut(axes.x_axis.numbers[1], rate_func = squish_rate_func(smooth, 0, 0.2)),
            Write(outputs)
        )
        self.wait()

        self.axes = axes
        self.inputs_label = inputs
        self.outputs_label = outputs

    def show_two_graphs(self):
        axes = self.axes
        f_graph = axes.get_graph(
            lambda x : 2*x*(x - 0.75)*(x - 1.5) + 1,
            color = BLUE
        )
        g_graph = axes.get_graph(
            lambda x : 1.8*np.cos(TAU*x/2),
            color = YELLOW
        )

        label_x_corod = 2
        f_label = TexMobject("f(x)")
        f_label.match_color(f_graph)
        f_label.next_to(axes.input_to_graph_point(label_x_corod, f_graph), LEFT)

        g_label = TexMobject("g(x)")
        g_label.match_color(g_graph)
        g_label.next_to(
            axes.input_to_graph_point(label_x_corod, g_graph), UP, SMALL_BUFF
        )

        solution = 0.24
        cross_point = axes.input_to_graph_point(solution, f_graph)
        l_v_line, r_v_line, v_line = [
            DashedLine(
                axes.coords_to_point(x, 0),
                axes.coords_to_point(x, f_graph.underlying_function(solution)),
            )
            for x in axes.x_min, axes.x_max, solution
        ]

        equation = TexMobject("f(x)", "=", "g(x)")
        equation[0].match_color(f_label)
        equation[2].match_color(g_label)
        equation.next_to(cross_point, UP, buff = 1.5, aligned_edge = LEFT)
        equation_arrow = Arrow(
            equation.get_bottom(), cross_point,
            buff = SMALL_BUFF,
            color = WHITE
        )
        equation.target = TexMobject("x^2", "=", "2")
        equation.target.match_style(equation)
        equation.target.to_edge(UP)

        for graph, label in (f_graph, f_label), (g_graph, g_label):
            self.play(
                ShowCreation(graph),
                Write(label, rate_func = squish_rate_func(smooth, 0.5, 1)),
                run_time = 2
            )
        self.wait()
        self.play(
            ReplacementTransform(r_v_line.copy().fade(1), v_line),
            ReplacementTransform(l_v_line.copy().fade(1), v_line),
            run_time = 2
        )
        self.play(
            ReplacementTransform(f_label.copy(), equation[0]),
            ReplacementTransform(g_label.copy(), equation[2]),
            Write(equation[1]),
            GrowArrow(equation_arrow),
        )
        for x in range(4):
            self.play(
                FadeOut(v_line.copy()),
                ShowCreation(v_line, rate_func = squish_rate_func(smooth, 0.5, 1)),
                run_time = 1.5
            )
        self.wait()
        self.play(
            MoveToTarget(equation, replace_mobject_with_target_in_scene = True),
            *map(FadeOut, [equation_arrow, v_line])
        )

        self.set_variables_as_attrs(
            f_graph, f_label, g_graph, g_label,
            equation = equation.target
        )

    def transition_to_sqrt_2_case(self):
        f_graph = self.f_graph
        f_label = VGroup(self.f_label)
        g_graph = self.g_graph
        g_label = VGroup(self.g_label)
        axes = self.axes
        for label in f_label, g_label:
            for x in range(2):
                label.add(VectorizedPoint(label.get_center()))
        for number in axes.y_axis.numbers:
            number.add_background_rectangle()

        squared_graph = axes.get_graph(lambda x : x**2)
        squared_graph.match_style(f_graph)
        two_graph = axes.get_graph(lambda x : 2)
        two_graph.match_style(g_graph)

        squared_label = TexMobject("f(x)", "=", "x^2")
        squared_label.next_to(
            axes.input_to_graph_point(2, squared_graph), RIGHT
        )
        squared_label.match_color(squared_graph)
        two_label = TexMobject("g(x)", "=", "2")
        two_label.next_to(
            axes.input_to_graph_point(3, two_graph), UP,
        )
        two_label.match_color(two_graph)

        find_sqrt_2 = self.find_sqrt_2 = TextMobject("(Find $\\sqrt{2}$)")
        find_sqrt_2.next_to(self.equation, DOWN)

        self.play(
            ReplacementTransform(f_graph, squared_graph),
            ReplacementTransform(f_label, squared_label),
        )
        self.play(
            ReplacementTransform(g_graph, two_graph),
            ReplacementTransform(g_label, two_label),
            Animation(axes.y_axis.numbers)
        )
        self.wait()
        self.play(Write(find_sqrt_2))
        self.wait()

        self.set_variables_as_attrs(
            squared_graph, two_graph,
            squared_label, two_label,
        )

    def show_example_binary_search(self):
        self.binary_search(
            self.squared_graph, self.two_graph,
            x0 = 1, x1 = 2,
            n_iterations = 8
        )

    ##

    def binary_search(
        self, 
        f_graph, g_graph, 
        x0, x1, 
        n_iterations,
        n_iterations_with_sign_mention = 0,
        zoom = False,
        ):

        axes = self.axes
        rect = Rectangle()
        rect.set_stroke(width = 0)
        rect.set_fill(YELLOW, 0.5)
        rect.replace(Line(
            axes.coords_to_point(x0, 0),
            axes.coords_to_point(x1, 0),
        ), dim_to_match = 0)
        rect.stretch_to_fit_height(self.search_range_rect_height)

        #Show first left and right
        mention_signs = n_iterations_with_sign_mention > 0
        kwargs = {"mention_signs" : mention_signs}
        leftovers0 = self.compare_graphs_at_x(f_graph, g_graph, x0, **kwargs)
        self.wait()
        leftovers1 = self.compare_graphs_at_x(f_graph, g_graph, x1, **kwargs)
        self.wait()
        self.play(GrowFromCenter(rect))
        self.wait()

        all_leftovers = VGroup(leftovers0, leftovers1)
        end_points = [x0, x1]
        if mention_signs:
            sign_word0 = leftovers0.sign_word
            sign_word1 = leftovers1.sign_word

        midpoint_line = Line(MED_SMALL_BUFF*UP, ORIGIN, color = YELLOW)
        midpoint_line_update = UpdateFromFunc(
            midpoint_line, lambda l : l.move_to(rect)
        )
        decimal = DecimalNumber(
            0,
            num_decimal_points = 3,
            show_ellipsis = True,
        )
        decimal.scale(0.7)
        decimal_update = ChangingDecimal(
            decimal, lambda a : axes.x_axis.point_to_number(rect.get_center()),
            position_update_func = lambda m : m.next_to(
                midpoint_line, DOWN, SMALL_BUFF,
                submobject_to_align = decimal[:-1],
            ),
        )
        if not self.show_midpoint_value:
            decimal.set_fill(opacity = 0)
            midpoint_line.set_stroke(width = 0)

        #Restrict to by a half each time
        kwargs = {"mention_signs" : False} 
        for x in range(n_iterations - 1):
            x_mid = np.mean(end_points)
            leftovers_mid = self.compare_graphs_at_x(f_graph, g_graph, x_mid, **kwargs)
            if leftovers_mid.too_high == all_leftovers[0].too_high:
                index_to_fade = 0
            else:
                index_to_fade = 1
            edge = [RIGHT, LEFT][index_to_fade]
            to_fade = all_leftovers[index_to_fade]
            all_leftovers.submobjects[index_to_fade] = leftovers_mid
            end_points[index_to_fade] = x_mid

            added_anims = []
            if mention_signs:
                word = [leftovers0, leftovers1][index_to_fade].sign_word
                if x < n_iterations_with_sign_mention:
                    added_anims = [word.next_to, leftovers_mid[0].get_end(), -edge]
                elif word in self.camera.extract_mobject_family_members(self.mobjects):
                    added_anims = [FadeOut(word)]

            rect.generate_target()
            rect.target.stretch(0.5, 0, about_edge = edge)
            rect.target.stretch_to_fit_height(self.search_range_rect_height)
            self.play(
                MoveToTarget(rect),
                midpoint_line_update,
                decimal_update,
                Animation(all_leftovers),
                FadeOut(to_fade),
                *added_anims
            )
            if zoom:
                everything = VGroup(*self.mobjects)
                factor = 2.0/rect.get_width()
                if factor > 1:
                    self.play(
                        everything.scale, factor, 
                        {"about_point" : rect.get_center()}
                    )
            else:
                self.wait()

    def compare_graphs_at_x(
        self, f_graph, g_graph, x, 
        mention_signs = False,
        show_decimal = False,
        ):
        axes = self.axes
        f_point = axes.input_to_graph_point(x, f_graph)
        g_point = axes.input_to_graph_point(x, g_graph)
        arrow = Arrow(
            g_point, f_point, buff = 0,
            **self.arrow_config
        )
        too_high = f_point[1] > g_point[1]
        if too_high:
            arrow.set_fill(GREEN, opacity = self.arrow_opacity)
        else:
            arrow.set_fill(RED, opacity = self.arrow_opacity)

        leftovers = VGroup(arrow)
        leftovers.too_high = too_high

        if self.show_dotted_line_to_f:
            v_line = DashedLine(axes.coords_to_point(x, 0), f_point)
            self.play(ShowCreation(v_line))
            leftovers.add(v_line)

        added_anims = []
        if mention_signs:
            if too_high:
                sign_word = TextMobject("Positive")
                sign_word.highlight(GREEN)
                sign_word.scale(0.7)
                sign_word.next_to(arrow.get_end(), RIGHT)
            else:
                sign_word = TextMobject("Negative")
                sign_word.highlight(RED)
                sign_word.scale(0.7)
                sign_word.next_to(arrow.get_end(), LEFT)
            sign_word.add_background_rectangle()
            added_anims += [FadeIn(sign_word)]
            leftovers.sign_word = sign_word

        self.play(GrowArrow(arrow), *added_anims)

        return leftovers

class PiCreaturesAreIntrigued(AltTeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "You can extend \\\\ this to 2d",
            bubble_kwargs = {"width" : 4, "height" : 3}
        )
        self.change_student_modes("pondering", "confused", "erm")
        self.look_at(self.screen)
        self.wait(3)

class TransitionFromEquationSolverToZeroFinder(Introduce1DFunctionCase):
    CONFIG = {
        "show_dotted_line_to_f" : False,
        "arrow_config" : {},
        "show_midpoint_value" : False,
    }
    def construct(self):
        #Just run through these without animating.
        self.force_skipping()
        self.show_axes_one_at_a_time()
        self.show_two_graphs()
        self.transition_to_sqrt_2_case()
        self.revert_to_original_skipping_status()
        ##

        self.transition_to_difference_graph()
        self.show_binary_search_with_signs()

    def transition_to_difference_graph(self):
        axes = self.axes
        equation = x_squared, equals, two = self.equation
        for s in "-", "0":
            tex_mob = TexMobject(s)
            tex_mob.scale(0.01)
            tex_mob.fade(1)
            tex_mob.move_to(equation.get_right())
            equation.add(tex_mob)
        find_sqrt_2 = self.find_sqrt_2
        rect = SurroundingRectangle(VGroup(equation, find_sqrt_2))
        rect.highlight(WHITE)

        f_graph = self.squared_graph
        g_graph = self.two_graph
        new_graph = axes.get_graph(
            lambda x : f_graph.underlying_function(x) - g_graph.underlying_function(x),
            color = GREEN
        )
        zero_graph = axes.get_graph(lambda x : 0)
        zero_graph.set_stroke(BLACK, 0)

        f_label = self.squared_label
        g_label = self.two_label
        new_label = TexMobject("f(x)", "-", "g(x)")
        new_label[0].match_color(f_label)
        new_label[2].match_color(g_label)
        new_label.next_to(
            axes.input_to_graph_point(2, new_graph),
            LEFT
        )

        fg_labels = VGroup(f_label, g_label)
        fg_labels.generate_target()
        fg_labels.target.arrange_submobjects(DOWN, aligned_edge = LEFT)
        fg_labels.target.to_corner(UP+RIGHT)

        new_equation = TexMobject("x^2", "-", "2", "=", "0")
        new_equation[0].match_style(equation[0])
        new_equation[2].match_style(equation[2])
        new_equation.move_to(equation, RIGHT)
        for tex in equation, new_equation:
            tex.sort_submobjects_alphabetically()

        self.play(ShowCreation(rect))
        self.play(FadeOut(rect))
        self.play(
            ReplacementTransform(equation, new_equation, path_arc = TAU/4),
            find_sqrt_2.next_to, new_equation, DOWN,
        )
        self.play(MoveToTarget(fg_labels))
        self.play(
            ReplacementTransform(f_graph, new_graph),
            ReplacementTransform(g_graph, zero_graph),
        )
        self.play(
            ReplacementTransform(f_label[0].copy(), new_label[0]),
            ReplacementTransform(g_label[0].copy(), new_label[2]),
            Write(new_label[1]),
        )
        self.wait()

        self.set_variables_as_attrs(new_graph, zero_graph)

    def show_binary_search_with_signs(self):
        self.play(FadeOut(self.axes.x_axis.numbers[2]))
        self.binary_search(
            self.new_graph, self.zero_graph,
            1, 2,
            n_iterations = 9,
            n_iterations_with_sign_mention = 2,
            zoom = True,
        )

class RewriteEquationWithTeacher(AltTeacherStudentsScene):
    def construct(self):
        root_two_equations = VGroup(
            TexMobject("x^2", "", "=", "2", ""),
            TexMobject("x^2", "-", "2", "=", "0"),
        )
        for equation in root_two_equations:
            equation.sort_submobjects_alphabetically()
            for part in equation.get_parts_by_tex("text"):
                part[2:-1].highlight(YELLOW)
                part[2:-1].scale(0.9)
            equation.move_to(self.hold_up_spot, DOWN)

        brace = Brace(root_two_equations[1], UP)
        f_equals_0 = brace.get_tex("f(x) = 0")

        self.teacher_holds_up(root_two_equations[0])
        self.wait()
        self.play(Transform(
            *root_two_equations, 
            run_time = 1.5,
            path_arc = TAU/2
        ))
        self.play(self.get_student_changes(*["pondering"]*3))
        self.play(
            GrowFromCenter(brace),
            self.teacher.change, "happy"
        )
        self.play(Write(f_equals_0))
        self.change_student_modes(*["happy"]*3)
        self.wait()

        #
        to_remove = VGroup(root_two_equations[0], brace, f_equals_0)
        two_d_equation = TexMobject("""
            \\left[\\begin{array}{c}
                ye^x \\\\
                \\sin(xy)
            \\end{array}\\right] = 
            \\left[\\begin{array}{c}
                y^2 + x^3 \\\\
                3y - x
            \\end{array}\\right]
        """)
        complex_equation = TexMobject("z", "^5 + ", "z", " + 1 = 0")
        z_def = TextMobject(
            "(", "$z$", " is complex, ", "$a + bi$", ")",
            arg_separator = ""
        )
        complex_group = VGroup(complex_equation, z_def)
        complex_group.arrange_submobjects(DOWN)
        for tex in complex_group:
            tex.highlight_by_tex("z", GREEN)
        complex_group.move_to(self.hold_up_spot, DOWN)

        self.play(
            ApplyMethod(
                to_remove.next_to, SPACE_WIDTH*RIGHT, RIGHT,
                remover = True,
                rate_func = running_start,
                path_arc = -TAU/4,
            ),
            self.teacher.change, "hesitant",
            self.get_student_changes(*["erm"]*3)
        )
        self.teacher_holds_up(two_d_equation)
        self.change_all_student_modes("horrified")
        self.wait()
        self.play(
            FadeOut(two_d_equation),
            FadeInFromDown(complex_group),
        )
        self.change_all_student_modes("confused")
        self.wait(3)

class InputOutputScene(Scene):
    CONFIG = {
        "plane_width" : 6,
        "plane_height" : 6,
        "x_shift" : SPACE_WIDTH/2,
        "y_shift" : MED_LARGE_BUFF,
        "output_scalar" : 10,
        "non_renormalized_func" : plane_func_by_wind_spec(
            (-2, -1, 2), 
            (1, 1, 1), 
            (2, -2, -1),
        ),
    }

    ###

    def func(self, coord_pair):
        out_coords = np.array(self.non_renormalized_func(coord_pair))
        out_norm = np.linalg.norm(out_coords)
        if out_norm > 1:
            angle = angle_of_vector(out_coords)
            factor = 0.5-0.1*np.cos(4*angle)
            target_norm = factor*np.log(out_norm)
            out_coords *= target_norm / out_norm
        else:
            out_coords = (0, 0)
        return tuple(out_coords)

    def point_function(self, point):
        in_coords = self.input_plane.point_to_coords(point)
        out_coords = self.func(in_coords)
        return self.output_plane.coords_to_point(*out_coords)

    def get_colorings(self):
        in_cmos = ColorMappedObjectsScene(
            func = lambda p : self.non_renormalized_func(
                (p[0]+self.x_shift, p[1]+self.y_shift)
            )
        )
        scalar = self.output_scalar
        out_cmos = ColorMappedObjectsScene(
            func = lambda p : (
                scalar*(p[0]-self.x_shift), scalar*(p[1]+self.y_shift)
            )
        )

        input_coloring = Rectangle(
            height = self.plane_height,
            width = self.plane_width,
            stroke_width = 0,
            fill_color = WHITE,
            fill_opacity = 1,
        )
        output_coloring = input_coloring.copy()
        colorings = VGroup(input_coloring, output_coloring)
        vects = [LEFT, RIGHT]
        cmos_pair = [in_cmos, out_cmos]
        for coloring, vect, cmos in zip(colorings, vects, cmos_pair):
            coloring.move_to(self.x_shift*vect + self.y_shift*DOWN)
            coloring.color_using_background_image(cmos.background_image_file)
        return colorings

    def get_planes(self):
        input_plane = self.input_plane = NumberPlane(
            x_radius = self.plane_width/2.0,
            y_radius = self.plane_height/2.0,
        )
        output_plane = self.output_plane = input_plane.copy()
        planes = VGroup(input_plane, output_plane)
        vects = [LEFT, RIGHT]
        label_texts = ["Input", "Output"]
        label_colors = [GREEN, RED]
        for plane, vect, text, color in zip(planes, vects, label_texts, label_colors):
            plane.stretch_to_fit_width(self.plane_width)
            plane.add_coordinates(x_vals = range(-2, 3), y_vals = range(-2, 3))
            plane.white_parts = VGroup(plane.axes, plane.coordinate_labels)
            plane.lines_to_fade = VGroup(plane.main_lines, plane.secondary_lines)
            plane.move_to(vect*SPACE_WIDTH/2 + self.y_shift*DOWN)
            label = TextMobject(text)
            label.scale(1.5)
            label.add_background_rectangle()
            label.move_to(plane)
            label.to_edge(UP, buff = MED_SMALL_BUFF)
            plane.add(label)
            plane.label = label
            for submob in plane.submobject_family():
                if isinstance(submob, TexMobject) and hasattr(submob, "background_rectangle"):
                    submob.remove(submob.background_rectangle)

        return planes

    def get_v_line(self):
        v_line = Line(UP, DOWN).scale(SPACE_HEIGHT)
        v_line.set_stroke(WHITE, 5)
        return v_line

    def get_dots(self, input_plane, output_plane):
        step = self.dot_density
        x_min = -3.0
        x_max = 3.0
        y_min = -3.0
        y_max = 3.0
        dots = VGroup()
        for x in np.arange(x_min, x_max + step, step):
            for y in np.arange(y_max, y_min - step, -step):
                out_coords = self.func((x, y))
                dot = Dot(radius = self.dot_radius)
                dot.set_stroke(BLACK, 1)
                dot.move_to(input_plane.coords_to_point(x, y))
                dot.original_position = dot.get_center()
                dot.generate_target()
                dot.target.move_to(output_plane.coords_to_point(*out_coords))
                dot.target_color = rgba_to_color(point_to_rgba(
                    tuple(self.output_scalar*np.array(out_coords))
                ))
                dots.add(dot)
        return dots

class IntroduceInputOutputScene(InputOutputScene):
    CONFIG = {
        "dot_radius" : 0.05,
        "dot_density" : 0.25,
    }
    def construct(self):
        self.setup_planes()
        self.map_single_point_to_point()

    def setup_planes(self):
        self.input_plane, self.output_plane = self.get_planes()
        self.v_line = self.get_v_line()
        self.add(self.input_plane, self.output_plane, self.v_line)

    def map_single_point_to_point(self):
        input_plane = self.input_plane
        output_plane = self.output_plane

        #Dots
        dots = self.get_dots()

        in_dot = dots[int(0.55*len(dots))].copy()
        out_dot = in_dot.target
        for mob in in_dot, out_dot:
            mob.scale(1.5)
        in_dot.highlight(YELLOW)
        out_dot.highlight(PINK)

        input_label_arrow = Vector(DOWN+RIGHT)
        input_label_arrow.next_to(in_dot, UP+LEFT, SMALL_BUFF)
        input_label = TextMobject("Input point")
        input_label.next_to(input_label_arrow.get_start(), UP, SMALL_BUFF)
        for mob in input_label, input_label_arrow:
            mob.match_color(in_dot)
        input_label.add_background_rectangle()
        
        output_label_arrow = Vector(DOWN+LEFT)
        output_label_arrow.next_to(out_dot, UP+RIGHT, SMALL_BUFF)
        output_label = TextMobject("Output point")
        output_label.next_to(output_label_arrow.get_start(), UP, SMALL_BUFF)
        for mob in output_label, output_label_arrow:
            mob.match_color(out_dot)
        output_label.add_background_rectangle()

        path_arc = -TAU/4
        curved_arrow = Arrow(
            in_dot, out_dot,
            buff = SMALL_BUFF,
            path_arc = path_arc,
            use_rectangular_stem = False,
            color = WHITE,
        )
        curved_arrow.pointwise_become_partial(curved_arrow, 0, 0.95)
        function_label = TexMobject("f(", "\\text{2d input}", ")")
        function_label.next_to(curved_arrow, UP)
        function_label.add_background_rectangle()


        self.play(LaggedStart(GrowFromCenter, dots))
        self.play(LaggedStart(
            MoveToTarget, dots,
            path_arc = path_arc
        ))
        self.wait()
        self.play(FadeOut(dots))
        self.play(
            GrowFromCenter(in_dot),
            GrowArrow(input_label_arrow),
            FadeIn(input_label)
        )
        self.wait()
        self.play(
            ShowCreation(curved_arrow),
            ReplacementTransform(
                in_dot.copy(), out_dot,
                path_arc = path_arc
            ),
            FadeIn(function_label),
        )
        self.play(
            GrowArrow(output_label_arrow),
            FadeIn(output_label)
        )
        self.wait()
        self.play(*map(FadeOut, [
            input_label_arrow, input_label,
            output_label_arrow, output_label,
            curved_arrow, function_label,
        ]))

        #General movements and wiggles
        out_dot_continual_update = self.get_output_dot_continual_update(in_dot, out_dot)
        self.add(out_dot_continual_update)

        for vect in UP, RIGHT:
            self.play(
                in_dot.shift, 0.25*vect,
                rate_func = lambda t : wiggle(t, 8),
                run_time = 2
            )
        for vect in compass_directions(4, UP+RIGHT):
            self.play(Rotating(
                in_dot, about_point = in_dot.get_corner(vect),
                radians = TAU,
                run_time = 1
            ))
        self.wait()
        for coords in (-2, 2), (-2, -2), (2, -2), (1.5, 1.5):
            self.play(
                in_dot.move_to, input_plane.coords_to_point(*coords),
                path_arc = -TAU/4,
                run_time = 2
            )
        self.wait()

    ###

    def get_dots(self):
        input_plane = self.input_plane
        dots = VGroup()
        step = self.dot_density
        x_max = input_plane.x_radius
        x_min = -x_max
        y_max = input_plane.y_radius
        y_min = -y_max

        reverse = False
        for x in np.arange(x_min+step, x_max, step):
            y_range = list(np.arange(x_min+step, x_max, step))
            if reverse:
                y_range.reverse()
            reverse = not reverse
            for y in y_range:
                dot = Dot(radius = self.dot_radius)
                dot.move_to(input_plane.coords_to_point(x, y))
                dot.generate_target()
                dot.target.move_to(self.point_function(dot.get_center()))
                dots.add(dot)
        return dots

    def get_output_dot_continual_update(self, input_dot, output_dot):
        return ContinualUpdateFromFunc(
            output_dot, 
            lambda od : od.move_to(self.point_function(input_dot.get_center()))
        )

class IntroduceVectorField(IntroduceInputOutputScene):
    CONFIG = {
        "dot_density" : 0.5,
    }
    def construct(self):
        self.setup_planes()
        input_plane, output_plane = self.input_plane, self.output_plane
        dots = self.get_dots()

        in_dot = dots[0].copy()
        in_dot.move_to(input_plane.coords_to_point(1.5, 1.5))
        out_dot = in_dot.copy()
        out_dot_continual_update = self.get_output_dot_continual_update(in_dot, out_dot)
        for mob in in_dot, out_dot:
            mob.scale(1.5)
        in_dot.highlight(YELLOW)
        out_dot.highlight(PINK)

        out_vector = Arrow(
            LEFT, RIGHT, 
            color = out_dot.get_color(),
        )
        out_vector.set_stroke(BLACK, 1)
        continual_out_vector_update = ContinualUpdateFromFunc(
            out_vector, lambda ov : ov.put_start_and_end_on(
                output_plane.coords_to_point(0, 0),
                out_dot.get_center(),
            )
        )

        in_vector = out_vector.copy()
        def update_in_vector(in_vector):
            Transform(in_vector, out_vector).update(1)
            in_vector.scale(0.5)
            in_vector.shift(in_dot.get_center() - in_vector.get_start())
        continual_in_vector_update = ContinualUpdateFromFunc(
            in_vector, update_in_vector
        )
        continual_updates = [
            out_dot_continual_update,
            continual_out_vector_update, 
            continual_in_vector_update
        ]

        self.add(in_dot, out_dot)
        self.play(GrowArrow(out_vector, run_time = 2))
        self.wait()
        self.add_foreground_mobjects(in_dot)
        self.play(ReplacementTransform(out_vector.copy(), in_vector))
        self.wait()
        self.add(*continual_updates)
        path = Square().rotate(-90*DEGREES)
        path.replace(Line(
            input_plane.coords_to_point(-1.5, -1.5),
            input_plane.coords_to_point(1.5, 1.5),
        ), stretch = True)
        in_vectors = VGroup()
        self.add(in_vectors)
        for a in np.linspace(0, 1, 25):
            self.play(
                in_dot.move_to, path.point_from_proportion(a),
                run_time = 0.2,
                rate_func = None,
            )
            in_vectors.add(in_vector.copy())

        # Full vector field
        newer_in_vectors = VGroup()
        self.add(newer_in_vectors)
        for dot in dots:
            self.play(in_dot.move_to, dot, run_time = 1./15)
            newer_in_vectors.add(in_vector.copy())
        self.remove(*continual_updates)
        self.remove()
        self.play(*map(FadeOut, [
            out_dot, out_vector, in_vectors, in_dot, in_vector
        ]))
        self.wait()
        target_length = 0.4
        for vector in newer_in_vectors:
            vector.generate_target()
            if vector.get_length() == 0:
                continue
            factor = target_length / vector.get_length()
            vector.target.scale(factor, about_point = vector.get_start())

        self.play(LaggedStart(MoveToTarget, newer_in_vectors))
        self.wait()

class TwoDScreenInOurThreeDWorld(AltTeacherStudentsScene, ThreeDScene):
    def construct(self):
        self.ask_about_2d_functions()
        self.show_3d()

    def ask_about_2d_functions(self):
        in_plane = NumberPlane(x_radius = 2.5, y_radius = 2.5)
        in_plane.add_coordinates()
        in_plane.scale_to_fit_height(3)
        out_plane = in_plane.copy()

        in_text = TextMobject("Input space")
        out_text = TextMobject("Output space")
        VGroup(in_text, out_text).scale(0.75)
        in_text.next_to(in_plane, UP, SMALL_BUFF)
        out_text.next_to(out_plane, UP, SMALL_BUFF)
        in_plane.add(in_text)
        out_plane.add(out_text)

        arrow = Arrow(
            LEFT, RIGHT, 
            path_arc = -TAU/4,
            use_rectangular_stem = False,
            color = WHITE
        )
        arrow.pointwise_become_partial(arrow, 0.0, 0.97)
        group = VGroup(in_plane, arrow, out_plane)
        group.arrange_submobjects(RIGHT)
        arrow.shift(UP)
        group.move_to(self.students)
        group.to_edge(UP)

        dots = VGroup()
        dots_target = VGroup()
        for x in np.arange(-2.5, 3.0, 0.5):
            for y in np.arange(-2.5, 3.0, 0.5):
                dot = Dot(radius = 0.05)
                dot.move_to(in_plane.coords_to_point(x, y))
                dot.generate_target()
                dot.target.move_to(out_plane.coords_to_point(
                    x + 0.25*np.cos(5*y), y + 0.25*np.sin(3*x)
                ))
                dots.add(dot)
                dots_target.add(dot.target)
        dots.gradient_highlight(YELLOW, RED)
        dots_target.gradient_highlight(YELLOW, RED)

        self.play(
            self.teacher.change, "raise_right_hand",
            Write(in_plane, run_time = 1)
        )
        self.play(
            ShowCreation(arrow),
            ReplacementTransform(
                in_plane.copy(), out_plane,
                path_arc = -TAU/4,
            )
        )
        self.play(
            LaggedStart(GrowFromCenter, dots, run_time = 1),
            self.get_student_changes(*3*["erm"]),
        )
        self.play(LaggedStart(MoveToTarget, dots, path_arc = -TAU/4))
        self.wait(3)


    def show_3d(self):
        laptop = Laptop().scale(2)
        laptop.rotate(-TAU/12, DOWN)
        laptop.rotate(-5*TAU/24, LEFT)
        laptop.rotate(TAU/8, LEFT)
        laptop.scale(2.3*SPACE_WIDTH/laptop.screen_plate.get_width())
        laptop.shift(-laptop.screen_plate.get_center() + 0.1*IN)
        should_shade_in_3d(laptop)

        everything = VGroup(laptop, *self.mobjects)
        everything.generate_target()
        # for mob in everything.target.submobject_family():
        #     if isinstance(mob, PiCreature):
        #         mob.change_mode("confused")
        everything.target.rotate(TAU/12, LEFT)
        everything.target.rotate(TAU/16, UP)
        everything.target.shift(4*UP)

        self.move_camera(
            distance = 12,
            run_time = 4,
            added_anims = [MoveToTarget(everything, run_time = 4)],
        )
        self.add(AmbientRotation(everything, axis = UP, rate = 3*DEGREES))
        self.wait(10)

class EveryOutputPointHasAColor(ColorMappedObjectsScene):
    CONFIG = {
        "func" : lambda p : p,
        "dot_spacing" : 0.1,
        "dot_radius" : 0.01,
    }
    def construct(self):
        full_rect = FullScreenRectangle()
        full_rect.set_fill(WHITE, 1)
        full_rect.set_stroke(WHITE, 0)
        full_rect.color_using_background_image(self.background_image_file)

        title = TextMobject("Output Space")
        title.scale(1.5)
        title.to_edge(UP, buff = MED_SMALL_BUFF)
        title.set_stroke(BLACK, 1)
        self.add_foreground_mobjects(title)

        plane = NumberPlane()
        plane.fade(0.5)
        plane.axes.set_stroke(WHITE, 3)
        plane.add(BackgroundRectangle(title))
        self.add(plane)


        dots = VGroup()
        step = self.dot_spacing
        for x in np.arange(-SPACE_WIDTH, SPACE_WIDTH+step, step):
            for y in np.arange(-SPACE_HEIGHT, SPACE_HEIGHT+step, step):
                dot = Dot(color = WHITE)
                dot.color_using_background_image(self.background_image_file)
                dot.move_to(x*RIGHT + y*UP)
                dots.add(dot)
        random.shuffle(dots.submobjects)

        m = 3 #exponential factor        
        n = 1
        dot_groups = VGroup()
        while n <= len(dots):
            dot_groups.add(dots[n-1:m*n-1])
            n *= m
        self.play(LaggedStart(
            LaggedStart, dot_groups,
            lambda dg : (GrowFromCenter,  dg),
            run_time = 8,
            lag_ratio = 0.2,
        ))

class DotsHoppingToColor(InputOutputScene):
    CONFIG = {
        "dot_radius" : 0.05,
        "dot_density" : 0.25,
    }
    def construct(self):
        input_coloring, output_coloring = self.get_colorings()
        input_plane, output_plane = self.get_planes()
        v_line = self.get_v_line()

        dots = self.get_dots(input_plane, output_plane)

        right_half_block = Rectangle(
            height = 2*SPACE_HEIGHT,
            width = SPACE_WIDTH - SMALL_BUFF,
            stroke_width = 0,
            fill_color = BLACK,
            fill_opacity = 0.8,
        )
        right_half_block.to_edge(RIGHT, buff = 0)

        #Introduce parts
        self.add(input_plane, output_plane, v_line)
        self.play(
            FadeIn(output_coloring), 
            Animation(output_plane),
            output_plane.white_parts.highlight, BLACK,
            output_plane.lines_to_fade.set_stroke, {"width" : 0},
        )
        self.wait()
        self.play(LaggedStart(GrowFromCenter, dots, run_time = 3))
        self.wait()

        #Hop over and back
        self.play(LaggedStart(
            MoveToTarget, dots, 
            path_arc = -TAU/4,
            run_time = 3,
        ))
        self.wait()
        self.play(LaggedStart(
            ApplyMethod, dots,
            lambda d : (d.set_fill, d.target_color),
        ))
        self.wait()
        self.play(LaggedStart(
            ApplyMethod, dots,
            lambda d : (d.move_to, d.original_position),
            path_arc = TAU/4,
            run_time = 3,
        ))
        self.wait()
        self.play(
            FadeIn(input_coloring),
            Animation(input_plane),
            input_plane.white_parts.highlight, BLACK,
            input_plane.lines_to_fade.set_stroke, {"width" : 0},
            FadeOut(dots),
        )
        self.wait()

        #Cover output half
        right_half_block.save_state()
        right_half_block.next_to(SPACE_WIDTH*RIGHT, RIGHT)
        self.play(right_half_block.restore)
        self.wait()

        # Show yellow points
        inspector = DashedLine(
            ORIGIN, TAU*UP,
            dashed_segment_length = TAU/24,
            fill_opacity = 0,
            stroke_width = 3,
            stroke_color = WHITE,
        )
        inspector.add(*inspector.copy().highlight(BLACK).shift((TAU/24)*UP))
        inspector.apply_complex_function(np.exp)
        inspector.scale(0.15)

        inspector_image = inspector.copy()
        def update_inspector_image(inspector_image):
            inspector_image.move_to(self.point_function(inspector.get_center()))

        inspector_image_update_anim = UpdateFromFunc(
            inspector_image, update_inspector_image
        )
        pink_points_label = TextMobject("Pink points")
        pink_points_label.scale(0.7)
        pink_points_label.highlight(BLACK)

        self.play(
            inspector.move_to, input_plane.coords_to_point(-2.75, 2.75),
            inspector.set_stroke, {"width" : 2},
        )
        pink_points_label.next_to(inspector, RIGHT)
        self.play(
            Rotating(
                inspector, about_point = inspector.get_center(),
                rate_func = smooth,
                run_time = 2,
            ),
            Write(pink_points_label)
        )
        self.wait()
        self.play(right_half_block.next_to, SPACE_WIDTH*RIGHT, RIGHT)
        inspector_image_update_anim.update(0)
        self.play(ReplacementTransform(
            inspector.copy(), inspector_image,
            path_arc = -TAU/4,
        ))
        self.play(
            ApplyMethod(
                inspector.move_to, 
                input_plane.coords_to_point(-2, 0),
                path_arc = -TAU/8,
                run_time = 3,
            ),
            inspector_image_update_anim
        )
        self.play(
            ApplyMethod(
                inspector.move_to, 
                input_plane.coords_to_point(-2.75, 2.75),
                path_arc = TAU/8,
                run_time = 3,
            ),
            inspector_image_update_anim
        )
        self.play(FadeOut(pink_points_label))

        # Show black zero
        zeros = tuple(it.starmap(input_plane.coords_to_point, [
            (-2., -1), (1, 1), (2, -2),
        ]))
        for x in range(2):
            for zero in zeros:
                path = ParametricFunction(
                    bezier([
                        inspector.get_center(), 
                        input_plane.coords_to_point(0, 0),
                        zero
                    ]),
                    t_min = 0, t_max = 1
                )
                self.play(
                    MoveAlongPath(inspector, path, run_time = 2),
                    inspector_image_update_anim,
                )
                self.wait()
        self.play(FadeOut(VGroup(inspector, inspector_image)))

        # Show all dots and slowly fade them out
        for dot in dots:
            dot.scale(1.5)
        self.play(
            FadeOut(input_coloring),
            input_plane.white_parts.highlight, WHITE,
            LaggedStart(GrowFromCenter, dots)
        )
        self.wait()
        random.shuffle(dots.submobjects)
        self.play(LaggedStart(
            FadeOut, dots,
            lag_ratio = 0.05,
            run_time = 10,
        ))

        # Ask about whether a region contains a zero
        question = TextMobject("Does this region \\\\ contain a zero?")
        question.add_background_rectangle(opacity = 1)
        question.next_to(input_plane.label, DOWN)
        square = Square()
        square.match_background_image_file(input_coloring)
        square.move_to(input_plane)

        self.play(ShowCreation(square), Write(question))
        self.wait()
        quads = [
            (0, 0.5, 6, 6.25),
            (1, 1, 0.5, 2),
            (-1, -1, 3, 4.5),
            (0, 1.25, 5, 1.7),
            (-2, -1, 1, 1),
        ]
        for x, y, width, height in quads:
            self.play(
                square.stretch_to_fit_width, width,
                square.stretch_to_fit_height, height,
                square.move_to, input_plane.coords_to_point(x, y)
            )
            self.wait()

class SoWeFoundTheZeros(AltTeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Aha! So we \\\\ found the solutions!",
            target_mode = "hooray",
            student_index = 2,
            bubble_kwargs = {"direction" : LEFT},
        )
        self.wait()
        self.teacher_says(
            "Er...only \\\\ kind of",
            target_mode = "hesitant"
        )
        self.wait(3)

class Rearrange2DEquation(AltTeacherStudentsScene):
    def construct(self):
        f_tex, g_tex, h_tex = [
            "%s(\\text{2d point})"%char
            for char in "f", "g", "h" 
        ]
        zero_tex = "\\vec{\\textbf{0}}"
        equations = VGroup(
            TexMobject(g_tex, "", "=", h_tex, ""),
            TexMobject(g_tex, "-", h_tex, "=", zero_tex),
        )
        equations.move_to(self.hold_up_spot, DOWN)
        equations.shift_onto_screen()

        brace = Brace(equations[1], UP)
        zero_eq = brace.get_tex("%s = %s"%(f_tex, zero_tex))

        for equation in equations:
            equation.highlight_by_tex(g_tex, BLUE)
            equation.highlight_by_tex(h_tex, YELLOW)
            equation.sort_submobjects_alphabetically()


        self.teacher_holds_up(equations[0])
        self.change_all_student_modes("pondering")
        self.play(Transform(
            *equations,
            run_time = 1.5,
            path_arc = TAU/2
        ))
        self.play(
            Succession(
                GrowFromCenter(brace),
                Write(zero_eq, run_time = 1)
            ),
            self.get_student_changes(*["happy"]*3)
        )
        self.play(*[
            ApplyMethod(pi.change, "thinking", self.screen)
            for pi in self.pi_creatures
        ])
        self.wait(3)

class SearchForZerosInInputSpace(ColorMappedObjectsScene):
    CONFIG = {
        "func" : example_plane_func,
    }
    def construct(self):
        title = TextMobject("Input space")
        title.scale(2)
        title.to_edge(UP)
        title.set_stroke(BLACK, 1)
        title.add_background_rectangle()

        plane = NumberPlane()
        plane.fade(0.5)
        plane.axes.set_stroke(WHITE, 3)

        self.add(plane, title)

        looking_glass = Circle()
        looking_glass.set_stroke(WHITE, 3)
        looking_glass.set_fill(WHITE, 0.6)
        looking_glass.color_using_background_image(self.background_image_file)
        question = TextMobject("Which points go to 0?")
        question.next_to(looking_glass, DOWN)
        question.add_background_rectangle()

        mover = VGroup(looking_glass, question)
        mover.move_to(4*LEFT + UP)

        self.play(FadeIn(mover))
        points = [4*RIGHT+UP, 2*RIGHT+2*DOWN, 2*LEFT+2*DOWN, 3*RIGHT+2.5*DOWN]
        for point in points:
            self.play(mover.move_to, point, run_time = 1.5)
            self.wait()

class OneDRegionBoundary(Scene):
    CONFIG = {
        "graph_color" : BLUE,
        "region_rect_height" : 0.1,
    }
    def construct(self):
        x0 = self.x0 = 3 
        x1 = self.x1 = 6
        fx0 = self.fx0 = -2
        fx1 = self.fx1 = 2

        axes = self.axes = Axes(
            x_min = -1, x_max = 10,
            y_min = -3, y_max = 3,
        )
        axes.center()
        axes.set_stroke(width = 2)

        input_word = TextMobject("Input")
        input_word.next_to(axes.x_axis, UP, SMALL_BUFF, RIGHT)
        output_word = TextMobject("Output")
        output_word.next_to(axes.y_axis, UP)
        axes.add(input_word, output_word)
        self.add(axes)

        graph = self.get_graph_part(1, 1)
        alt_graphs = [
            self.get_graph_part(*points)
            for points in [
                (-1, -2),
                (-1, -1, -1),
                (1, 1, 1),
                (-0.75, 0, 1.75),
                (-3, -2, -1),
            ]
        ]

        #Region and boundary
        line = Line(axes.coords_to_point(x0, 0), axes.coords_to_point(x1, 0))
        region = Rectangle(
            stroke_width = 0,
            fill_color = YELLOW,
            fill_opacity = 0.5,
            height = self.region_rect_height
        )
        region.match_width(line, stretch = True)
        region.move_to(line)

        region_words = TextMobject("Input region")
        region_words.scale_to_fit_width(0.8*region.get_width())
        region_words.next_to(region, UP)

        x0_arrow, x1_arrow = arrows = VGroup(*[
            Arrow(
                axes.coords_to_point(x, 0),
                axes.coords_to_point(x, fx),
                color = color,
                buff = 0
            )
            for x, fx, color in (x0, fx0, RED), (x1, fx1, GREEN)
        ])
        minus = TexMobject("-")
        minus.match_color(x0_arrow)
        minus.next_to(x0_arrow, UP)
        plus = TexMobject("+")
        plus.match_color(x1_arrow)
        plus.next_to(x1_arrow, DOWN)
        signs = VGroup(plus, minus)


        self.play(
            GrowFromCenter(region),
            FadeIn(region_words)
        )
        self.wait()
        self.play(*it.chain(
            map(GrowArrow, arrows),
            map(Write, signs)
        ))
        self.wait()
        self.play(
            ShowCreation(graph), 
            FadeOut(region_words),
        )
        self.wait()
        for alt_graph in alt_graphs + alt_graphs:
            self.play(Transform(graph, alt_graph, path_arc = 0.1*TAU))
        self.wait()


    ###

    def get_graph_part(self, *interim_values):
        result = VMobject()
        result.set_stroke(self.graph_color, 3)
        result.set_fill(opacity = 0)
        values = [self.fx0] + list(interim_values) + [self.fx1]
        result.set_points_smoothly([
            self.axes.coords_to_point(x, fx)
            for x, fx in zip(
                np.linspace(self.x0, self.x1, len(values)),
                values
            )
        ])
        return result

class DirectionOfA2DFunctionAlongABoundary(InputOutputScene):
    def construct(self):
        colorings = self.get_colorings()
        colorings.set_fill(opacity = 0.25)
        input_plane, output_plane = planes = self.get_planes()
        for plane in planes:
            plane.lines_to_fade.set_stroke(width = 0)
        v_line = self.get_v_line()

        rect = Rectangle()
        rect.set_stroke(WHITE, 5)
        rect.set_fill(WHITE, 0)
        line = Line(
            input_plane.coords_to_point(-0.75, 2.5),
            input_plane.coords_to_point(2.5, -1.5),
        )
        rect.replace(line, stretch = True)
        rect.insert_n_anchor_points(50)
        rect.match_background_image_file(colorings[0])

        rect_image = rect.copy()
        rect_image.match_background_image_file(colorings[1])
        def update_rect_image(rect_image):
            rect_image.points = np.array(rect.points)
            rect_image.apply_function(self.point_function)
        rect_image_update_anim = UpdateFromFunc(rect_image, update_rect_image)


        def get_input_point():
            return rect.points[-1]

        def get_output_coords():
            in_coords = input_plane.point_to_coords(get_input_point())
            return self.func(in_coords)

        def get_angle():
            return angle_of_vector(get_output_coords())

        def get_color():
            return rev_to_color(get_angle()/TAU) #Negative?


        out_vect = Vector(RIGHT, color = WHITE)
        out_vect_update_anim = UpdateFromFunc(
            out_vect,
            lambda ov : ov.put_start_and_end_on(
                output_plane.coords_to_point(0, 0),
                rect_image.points[-1]
            ).highlight(get_color())
        )

        dot = Dot()
        dot.set_stroke(BLACK, 1)
        dot_update_anim = UpdateFromFunc(
            dot, lambda d : d.move_to(get_input_point()).set_fill(get_color())
        )

        in_vect = Vector(RIGHT)
        def update_in_vect(in_vect):
            in_vect.put_start_and_end_on(ORIGIN, 0.5*RIGHT)
            in_vect.rotate(get_angle())
            in_vect.highlight(get_color())
            in_vect.shift(get_input_point() - in_vect.get_start())
            return in_vect
        in_vect_update_anim = UpdateFromFunc(in_vect, update_in_vect)

        self.add(colorings, planes, v_line)

        self.play(
            GrowArrow(out_vect),
            GrowArrow(in_vect),
            Animation(dot),
        )
        self.play(
            ShowCreation(rect),
            ShowCreation(rect_image),
            out_vect_update_anim,
            in_vect_update_anim,
            dot_update_anim,
            rate_func = bezier([0, 0, 1, 1]),
            run_time = 10,
        )

class AskAboutHowToGeneralizeSigns(AltTeacherStudentsScene):
    def construct(self):
        # 2d plane
        plane = NumberPlane(x_radius = 2.5, y_radius = 2.5)
        plane.scale(0.8)
        plane.to_corner(UP+LEFT)
        plane.add_coordinates()

        dot = Dot(color = YELLOW)
        label = TextMobject("Sign?")
        label.add_background_rectangle()
        label.scale(0.5)
        label.next_to(dot, UP, SMALL_BUFF)
        dot.add(label)
        dot.move_to(plane.coords_to_point(1, 1))
        dot.save_state()
        dot.fade(1)
        dot.center()

        question = TextMobject(
            "Wait...what would \\\\ positive and negative \\\\ be in 2d?",
        )
        # question.highlight_by_tex_to_color_map({
        #     "+" : "green", 
        #     "textminus" : "red"
        # })


        self.student_says(
            question,
            target_mode = "sassy",
            student_index = 2,
            added_anims = [
                self.teacher.change, "plain",
            ],
            bubble_kwargs = {"direction" : LEFT},
            run_time = 1,
        )
        self.play(
            Write(plane, run_time = 1),
            self.students[0].change, "confused",
            self.students[1].change, "confused",
        )
        self.play(dot.restore)
        for coords in (-1, 1), (1, -1), (0, -2), (-2, 1):
            self.wait(0.5)
            self.play(dot.move_to, plane.coords_to_point(*coords))
        self.wait()

class HypothesisAboutFullyColoredBoundary(ColorMappedObjectsScene):
    CONFIG = {
        "func" : plane_func_from_complex_func(lambda z : z**3),
    }
    def construct(self):
        ColorMappedObjectsScene.construct(self)
        square = Square(side_length = 4)
        square.color_using_background_image(self.background_image_file)
        hypothesis = TextMobject(
           "Working Hypothesis: \\\\",
           "If a 2d function hits outputs of all possible colors \\\\" + 
           "on the boundary of a 2d region,", 
           "that region \\\\ contains a zero.",
           alignment = "",
        )
        hypothesis[0].next_to(hypothesis[1:], UP)
        hypothesis[0].highlight(YELLOW)
        s = hypothesis[1].get_tex_string()
        s = filter(lambda c : c not in string.whitespace, s)
        n = s.index("colors")
        hypothesis[1][n:n+len("colors")].gradient_highlight(
            # RED, GOLD_E, YELLOW, GREEN, BLUE, PINK,
            BLUE, PINK, YELLOW,
        )
        hypothesis.to_edge(UP)
        square.next_to(hypothesis, DOWN, MED_LARGE_BUFF)

        self.add(hypothesis[0])
        self.play(
            LaggedStart(FadeIn, hypothesis[1]),
            ShowCreation(square, run_time = 8)
        )
        self.play(LaggedStart(FadeIn, hypothesis[2]))
        self.play(square.set_fill, {"opacity" : 1}, run_time = 2)
        self.wait()

class PiCreatureAsksWhatWentWrong(PiCreatureScene):
    def construct(self):
        randy = self.pi_creature
        randy.set_color(YELLOW_E)
        randy.flip()
        randy.to_corner(DOWN+LEFT)
        question = TextMobject("What went wrong?")
        question.next_to(randy, UP)
        question.shift_onto_screen()
        question.save_state()
        question.shift(DOWN).fade(1)

        self.play(randy.change, "erm")
        self.wait(2)
        self.play(
            Animation(VectorizedPoint(ORIGIN)),
            question.restore,
            randy.change, "confused",
        )
        self.wait(5)

class ForeverNarrowingLoop(InputOutputScene):
    CONFIG = {
        "target_coords" : (1, 1),
        "input_plane_corner" : UP+RIGHT,
        "shrink_time" : 20,
    }
    def construct(self):
        input_coloring, output_coloring = colorings = VGroup(*self.get_colorings())
        input_plane, output_plane = planes = VGroup(*self.get_planes())
        for plane in planes:
            plane.white_parts.highlight(BLACK)
            plane.lines_to_fade.set_stroke(width = 0)

        v_line = Line(UP, DOWN).scale(SPACE_HEIGHT)
        v_line.set_stroke(WHITE, 5)

        self.add(colorings, v_line, planes)
        self.play(*it.chain(
            [
                ApplyMethod(coloring.set_fill, {"opacity" : 0.2})
                for coloring in colorings
            ],
            [
                ApplyMethod(plane.white_parts.highlight, WHITE)
                for plane in planes
            ]
        ), run_time = 2)

        # circle
        circle = Circle(color = WHITE, radius = 2.25)
        circle.flip(axis = RIGHT)
        circle.insert_n_anchor_points(50)
        circle.next_to(
            input_coloring.get_corner(self.input_plane_corner), 
            -self.input_plane_corner, 
            SMALL_BUFF
        )
        circle.set_stroke(width = 5)
        circle_image = circle.copy()
        circle.match_background_image_file(input_coloring)
        circle_image.match_background_image_file(output_coloring)

        def update_circle_image(circle_image):
            circle_image.points = circle.points
            circle_image.apply_function(self.point_function)
            circle_image.make_smooth()

        circle_image_update_anim = UpdateFromFunc(
            circle_image, update_circle_image
        )

        self.play(
            ShowCreation(circle),
            ShowCreation(circle_image),
            run_time = 3,
            rate_func = bezier([0, 0, 1, 1])
        )
        self.play(
            circle.scale, 0,
            circle.move_to, input_plane.coords_to_point(*self.target_coords),
            circle_image_update_anim,
            run_time = self.shrink_time,
            rate_func = bezier([0, 0, 1, 1])
        )

class AltForeverNarrowingLoop(ForeverNarrowingLoop):
    CONFIG = {
        "target_coords" : (-2, -1),
        "input_plane_corner" : DOWN+LEFT,
        "shrink_time" : 3,
    }

class FailureOfComposition(ColorMappedObjectsScene):
    CONFIG = {
        "func" : lambda p : (
            np.cos(TAU*p[1]/3.5), 
            np.sin(TAU*p[1]/3.5)
        )
    }
    def construct(self):
        ColorMappedObjectsScene.construct(self)

        big_square = Square(side_length = 4)
        big_square.move_to(ORIGIN, RIGHT)
        small_squares = VGroup(*[
            Square(side_length = 2) for x in range(2)
        ])
        small_squares.match_width(big_square, stretch = True)
        small_squares.arrange_submobjects(DOWN, buff = 0)
        small_squares.move_to(big_square)
        small_squares.space_out_submobjects(1.1)
        all_squares = VGroup(big_square, *small_squares)
        all_squares.set_stroke(width = 6)

        for square in all_squares:
            square.highlight(WHITE)
            square.color_using_background_image(self.background_image_file)

        question = TextMobject("Does my border go through every color?")
        question.to_edge(UP)
        no_answers = VGroup()
        yes_answers = VGroup()
        for square in all_squares:
            if square is big_square:
                square.answer = TextMobject("Yes")
                square.answer.highlight(GREEN)
                yes_answers.add(square.answer)
            else:
                square.answer = TextMobject("No")
                square.answer.highlight(RED)
                no_answers.add(square.answer)
            square.answer.move_to(square)

        no_answers_in_equation = no_answers.copy()
        yes_answers_in_equation = yes_answers.copy()
        plus, equals = plus_equals = TexMobject("+=")
        equation = VGroup(
            no_answers_in_equation[0], plus,
            no_answers_in_equation[1], equals,
            yes_answers_in_equation
        )
        equation.arrange_submobjects(RIGHT, buff = SMALL_BUFF)
        equation.next_to(big_square, RIGHT, MED_LARGE_BUFF)
        q_marks = TexMobject("???")
        q_marks.next_to(equals, UP)


        self.add(question)
        self.play(LaggedStart(ShowCreation, small_squares, lag_ratio = 0.8))
        self.play(LaggedStart(Write, no_answers))
        self.wait()
        self.play(
            small_squares.arrange_submobjects, DOWN, {"buff" : 0},
            small_squares.move_to, big_square,
            no_answers.space_out_submobjects, 0.9,
        )
        self.add(big_square)
        no_answers_copy = no_answers.copy()
        small_squares.save_state()
        self.play(
            Transform(no_answers, no_answers_in_equation),
            Write(plus_equals),
            small_squares.set_stroke, {"width" : 0},
        )
        self.play(
            Write(yes_answers),
            Write(yes_answers_in_equation),
        )
        self.play(LaggedStart(FadeIn, q_marks, run_time = 1, lag_ratio = 0.8))
        self.wait(2)
        self.play(
            small_squares.restore,
            FadeOut(yes_answers),
            FadeIn(no_answers_copy),
        )
        self.wait()
        self.play(
            small_squares.set_stroke, {"width" : 0},
            FadeOut(no_answers_copy),
            FadeIn(yes_answers),
        )
        self.wait()

        # We can find a better notion of what we want

        cross = Cross(question)

        self.play(
            ShowCreation(cross, run_time = 2),
            FadeOut(equation),
            FadeOut(no_answers),
            FadeOut(q_marks),
            FadeOut(yes_answers),
        )

        x, plus, y = x_plus_y = TexMobject("x+y")
        x_plus_y.move_to(big_square)
        x_plus_y.save_state()
        x.move_to(no_answers_copy[0])
        y.move_to(no_answers_copy[1])
        plus.fade(1)

        for square, char in zip(small_squares, [x, y]):
            ghost = square.copy()
            ghost.set_stroke(width = 5)
            ghost.background_image_file = None
            self.play(
                small_squares.restore,
                ShowPassingFlash(ghost),
                Write(char)
            )
        self.wait()
        ghost = big_square.copy()
        ghost.background_image_file = None
        self.play(
            small_squares.set_stroke, {"width" : 0},
            x_plus_y.restore,
        )
        self.play(ShowPassingFlash(ghost))
        self.wait()










































