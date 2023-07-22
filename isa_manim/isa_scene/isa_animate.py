"""
Define data structure for animate for dependency analysis.
"""

from typing import List, Any
from manim import Animation

class IsaAnimate:
    """
    Data structure for animate for dependency analysis.

    Attributes:
        animate: Animate
        src_item_list: source items
        dst_item_list: destination items
        dep_item_list: dependency items

        predecessor_list: predecessor animate list
        successor_list: successor animate list
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
            animate: Animation, AnimationGroup
            src: Source item.
            dst: Destination item.
            dep: Dependency item.
        """
        self.animate = animate

        if isinstance(src, list):
            self.src_item_list = src
        elif src is None:
            self.src_item_list = []
        else:
            self.src_item_list = [src]

        if isinstance(dst, list):
            self.dst_item_list = dst
        elif dst is None:
            self.dst_item_list = []
        else:
            self.dst_item_list = [dst]

        if isinstance(dep, list):
            self.dep_item_list = dep
        elif dep is None:
            self.dep_item_list = []
        else:
            self.dep_item_list = [dep]

        self.predecessor_list = []
        self.successor_list = []

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
