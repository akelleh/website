import json
from auth import get_client
import logging
import os

class ImgurPoster(object):
    def __init__(self):
        self.client = get_client()

    def create_album(self, path):

        target = path.split('/')[-1]

        with open(os.path.join(path, target + '.json'), 'r') as fp:
            post = json.loads(fp.read())
        album_fields = {"title": target,
                        "description": '',
                        "privacy": "hidden"}
        album = self.client.create_album(album_fields)

        uploaded_images = []
        for element in post:
            image_path = os.path.join(path, element['image'])
            description = element.get('description', '')
            config = {"description": description,
                      "privacy": "hidden",
                      "album": album["id"]}
            image = self.client.upload_from_path(image_path,
                                                 config=config,
                                                 anon=False)

            uploaded_images.append(image)
            print(image['link'])
            print(uploaded_images)

        logging.info(post)


