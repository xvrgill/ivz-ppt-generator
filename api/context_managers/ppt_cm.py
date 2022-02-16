# Context manager to manage saved assets - images, videos, and ppt files on teardown
from typing import IO, List, Optional, Type
from os import remove
from os.path import exists


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
        for filename in self.asset_paths:
            if (filename.split(".")[1] in accepted_image_types) and exists(f"images/{filename}"):
                remove(f"images/{filename}")
                print(f"deleted: images/{filename}")
            elif (filename.split(".")[1] in accepted_video_types) and exists(f"videos/{filename}"):
                remove(f"videos/{filename}")
                print(f"deleted: videos/{filename}")
        print("done")
