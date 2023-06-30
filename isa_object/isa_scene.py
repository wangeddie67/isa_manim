
import numpy as np
from typing import List
from manim import config
from manim import MovingCameraScene, MovingCamera
from manim import Text, Mobject, Rectangle
from manim import UP, DOWN, LEFT, RIGHT
from manim import FadeIn, FadeOut, Transform
from .vector_reg import VectorReg
from .scalar_reg import ScalarReg

class IsaScene(MovingCameraScene):

    def __init__(self, camera_class=MovingCamera, **kwargs):
        super().__init__(camera_class=camera_class, **kwargs)

        self.section_fadein_list : List = []
        self.section_fadeout_list : List = []

        self.frame_fadein_list : List = []
        self.frame_play_list : List = []
        self.frame_fadeout_list : List = []

        self.within_frame = False

        self.vertical_coord = 0
        self.horizontal_coord = 1.0
        self.camera_scale_rate = 1.0
        self.camera_origin_h = 0.0

    #
    # Private
    #

    def _play_frame_fadein(self, no_wait = False):
        if len(self.frame_fadein_list) > 0:
            camera_animate = self.update_camera()
            if camera_animate is None:
                self.play(FadeIn(*self.frame_fadein_list))
            else:
                self.play(FadeIn(*self.frame_fadein_list), camera_animate)
            if not no_wait:
                self.wait()
        self.frame_fadein_list.clear()

    def _play_frame_play(self, no_wait = False):
        if len(self.frame_play_list) > 0:
            self.play(*self.frame_play_list)
            if not no_wait:
                self.wait()
        self.frame_play_list.clear()

    def _play_frame_fadeout(self, no_wait = False):
        if len(self.frame_fadeout_list) > 0:
            self.play(FadeOut(*self.frame_fadeout_list))
            if not no_wait:
                self.wait()
        self.frame_fadeout_list.clear()

    def _play_section_fadein(self, no_wait = False):
        all_fadein_list = self.section_fadein_list + self.frame_fadein_list
        if len(all_fadein_list) > 0:
            camera_animate = self.update_camera()
            if camera_animate is None:
                self.play(FadeIn(*all_fadein_list))
            else:
                self.play(FadeIn(*all_fadein_list), camera_animate)
            if not no_wait:
                self.wait()
        self.section_fadein_list.clear()
        self.frame_fadein_list.clear()

    def _play_section_fadeout(self, no_wait = False):
        all_fadeout_list = self.section_fadeout_list + self.frame_fadeout_list
        if len(all_fadeout_list) > 0:
            self.play(FadeOut(*all_fadeout_list))
            if not no_wait:
                self.wait()
        self.section_fadeout_list.clear()
        self.frame_fadeout_list.clear()

    #
    # Frame
    #

    def start_frame(self):
        # End previous frame
        if self.within_frame:
            self.end_frame()

        # End unplayed section behaviors
        self._play_section_fadein()

        self.within_frame = True

    def end_frame(self):
        self._play_frame_fadein()
        self._play_frame_play()
        self._play_frame_fadeout()

        self.within_frame = False

    def switch_step(self, no_wait : bool = True):
        if len(self.frame_fadein_list) + len(self.frame_play_list) > 0:
            self._play_frame_fadein(no_wait=no_wait)
            self._play_frame_play(no_wait=no_wait)
            self.wait()

    def frame_read_elem(self, reg: VectorReg, color, *index):
        if isinstance(reg, ScalarReg):
            elem = reg.get_elem(color)
        elif isinstance(reg, VectorReg):
            elem = reg.get_elem(color, index[0])

        self.frame_fadein_list.append(elem)
        self.frame_fadeout_list.append(elem)
        return elem

    def frame_move_elem(self, elem: Mobject, reg: VectorReg, *index, scale: float = 1.0):
        if scale != 1.0:
            animate = elem.animate.move_to(reg.get_elem_center(index[0])).stretch(scale, 0)
        else:
            animate = elem.animate.move_to(reg.get_elem_center(index[0]))
        self.frame_play_list.append(animate)

    #
    # Section
    #

    def draw_title(self, title: str):
        title_obj = Text(title).move_to(UP * 3)
        camera_animate = self.update_camera()
        if camera_animate is None:
            self.play(FadeIn(title_obj))
        else:
            self.play(FadeIn(title_obj), camera_animate)
        self.wait()

    def start_section(self, subtitle: str):
        subtitle_obj = Text(subtitle, font_size=40).move_to(UP * 2)
        self.section_fadein_list.append(subtitle_obj)
        self.section_fadeout_list.append(subtitle_obj)
        self.vertical_coord = 0
        self.horizontal_coord = 1.0

    def end_section(self):
        self._play_section_fadein()
        self._play_frame_play()
        self._play_section_fadeout()

        self.within_frame = False

    def section_decl_scalar(self, *args, **kargs):
        scalar = ScalarReg(*args, **kargs, font_size=40).shift(DOWN * self.vertical_coord)
        self.vertical_coord += 2

        self.section_fadein_list.append(scalar)
        self.section_fadeout_list.append(scalar)

        if self.horizontal_coord < scalar.get_left_boundary_width():
            self.horizontal_coord = scalar.get_left_boundary_width()

        return scalar

    def section_decl_vector(self, *args, **kargs):
        vector = VectorReg(*args, **kargs, font_size=40).shift(DOWN * self.vertical_coord)
        self.vertical_coord += 2

        self.section_fadein_list.append(vector)
        self.section_fadeout_list.append(vector)

        if self.horizontal_coord < vector.get_left_boundary_width():
            self.horizontal_coord = vector.get_left_boundary_width()

        return vector

    def section_decl_vector_group(self, names, *args, **kargs):
        vector_list = []
        for i, name in enumerate(names):
            vector_list.append(
                VectorReg(name, *args, **kargs, font_size=40).shift(DOWN * (self.vertical_coord + i))
                )
        self.vertical_coord += len(names) + 1

        self.section_fadein_list.extend(vector_list)
        self.section_fadeout_list.extend(vector_list)

        if self.horizontal_coord < vector_list[0].get_left_boundary_width():
            self.horizontal_coord = vector_list[0].get_left_boundary_width()

        return vector_list

    def update_camera(self):
        boundary = 1

        next_height = 4 + self.vertical_coord
        if (config.frame_height - boundary) < next_height:
            vertical_scale_rate = (config.frame_height - boundary) / next_height
        else:
            vertical_scale_rate = 1.0

        next_width = self.horizontal_coord * 2
        if (config.frame_width - boundary * 2) < next_width:
            horizontal_scale_rate = (config.frame_width - boundary * 2) / next_width
        else:
            horizontal_scale_rate = 1.0

        scale_rate = min(vertical_scale_rate, horizontal_scale_rate)

        origin_h = (config.frame_height * (1.0/3.0) - 3 * scale_rate) / scale_rate

        if abs(scale_rate - self.camera_scale_rate) > 1e-3 \
                or abs(origin_h - self.camera_origin_h) > 1e-3:
            animate = self.camera.frame.animate.scale(self.camera_scale_rate / scale_rate) \
                      .move_to(DOWN * origin_h)
            self.camera_scale_rate = scale_rate
            self.camera_origin_h = origin_h

            return animate
        else:
            return None

    #
    # Predefined frame
    #

    def frame_counter_to_predicate(self, png_obj: ScalarReg, *args, **kargs):
        self.start_frame()
        predicate = self.section_decl_vector(*args, **kargs)
        predicate.shift(png_obj.get_reg_center() - predicate.get_reg_center())
        self.vertical_coord -= 2

        camera_animate = self.update_camera()
        if camera_animate is None:
            self.play(FadeIn(predicate), FadeOut(png_obj))
        else:
            self.play(FadeIn(predicate), FadeOut(png_obj), camera_animate)
        self.wait()
        self.end_frame()

        if png_obj in self.section_fadein_list:
            self.section_fadein_list.remove(png_obj)
        if predicate in self.section_fadein_list:
            self.section_fadein_list.remove(predicate)
        if png_obj in self.section_fadeout_list:
            self.section_fadeout_list.remove(png_obj)

        return predicate

    def frame_concat_vector(self,
                            v1: VectorReg,
                            v2: VectorReg,
                            *args, **kargs) -> VectorReg:
        elements = v1.elements + v2.elements
        elem_width = int(min(v1.elem_width, v2.elem_width))
        if "ratio" not in kargs:
            kargs["ratio"] = max(v1.ratio, v2.ratio)

        self.start_frame()
        vector = self.section_decl_vector(*args, elements=elements, elem_width=elem_width, **kargs)
        vector.shift(v1.get_reg_center() - vector.get_reg_center())
        self.vertical_coord -= 2

        self.play(v1.animate.move_to(v1.get_center() + LEFT * v1.get_reg_width() / 2),
                  v2.animate.move_to(v1.get_center() + RIGHT * v2.get_reg_width() / 2))

        camera_animate = self.update_camera()
        if camera_animate is None:
            self.play(FadeIn(vector), FadeOut(v1), FadeOut(v2))
        else:
            self.play(FadeIn(vector), FadeOut(v1), FadeOut(v2), camera_animate)
        self.wait()
        self.end_frame()

        if v1 in self.section_fadein_list:
            self.section_fadein_list.remove(v1)
        if v2 in self.section_fadein_list:
            self.section_fadein_list.remove(v2)
        if vector in self.section_fadein_list:
            self.section_fadein_list.remove(vector)
        if v1 in self.section_fadeout_list:
            self.section_fadeout_list.remove(v1)
        if v2 in self.section_fadeout_list:
            self.section_fadeout_list.remove(v2)

        return vector

    #
    # Predefined step
    #

    def step_data_convert(self,
                          elem: Rectangle,
                          scale: float,
                          index: int) -> Rectangle:
        elem_width = elem.width * scale

        elem_target = elem.copy().stretch(scale, 0) \
            .move_to(elem.get_right() + LEFT * (index + 0.5) * elem_width)

        self.play(Transform(elem, elem_target))

        return elem

