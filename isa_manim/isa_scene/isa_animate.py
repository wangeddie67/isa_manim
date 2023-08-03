"""
Animation flow analysis.
"""

import numpy as np
from typing import List, Tuple, Union, Any
from manim import Animation, Mobject, FadeOut

class IsaAnimateItem:
    """
    Data structure for animate for dependency analysis.

    It contains the list of source items and destination items of one item, which can conclude the
    dependency of animations.

    It also has a list of dependency items, which must be maintained in scene during this animation.

    Attributes:
        animate: Animate
        src_item_list: List of source items.
        dst_item_list: List of destination items.
        dep_item_list: List of dependency items.

        predecessor_list: List of predecessor animates.
        successor_list: List of successor animates.
    """

    def __init__(self,
                 animate: Animation,
                 src: List[Any],
                 dst: List[Any],
                 dep: List[Any] = None
        ):
        """
        Construct one data structure for animate.

        Args:
            animate: One animation.
            src: Source items.
            dst: Destination items.
            dep: Dependency items.
        """
        self.animate = animate

        # Add source object.
        if isinstance(src, list):
            self.src_item_list = src
        elif src is None:
            self.src_item_list = []
        else:
            self.src_item_list = [src]

        # Add destination object.
        if isinstance(dst, list):
            self.dst_item_list = dst
        elif dst is None:
            self.dst_item_list = []
        else:
            self.dst_item_list = [dst]

        # Add dependency object.
        if isinstance(dep, list):
            self.dep_item_list = dep
        elif dep is None:
            self.dep_item_list = []
        else:
            self.dep_item_list = [dep]

        self.predecessor_list = []
        self.successor_list = []

        self.copy_list = []

        if not self.src_item_list and not self.dst_item_list:
            raise ValueError("Animate should have either source or destination.")

    def is_beginner(self):
        """
        Check whether this item is the beginner.
        Return True if animate does not have source item.
        """
        return self.src_item_list is None or self.src_item_list == []

    def is_terminator(self):
        """
        Check whether this item is the beginner.
        Return True if animate does not have destination item.
        """
        return self.dst_item_list is None or self.dst_item_list == []

    def is_predecessor_of(self, post):
        """
        Check whether this item is predecessor of post.
        Successor should play after this animation.
        """
        for dst_item in self.dst_item_list:
            if dst_item in post.src_item_list:
                return True

        return False

    def is_successor_of(self, pre):
        """
        Check whether this item is successor of pre.
        Predecessor should play before this animation.
        """
        for src_item in self.src_item_list:
            if src_item in pre.dst_item_list:
                return True

        return False

    def has_background(self, dep):
        """
        Check whether dep is background of this item.
        Background item should not change during this animation.
        """
        return dep in self.dep_item_list

    def add_copy_item(self, copy_item):
        """
        Add copy item.
        """
        self.copy_list.append(copy_item)

    def __str__(self) -> str:
        string = f"[Animate={str(self.animate)}, " + \
                 f"src={str(self.src_item_list)}, " + \
                 f"dst={self.dst_item_list}, " + \
                 f"dep={self.dep_item_list}, " + \
                 f"predecessor={self.predecessor_list}]"
        return string

    def __repr__(self) -> str:
        string = f"[Animate={str(self.animate)}, " + \
                 f"src={str(self.src_item_list)}, " + \
                 f"dst={self.dst_item_list}, " + \
                 f"dep={self.dep_item_list}, " + \
                 f"predecessor={self.predecessor_list}]"
        return string

class _IsaAnimateSection():
    """
    One section of ISA Animation.

    Attributes:
        animate_list: List of animation.
        wait: Wait time after this section. <=0 means no wait.
        fade_out: Whether fade out left items after this section.
        camera_animate: Animation of move camera before this section, which is a tuple of one float
            and a position. The float provides the scaling of camera while position provides the
            new central position of camera.
    """

    def __init__(self,
                 animate_list: List[IsaAnimateItem],
                 wait: int = 0,
                 fade_out: bool = True,
                 camera_animate: Tuple[float, np.ndarray] = None):

        self.animate_list = animate_list
        self.wait = wait
        self.fade_out = fade_out
        self.camera_animate = camera_animate

