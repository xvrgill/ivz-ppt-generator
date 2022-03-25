"""Context manager to manage images, videos, and ppt files on teardown."""

from os.path import isdir
from shutil import rmtree


class PPTContextManager:
    """Context manager for managing send of ppt to client.

    This is a context manager class that automatically deletes
    cached files on :method:``__exit__``

    :param presentation: an instance of a presentation object
    :param ppt_filename: filename used to save pptx file
    :type presentation: object
    :type ppt_filename: str
    :return: object
    """

    def __init__(self, presentation, ppt_filename) -> None:
        """Initialize context."""
        self.presentation = presentation
        self.ppt_filename = ppt_filename

    def __enter__(self) -> object:
        """Make presentation object accessible in context."""
        return self.presentation

    def __exit__(self, exc_type, exec_val, traceback) -> None:
        """Teardown context by clearing cached assets."""
        if isdir("api/power_points"):
            rmtree("api/power_points")
        if isdir("api/images"):
            rmtree("api/images")
        if isdir("api/videos"):
            rmtree("api/videos")
