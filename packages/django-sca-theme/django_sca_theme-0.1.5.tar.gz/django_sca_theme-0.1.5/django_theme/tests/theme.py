from django.core.files import File

from ..models import Theme


class ThemeCase:
    """
    create a sample theme
    """

    def __init__(self, corporate_logo_path="fixtures/test_file/image.jpg", tab_logo_path="fixtures/test_file/AAV43679.png"):
        self.theme = {
            "title": "天和双利",
            "theme_color": "#e60000",
            "aux_color": "#666666",
        }
        self.theme_object = self.create_theme()

        self.theme_object.corporate_logo.save(
            "logo.jpg", File(open(corporate_logo_path, "rb"))
        )
        self.theme_object.tab_logo.save(
            "tab_logo.png", File(open(tab_logo_path, "rb"))
        )

    def attach_file(self):
        return [
            (
                "corporate_logo",
                ("logo.jpg", open("fixtures/test_file/image.jpg", "rb"), "image/jpg"),
            ),
            (
                "tab_logo",
                (
                    "tab_logo.png",
                    open("fixtures/test_file/AAV43679.png", "rb"),
                    "image/png",
                ),
            ),
        ]

    def create_theme(self):
        return Theme.objects.create(**self.theme)
