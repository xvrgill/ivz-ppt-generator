"""Script that contains rudamentary logic for ppt generator."""

# Import ppt package
from typing import Union
from pptx import Presentation

# move to strategy
from flask import Response, abort, send_file

# import strategies
from api.strategies.slide_layout_strategy import Organic

# import context manager
from api.context_managers.ppt_cm import PPTContextManager

# import IO operations
from os import mkdir, path

# Todo: Add Paid/Organic and Paid Headline elements
# Todo: Enable multiple creative assets to be added for each post if required
# Todo: Convert PDF files to jpgs if they are given


class PowerPointGenerator:
    """Object for creating power points."""

    # todo: create init that takes in post data
    def __init__(self, posts: list, ppt_filename: str) -> None:
        self.posts = posts
        self.ppt_filename = ppt_filename

    def create_presentation(self):
        """Create *presentation* object.

        :returns
        """
        self.prs = Presentation()

    # def create_slides(self):

    #     blank_slide_layout = self.prs.slide_layouts[6]
    #     for post in self.posts:
    #         self.prs.slides.add_slide(blank_slide_layout)

    def create_slides(self):

        # ensure that strategy is either paid or organic - handle errors accordingly
        for post in self.posts:
            try:
                paid_v_organic: str = post["paid_v_organic"]
                assert paid_v_organic == "organic" or "paid"
            except (KeyError):
                return abort(500, "No paid or organic status supplied for a post in this post group. Ensure that all posts are identified as either paid or organic.")
            except (AssertionError):
                return abort(
                    500,
                    f"Unable to process a post with Paid v Organic status of {paid_v_organic}. Ensure that this field is either paid or organic. If a new option has been added to Air Table, please contact the system administrator to enable processing of the new option {paid_v_organic}",
                )

            # choose strategy - must be either paid or organic now that we validated with try block
            if paid_v_organic == "organic":
                # implement organic strategy here
                layout_strategy = Organic(self.prs, post)
                # use strategy to create layout
                layout_strategy.build_layout()
                # return layout_strategy.presentation
            else:
                # implement organic strategy here
                layout_strategy = Organic(self.prs, post)
                # use strategy to create layout
                layout_strategy.build_layout()

        # use strategy to create layout
        # layout_strategy.build_layout()

    def save_ppt(self) -> None:
        # todo: reformat slashes in filename if they exist - will throw 'file not found error' if saved this way
        if not path.isdir("api/power_points"):
            mkdir("api/power_points")
        self.prs.save(f"api/power_points/{self.ppt_filename}.pptx")

    def build_and_save(self):

        # make new presentation instance
        self.create_presentation()
        # create slide(s)
        self.create_slides()
        # save power point presentation
        self.save_ppt()

    def run(self):
        self.build_and_save()
        self.save_ppt()

    def send_to_client(self) -> Response:
        with PPTContextManager(self.prs, f"{self.ppt_filename}.pptx"):
            return send_file(f"power_points/{self.ppt_filename}.pptx", as_attachment=True, attachment_filename=f"{self.ppt_filename}.pptx")

    # #! replace contents of method with strategy logic
    # #! this will run in a for loop - construct as if only one post is passed in at a time [May not work]
    # def create_slides(self, prs, post: dict):
    #     """
    #     Creates a blank slide and adds the elements required for compliance to it.

    #     Args:
    #         prs (Type[Presentation]): _description_
    #         post_data (dict): _description_
    #     """
    #     # ensure that strategy is either paid or organic - handle errors accordingly
    #     try:
    #         paid_v_organic: str = post["paid_v_organic"]
    #         assert paid_v_organic == "organic" or "paid"
    #     except (KeyError):
    #         return abort(500, "No paid or organic status supplied for a post in this post group. Ensure that all posts are identified as either paid or organic.")
    #     except (AssertionError):
    #         return abort(
    #             500,
    #             f"Unable to process a post with Paid v Organic status of {paid_v_organic}. Ensure that this field is either paid or organic. If a new option has been added to Air Table, please contact the system administrator to enable processing of the new option {paid_v_organic}",
    #         )

    #     # choose strategy - must be either paid or organic now that we validated with try block
    #     if paid_v_organic == "organic":
    #         # implement organic strategy here
    #         layout_strategy = Organic(prs, post)
    #         # use strategy to create layout
    #         layout_strategy.build_layout()
    #         return layout_strategy.presentation
    #     else:
    #         # implement organic strategy here
    #         layout_strategy = Organic(prs, post)
    #         # use strategy to create layout
    #         layout_strategy.build_layout()
    #         return layout_strategy.presentation

    # use strategy to create layout
    # layout_strategy.build_layout()

    # # save the power point - filename should be the post group name
    # @staticmethod
    # def save_ppt(prs, ppt_filename: str) -> None:
    #     # reformat slashes in filename if they exist - will throw 'file not found error' if saved this way
    #     # todo: use ppt context manager to implement tear down logic
    #     # if not path.isdir("api/powerpoints"):
    #     #     mkdir("api/power_points")
    #     prs.save(f"api/power_points/{ppt_filename}.pptx")

    # # todo: create function that generates ppt file
    # def build_and_save(self, posts: dict, ppt_filename: str):

    #     # make new presentation instance
    #     self.create_presentation()

    #     # create slide(s)
    #     #! update presentation whenever slides are created
    #     for post in posts:
    #         result = self.create_slides(self.prs, post)
    #         self.prs = result

    #     # save power point presentation
    #     self.save_ppt(self.prs, ppt_filename)

    # # todo: create cunction that sends ppt to client
    # @staticmethod
    # def send_to_client(ppt_filename: str) -> Response:
    #     return send_file(f"power_points/{ppt_filename}.pptx", as_attachment=True, attachment_filename=ppt_filename)

    # # todo: create function that completes the entire process in one call
    # def process(self) -> Response:

    #     # generate full power point
    #     self.build_and_save(self.posts, self.ppt_filename)

    #     # send power point to client
    #     self.send_to_client(self.ppt_filename)


if __name__ == "__main__":
    pass
