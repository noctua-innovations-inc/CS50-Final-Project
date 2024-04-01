"""
+-------------------------------------------------------------------------------
| Project Title:      Image Genie
| Author/Student:     Christopher Zielinski
| edX Username:       Code_Cortex
| GitHub Username:    noctua-innovations-inc
| City, Country:      Oshawa, Canada
+-------------------------------------------------------------------------------

https://cs50.harvard.edu/python/2022/project/

Project must be implemented in Python.

Project must have a "main" function and three or more additional functions.  At least three of those additional functions must be
accompanied by tests that can be executed with "pytest".

The "main" function must be in a file called "project.py" (this file), which is to be in the "root" (top-level folder), of the project.

The three required custom functions other than "main" must also be in "project.py" (this file) and be defined at the same indentation
level as "main" (not nested under any classes or functions).  These three functions are:

    1. build_image_inquiry()
    2. build_image_prompt()
    3. write_image_to_disk()

Test functions must be in a file called "test_project.py", which must also be in the "root" (top-level folder), of the project.  Test
functions are to have the same name as the custom functions, with "test_" prepended to the function name.

Additional classes and functions can be implemented beyond the minimum project requirements.

The project implementation is to entail more time and effort than was required for each of the course's problem sets.

Any "pip"-installable libraries that the project requires, must be listed, one per line, in a file called "requirements.txt" in the
root folder of the project.

"""


from imagegeneration import ImageGeneration
from openai_image_dto import OpenAiImageDto


image_generation = ImageGeneration()


def main():
    print("Welcome to the Image Genie!")

    human_image_inquiry = build_image_inquiry()
    image_definition = image_generation.execute_image_inquiry(human_image_inquiry)

    if image_definition[ImageGeneration.OpenApi.SUBMIT]:
        image_prompt = build_image_prompt(image_definition)
        generated_image = image_generation.request_image_generation(image_prompt, image_definition)
        write_image_to_disk(generated_image)


# Function exists solely for project requirement compliance.
def build_image_inquiry() -> list:
    return image_generation.build_image_inquiry()


# Function exists solely for project requirement compliance.
def build_image_prompt(image_definition: dict) -> str:
    return image_generation.build_image_prompt(image_definition)


# Function exists solely for project requirement compliance.
def write_image_to_disk(image: OpenAiImageDto) -> None:
    image.save(f"{image.created}.jpg")


if __name__ == "__main__":
    main()
