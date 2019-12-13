from manimlib.imports import *
import typing


def set_colors(object: typing.Union[Mobject, Group, typing.Sequence], colors: typing.List[str]) -> object:
    [object[i].set_color(color) for i, color in enumerate(colors)]
    return object


def ReplacementMultiIndex(
        m1: Mobject, i1: typing.Iterable[typing.Union[int, typing.Sequence[int], range]],
        m2: Mobject, i2: typing.Iterable[typing.Union[int, typing.Sequence[int], range]],
        *, copy_first: bool = False, copy_second: bool = False, transformation: type = ReplacementTransform
):
    """
    Does a multi-index replacement.
    :param m1: The first object; is replaced.
    :param i1: The respective indexes.
    :param m2: The second object; is the replacer.
    :param i2: The respective replacer indexes.
    :param copy_first: If all replaced objects (in m1) should be copied. Defaults to False.
    :param copy_second: If all replacer objects (in m2) should be copied. Defaults to False.
    :param transformation: The transformation class to use (defaults to ReplacementTransform).
    :return:
    """
    def copy_if_copy_first(obj):
        if copy_first:
            return obj.copy()
        return obj

    def copy_if_copy_second(obj):
        if copy_second:
            return obj.copy()
        return obj

    def converter(m, ii):
        if type(ii) == range or isinstance(ii, range):
            return m[ii.start:ii.stop:ii.step]

        if type(ii) in (list, tuple) or isinstance(ii, list) or isinstance(ii, tuple):
            return VGroup(*map(lambda i: m[i], ii))

        return m[ii]

    replacements = [
        transformation(
            copy_if_copy_first(
                converter(m1, ii1)
            ),

            copy_if_copy_second(
                converter(m2, ii2)
            )
        ) for ii1, ii2 in zip(i1, i2)
    ]
    return replacements


class Unwrite(Write):
    CONFIG = {
        "rate_func": lambda t: linear(1 - t),
        "remover": True
    }


class UnDrawBorderThenFill(DrawBorderThenFill):
    CONFIG = {
        "rate_func": lambda t: double_smooth(1 - t),
        "remover": True
    }


class ReplaceClockwiseTransform(ClockwiseTransform):
    CONFIG = {
        "replace_mobject_with_target_in_scene": True,
    }


class ReplaceCounterclockwiseTransform(CounterclockwiseTransform):
    CONFIG = {
        "replace_mobject_with_target_in_scene": True,
    }
