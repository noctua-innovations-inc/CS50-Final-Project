import base64

from io import BytesIO
from PIL import Image

import imagegeneration as ig


class OpenAiImageDto:

    def __init__(self, response: object):
        image_object = response[ig.ImageGeneration.OpenApi.PAYLOAD_DATA][0]
        self._created = response[ig.ImageGeneration.OpenApi.IMAGE_TIMESTAMP]
        self._b64_image = image_object[ig.ImageGeneration.OpenApi.PAYLOAD_B64_JSON]
        self._bitmap = base64.b64decode(self._b64_image)
        self._image = Image.open(BytesIO(self._bitmap))
        self._image = self._image.convert("RGB")
        self._revised_prompt = image_object[ig.ImageGeneration.OpenApi.REVISED_PROMPT]

    @property
    def created(self):
        return self._created

    @property
    def b64_json(self):
        return self._b64_image

    @property
    def bitmap(self):
        return self._bitmap

    @property
    def revised_prompt(self):
        return self._revised_prompt

    @property
    def image(self):
        return self._image

    def save(self, filename: str) -> None:
        self._image.save(filename)
