import project

from unittest.mock import Mock

from imagegeneration import ImageGeneration
from imagegenerationdb import ImageGenerationDb


specialization = "Photographer"
image_aesthetic_pattern = "current"
image_color_scheme = "vibrant"
image_composition_type = "illustration"
image_contrast = "normal"
image_depth_of_field = "subject isolation technique"
image_lighting = "ambient"
image_style = "digital art"

prompt = "Small owl under the moonlight."


"""
NOTE: Test(s) require a seeded database. Execute this prior to running this test proejct:
python imagegenerationdb.py

Execution of the imagegenerationdb.py program will have database side effects.
"""


def main():
    test_build_image_inquiry()
    test_build_image_prompt()
    test_write_image_to_disk()


"""
1. Verify that the built inquiry collects all of the required answers from the end-user.
"""
def test_build_image_inquiry():
    entries = [entry.name for entry in project.build_image_inquiry()]

    assert ImageGeneration.OpenApi.IMAGE_SIZE in entries
    assert ImageGeneration.OpenApi.IMAGE_QUALITY in entries
    assert ImageGeneration.OpenApi.IMAGE_STYLE in entries
    assert ImageGenerationDb.Entity.TABLE_SPECIALIZATION in entries
    assert ImageGenerationDb.Entity.TABLE_IMAGE_COMPOSITION_TYPE in entries
    assert ImageGenerationDb.Entity.TABLE_IMAGE_STYLE in entries
    assert ImageGenerationDb.Entity.TABLE_IMAGE_COLOR_SCHEME in entries
    assert ImageGenerationDb.Entity.TABLE_IMAGE_AESTHETIC_PATTERN in entries
    assert ImageGenerationDb.Entity.TABLE_IMAGE_DEPTH_OF_FIELD in entries
    assert ImageGenerationDb.Entity.TABLE_IMAGE_LIGHTING in entries
    assert ImageGenerationDb.Entity.TABLE_IMAGE_AESTHETIC_PATTERN in entries
    assert ImageGeneration.OpenApi.PROMPT_OVERRIDE in entries
    assert ImageGeneration.OpenApi.PROMPT_TEXT in entries
    assert ImageGeneration.OpenApi.SUBMIT in entries


"""
2. Verify that all required answers are included in the image generation prompt.
"""
def test_build_image_prompt():
    config = {
        ImageGenerationDb.Entity.TABLE_SPECIALIZATION: specialization,
        ImageGenerationDb.Entity.TABLE_IMAGE_AESTHETIC_PATTERN: image_aesthetic_pattern,
        ImageGenerationDb.Entity.TABLE_IMAGE_COLOR_SCHEME: image_color_scheme,
        ImageGenerationDb.Entity.TABLE_IMAGE_COMPOSITION_TYPE: image_composition_type,
        ImageGenerationDb.Entity.TABLE_IMAGE_CONTRAST: image_contrast,
        ImageGenerationDb.Entity.TABLE_IMAGE_DEPTH_OF_FIELD: image_depth_of_field,
        ImageGenerationDb.Entity.TABLE_IMAGE_LIGHTING: image_lighting,
        ImageGenerationDb.Entity.TABLE_IMAGE_STYLE: image_style,
        ImageGeneration.OpenApi.PROMPT_TEXT: prompt,
        ImageGeneration.OpenApi.PROMPT_OVERRIDE: "",
    }

    # Assert presence of expected prompt values in generated prompt,
    # without overriding AI prompt revision.
    complete_prompt = project.build_image_prompt(config)
    assert_prompt_contents(complete_prompt, False)

    # Assert presence of expected prompt values in generated prompt,
    # overriding AI prompt revision.
    config[project.ImageGeneration.OpenApi.PROMPT_OVERRIDE] = (
        project.ImageGeneration.OpenApi.PROMPT_OVERRIDE_INDICATOR
    )
    complete_prompt = project.build_image_prompt(config)
    assert_prompt_contents(complete_prompt, True)


def assert_prompt_contents(prompt: str, override: bool):
    # Expected/required prompt (attribute) values:
    assert specialization in prompt
    assert image_aesthetic_pattern in prompt
    assert image_color_scheme in prompt
    assert image_composition_type in prompt
    assert image_contrast in prompt
    assert image_depth_of_field in prompt
    assert image_lighting in prompt
    assert image_style in prompt

    # Conditional AI prompt revision override.
    if override:
        assert ImageGeneration.OpenApi.PROMPT_OVERRIDE_TEXT in prompt
    else:
        assert ImageGeneration.OpenApi.PROMPT_OVERRIDE_TEXT not in prompt

"""
3. Contrived test that verifies that the Project's write_image_to_disk() function call the appropriate image method witht he expected filename.
"""
def test_write_image_to_disk():
    image = Mock()
    image.created = 1711920536
    project.write_image_to_disk(image)
    image.save.assert_called_once_with(f"{image.created}.jpg")


if __name__ == "__main__":
    main()
