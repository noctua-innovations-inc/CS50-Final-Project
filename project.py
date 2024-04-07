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
from imagegenerationdb import ImageGenerationDb
from openai_image_dto import OpenAiImageDto

from urllib.parse import parse_qs

import eel


db =  ImageGenerationDb()
image_generation = ImageGeneration()


@eel.expose
def submit_form(data):
    print(data)


@eel.expose
def say_hello_py(x):
    print('Hello from %s' % x)


#region Selection Lists

@eel.expose
def get_specialization():
    return [record[ImageGenerationDb.Entity.COLUMN_NAME] for record in  db.specialization]

@eel.expose
def get_image_lighting():
    return [record[ImageGenerationDb.Entity.COLUMN_NAME] for record in  db.image_lighting]

@eel.expose
def get_image_contrast():
    return [record[ImageGenerationDb.Entity.COLUMN_NAME] for record in  db.image_contrast]

@eel.expose
def get_image_composition_type():
    return [record[ImageGenerationDb.Entity.COLUMN_NAME] for record in  db.image_composition_type]

@eel.expose
def get_image_style():
    return [record[ImageGenerationDb.Entity.COLUMN_NAME] for record in  db.image_style]

@eel.expose
def get_image_color():
    return [record[ImageGenerationDb.Entity.COLUMN_NAME] for record in  db.image_color_scheme]

@eel.expose
def get_image_aesthetic_pattern():
    return [record[ImageGenerationDb.Entity.COLUMN_NAME] for record in  db.image_aesthetic_pattern]

@eel.expose
def get_image_depth_of_field():
    return [record[ImageGenerationDb.Entity.COLUMN_NAME] for record in  db.image_depth_of_field]

#endregion


@eel.expose                         # Expose this function to Javascript
def handleinput(form_data):
    dataset = parse_qs(form_data)
    for i, (k, v)  in enumerate(dataset.items()):
        dataset[k] = v[0]

    image_prompt = build_image_prompt(dataset)
    generated_image = image_generation.request_image_generation(image_prompt, dataset)
    write_image_to_disk(generated_image)

     
    eel.show(f"image.html?image={generated_image.created}&height=1024&width=1792");


@eel.expose
def handledelete(query_string):
    dataset = parse_qs(query_string)
    None


def main():
    eel.init('web')

    say_hello_py('Python World!')
    eel.say_hello_js('Python World!')   # Call a Javascript function

    eel.start('index.html')

    
    # print("Welcome to the Image Genie!")

    # human_image_inquiry = build_image_inquiry()
    # image_definition = image_generation.execute_image_inquiry(human_image_inquiry)

    # if image_definition[ImageGeneration.OpenApi.SUBMIT]:
    #     image_prompt = build_image_prompt(image_definition)
    #     generated_image = image_generation.request_image_generation(image_prompt, image_definition)
    #     write_image_to_disk(generated_image)
    None


# Function exists solely for project requirement compliance.
def build_image_inquiry() -> list:
    return image_generation.build_image_inquiry()


# Function exists solely for project requirement compliance.
def build_image_prompt(image_definition: dict) -> str:
    return image_generation.build_image_prompt(image_definition)


# Function exists solely for project requirement compliance.
def write_image_to_disk(image: OpenAiImageDto) -> None:
    image.save(f"web/img/{image.created}.jpg")



if __name__ == "__main__":
    main()

