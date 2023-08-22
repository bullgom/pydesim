from . import base_parent, child


class Parent(base_parent._BaseParent):
    _children: list[child.Child]
    _imminent_children: list[child.Child]

    def adopt(self, *child: child.Child) -> None:
        self._children.extend(child)