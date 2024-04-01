import inquirer  # Provide the most basic, terminal-based, user-interface.  See also... https://github.com/magmax/python-inquirer
import json
import requests  # The Requests package is recommended for a higher-level HTTP client interface.

from httpclient import HttpClient
from imagegenerationdb import ImageGenerationDb
from openai_image_dto import OpenAiImageDto

"""
Single Responsibility Principle (SRP): This class has the single resposiblity of handling the details Image Generation.
"""


class ImageGeneration:
    USER_AGENT = "ImgGen/1.0"

    class OpenApi:
        KEY = "<put-your-open-ai-key-here>"
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

    """
    DALL-E 3 does not explicitly support negative prompts (instructing DALL-E not to include certain elements).
    Emphasis is placed on providing DALL-E 3 with a succinct prompt that focuses on the desired outcome and therfore the
    image inquirer prompts the end-user for details that will have the largest and most impactful influence on the image generated.

    For dictionary keys, I used the database table names, because the data is already tied to the database and I didn't want to
    repeat the work of maintaining identifier keys solely for the purpose of isolation.  Refactoring code is faster than maintaining
    duplication.
    """

    def build_image_inquiry(self) -> list:
        return [
            # --[ DALL-E 3 API parameters ]--
            # The size of the generated image
            inquirer.List(
                ImageGeneration.OpenApi.IMAGE_SIZE,
                message="What size do you want?",
                choices=["1024x1024", "1792x1024", "1024x1792"],
                default="1792x1024",
            ),
            # The quality of the image to generate
            inquirer.List(
                ImageGeneration.OpenApi.IMAGE_QUALITY,
                message="What quality do you want?",
                choices=["standard", "hd"],
                default="hd",
            ),
            # The style of the generated image
            inquirer.List(
                ImageGeneration.OpenApi.IMAGE_STYLE,
                message="What style do you want?",
                choices=["vivid", "natural"],
                default="vivid",
            ),
            # -------------------------------
            # Specialization
            inquirer.List(
                self._db.Entity.TABLE_SPECIALIZATION,
                message="What specialization/perspective are we using?",
                choices=[
                    record[self._db.Entity.COLUMN_NAME]
                    for record in self._db.specialization.all()
                ],
            ),
            # Image Composition Type
            inquirer.List(
                self._db.Entity.TABLE_IMAGE_COMPOSITION_TYPE,
                message="What is the image composition type?",
                choices=[
                    record[self._db.Entity.COLUMN_NAME]
                    for record in self._db.image_composition_type.all()
                ],
            ),
            # Image Style
            inquirer.List(
                self._db.Entity.TABLE_IMAGE_STYLE,
                message="What is the imagery style?",
                choices=[
                    record[self._db.Entity.COLUMN_NAME]
                    for record in self._db.image_style.all()
                ],
            ),
            # Image Color Scheme
            inquirer.List(
                self._db.Entity.TABLE_IMAGE_COLOR_SCHEME,
                message="What color scheme is to be used?",
                choices=[
                    record[self._db.Entity.COLUMN_NAME]
                    for record in self._db.image_color_scheme.all()
                ],
            ),
            # Image Aesthetic Pattern
            inquirer.List(
                self._db.Entity.TABLE_IMAGE_AESTHETIC_PATTERN,
                message="What aesthetic pattern is to be used?",
                choices=[
                    record[self._db.Entity.COLUMN_NAME]
                    for record in self._db.image_aesthetic_pattern.all()
                ],
            ),
            # Image Depth of Field
            inquirer.List(
                self._db.Entity.TABLE_IMAGE_DEPTH_OF_FIELD,
                message="What aesthetic pattern is to be used?",
                choices=[
                    record[self._db.Entity.COLUMN_NAME]
                    for record in self._db.image_depth_of_field.all()
                ],
            ),
            # Image Lighting
            inquirer.List(
                self._db.Entity.TABLE_IMAGE_LIGHTING,
                message="What type of lighting is to be applied?",
                choices=[
                    record[self._db.Entity.COLUMN_NAME]
                    for record in self._db.image_lighting.all()
                ],
            ),
            # Image Contrast
            inquirer.List(
                self._db.Entity.TABLE_IMAGE_CONTRAST,
                message="What type of contrast is to be used?",
                choices=[
                    record[self._db.Entity.COLUMN_NAME]
                    for record in self._db.image_contrast.all()
                ],
            ),
            # Override automatic DALL-E prompt revision?
            inquirer.Checkbox(
                ImageGeneration.OpenApi.PROMPT_OVERRIDE,
                message="Do you want to prevent DALL-E from revising the prompt?",
                choices=[ImageGeneration.OpenApi.PROMPT_OVERRIDE_INDICATOR],
            ),
            # Actual end-user defined image request
            inquirer.Text(
                ImageGeneration.OpenApi.PROMPT_TEXT,
                message="What image is to be generated?",
            ),
            inquirer.Confirm(
                ImageGeneration.OpenApi.SUBMIT,
                message="This will generate an image.  Continue?",
                default=False,
            ),
        ]

    def execute_image_inquiry(self, questions: dict) -> dict:
        return inquirer.prompt(questions)

    def build_image_request_header(self) -> object:
        return {
            HttpClient.USER_AGENT: self.USER_AGENT,
            HttpClient.CONTENT_TYPE: HttpClient.MediaType.JSON,
            HttpClient.AUTHORIZATION: f"Bearer {self.OpenApi.KEY}",
        }

    """
    The maximum prompt text (description of the desired image) length for OpenAI DALL-E 3 (dall-e-3), is 4,000 characters.
    """

    def build_image_prompt(self, dataset: dict) -> str:
        prompt_preamble = ""
        specialization = (
            f"Specializing as a {dataset[self._db.Entity.TABLE_SPECIALIZATION]}"
        )
        composition_type = (
            f"use a {dataset[self._db.Entity.TABLE_IMAGE_COMPOSITION_TYPE]} composition type"
        )
        image_style = f"with {dataset[self._db.Entity.TABLE_IMAGE_STYLE]} imagery style"
        color_scheme = f"use a {dataset[self._db.Entity.TABLE_IMAGE_COLOR_SCHEME]} color scheme"
        aesthetics = (
            f"use a {dataset[self._db.Entity.TABLE_IMAGE_AESTHETIC_PATTERN]} aesthetic style"
        )
        depth_of_view = f"{dataset[self._db.Entity.TABLE_IMAGE_DEPTH_OF_FIELD]} is used for the depth of field"
        lighting = f"while the lighting is {dataset[self._db.Entity.TABLE_IMAGE_LIGHTING]}"
        contrast = f"the image has a {dataset[self._db.Entity.TABLE_IMAGE_CONTRAST]} contrast"

        prompt_preamble = ("", ImageGeneration.OpenApi.PROMPT_OVERRIDE_TEXT)[
            dataset[ImageGeneration.OpenApi.PROMPT_OVERRIDE]
            == ImageGeneration.OpenApi.PROMPT_OVERRIDE_INDICATOR
        ]

        return f"{prompt_preamble}{specialization}, {composition_type}, {image_style}, {color_scheme}. {aesthetics}, {depth_of_view}, {lighting}, {contrast}: {dataset[ImageGeneration.OpenApi.PROMPT_TEXT]}"

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
        reply = requests.post(
            ImageGeneration.OpenApi.URL, data=json.dumps(body), headers=headers
        )

        if reply.ok:
            image_object = OpenAiImageDto(reply.json())
            self.__log_event(prompt, image_object)
            return image_object
        else:
            # Error handling - retrieve the error message and then raise it.
            if reply.status_code in {
                requests.codes.bad_request,
                requests.codes.not_found,
            }:
                if (int(reply.headers[HttpClient.CONTENT_LENGTH]) > 0) and (
                    reply.headers[HttpClient.CONTENT_TYPE] == HttpClient.MediaType.JSON
                ):
                    reply_body = reply.json()
                    raise RuntimeError(reply_body["error"]["message"])

    def __log_event(self, prompt: str, image_object: OpenAiImageDto) -> None:
        log_record = {
            ImageGeneration.OpenApi.PROMPT_TEXT: prompt,
            ImageGeneration.OpenApi.REVISED_PROMPT: image_object.revised_prompt,
            ImageGeneration.OpenApi.IMAGE_TIMESTAMP: image_object.created,
        }
        self._db.write_event(log_record)
