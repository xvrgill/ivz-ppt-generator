from abc import ABC, abstractmethod
from pptx.util import Inches, Pt
from os import path, chdir, getcwd, mkdir
import requests
from flask import abort

# todo: add type hints everywhere
class CreativeAssetStrategy(ABC):
    """Base class for creative asset strategies."""

    def __init__(self, detail_slide: object, creative_asset_data: dict) -> None:
        self.detail_slide = detail_slide
        self.creative_asset_data = creative_asset_data

    @abstractmethod
    def create_creative_asset_title_textbox(self) -> None:
        pass

    @staticmethod
    def download_creative_asset(creative_asset_details: dict) -> str:
        """Download creative asset from Air Table link and cache locally.

        Downloads creative asset with `requests.get` and caches it in the
        `api/videos` or `api/images` folders depending on the asset's fiile extension.
        """
        link_to_asset = creative_asset_details["url"]
        filename = link_to_asset.split("/")[-1]
        file_extension = filename.split(".")[1]
        accepted_image_types = ["jpg", "png", "gif", "raw", "svg", "heic"]
        accepted_video_types = ["mp4", "mov", "m4v", "mpg", "mpeg", "wmv"]
        current_dir = path.abspath(getcwd())

        if path.isdir("api/videos") is False:
            mkdir("api/videos")
        if path.isdir("api/images") is False:
            mkdir("api/images")

        if file_extension in accepted_image_types:
            chdir("api/images")
            cached_file_path: str = path.abspath(filename)
        elif file_extension in accepted_video_types:
            chdir("api/videos")
            cached_file_path: str = path.abspath(filename)

        data = requests.get(link_to_asset)

        with open(cached_file_path, "wb") as f:
            f.write(data.content)
            chdir(current_dir)

        return cached_file_path

    @abstractmethod
    def insert_creative(self) -> None:
        pass

    @abstractmethod
    def build_asset_layout(self) -> None:
        pass


class SingleAsset(CreativeAssetStrategy):
    """Strategy for laying out slide with single creative asset."""

    # inherited init includes: detail_slide, creative_asset_data: dict

    # Done!
    def create_creative_asset_title_textbox(self) -> None:
        """Create creative asset textbox as default."""
        # Text box positioning and size definitions
        # Insert creative asset as normal
        left = Inches(5.25)
        top = Inches(2.55)
        width = Inches(4.4)
        height = Inches(0.4)

        slide = self.detail_slide

        # Textbox setup
        account_tbox = slide.shapes.add_textbox(left, top, width, height)
        account_tf = account_tbox.text_frame
        # Adding bold text with run
        p = account_tf.paragraphs[0]
        # Bold run
        bold_run = p.add_run()
        bold_run.text = "Creative Asset:"
        bold_run_font = bold_run.font
        bold_run_font.bold = True
        bold_run_font.size = Pt(14)

    def insert_creative(self, path_to_asset: str):
        # Add creative asset file
        filename = path.basename(path_to_asset)
        file_extension = filename.split(".")[1]

        # throw error if pdf extension
        if file_extension == "pdf":
            return abort(404, "pdf is not an accepted Asset type. Please convert PDF to JPG")

        accepted_image_types = [
            "jpg",
            "png",
            "gif",
            "raw",
            "svg",
            "heic",
        ]
        accepted_video_types = ["mp4", "mov", "m4v", "mpg", "mpeg", "wmv"]

        # todo: throw error if asset doesn't match accepted types

        slide = self.detail_slide

        if file_extension in accepted_image_types:
            # Creative asset positioning and size definitions
            left = Inches(5.25)
            top = Inches(3.1)
            width = Inches(4.1)
            slide.shapes.add_picture(path_to_asset, left, top, width)
        elif file_extension in accepted_video_types:
            # todo: add video thumbnail
            # Creative asset positioning and size definitions
            left = Inches(5.25)
            top = Inches(3.1)
            width = Inches(4.1)
            height = Inches(3.1)
            slide.shapes.add_movie(path_to_asset, left, top, width, height)

    def build_asset_layout(self) -> None:
        # create title textbox
        self.create_creative_asset_title_textbox()
        # download creative asset - pass in only single post
        creative_asset_details: dict = self.creative_asset_data[0]
        cached_file_path = self.download_creative_asset(creative_asset_details)
        # insert creative asset - pass in path to file
        self.insert_creative(cached_file_path)
        # ? need to return the modified detail slide?
        # return self.detail_slide


class MultipleAssets(CreativeAssetStrategy):
    """Strategy for laying out slide with multiple creative assets."""

    # need to add asset counter to init method
    def __init__(self, detail_slide: object, creative_asset_data: dict, asset_counter: int) -> None:
        self.detail_slide = detail_slide
        self.creative_asset_data = creative_asset_data
        self.asset_counter = asset_counter

    def create_creative_asset_title_textbox(self, creative_asset_slide: object) -> None:
        """Create creative asset textbox as default."""
        #! Pass a mew slide and add it to that
        # Text box positioning and size definitions
        left = Inches(5.25)
        top = Inches(2.55)
        width = Inches(4.4)
        height = Inches(0.4)
        # Textbox setup
        account_tbox = creative_asset_slide.shapes.add_textbox(left, top, width, height)
        account_tf = account_tbox.text_frame
        # Adding bold text with run
        p = account_tf.paragraphs[0]
        # Bold run
        bold_run = p.add_run()
        bold_run.text = "Creative Asset:"
        bold_run_font = bold_run.font
        bold_run_font.bold = True

    def insert_creative(self, path_to_asset: str):
        # !Define rules for where each asset should go depending on it's position - tuple?
        # Add creative asset file
        filename = path.basename(path_to_asset)
        file_extension = filename.split(".")[1]

        # throw error if pdf extension
        if file_extension == "pdf":
            return abort(404, "pdf is not an accepted Asset type. Please convert PDF to JPG")

        accepted_image_types = [
            "jpg",
            "png",
            "gif",
            "raw",
            "svg",
            "heic",
        ]
        accepted_video_types = ["mp4", "mov", "m4v", "mpg", "mpeg", "wmv"]

        slide = self.detail_slide

        if file_extension in accepted_image_types:
            # Creative asset positioning and size definitions
            left = Inches(5.25)
            top = Inches(3.1)
            width = Inches(4.1)
            slide.shapes.add_picture(path_to_asset, left, top, width)
        elif file_extension in accepted_video_types:
            # Creative asset positioning and size definitions
            left = Inches(5.25)
            top = Inches(3.1)
            width = Inches(4.1)
            height = Inches(3.1)
            slide.shapes.add_movie(path_to_asset, left, top, width, height)

    def build_asset_layout(self) -> None:
        pass
