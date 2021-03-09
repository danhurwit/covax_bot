class DisplayProperties:
    logo_url = ""
    theme_color = ""

    def __init__(self, logo_url, theme_color):
        self.logo_url = logo_url
        self.theme_color = theme_color

    def get_logo_url(self):
        return self.logo_url

    def get_theme_color(self):
        return self.theme_color