class _IsaAnimateStep():
    """
    One step of ISA Animation, which contains a set of animations that can play simultaneously.

    Attributes:
        animate_list: List of animation.
        left_item_list: List of items that still in scene.
        wait: Wait time after this step. <=0 means no wait.
        camera_animate: Animation of move camera before this section, which is a tuple of one float
            and a position. The float provides the scaling of camera while position provides the
            new central position of camera.
    """

    def __init__(self,
                 animate_list: List[IsaAnimateItem],
                 left_item_list: List[Mobject],
                 wait: int = 0,
                 camera_animate: Tuple[float, np.ndarray] = None):

        self.animate_list = animate_list
        self.left_item_list = left_item_list
        self.wait = wait
        self.camera_animate = camera_animate

class IsaAnimationMap:
    """
    This class is used to analyse the order of animations.

    Attributes:
        isa_animation_section_list: List of ISA animation section, which contains a set of 
            animations.
        isa_animation_step_list: List of ISA step section, which contains a set of animations
            after analysis animation flow.
        _section_animate_list: List of animations after previous section, which will be packed into
            one section.
        always_on_item_list: List of items that will not be faded out between section.
    """

    def __init__(self):
        self.isa_animation_section_list: List[_IsaAnimateSection] = []
        self._section_animate_list: List[IsaAnimateItem] = []
        self.always_on_item_list: List[Mobject] = []
        self.isa_animation_step_list: List[_IsaAnimateStep] = []

    def register_always_on_item(self, item: Mobject):
        """
        Register one always-on item, which will not fade out when switch section.

        Args:
            item: Mobject to register.
        """
        self.always_on_item_list.append(item)

    def animation_add_animation(self,
                                animate: Animation,
                                src: List[Any],
                                dst: List[Any],
                                dep: List[Any] = None) -> IsaAnimateItem:
        """
        Register animation to scene and build dependency.

        Args:
            animate: IsaAnimateItem or a list of IsaAnimateItem.
        """
        animate_item = IsaAnimateItem(animate, src, dst, dep)

        for item in self._section_animate_list:
            # new animate is successor of one existed item.
            if animate_item.is_successor_of(item):
                animate_item.predecessor_list.append(item)
                item.successor_list.append(animate_item)
            # new animate is predecessor of one existed item.
            if animate_item.is_predecessor_of(item):
                animate_item.successor_list.append(item)
                item.predecessor_list.append(animate_item)

            # serialization dependency.
            for dep_item in animate_item.dep_item_list:
                if not dep_item.require_serialization:
                    continue

                # new animate is successor of one existed item.
                if item.has_background(dep_item):
                    animate_item.predecessor_list.append(item)
                    item.successor_list.append(animate_item)

        self._section_animate_list.append(animate_item)

        return animate_item

    def switch_section(self,
                       wait: float = 0,
                       fade_out: bool = True,
                       camera_animate: Tuple[float, np.ndarray] = None):
        """
        Switch section. Save registered animate to an animate section and clear animation list.

        Args:
            wait: Seconds to wait before end of this section.
            fade_out: Clear all items at the send of this section.
            camera_animate: Animate to scale/move camera.
        """
        if len(self._section_animate_list) > 0:
            self.isa_animation_section_list.append(
                _IsaAnimateSection(
                    animate_list=self._section_animate_list,
                    wait=wait,
                    fade_out=fade_out,
                    camera_animate=camera_animate))

        self._section_animate_list = []

    def analysis_animation_flow(self):
        """
        Analysis the data flow and organize animations into several step.

        Args:
            bg_items: Items left from previous section.

        Returns:
            Left items to next section.
        """
        step_item = []

        for animation_section in self.isa_animation_section_list:
            iter_animate_list: List[IsaAnimateItem] = animation_section.animate_list

            first_step_in_section = True
            while len(iter_animate_list) > 0:

                new_iter_animate_list: List[IsaAnimateItem] = []
                new_step_animate: List[IsaAnimateItem] = []

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
                step_camera_animate = \
                    animation_section.camera_animate if first_step_in_section else None
                self.isa_animation_step_list.append(_IsaAnimateStep(
                    animate_list=[item.animate for item in new_step_animate],
                    left_item_list=step_item.copy(),
                    camera_animate=step_camera_animate))

                first_step_in_section = False

            # Wait after step
            self.isa_animation_step_list[-1].wait = animation_section.wait

            # Fade out
            if animation_section.fade_out:
                item_list = step_item.copy()
                step_item = []
                # filter out always-on item.
                for item in self.always_on_item_list:
                    if item in item_list:
                        item_list.remove(item)
                        step_item.add(item)
                if len(item_list) > 0:
                    self.isa_animation_step_list.append(_IsaAnimateStep(
                        animate_list=[FadeOut(*item_list)],
                        left_item_list=step_item.copy()))

