"""Script that contains rudamentary logic for ppt generator."""

from pptx import Presentation
from flask import Response, abort, send_file
from api.strategies.slide_layout_strategy import Organic
from api.context_managers.ppt_cm import PPTContextManager
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

        :return: presentation object `pptx.Presentation()`
        :rtype: object
        """
        self.prs = Presentation()

    def create_slides(self):
        """Create slides for each post in the post group."""

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
                # todo: implement paid strategy here
                layout_strategy = Organic(self.prs, post)
                # use paid to create layout
                layout_strategy.build_layout()

    def save_ppt(self) -> None:
        # todo: reformat slashes in filename if they exist - will throw 'file not found error' if saved this way
        if not path.isdir("api/power_points"):
            mkdir("api/power_points")
        self.prs.save(f"api/power_points/{self.ppt_filename}.pptx")

    def build_and_save(self):
        """Build and save power point to cache folder."""
        # make new presentation instance
        self.create_presentation()
        # create slide(s)
        self.create_slides()
        # save power point presentation
        self.save_ppt()

    def send_to_client(self) -> Response:
        with PPTContextManager(self.prs, f"{self.ppt_filename}.pptx"):
            return send_file(f"power_points/{self.ppt_filename}.pptx", as_attachment=True, attachment_filename=f"{self.ppt_filename}.pptx")


if __name__ == "__main__":
    pass
