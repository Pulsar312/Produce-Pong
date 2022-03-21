class Ingredient:
    def __init__(self, technical_name: str,
                 friendly_name: str,
                 image_name: str = ""):
        self.image_name = image_name
        self.friendly_name = friendly_name
        self.technical_name = technical_name

    # TODO a lot more
