from tinydb import Query, TinyDB


# Single Responsibility Principle (SRP): Data persistance "bridge" design pattern, that provides an abstraction
# of data persistence from its implementation so the two can be defined and extended independently from each other.


# TinyDB is a lightweight database and this is the only class in the project that has interaction with its implementation.
class ImageGenerationDb:

    def __init__(self):
        self._db = TinyDB(self.DATABASE)

    DATABASE = "db.json"

    class Entity:
        TABLE_DEFAULT = "_default"
        TABLE_EVENT_LOG = "event_log"
        TABLE_SPECIALIZATION = "specialization"
        TABLE_IMAGE_AESTHETIC_PATTERN = "image_aesthetic_pattern"
        TABLE_IMAGE_COLOR_SCHEME = "image_color_scheme"
        TABLE_IMAGE_COMPOSITION_TYPE = "image_composition_type"
        TABLE_IMAGE_CONTRAST = "image_contrast"
        TABLE_IMAGE_DEPTH_OF_FIELD = "image_depth_of_field"
        TABLE_IMAGE_LIGHTING = "image_lighting"
        TABLE_IMAGE_STYLE = "image_style"
        COLUMN_NAME = "name"

    @property
    def database(self):
        return self._db

    # Specialization - The response perspective and/or viewpoint.
    @property
    def specialization(self):
        return self._db.table(self.Entity.TABLE_SPECIALIZATION)

    # Composition Type - Type of image that is to be generated.
    @property
    def image_composition_type(self):
        return self._db.table(self.Entity.TABLE_IMAGE_COMPOSITION_TYPE)

    # Image Style - Distinctive style or approach to creating the image.
    @property
    def image_style(self):
        return self._db.table(self.Entity.TABLE_IMAGE_STYLE)

    # Color Scheme - Influences the images essential mood, tone, and visual appeal.
    @property
    def image_color_scheme(self):
        return self._db.table(self.Entity.TABLE_IMAGE_COLOR_SCHEME)

    # Aesthetic Style - Defines particular visual characteristics, techniques and themes to be applied to the image
    # and is particularly useful in setting the images distinct era.
    @property
    def image_aesthetic_pattern(self):
        return self._db.table(self.Entity.TABLE_IMAGE_AESTHETIC_PATTERN)

    # Depth of Field - Provides guidance in the clarity and distances within the image.
    @property
    def image_depth_of_field(self):
        return self._db.table(self.Entity.TABLE_IMAGE_DEPTH_OF_FIELD)

    # Lighting - Describes the lighting qualities desired in the image.
    @property
    def image_lighting(self):
        return self._db.table(self.Entity.TABLE_IMAGE_LIGHTING)

    # Contrast - Allows for guidance in the different levels of distinction or difference between light and dark areas within an image.
    @property
    def image_contrast(self):
        return self._db.table(self.Entity.TABLE_IMAGE_CONTRAST)

    def get_event_log_by_created(self, created: int) -> dict:
        query = Query()
        result = self._db.table(self.Entity.TABLE_EVENT_LOG).search(
            query.created == created
        )
        return next(iter(result), None)

    def write_event(self, event: object) -> None:
        self._db.table(self.Entity.TABLE_EVENT_LOG).insert(event)

    # Populates the database with initial data to provide a consistent starting point.
    # Each dataset is maintained in its own database table which avoids the need to preprocess it upon retrieval (e.g. filtering),
    # and add extra data attributes to be able to select a specific dataset.

    # Image aspect datasets, are datasets that refer to a specific attribute or feature of a image which can be analyzed or
    # considered independently or in relation to other aspects.  The following image aspects are believed to have significant and
    # meaninfulg influence over the definition of an image:

    # Specialization:
    # Instructs what context (perspective or viewpoint), is to be applied to the generated response.

    # Composition Type:
    # Type of image that is to be generated.

    # Image Style:
    # Distinctive style or approach to creating the image.

    # Color Scheme:
    # Influences the images essential mood, tone, and visual appeal.

    # Aesthetic Style:
    # Defines particular visual characteristics, techniques and themes to be applied to the image and is
    # particularly useful in setting the images distinct period of time characterized by particular
    # cultural, historical, social, or artistic trends and events.

    # Depth of Field:
    # Provides guidance in the clarity and distances within the image.

    # Lighting:
    # Describes the lighting qualities desired in the image.

    # Contrast:
    # Allows for guidance in the different levels of distinction or difference between light and dark areas within an image.
    def seed_database(self):
        self.specialization.truncate()
        specializations = [
            {self.Entity.COLUMN_NAME: "Digital Artist"},
            {self.Entity.COLUMN_NAME: "Illustrator"},
            {self.Entity.COLUMN_NAME: "Animator"},
            {self.Entity.COLUMN_NAME: "Calligrapher"},
            {self.Entity.COLUMN_NAME: "Cartoonist"},
            {self.Entity.COLUMN_NAME: "Graphic Designer"},
            {self.Entity.COLUMN_NAME: "Native Artist"},
            {self.Entity.COLUMN_NAME: "Painter"},
            {self.Entity.COLUMN_NAME: "Photographer"},
            {self.Entity.COLUMN_NAME: "Street Artist"},
        ]
        self.specialization.insert_multiple(specializations)

        self.image_composition_type.truncate()
        composition_type = [
            {self.Entity.COLUMN_NAME: "illustration"},
            {self.Entity.COLUMN_NAME: "avatar"},
            {self.Entity.COLUMN_NAME: "cinematic"},
            {self.Entity.COLUMN_NAME: "diagram"},
            {self.Entity.COLUMN_NAME: "icon"},
            {self.Entity.COLUMN_NAME: "logo"},
            {self.Entity.COLUMN_NAME: "painting"},
            {self.Entity.COLUMN_NAME: "photo"},
            {self.Entity.COLUMN_NAME: "picture"},
            {self.Entity.COLUMN_NAME: "poster"},
        ]
        self.image_composition_type.insert_multiple(composition_type)

        self.image_style.truncate()
        image_style = [
            {self.Entity.COLUMN_NAME: "digital art"},
            {self.Entity.COLUMN_NAME: "aboriginal-styled"},
            {self.Entity.COLUMN_NAME: "abstract"},
            {self.Entity.COLUMN_NAME: "anime-styled"},
            {self.Entity.COLUMN_NAME: "comic-styled"},
            {self.Entity.COLUMN_NAME: "expressionism"},
            {self.Entity.COLUMN_NAME: "flat design"},
            {self.Entity.COLUMN_NAME: "glyph design"},
            {self.Entity.COLUMN_NAME: "masterpiece"},
            {self.Entity.COLUMN_NAME: "muralism"},
            {self.Entity.COLUMN_NAME: "photo-realistic"},
            {self.Entity.COLUMN_NAME: "pointillism"},
            {self.Entity.COLUMN_NAME: "pop art"},
            {self.Entity.COLUMN_NAME: "realism"},
            {self.Entity.COLUMN_NAME: "skeuomorphic design"},
            {self.Entity.COLUMN_NAME: "stencil art"},
            {self.Entity.COLUMN_NAME: "surrealism"},
            {self.Entity.COLUMN_NAME: "35mm film"},
            {self.Entity.COLUMN_NAME: "charcoal"},
            {self.Entity.COLUMN_NAME: "oil painting"},
        ]
        self.image_style.insert_multiple(image_style)

        self.image_color_scheme.truncate()
        color_scheme = [
            {self.Entity.COLUMN_NAME: "vibrant"},
            {self.Entity.COLUMN_NAME: "realistic"},
            {self.Entity.COLUMN_NAME: "monochromatic"},
            {self.Entity.COLUMN_NAME: "duotone"},
            {self.Entity.COLUMN_NAME: "neutral"},
            {self.Entity.COLUMN_NAME: "subdued"},
            {self.Entity.COLUMN_NAME: "analogous"},
            {self.Entity.COLUMN_NAME: "complementary"},
            {self.Entity.COLUMN_NAME: "split-complementary"},
            {self.Entity.COLUMN_NAME: "triadic"},
            {self.Entity.COLUMN_NAME: "gradient"},
            {self.Entity.COLUMN_NAME: "warm"},
            {self.Entity.COLUMN_NAME: "cool"},
            {self.Entity.COLUMN_NAME: "pastel"},
        ]
        self.image_color_scheme.insert_multiple(color_scheme)

        self.image_aesthetic_pattern.truncate()
        aesthetic_pattern = [
            {self.Entity.COLUMN_NAME: "current"},
            {self.Entity.COLUMN_NAME: "anime-inspired"},
            {self.Entity.COLUMN_NAME: "futuristic"},
            {self.Entity.COLUMN_NAME: "geometric"},
            {self.Entity.COLUMN_NAME: "grunge"},
            {self.Entity.COLUMN_NAME: "minimalist"},
            {self.Entity.COLUMN_NAME: "modern"},
            {self.Entity.COLUMN_NAME: "retro"},
            {self.Entity.COLUMN_NAME: "vintage"},
        ]
        self.image_aesthetic_pattern.insert_multiple(aesthetic_pattern)

        self.image_depth_of_field.truncate()
        depth_of_field = [
            {self.Entity.COLUMN_NAME: "subject isolation technique"},
            {self.Entity.COLUMN_NAME: "hyperfocal distance"},
            {self.Entity.COLUMN_NAME: "depth compression"},
            {self.Entity.COLUMN_NAME: "macro focus"},
            {self.Entity.COLUMN_NAME: "background blur"},
            {self.Entity.COLUMN_NAME: "foreground blur"},
            {self.Entity.COLUMN_NAME: "motion blur"},
        ]
        self.image_depth_of_field.insert_multiple(depth_of_field)

        self.image_lighting.truncate()
        lighting = [
            {self.Entity.COLUMN_NAME: "ambient"},
            {self.Entity.COLUMN_NAME: "natural"},
            {self.Entity.COLUMN_NAME: "subtle"},
            {self.Entity.COLUMN_NAME: "dramatic"},
        ]
        self.image_lighting.insert_multiple(lighting)

        self.image_contrast.truncate()
        contrast = [
            {self.Entity.COLUMN_NAME: "normal"},
            {self.Entity.COLUMN_NAME: "high"},
            {self.Entity.COLUMN_NAME: "low"},
        ]
        self.image_contrast.insert_multiple(contrast)


if __name__ == "__main__":
    obj = ImageGenerationDb()
    obj.seed_database()
