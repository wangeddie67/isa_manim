"""
ISA scene with single instruction.
"""

from typing import Union, Tuple
import numpy as np
from manim import logger
from manim import (Text,
                   ORIGIN, UP, DOWN, RIGHT,
                   ZoomedScene,
                   BLACK,
                   config)
from .isa_data_flow import IsaDataFlow

config.frame_height = 9
config.frame_width = 16

class SingleIsaScene(ZoomedScene, IsaDataFlow):
    """
    ISA scene with single instructions.

    Attributes:
        camera_scale_rate: scale factor of zoomed camera.
        camera_origin: origin of zoomed camera.
    """

    def __init__(self, **kwargs):
        """
        Construct scene.
        """
        ZoomedScene.__init__(
            self,
            zoom_factor=1.0,
            zoomed_display_height=config.frame_height / 2 + 3,
            zoomed_display_width=config.frame_width,
            zoomed_display_center=DOWN * ((config.frame_height / 2 - 3) / 2),
            image_frame_stroke_width=0,
            zoomed_camera_config={
                "background_opacity": 1,
                "default_frame_stroke_width": 0,
                },
            **kwargs
        )
        IsaDataFlow.__init__(self)

        self.camera_scale_rate: float = 1.0
        self.camera_origin: np.array = ORIGIN

    def construct(self):
        """
        Construct animation.
        """
        self.construct_isa_flow()

        self.zoomed_display.display_frame.set_color(BLACK)
        self.zoomed_camera.frame.move_to(DOWN * ((config.frame_height / 2 - 2) / 2))

        self.activate_zooming()

        msg = f"Register {len(self.isa_animation_section_list)} sections."
        logger.info(msg)

        # Analysis flow
        self.analysis_animation_flow()
        msg = f"Register {len(self.isa_animation_step_list)} steps."
        logger.info(msg)

        # Play flow
        # Play each section
        for animation_step in self.isa_animation_step_list:
            # Update camera to hold section.
            if animation_step.camera_animate:
                camera_ratio = animation_step.camera_animate[0]
                camera_target = animation_step.camera_animate[1]
                self.play(self.zoomed_camera.frame.animate.scale(camera_ratio)
                          .move_to(camera_target))

            # Play each step in section.
            self.remove(*animation_step.remove_before)
            self.add(*animation_step.add_before)
            self.play(*animation_step.animate_list)
            self.remove(*animation_step.remove_after)
            self.add(*animation_step.add_after)

            # Wait after animation.
            if animation_step.wait > 0:
                self.wait(animation_step.wait)

    def construct_isa_flow(self):
        """
        Construct ISA flow. Rewrite in inherited class.
        """
        pass

    def draw_title(self, title: str):
        """
        Draw title.

        Args:
            title: String of title.
        """
        title_obj = Text(title, font_size=35).move_to(UP * 3.5)
        self.add(title_obj)

    def end_section(self,
                    wait: int = 1,
                    fade_out: bool = True):
        """
        Terminate or temporary stop of section, and update camera.

        Args:
            wait: Time of wait before end of section.
            fade_out: True means fade_out all items on scene except always-on items.
        """
        camera_animate = self._update_camera()
        self.switch_section(wait=wait,
                            fade_out=fade_out,
                            camera_animate=camera_animate)

        self.elem_source_dict.clear()

    def _update_camera(self) -> Union[Tuple[float, np.array], None]:
        """
        Update location and scale factor of zoomed camera.

        If no update, return None. Otherwise, return a tuple of scaling factor and new location.
        The returned scaling factor the ratio of new scaling factor and old scaling factor.
        """
        zoomed_frame_width = self.placement_width()
        zoomed_frame_scale = \
            self.placement_scale(self.zoomed_display_width, self.zoomed_display_height)

        zoomed_frame_origin_x = zoomed_frame_width / 2
        zoomed_frame_origin_y = (self.zoomed_display_height * zoomed_frame_scale) / 2
        zoomed_frame_origin = RIGHT * zoomed_frame_origin_x + DOWN * zoomed_frame_origin_y

        if abs(zoomed_frame_scale - self.camera_scale_rate) > 1e-3 \
                or abs(zoomed_frame_origin[0] - self.camera_origin[0]) > 1e-3 \
                or abs(zoomed_frame_origin[1] - self.camera_origin[1]) > 1e-3 :
            temp_frame_scale = zoomed_frame_scale / self.camera_scale_rate
            self.camera_scale_rate = zoomed_frame_scale
            self.camera_origin = zoomed_frame_origin

            return [temp_frame_scale, zoomed_frame_origin]
        else:
            return None
