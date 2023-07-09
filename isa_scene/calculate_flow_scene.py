
from typing import List
from colour import Color
from manim import config
from manim import UP, DOWN
from ..isa_animate import read_scalar_reg, read_vector_group, read_vector_reg
from ..isa_animate import read_elem, assign_elem
from ..isa_animate import concat_vector, counter_to_predicate, data_convert
from ..isa_animate import def_func_call, function_call
from ..isa_objects import OneDimReg, OneDimRegElem, FunctionCall
from .isa_scene import IsaScene

class CalculateFlowScene(IsaScene):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.vertical_coord = 0
        self.horizontal_coord = 1.0
        self.camera_scale_rate = 1.0
        self.camera_origin_h = 0.0

        self.function_dict = dict()

    #
    # Section
    #

    def start_section(self, subtitle: str):
        """
        Start of one section. Draw subtitle and clear boundary of scene.

        Args:
            subtitle: String of subtitle.
        """
        self.draw_subtitle(subtitle)

        self.vertical_coord = 0
        self.horizontal_coord = 1.0
        self.function_dict = dict()

    def end_section(self,
                    wait: int = 1,
                    fade_out: bool = True):
        """
        Terminate or temporary stop of section. Update camera.

        Args:
            wait: Time of wait before end of section.
            fade_out: True means fade_out all items on scene except always-on
                      items.
        """
        camera_animate = self._update_camera()
        self.switch_section(wait=wait,
                            fade_out=fade_out,
                            camera_animate=camera_animate)

    def _update_camera(self):
        boundary = 1

        zoomed_frame_height = config.frame_height / 2 + 2
        zoomed_frame_width = config.frame_width

        next_height = 2 + self.vertical_coord
        if (zoomed_frame_height - boundary) < next_height:
            vertical_scale_rate = (zoomed_frame_height - boundary) / next_height
        else:
            vertical_scale_rate = 1.0

        next_width = self.horizontal_coord * 2
        if (zoomed_frame_width - boundary * 2) < next_width:
            horizontal_scale_rate = (zoomed_frame_width - boundary * 2) / next_width
        else:
            horizontal_scale_rate = 1.0

        scale_rate = min(vertical_scale_rate, horizontal_scale_rate)

        origin_h = 2 - (zoomed_frame_height / 2) / scale_rate

        if abs(scale_rate - self.camera_scale_rate) > 1e-3 \
                or abs(origin_h - self.camera_origin_h) > 1e-3:
            #animate = self.camera.frame.animate.scale(self.camera_scale_rate / scale_rate) \
            #          .move_to(DOWN * origin_h)
            camera_ratio = self.camera_scale_rate / scale_rate
            camera_target = UP * origin_h
            self.camera_scale_rate = scale_rate
            self.camera_origin_h = origin_h

            return [camera_ratio, camera_target]
        else:
            return None

    #
    # Animations frame
    #

    def decl_scalar(self,
                    text: str,
                    color: Color,
                    width: int,
                    **kwargs) -> OneDimReg:
        """
        Declare scalar variables, return one-dim register.
        """
        animate = read_scalar_reg(text, color, width, **kwargs)

        scalar_reg = animate.dst_item_list[0]
        scalar_reg.shift(DOWN * self.vertical_coord)
        self.vertical_coord += 2

        if self.horizontal_coord < scalar_reg.get_max_boundary_width():
            self.horizontal_coord = scalar_reg.get_max_boundary_width()

        self.register_animation(animate)
        return scalar_reg

    def decl_vector(self,
                    text: str,
                    color: Color,
                    width: int,
                    elements: int = 1,
                    **kwargs):
        """
        Declare vector variables, return one-dim register.
        """
        animate = read_vector_reg(text, color, width, elements, **kwargs)

        vector_reg = animate.dst_item_list[0]
        vector_reg.shift(DOWN * self.vertical_coord)
        self.vertical_coord += 2

        if self.horizontal_coord < vector_reg.get_max_boundary_width():
            self.horizontal_coord = vector_reg.get_max_boundary_width()

        self.register_animation(animate)
        return vector_reg

    def decl_vector_group(self,
                          text_list: List[str],
                          color: Color,
                          width: int,
                          elements: int = 1,
                          **kwargs):
        """
        Declare a list of vector variables, return a list of one-dim register.
        """
        animate = read_vector_group(text_list, color, width, elements, **kwargs)

        vector_reg_list = animate.dst_item_list
        for index, vector_reg in enumerate(vector_reg_list):
            vector_reg.shift(DOWN * (self.vertical_coord + index))
        self.vertical_coord += len(vector_reg_list) + 1

        if self.horizontal_coord < vector_reg_list[0].get_max_boundary_width():
            self.horizontal_coord = vector_reg_list[0].get_max_boundary_width()

        self.register_animation(animate)
        return vector_reg_list

    def read_elem(self,
                  vector: OneDimReg,
                  color: Color,
                  size: float = -1.0,
                  index: int = 0,
                  **kwargs):
        """
        Read element from register, return one Rectangle.

        Args:
            vector: Register.
            color: Color of new element.
            size: Width of element in byte.
            e: Index of element.
            kargs: Arguments to new element.
        """
        animate = read_elem(vector, color, size, index, **kwargs)
        self.register_animation(animate)
        return animate.dst_item_list[0]

    def move_elem(self,
                  elem: OneDimRegElem,
                  vector: OneDimReg,
                  size: float = -1.0,
                  index: int = 0):
        """
        Move element to register, add animate to list.

        Args:
            elem: Element object.
            vector: Register.
            size: Width of element in byte.
            e: Index of element.
        """
        animate = assign_elem(elem, vector, size, index)
        self.register_animation(animate)

    def counter_to_predicate(self,
                             png_obj: OneDimReg,
                             text: str,
                             color: Color,
                             width: int,
                             elements: int = 1,
                             **kwargs):
        """
        Animate of predict-as-counter to mask predicate.
        """
        animate = counter_to_predicate(png_obj, text, color, width, elements, **kwargs)
        self.register_animation(animate)
        return animate.dst_item_list[0]

    def concat_vector(self,
                      v1: OneDimReg,
                      v2: OneDimReg,
                      text: str,
                      color: Color,
                      **kwargs) -> OneDimReg:
        """
        Animate of vector concat.
        """
        animate = concat_vector(v1, v2, text, color, **kwargs)
        new_vector = animate.dst_item_list[0]

        if self.horizontal_coord < new_vector.get_max_boundary_width():
            self.horizontal_coord = new_vector.get_max_boundary_width()

        self.register_animation(animate)
        return new_vector

    def data_convert(self,
                     elem: OneDimRegElem,
                     color: Color,
                     size: float,
                     index: int,
                     **kwargs) -> OneDimRegElem:
        """
        Animate of data convert.
        """
        animate = data_convert(elem, color, size, index, **kwargs)
        self.register_animation(animate)
        return animate.dst_item_list[0]

    def function_call(self,
                      func: str,
                      color: Color,
                      size: float,
                      args: List[OneDimRegElem],
                      **kwargs) -> OneDimRegElem:
        """
        Animate of Function call.
        """
        func_kwargs = dict()
        if "args_value" in kwargs:
            func_kwargs["args_value"] = kwargs["args_value"]
            del kwargs["args_value"]

        if func in self.function_dict:
            func_obj = self.function_dict[func]
        else:
            animate_func = def_func_call(
                func=func,
                color=color,
                args_width=[x.get_elem_width() for x in args],
                res_width=size,
                **func_kwargs)

            func_obj : FunctionCall = animate_func.dst_item_list[0]
            self.function_dict[func] = func_obj

            func_obj.shift(DOWN * (self.vertical_coord + func_obj.func_height / 2))
            self.vertical_coord += func_obj.func_height + 1

            if self.horizontal_coord < func_obj.get_max_boundary_width():
                self.horizontal_coord = func_obj.get_max_boundary_width()

            self.register_animation(animate_func)

        animate = function_call(
            func=func_obj, args=args, color=color, width=size, **kwargs)
        self.register_animation(animate)
        return animate.dst_item_list[0]