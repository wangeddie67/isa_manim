"""
Animation flow analysis.
"""

import itertools
import numpy as np
from typing import List, Tuple
from typing_extensions import Self
from manim import Animation, Mobject, FadeOut
from ..isa_objects import MemoryUnit

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
                 src: List[Mobject],
                 dst: List[Mobject],
                 dep: List[Mobject] = None,
                 add_before: List[Mobject] = None,
                 add_after: List[Mobject] = None,
                 rm_before: List[Mobject] = None,
                 rm_after: List[Mobject] = None
        ):
        """
        Construct one data structure for animate.

        Args:
            animate: One animation.
            src: Source Objects.
            dst: Destination Objects.
            dep: Dependency Objects.
            add_before: Objects to add before this animation.
            add_after: Objects to add after this animation.
            rm_before: Objects to remove before this animation.
            rm_after: Objects to remove after this animation.
        """
        # Convert None to [], Convert single item to list.
        def _regular_input_argument(arg):
            if isinstance(arg, list):
                return list(set(arg))
            elif arg is None:
                return []
            else:
                return [arg]

        self.animate: Animation = animate
        self.src_item_list: List[Mobject] = _regular_input_argument(src)
        self.dst_item_list: List[Mobject] = _regular_input_argument(dst)
        self.dep_item_list: List[Mobject] = _regular_input_argument(dep)
        self.add_before_list: List[Mobject] = _regular_input_argument(add_before)
        self.add_after_list: List[Mobject] = _regular_input_argument(add_after)
        self.rm_before_list: List[Mobject] = _regular_input_argument(rm_before)
        self.rm_after_list: List[Mobject] = _regular_input_argument(rm_after)

        self.predecessor_list: List[Self] = []
        self.successor_list: List[Self] = []

        if not self.src_item_list and not self.dst_item_list:
            raise ValueError("Animate should have either source or destination.")

    def is_beginner(self) -> bool:
        """
        Check whether this item is a beginner of a dependency chain.

        Returns:
            Return True if animate does not have source item.
        """
        return self.src_item_list is None or len(self.src_item_list) == 0

    def is_terminator(self) -> bool:
        """
        Check whether this item is a terminator of a dependency chain.

        Returns:
            Return True if animate does not have destination item.
        """
        return self.dst_item_list is None or len(self.dst_item_list) == 0

    def is_predecessor_of(self, post: Self) -> bool:
        """
        Check whether this item is predecessor of `post`. Successor `post` should play after this
        animation.

        Args:
            post: Another animation item.

        Returns:
            Return True if one of the destination item of this animation is also a source item of
                the `post` item.
        """
        for dst_item in self.dst_item_list:
            if dst_item in post.src_item_list:
                return True

        return False

    def is_successor_of(self, pre: Self) -> bool:
        """
        Check whether this item is successor of `pre`. Predecessor `pre` should play before this
        animation.

        Args:
            pre: Another animation item.

        Returns:
            Return True if one of the source item of this animation is also a destination item of
                the `pre` item.
        """
        for src_item in self.src_item_list:
            if src_item in pre.dst_item_list:
                return True

        return False

    def has_background(self, dep: Mobject) -> bool:
        """
        Check whether dep is background of this item. Background item should not change during this
        animation.
        
        Args:
            dep: Another manim object.

        Returns:
            Return true if `dep` is a dependency item of this animation.
        """
        return dep in self.dep_item_list

    def __str__(self) -> str:
        string = f"[Animate={str(self.animate)}, " + \
                 f"src={self.src_item_list}, " + \
                 f"dst={self.dst_item_list}, " + \
                 f"dep={self.dep_item_list}, " + \
                 f"predecessor={self.predecessor_list}]"
        return string

    def __repr__(self) -> str:
        string = f"[Animate={str(self.animate)}, " + \
                 f"src={self.src_item_list}, " + \
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
        keep_objects: List of objects that keep on scene between section.
    """

    def __init__(self,
                 animate_list: List[IsaAnimateItem],
                 wait: int = 0,
                 fade_out: bool = True,
                 camera_animate: Tuple[float, np.ndarray] = None,
                 keep_objects: List[Mobject] = None):

        self.animate_list: List[IsaAnimateItem] = animate_list
        self.wait: int = wait
        self.fade_out: bool = fade_out
        self.camera_animate: Tuple[float, np.ndarray] = camera_animate
        self.keep_objects: List[Mobject] = keep_objects

class _IsaAnimateStep():
    """
    One step of ISA Animation, which contains a set of animations that can play simultaneously.

    Attributes:
        animate_list: List of animation.
        wait: Wait time after this step. <=0 means no wait.
        camera_animate: Animation of move camera before this section, which is a tuple of one float
            and a position. The float provides the scaling of camera while position provides the
            new central position of camera.
        add_before: Objects to add before this animation.
        add_after: Objects to add after this animation.
        rm_before: Objects to remove before this animation.
        rm_after: Objects to remove after this animation.
    """

    def __init__(self,
                 animate_list: List[IsaAnimateItem],
                 wait: int = 0,
                 camera_animate: Tuple[float, np.ndarray] = None,
                 add_before: List[Mobject] = None,
                 add_after: List[Mobject] = None,
                 rm_before: List[Mobject] = None,
                 rm_after: List[Mobject] = None):

        self.animate_list: List[IsaAnimateItem] = animate_list
        self.wait: int = wait
        self.camera_animate: Tuple[float, np.ndarray] = camera_animate

        self.add_before: List[Mobject] = [] if add_before is None else add_before
        self.add_after: List[Mobject] = [] if add_after is None else add_after
        self.rm_before: List[Mobject] = [] if rm_before is None else rm_before
        self.rm_after: List[Mobject] = [] if rm_after is None else rm_after

class IsaAnimationFlow:
    """
    This class is used to analyse the order of animations.

    Attributes:
        isa_animation_section_list: List of ISA animation section, which contains a set of 
            animations.
        isa_animation_step_list: List of ISA step section, which contains a set of animations
            after analysis animation flow.
        _section_animate_list: List of animations after previous section, which will be packed into
            one section.
    """

    def __init__(self):
        self.animation_section_list: List[_IsaAnimateSection] = []
        self._animate_list: List[IsaAnimateItem] = []
        self.animation_step_list: List[_IsaAnimateStep] = []

    def add_animation(self,
                      animate: Animation,
                      src: List[Mobject],
                      dst: List[Mobject],
                      dep: List[Mobject] = None,
                      add_before: List[Mobject] = None,
                      add_after: List[Mobject] = None,
                      remove_before: List[Mobject] = None,
                      remove_after: List[Mobject] = None) -> IsaAnimateItem:
        """
        Register animation to scene and build dependency.

        Args:
            animate: One Manim animation.
            src: List of source objects of this animation.
            dst: List of destination objects of this animation.
            dep: List of dependency objects of this animation.
            add_before: List of objects to add into the scene before this animation.
            add_after: List of objects to add into the scene after this animation.
            remove_before: List of objects to remove from the scene before this animation.
            remove_after: List of objects to remove from the scene after this animation.

        Returns:
            Return an entity of data structure for animation flow analysis.
        """
        # Create animation flow data structure
        animate_item = IsaAnimateItem(animate, src, dst, dep,
                                      add_before, add_after, remove_before, remove_after)

        # Analysis dependency between this animation and existing animation.
        for item in self._animate_list:
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

        # Add this animation to the list of animation.
        self._animate_list.append(animate_item)

        return animate_item

    def switch_section(self,
                       wait: float = 0,
                       fade_out: bool = True,
                       camera_animate: Tuple[float, np.ndarray] = None,
                       keep_objects: List[Mobject] = None):
        """
        Switch animation section.

        Save registered animate to an animate section structure and clear animation list for next
        section.

        Args:
            wait: Seconds to wait before end of this section.
            fade_out: True means clear all items at the end of this section.
            camera_animate: Animate to scale/move camera.
            keep_objects: Objects keep on the scene between sections
        """
        # Create animation list.
        if len(self._animate_list) > 0:
            self.animation_section_list.append(_IsaAnimateSection(self._animate_list,
                                                                  wait=wait,
                                                                  fade_out=fade_out,
                                                                  camera_animate=camera_animate,
                                                                  keep_objects=keep_objects))
        # If two end_section subquently, intersection the defintion of them.
        elif len(self.animation_section_list) > 0:
            self.animation_section_list[-1].wait += wait
            self.animation_section_list[-1].fade_out |= fade_out
            new_keep_objects = []
            # Only objects appear in keep_objects of both end_section will keep.
            if self.animation_section_list[-1].keep_objects and keep_objects:
                for t_object in self.animation_section_list[-1].keep_objects:
                    if t_object in keep_objects:
                        new_keep_objects.append(t_object)
                self.animation_section_list[-1].keep_objects = new_keep_objects
            else:
                self.animation_section_list[-1].keep_objects = None

        self._animate_list = []

    def analysis_animation_flow(self):
        """
        Analysis the data flow and organize animations into several step.
        """
        # A list of objects on scene
        item_on_scene = []

        for animation_section in self.animation_section_list:
            iter_animate_list: List[IsaAnimateItem] = animation_section.animate_list

            first_step_in_section = True
            while len(iter_animate_list) > 0:

                # Holds animation items still has dependency
                new_iter_animate_list: List[IsaAnimateItem] = []
                # Holds animation items without dependency
                new_step_animate: List[IsaAnimateItem] = []
                # Distinguish items without/without dependency.
                for animate_item in iter_animate_list:
                    if len(animate_item.predecessor_list) == 0:
                        new_step_animate.append(animate_item)
                    else:
                        new_iter_animate_list.append(animate_item)

                assert len(new_step_animate) > 0

                # Update dependency of items.
                for left_item in new_iter_animate_list:
                    new_pre_item_list = []
                    for src_item in left_item.predecessor_list:
                        if src_item not in new_step_animate:
                            new_pre_item_list.append(src_item)
                    left_item.predecessor_list = new_pre_item_list

                # Updata the objects on scene
                # Remove the consumed source objects.
                for animate_item in new_step_animate:
                    for item in animate_item.src_item_list:
                        if item not in animate_item.dep_item_list:
                            if item in item_on_scene:
                                item_on_scene.remove(item)
                # Add the produced destination objects.
                for animate_item in new_step_animate:
                    for item in animate_item.dst_item_list:
                        if item not in item_on_scene:
                            item_on_scene.append(item)

                # The first step in each section will move/scale the camera.
                step_camera_animate = \
                    animation_section.camera_animate if first_step_in_section else None
                # Create data structure for animations step
                animation_step = _IsaAnimateStep(
                    animate_list=[item.animate for item in new_step_animate],
                    camera_animate=step_camera_animate,
                    add_before=itertools.chain.from_iterable(
                        [item.add_before_list for item in new_step_animate]),
                    add_after=itertools.chain.from_iterable(
                        [item.add_after_list for item in new_step_animate]),
                    rm_before=itertools.chain.from_iterable(
                        [item.rm_before_list for item in new_step_animate]),
                    rm_after=itertools.chain.from_iterable(
                        [item.rm_after_list for item in new_step_animate]))
                self.animation_step_list.append(animation_step)

                # Update left animation item for next iteration.
                iter_animate_list = new_iter_animate_list
                # Remove flag.
                first_step_in_section = False

            # The last step in each section will wait for next section.
            self.animation_step_list[-1].wait = animation_section.wait

            # Fade out items.
            if animation_section.fade_out:
                item_list = item_on_scene.copy()
                item_on_scene = []

                # Remove memory marks on memory unit as well.
                if animation_section.keep_objects is not None:
                    for item in animation_section.keep_objects:
                        if isinstance(item, MemoryUnit):
                            animation_section.keep_objects.extend(item.get_mem_mark_list())

                        if item in item_list:
                            item_list.remove(item)
                            item_on_scene.append(item)

                # Add one step to fade-out objects.
                if len(item_list) > 0:
                    self.animation_step_list.append(_IsaAnimateStep(
                        animate_list=[FadeOut(*item_list)]))
