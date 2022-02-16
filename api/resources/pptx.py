"""Resource that generates ppt from post group"""
# from api import app
from flask import send_file
from flask_restful import Resource
import requests
from os import path, mkdir
from typing import List, Optional
from api.context_managers.ppt_cm import PPTContextManager
from api.models.post_key_mappings import post_key_mappings as pkm
from scripts.ppt_generator import PowerPointGenerator
from api.resources.post_group import PostGroup
from api.resources.post import Post


class PPT(Resource):
    def get(self, id):
        ppt_data = dict()
        # post_group_url = api.url_for(PostGroup, id=id)
        post_group_response = PostGroup().get(id)
        # print(post_group_response)
        post_group_data = post_group_response.json

        ppt_data["group_name"] = post_group_data["fields"]["Name"]
        ppt_data["posts"] = list()

        for _id in post_group_data["fields"]["Linked Posts"]:
            # get data from post route
            # post_url = f"http://{root_url}/post/{str(_id)}"
            post_response = Post().get(_id)
            post_data = post_response.json
            # key mappings to make them more pythonic and uniform
            updated_post_data = {(pkm[k] if k in pkm else k): v for k, v in post_data["fields"].items()}
            # append dictionary of post data
            ppt_data["posts"].append(updated_post_data)

        # return ppt_data
        print(ppt_data)
        # Create the powerpoint with the collected data
        ppt = PowerPointGenerator()
        prs = ppt.create_presentation()
        asset_paths: List[Optional[str]] = list()
        for post in ppt_data["posts"]:
            asset_path = ppt.create_slide(prs, post)
            # If asset url is not none and the file name does not already exist in the list, append it
            if asset_path and (asset_path.split("/")[-1] not in asset_paths):
                asset_paths.append(asset_path.split("/")[-1])

        # Define absolute paths to the powerpoint file for easy reuse
        ppt_dir = path.abspath("power_points")
        ppt_path = path.join(ppt_dir, f'{ppt_data["group_name"]}.pptx')

        # Use coontext manager to save ppt and remove associated assets
        with PPTContextManager(prs, ppt_path, asset_paths) as f:
            if not path.isdir("api/powerpoints"):
                mkdir("api/powerpoints")
            f.save(ppt_path)
            return send_file(ppt_path)
