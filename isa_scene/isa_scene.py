
from typing import List, Union, Tuple
import numpy as np
from manim import logger
from manim import Mobject
from manim import FadeOut
from manim import MovingCameraScene, MovingCamera
from ..isa_animate import IsaAnimate

class _IsaAnimateSection():
    """
    This scene is used for those instruction with neither arithmetic/logic
    operation nor load/store operation.
    For example:
    - move instruction.
    - shuffle instruction.
    - data convert instruction.
    """

    def __init__(self,
                 animate_list: List[IsaAnimate],
                 wait: int = 0,
                 fade_out: bool = True,
                 camera_animate: Tuple[float, np.ndarray] = None):

        self.animate_list = animate_list
        self.wait = wait
        self.fade_out = fade_out
        self.camera_animate = camera_animate

        self.step_animate_list = []
        self.step_item_list = []

    def analysis_flow(self,
                      bg_items: List[Mobject] = []) -> List[Mobject]:
        """
        Analysis the data flow and organize animations into several step.

        Args:
            bg_items: Items left from previous section.

        Returns:
            Left items to next section.
        """
        iter_animate_list: List[IsaAnimate] = self.animate_list

        self.step_animate_list = []
        self.step_item_list = []
        step_item = bg_items

        while len(iter_animate_list) > 0:

            new_iter_animate_list: List[IsaAnimate] = []
            new_step_animate: List[IsaAnimate] = []

            # Find all items without dependency.
            for animate_item in iter_animate_list:
                if len(animate_item.predecessor_list) == 0:
                    new_step_animate.append(animate_item)
                else:
                    new_iter_animate_list.append(animate_item)

            assert len(new_step_animate) > 0

            # Update dependency.
            for left_item in new_iter_animate_list:
                new_pre_item_list = []
                for src_item in left_item.predecessor_list:
                    if src_item not in new_step_animate:
                        new_pre_item_list.append(src_item)
                left_item.predecessor_list = new_pre_item_list

            # Calculate left items.
            for animate_item in new_step_animate:
                for item in animate_item.src_item_list:
                    if item not in animate_item.dep_item_list:
                        if item in step_item:
                            step_item.remove(item)
            for animate_item in new_step_animate:
                for item in animate_item.dst_item_list:
                    if item not in step_item:
                        step_item.append(item)

            # Iterate loop
            iter_animate_list = new_iter_animate_list
            self.step_animate_list.append(new_step_animate)
            self.step_item_list.append(step_item.copy())

        return [] if self.fade_out else step_item


class IsaScene(MovingCameraScene):
    """
    This scene is used for those instruction with neither arithmetic/logic
    operation nor load/store operation.
    For example:
    - move instruction.
    - shuffle instruction.
    - data convert instruction.
    """

    def __init__(self, camera_class=MovingCamera, **kwargs):
        super().__init__(camera_class=camera_class, **kwargs)

        self._isa_flow_section_list: List[_IsaAnimateSection] = []
        self._section_animate_list: List[IsaAnimate] = []
        self._always_on_item_list: List[Mobject] = []

    def construct(self):
        """
        Construct animation.
        """
        self.construct_isa_flow()

        msg = f"Register {len(self._isa_flow_section_list)} sections."
        logger.info(msg)

        # Analysis flow
        left_item = []
        for section in self._isa_flow_section_list:
            left_item = section.analysis_flow(left_item)

        # Play flow
        # Play each section
        for section in self._isa_flow_section_list:
            # Update camera to hold section.
            if section.camera_animate:
                camera_ratio = section.camera_animate[0]
                camera_target = section.camera_animate[1]
                self.play(self.camera.frame.animate.scale(camera_ratio)
                          .move_to(camera_target))

            # Play each step in section.
            for animate_list in section.step_animate_list:
                animate_list = [x.animate for x in animate_list]
                self.play(*animate_list)

            if section.wait > 0:
                self.wait(section.wait)

            # Remove all elements left in such section.
            if section.fade_out:
                item_list = section.step_item_list[-1]
                # filter out always-on item.
                for item in self._always_on_item_list:
                    if item in item_list:
                        item_list.remove(item)
                if len(item_list) > 0:
                    self.play(FadeOut(*item_list))

    def construct_isa_flow(self):
        """
        Construct ISA flow. Rewrite in inherited class.
        """
        pass

    def register_always_on_item(self, item: Mobject):
        """
        Register one always-on item, which will not fade out when switch section.

        Args:
            item: Mobject to register.
        """
        self._always_on_item_list.append(item)

    def _register_animation(self,
                            animate: IsaAnimate):
        """
        Register animation to scene and build dependency.

        Args:
            animate
        """
        for item in self._section_animate_list:
            # new animate is predecessor of one existed item.
            if animate.is_predecessor(item):
                animate.predecessor_list.append(item)
                item.successor_list.append(animate)
            # new animate is successor of one existed item.
            if animate.is_successor(item):
                animate.successor_list.append(item)
                item.predecessor_list.append(animate)

        self._section_animate_list.append(animate)

    def register_animation(self,
                           animate: Union[IsaAnimate, List[IsaAnimate]]):
        """
        Register animation to scene.

        Args:
            animate: IsaAnimate of a list of IsaAnimate.
        """
        if isinstance(animate, list):
            for item in animate:
                if not isinstance(item, IsaAnimate):
                    raise ValueError(
                        "Arguments must be IsaAnimate or a list of IsaAnimate.")
                else:
                    self._register_animation(item)
        elif isinstance(animate, IsaAnimate):
            self._register_animation(animate)
        else:
            raise ValueError(
                "Arguments must be IsaAnimate or a list of IsaAnimate.")

    def switch_section(self,
                       wait: int = 0,
                       fade_out: bool = True,
                       camera_animate: Tuple[float, np.ndarray] = None):
        """
        Switch section. Save registered animate to an animate section and clear
        animation list.

        Args:
            wait: Seconds to wait before end of this section.
            fade_out: Clear all items at the send of this section.
            camera_animate: Animate to scale/move camera.
        """
        if len(self._section_animate_list) > 0:
            self._isa_flow_section_list.append(
                _IsaAnimateSection(
                    animate_list=self._section_animate_list,
                    wait=wait,
                    fade_out=fade_out,
                    camera_animate=camera_animate))

        self._section_animate_list = []
