from fpdf import FPDF
from utils import path


# Créer une classe qui hérite de FPDF
class PDF(FPDF):

    def __init__(self, tirages: dict, json_teams: list):

        super().__init__()

        self.__tirages = tirages

        self.__json_teams = json_teams

        self.per_page = 4

        self.total_pages = (
            int(len(tirages.keys()) / self.per_page)
            if len(tirages.keys()) % self.per_page == 0
            else int(len(tirages.keys()) / self.per_page) + 1
        )
        self.img_target_x = 3
        self.cell_w = 15
        self.cell_h = 38
        self.img_w = self.img_h = 15
        self.img_x = 10
        self.img_y = 32
        self.e = 10
        self.border = 0

    @property
    def tirages(self) -> dict:
        return self.__tirages

    @tirages.setter
    def tirages(self, value: dict) -> None:
        self.__tirages = value

    @property
    def json_teams(self) -> list:
        return self.__json_teams

    @json_teams.setter
    def json_teams(self, value: list) -> None:
        self.__json_teams = value

    def get_logo(self, name: str) -> str | None:
        logo = None
        for club in self.json_teams:
            if club["nom"] == name:
                logo = club["logo"]
                break
        return logo

    # methods

    def footer(self):
        # Select Arial bold 15
        self.set_font("helvetica", "Ib", 15)
        self.set_y(-25)
        self.cell(
            0,
            0,
            f"Résults from champions league 2024-2025 : page {self.page_no()}/{self.total_pages}",
            align="C",
            ln=1,
        )
        self.set_text_color(r=255, g=215, b=0)
        self.set_y(-15)
        self.cell(
            0,
            0,
            f"made with love by :".capitalize() + "Ulrich/Amine/Alain",
            align="C",
            ln=1,
        )

    def export(self) -> None:
        self.output("data/tirages.pdf")
        print("draw done successfully!!!")

    def generate(self):

        if not len(self.tirages):
            raise Exception("cannot generate PDF from empty tirage")

        j = 0  # index of club

        for club, matches in self.tirages.items():

            i = 0  # index for image

            if j % self.per_page == 0:
                self.add_page(orientation="P", same=False)
                self.set_text_color(r=255, g=255, b=255)
                self.image(
                    name=path("logos/bg.jpg"), x=0, y=0, w=self.w, h=self.h, type="jpg"
                )
                j = 0

            if self.get_logo(name=club):
                self.image(
                    name=path(name=f"logos/{self.get_logo(name=club)}"),
                    x=(self.w - self.img_w * 1.2) / 2,
                    y=self.img_target_x
                    + (self.img_h * 1.2 + self.e + self.cell_h - 10) * j,
                    w=self.img_w * 1.2,
                    h=self.img_h * 1.2,
                    type="png",
                )

            self.ln(self.e)
            self.set_font("helvetica", "b", 15)
            self.cell(0, self.e, club.upper(), border=self.border, ln=1, align="C")

            for _, match in matches.items():
                self.image(
                    name=path(name=f"logos/{match['home']['logo']}"),
                    x=self.img_x + (self.img_w + self.e) * i,
                    y=self.img_y + (self.cell_h + self.e * 2) * j,
                    w=self.img_w,
                    h=self.img_h,
                    alt_text=match["home"]["nom"],
                    title=match["home"]["nom"],
                    type="png",
                )  # image

                if i != 0:
                    self.cell(self.e, self.cell_h, "", border=self.border)

                self.cell(
                    self.cell_w, self.cell_h, "home", border=self.border, align="C"
                )

                i += 1

                self.image(
                    name=path(name=f"logos/{match['away']['logo']}"),
                    x=self.img_x + (self.img_w + self.e) * i,
                    y=self.img_y + (self.cell_h + self.e * 2) * j,
                    w=self.img_w,
                    h=self.img_h,
                    type="png",
                    alt_text=match["home"]["nom"],
                    title=match["home"]["nom"],
                )  # image

                self.cell(self.e, self.cell_h, "", border=self.border)

                self.cell(
                    self.cell_w,
                    self.cell_h,
                    "away",
                    border=self.border,
                    align="C",
                    ln=0 if i != 7 else 1,
                )

                i += 1
            j += 1
