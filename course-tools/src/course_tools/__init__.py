"""Course curriculum query tools backed by local JSON data.

This package contains two public entry points:

* ``course_chapter_lookup``: chapter and knowledge point lookup.
* ``course_prerequisite_lookup``: prerequisite and related-relation lookup.
"""

from .chapters import course_chapter_lookup
from .prerequisites import course_prerequisite_lookup

__all__ = [
    "course_chapter_lookup",
    "course_prerequisite_lookup",
]

