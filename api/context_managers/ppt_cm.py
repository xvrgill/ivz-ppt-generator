# Context manager to manage saved assets - images, videos, and ppt files on teardown
from genericpath import isdir
from posixpath import relpath
from typing import List, Optional, Type
from os import remove, chdir, getcwd, rmdir
from os.path import exists, abspath, join, isdir
from shutil import rmtree

from flask_restplus import abort


class PPTContextManager:
    def __init__(self, presentation, ppt_filename, asset_filenames: List[str]) -> None:
        self.presentation = presentation
        self.ppt_filename = ppt_filename
        self.asset_filenames = asset_filenames

    def __enter__(self):
        # ? --- maybe use a tempfile here instead of writing to disk? --- ?#
        return self.presentation

    def __exit__(self, exc_type, exec_val, traceback) -> None:
        # save current directoy of instance call for use later
        # current_dir = abspath(getcwd())
        # change to the ppt directory for file removal in exit
        # chdir("api/power_points")
        # print("current directory after trying to change to ppt dir: " + getcwd())
        # delete the ppt file with passed filename
        remove(f"api/power_points/{self.ppt_filename}")
        # chdir(current_dir)
        # delete the assets from their respective folders depending on asset type
        accepted_image_types = ["jpg", "png", "gif", "raw", "svg", "heic"]
        accepted_video_types = ["mp4", "mov", "m4v", "mpg", "mpeg", "wmv"]

        if isdir("api/images"):
            rmtree("api/images")
        if isdir("api/videos"):
            rmtree("api/videos")

        # for filename in self.asset_filenames:
        #     try:
        #         if (filename.split(".")[1] in accepted_image_types) and exists(f"api/images/{filename}"):
        #             #! Development path
        #             # chdir("api/images")
        #             # remove(filename)

        #             #! Development path
        #             print(f"deleted: api/images/{filename}")
        #         elif (filename.split(".")[1] in accepted_video_types) and exists(f"api/videos/{filename}"):
        #             #! Development path
        #             # chdir("api/videos")
        #             # remove(filename)
        #             #! Development path
        #             print(f"deleted: api/videos/{filename}")
        #     except ValueError as e:
        #         return abort(400, "Asset is not of an accepted format", asset=filename, error=e.message)
        #     finally:
        #         if isdir("api/images"):
        #             rmtree("api/images")
        #         if isdir("api/videos"):
        #             rmtree("api/videos")
