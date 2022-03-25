"""Resource that generates ppt from post group."""
from flask_restful import Resource
from flask import send_file
from os import path, mkdir
from api.context_managers.ppt_cm import PPTContextManager
from api.models.post_key_mappings import post_key_mappings as pkm
from scripts.ppt_generator import PowerPointGenerator
from api.resources.post_group import PostGroup
from api.resources.post import Post


class PPT(Resource):
    """Route that generates powerpoint.

    Methods available: `get`
    """

    def get(self, id):
        """Get method definition for ppt resource.

        Uses an Air Table post group to collect associated posts.

        :param id: unique ID of a social post group from Air Table
        :type id: string

        :return: returns a power point file to client in pptx format
        :rtype: `IO`
        """
        ppt_data = dict()
        post_group_response = PostGroup().get(id)
        post_group_data = post_group_response.json

        ppt_data["group_name"] = post_group_data["fields"]["Name"]
        ppt_data["posts"] = list()

        for _id in post_group_data["fields"]["Linked Posts"]:
            # get data from post resource w/o http
            post_response = Post().get(_id)
            post_data = post_response.json

            # key mappings to make them more pythonic and uniform
            updated_post_data = {(pkm[k] if k in pkm else k): v for k, v in post_data["fields"].items()}
            ppt_data["posts"].append(updated_post_data)

        # Define power point parameters
        ppt_filename = f'{ppt_data["group_name"]}'
        posts = ppt_data["posts"]

        # Create the powerpoint with the collected data
        ppt = PowerPointGenerator(posts, ppt_filename)

        # run generator
        ppt.run()

        # send the powerpoint file to client
        return ppt.send_to_client()

        # Working!
        # return send_file(
        #     f"power_points/{ppt_filename}.pptx",
        #     as_attachment=True,
        #     attachment_filename=f"power_points/{ppt_filename}.pptx",
        # )

        #! probably no longer need asset paths
        # asset_paths: List[Optional[str]] = list()
        # for post in ppt_data["posts"]:
        #     asset_path = ppt.create_slide(prs, post)
        #     if asset_path and (asset_path.split("/")[-1] not in asset_paths):
        #         asset_paths.append(asset_path.split("/")[-1])

        # ppt_filename = f'{ppt_data["group_name"]}.pptx'

        # # Use context manager to save ppt and remove associated assets
        # if not path.isdir("api/power_points"):
        #     mkdir("api/power_points")
        # with PPTContextManager(prs, ppt_filename) as f:
        #     f.save(f"api/power_points/{ppt_filename}")

        #     return send_file(
        #         f"power_points/{ppt_filename}",
        #         as_attachment=True,
        #         attachment_filename=ppt_filename,
        #     )
