# +-------------------------------------------------------------------------------
# | Project Title:      Image Genie
# | Author/Student:     Christopher Zielinski
# | edX Username:       Code_Cortex
# | GitHub Username:    noctua-innovations-inc
# | City, Country:      Oshawa, Canada
# | Date:               09-April-2024
# +-------------------------------------------------------------------------------

# https://cs50.harvard.edu/python/2022/project/

# Project must be implemented in Python.

# Project must have a "main" function and three or more additional functions.  At least three of those additional functions must be
# accompanied by tests that can be executed with "pytest".

# The "main" function must be in a file called "project.py" (this file), which is to be in the "root" (top-level folder), of the project.

# The three required custom functions other than "main" must also be in "project.py" (this file) and be defined at the same indentation
# level as "main" (not nested under any classes or functions).  These three functions are:

#     1. build_image_inquiry()
#     2. build_image_prompt()
#     3. write_image_to_disk()

# Test functions must be in a file called "test_project.py", which must also be in the "root" (top-level folder), of the project.  Test
# functions are to have the same name as the custom functions, with "test_" prepended to the function name.

# Additional classes and functions can be implemented beyond the minimum project requirements.

# The project implementation is to entail more time and effort than was required for each of the course's problem sets.

# Any "pip"-installable libraries that the project requires, must be listed, one per line, in a file called "requirements.txt" in the
# root folder of the project.


from imagegeneration import ImageGeneration
from imagegenerationdb import ImageGenerationDb
from openai_image_dto import OpenAiImageDto

from urllib.parse import parse_qs

import os
import eel


db = ImageGenerationDb()
image_generation = ImageGeneration()


def main():
    eel.init("web")
    eel.start("home.html")


# region JavaScript exposed functions


# region Selection Lists


@eel.expose
def get_specialization():
    return [
        record[ImageGenerationDb.Entity.COLUMN_NAME] for record in db.specialization
    ]


@eel.expose
def get_image_lighting():
    return [
        record[ImageGenerationDb.Entity.COLUMN_NAME] for record in db.image_lighting
    ]


@eel.expose
def get_image_contrast():
    return [
        record[ImageGenerationDb.Entity.COLUMN_NAME] for record in db.image_contrast
    ]


@eel.expose
def get_image_composition_type():
    return [
        record[ImageGenerationDb.Entity.COLUMN_NAME]
        for record in db.image_composition_type
    ]


@eel.expose
def get_image_style():
    return [record[ImageGenerationDb.Entity.COLUMN_NAME] for record in db.image_style]


@eel.expose
def get_image_color():
    return [
        record[ImageGenerationDb.Entity.COLUMN_NAME] for record in db.image_color_scheme
    ]


@eel.expose
def get_image_aesthetic_pattern():
    return [
        record[ImageGenerationDb.Entity.COLUMN_NAME]
        for record in db.image_aesthetic_pattern
    ]


@eel.expose
def get_image_depth_of_field():
    return [
        record[ImageGenerationDb.Entity.COLUMN_NAME]
        for record in db.image_depth_of_field
    ]


# endregion


# region View Event Handlers


@eel.expose
def form_submit_handler(form_data):
    dataset = query_string_to_dict(form_data)
    image_prompt = build_image_prompt(dataset)

    try:
        generated_image = image_generation.request_image_generation(
            image_prompt, dataset
        )
        write_image_to_disk(generated_image)

        dimensions = string_to_dimensions(dataset[ImageGeneration.OpenApi.IMAGE_SIZE])
        eel.show(
            f"image.html?image={generated_image.created}&height={dimensions['height']}&width={dimensions['width']}"
        )

    # From the end-user's perspective, it either worked, or did not.
    # pylint: disable=broad-exception-caught
    except Exception as e:
        # Callback is defined in JavaScript
        # pylint: disable=no-member
        eel.image_generation_error_notification(str(e))

    # Callback is defined in JavaScript
    # pylint: disable=no-member
    eel.image_generation_completion_notification()


@eel.expose
def request_image_prompts_handler(image_created: str):
    entry = db.get_event_log_by_created(int(image_created))
    if entry:
        original_prompt = f"<b>Original Prompt:</b> {entry['prompt']}"
        revised_prompt = f"<b>Revised Prompt:</b> {entry['revised_prompt']}"
        # Callback is defined in JavaScript
        # pylint: disable=no-member
        eel.set_image_prompts(original_prompt, revised_prompt)


@eel.expose
def delete_image_handler(query_string):
    try:
        image_created = query_string_to_dict(query_string)["image"]
        delete_image_from_disk(image_created)
        # Callback is defined in JavaScript
        # pylint: disable=no-member
        eel.image_deletion_completion_notification()

    # From the end-user's perspective, it either worked, or did not.
    # pylint: disable=broad-exception-caught
    except Exception as e:
        # Callback is defined in JavaScript
        # pylint: disable=no-member
        eel.image_generation_error_notification(str(e))


# endregion


# endregion


def query_string_to_dict(query_string: str) -> dict[str, str]:
    result = dict[str, str]()
    collection = parse_qs(query_string)
    for _, (k, v) in enumerate(collection.items()):
        result[k] = v[0]
    return result


def string_to_dimensions(value: str) -> dict:
    parts = value.split("x")
    return {"width": int(parts[0]), "height": int(parts[1])}


# Function exists solely for project requirement compliance.
def build_image_prompt(image_definition: dict) -> str:
    return image_generation.build_image_prompt(image_definition)


# Function exists solely for project requirement compliance.
def write_image_to_disk(image: OpenAiImageDto) -> None:
    image.save(f"web/img/{image.created}.jpg")


def delete_image_from_disk(image_created: str) -> None:
    file = f"web/img/{image_created}.jpg"
    if os.path.exists(file):
        os.remove(file)


if __name__ == "__main__":
    main()
