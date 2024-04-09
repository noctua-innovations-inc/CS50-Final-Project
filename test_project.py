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

test_prompt_string = "Small owl under the moonlight."

test_field_image = "image"
test_field_width = "width"
test_field_height = "height"
test_created_value = 1711935452
test_height_dimension = "1024"
test_width_dimension = "1792"
test_query_string = f"?{test_field_image}={test_created_value}&{test_field_height}={test_height_dimension}&{test_field_width}={test_width_dimension}"

test_dimension = f"{test_width_dimension}x{test_height_dimension}"


# NOTE: Test(s) require a seeded database. Execute this prior to running this test proejct:
# python imagegenerationdb.py

# Execution of the imagegenerationdb.py program will have database side effects.
def main():
    test_query_string_to_dict()
    test_build_image_prompt()
    test_write_image_to_disk()


# 1. Verify query-string to dictionary works as expected.
def test_query_string_to_dict():
    collection = project.query_string_to_dict(test_query_string[1:]);
    assert len(collection) == 3
    assert collection[test_field_image] == test_created_value
    assert collection[test_field_height] == test_height_dimension
    assert collection[test_field_width] == test_width_dimension


# 2. Verify dimension parsing happy-path works as expected.
def test_query_string_to_dict():
    dimensions = project.string_to_dimensions(test_dimension)
    assert len(dimensions) == 2
    assert dimensions[test_field_width] == int(test_width_dimension)
    assert dimensions[test_field_height] == int(test_height_dimension)



# 3. Verify that all required answers are included in the image generation prompt.
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
        ImageGeneration.OpenApi.PROMPT_TEXT: test_prompt_string,
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


def assert_prompt_contents(prompt_text: str, override: bool):
    # Expected/required prompt (attribute) values:
    assert specialization in prompt_text
    assert image_aesthetic_pattern in prompt_text
    assert image_color_scheme in prompt_text
    assert image_composition_type in prompt_text
    assert image_contrast in prompt_text
    assert image_depth_of_field in prompt_text
    assert image_lighting in prompt_text
    assert image_style in prompt_text

    # Conditional AI prompt revision override.
    if override:
        assert ImageGeneration.OpenApi.PROMPT_OVERRIDE_TEXT in prompt_text
    else:
        assert ImageGeneration.OpenApi.PROMPT_OVERRIDE_TEXT not in prompt_text


# 4. Contrived test that verifies that the Project's write_image_to_disk() function call the appropriate image method witht he expected filename.
def test_write_image_to_disk():
    image = Mock()
    image.created = 1711920536
    project.write_image_to_disk(image)
    image.save.assert_called_once_with(f"web/img/{image.created}.jpg")


if __name__ == "__main__":
    main()