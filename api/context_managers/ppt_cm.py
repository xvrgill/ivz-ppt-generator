# Context manager to manage saved assets - images, videos, and ppt files on teardown
from os.path import isdir
from shutil import rmtree


class PPTContextManager:
    def __init__(self, presentation, ppt_filename) -> None:
        self.presentation = presentation
        self.ppt_filename = ppt_filename

    def __enter__(self):
        # ? --- maybe use a tempfile here instead of writing to disk? --- ?#
        return self.presentation

    def __exit__(self, exc_type, exec_val, traceback) -> None:
        # ! Development paths - not to be used in production
        # remove(f"api/power_points/{self.ppt_filename}")
        if isdir("api/power_points"):
            rmtree("api/power_points")
        if isdir("api/images"):
            rmtree("api/images")
        if isdir("api/videos"):
            rmtree("api/videos")
        # ! Production paths - to be used in production
        # if isdir("app/images"):
        #     rmtree("app/images")
        # if isdir("app/videos"):
        #     rmtree("app/videos")
        # remove(f"app/power_points/{self.ppt_filename}")
