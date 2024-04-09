import json
from typing import Mapping
import requests  # The Requests package is recommended for a higher-level HTTP client interface.

from httpclient import HttpClient
from imagegenerationdb import ImageGenerationDb
from openai_image_dto import OpenAiImageDto


# Single Responsibility Principle (SRP): This class has the single resposiblity of handling the details Image Generation.
class ImageGeneration:
    USER_AGENT = "ImgGen/1.0"

    class OpenApi:
        KEY = "<<put-your-OpenAI-key-here!>>"
        URL = "https://api.openai.com/v1/images/generations"
        MODEL = "dall-e-3"
        SUBMIT = "correct"
        IMAGE_COUNT = "n"
        IMAGE_TIMESTAMP = "created"
        IMAGE_SIZE = "size"
        IMAGE_QUALITY = "quality"
        IMAGE_RESPONSE_FORMAT = "response_format"
        IMAGE_STYLE = "style"
        IMAGE_MODEL = "model"
        PAYLOAD_DATA = "data"
        PAYLOAD_B64_JSON = "b64_json"
        PROMPT_TEXT = "prompt"
        PROMPT_OVERRIDE = "prompt_override"
        PROMPT_OVERRIDE_INDICATOR = "yes"
        PROMPT_OVERRIDE_TEXT = "I NEED to test hos the tool works with extremely simple prompts.  DO NOT add any detail, just use it AS-IS:"
        REVISED_PROMPT = "revised_prompt"

    def __init__(self):
        self._db = ImageGenerationDb()

    def build_image_request_header(self) -> Mapping[str, str]:
        return {
            HttpClient.USER_AGENT: self.USER_AGENT,
            HttpClient.CONTENT_TYPE: HttpClient.MediaType.JSON,
            HttpClient.AUTHORIZATION: f"Bearer {self.OpenApi.KEY}",
        }

    # The maximum prompt text (description of the desired image) length for OpenAI DALL-E 3 (dall-e-3), is 4,000 characters.
    def build_image_prompt(self, dataset: dict) -> str:
        prompt_preamble = ""
        specialization = (
            f"Specializing as a {dataset[self._db.Entity.TABLE_SPECIALIZATION]}.  "
        )
        composition_type = (
            f"Create a {dataset[self._db.Entity.TABLE_IMAGE_COMPOSITION_TYPE]}, "
        )
        image_style = (
            f"with a {dataset[self._db.Entity.TABLE_IMAGE_STYLE]} imagery style, "
        )
        color_scheme = (
            f"and a {dataset[self._db.Entity.TABLE_IMAGE_COLOR_SCHEME]} color scheme.  "
        )
        aesthetics = f"Use a {dataset[self._db.Entity.TABLE_IMAGE_AESTHETIC_PATTERN]} aesthetic style.  "
        depth_of_view = f"Depth of field is to be {dataset[self._db.Entity.TABLE_IMAGE_DEPTH_OF_FIELD]}.  "
        lighting = f"Lighting is {dataset[self._db.Entity.TABLE_IMAGE_LIGHTING]}.  "
        contrast = f"The image is to have {dataset[self._db.Entity.TABLE_IMAGE_CONTRAST]} contrast.  "

        if ImageGeneration.OpenApi.PROMPT_OVERRIDE not in dataset:
            dataset[ImageGeneration.OpenApi.PROMPT_OVERRIDE] = "no"

        prompt_preamble = ("", ImageGeneration.OpenApi.PROMPT_OVERRIDE_TEXT)[
            dataset[ImageGeneration.OpenApi.PROMPT_OVERRIDE]
            == ImageGeneration.OpenApi.PROMPT_OVERRIDE_INDICATOR
        ]

        return f"{prompt_preamble}{specialization}{composition_type}{image_style}{color_scheme}{aesthetics}{depth_of_view}{lighting}{contrast}Subject: {dataset[ImageGeneration.OpenApi.PROMPT_TEXT]}"

    def build_image_request_body(self, prompt: str, configuration: dict) -> object:
        return {
            self.OpenApi.PROMPT_TEXT: prompt,
            self.OpenApi.IMAGE_COUNT: 1,
            self.OpenApi.IMAGE_SIZE: configuration[self.OpenApi.IMAGE_SIZE],
            self.OpenApi.IMAGE_MODEL: self.OpenApi.MODEL,
            self.OpenApi.IMAGE_RESPONSE_FORMAT: self.OpenApi.PAYLOAD_B64_JSON,
            self.OpenApi.IMAGE_QUALITY: configuration[self.OpenApi.IMAGE_QUALITY],
            self.OpenApi.IMAGE_STYLE: configuration[self.OpenApi.IMAGE_STYLE],
        }

    def request_image_generation(
        self, prompt: str, configuration: dict
    ) -> OpenAiImageDto:
        headers = self.build_image_request_header()
        body = self.build_image_request_body(prompt, configuration)

        # Timeout is intentionally missing (appropriate timeout for OpenAI DALL-E is undefined).
        # pylint: disable=missing-timeout
        reply = requests.post(
            ImageGeneration.OpenApi.URL, data=json.dumps(body), headers=headers
        )

        if reply.ok:
            image_object = OpenAiImageDto(reply.json())
            self.__log_event(prompt, image_object)
            return image_object
        else:
            # Error handling - retrieve the error message and then raise it.
            if (int(reply.headers[HttpClient.CONTENT_LENGTH]) > 0) and (
                reply.headers[HttpClient.CONTENT_TYPE] == HttpClient.MediaType.JSON
            ):
                reply_body = reply.json()
                if "error" in reply_body:
                    raise RuntimeError(reply_body["error"]["message"])

        raise RuntimeError(
            f"Server responded with status code {reply.status_code} due to the call being: {reply.reason}."
        )

    def __log_event(self, prompt: str, image_object: OpenAiImageDto) -> None:
        log_record = {
            ImageGeneration.OpenApi.PROMPT_TEXT: prompt,
            ImageGeneration.OpenApi.REVISED_PROMPT: image_object.revised_prompt,
            ImageGeneration.OpenApi.IMAGE_TIMESTAMP: image_object.created,
        }
        self._db.write_event(log_record)
