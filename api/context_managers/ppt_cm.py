# Context manager to manage saved assets - images, videos, and ppt files on teardown
from typing import IO, List, Optional, Type
from os import remove, chdir, getcwd
from os.path import exists, abspath

from flask_restplus import abort


class PPTContextManager:
    def __init__(self, presentation, ppt_path, asset_paths) -> None:
        self.presentation = presentation
        self.ppt_path = ppt_path
        self.asset_paths = asset_paths

    def __enter__(self):
        # ? --- maybe use a tempfile here instead of writing to disk? --- ?#
        return self.presentation

    def __exit__(self, exc_type, exec_val, traceback) -> None:
        # delete the file
        remove(self.ppt_path)
        # delete the assets from their respective folders depending on asset type
        accepted_image_types = ["jpg", "png", "gif", "raw", "svg", "heic"]
        accepted_video_types = ["mp4", "mov", "m4v", "mpg", "mpeg", "wmv"]
        print(self.asset_paths)
        current_dir = abspath(getcwd())
        for filename in self.asset_paths:
            try:
                if (filename.split(".")[1] in accepted_image_types) and exists(f"images/{filename}"):
                    chdir("api/images")
                    remove(filename)
                    print(f"deleted: api/videos/{filename}")
                elif (filename.split(".")[1] in accepted_video_types) and exists(f"videos/{filename}"):
                    chdir("api/videos")
                    remove(filename)
                    print(f"deleted: api/videos/{filename}")
            except ValueError as e:
                return abort(400, "Asset is not of an accepted format", asset=filename, error=e.message)
            finally:
                chdir(current_dir)
