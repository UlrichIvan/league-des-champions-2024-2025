from fpdf import FPDF
from utils import path, HOME, AWAY, load_json, tirages_path_json, draw_pdf_path
from backend.Draw import Draw


# Créer une classe qui hérite de FPDF
class PDF(FPDF):

    def __init__(self, draw: Draw, json_teams: list):

        super().__init__()

        self.__tirages = []

        self.__json_teams = json_teams

        self.__per_page = 4

        self.__total_pages = 0

        self.__img_target_init_pos_y = 3
        self.__cell_w = 15
        self.__cell_h = 38
        self.__img_w = 15
        self.__img_h = 15
        self.__img_x = 10
        self.__img_y = 32
        self.__e = 10
        self.__border = 0

        # get draw instance
        self.__draw = draw

    # ================== properties instances ==================

    @property
    def draw(self) -> Draw:
        return self.__draw

    @draw.setter
    def draw(self, value: Draw) -> None:
        self.__draw = value

    @property
    def per_page(self) -> int:
        """number of clubs by page

        Returns:
            int: clubs by page
        """
        return self.__per_page

    @property
    def total_pages(self) -> int:
        """total page for PDF documents

        Returns:
            int: number of PDF pages
        """
        return self.__total_pages

    @total_pages.setter
    def total_pages(self, value: int) -> None:
        self.__total_pages = value

    @property
    def border(self) -> int:
        """display or hide border on pdf

        Returns:
            int: 1 to show border. 0 to hide border
        """
        return self.__border

    @border.setter
    def border(self, value: int) -> None:
        self.__border = value

    @property
    def e(self) -> float:
        """default width of space for new line

        Returns:
            float: width of space for new line
        """
        return self.__e

    @e.setter
    def e(self, value: float) -> None:
        self.__e = value

    @property
    def img_y(self) -> float:
        """default y position of logo on pdf

        Returns:
            float: y position of logo
        """
        return self.__img_y

    @img_y.setter
    def img_y(self, value: float) -> None:
        self.__img_y = value

    @property
    def img_x(self) -> float:
        """default x position of logo on pdf

        Returns:
            float: x position of logo
        """
        return self.__img_x

    @img_x.setter
    def img_x(self, value: float) -> None:
        self.__img_x = value

    @property
    def img_h(self) -> float:
        """height of each club logo

        Returns:
            float: height of club logo
        """
        return self.__img_h

    @img_h.setter
    def img_h(self, value: float) -> None:
        self.__img_h = value

    @property
    def img_w(self) -> float:
        """width of each club logo

        Returns:
            float: width of club logo
        """
        return self.__img_w

    @img_w.setter
    def img_w(self, value: float) -> None:
        self.__img_w = value

    @property
    def cell_h(self) -> float:
        """height of ceil for each image

        Returns:
            float: height ceil image
        """
        return self.__cell_h

    @cell_h.setter
    def cell_h(self, value: float) -> None:
        self.__cell_h = value

    @property
    def cell_w(self) -> float:
        """width of ceil for each image

        Returns:
            float: width ceil of image
        """
        return self.__cell_w

    @cell_w.setter
    def cell_w(self, value: float) -> None:
        self.__cell_w = value

    @property
    def img_target_init_pos_y(self) -> float:
        """init y position of central target image

        Returns:
            float: default y position of target central image
        """
        return self.__img_target_init_pos_y

    @img_target_init_pos_y.setter
    def img_target_init_pos_y(self, value: float) -> None:
        self.__img_target_init_pos_y = value

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

    # ================== properties instances ==================

    def __get_logo(self, name: str) -> str | None:
        """return the logo of name found for team name

        Args:
            name (str): name of team. example : PSG

        Returns:
            str | None: the name of logo if found. None if not found
        """
        logo = None
        for club in self.json_teams:
            if club["nom"] == name:
                logo = club["logo"]
                break
        return logo

    def footer(self):
        """redefine method from parent class FPDF  to display a custom footer for each page into PDF"""
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
            f"made with love by : ".capitalize() + "Ulrich",
            align="C",
            ln=1,
        )

    def export(self) -> None:
        """export json file to pdf"""
        self.output(draw_pdf_path)
        print("PDF exported successfully!!!")

    def __set_team_target_header(self, row_index: int, team_name: str) -> int:
        """set top team as center header on pdf

        Args:
            row_index (int): index on row on pdf
            team_name (str): name of team target

        Returns:
            int: current row index modified if necessary
        """
        index = row_index
        if row_index % self.per_page == 0:
            self.add_page(orientation="P", same=False)
            self.set_text_color(r=255, g=255, b=255)
            self.image(
                name=path("logos/bg.jpg"), x=0, y=0, w=self.w, h=self.h, type="jpg"
            )
            index = 0

        if self.__get_logo(name=team_name):
            self.image(
                name=path(name=f"logos/{self.__get_logo(name=team_name)}"),
                x=(self.w - self.img_w * 1.2) / 2,
                y=self.img_target_init_pos_y
                + (self.img_h * 1.2 + self.e + self.cell_h - 10) * index,
                w=self.img_w * 1.2,
                h=self.img_h * 1.2,
                type="png",
            )

        self.ln(self.e)
        self.set_font("helvetica", "b", 15)
        self.cell(0, self.e, team_name.upper(), border=self.border, ln=1, align="C")

        return index

    def __set_team_opponents(self, row_index: int, matches: dict) -> None:
        """set all match for current team for team

        Args:
            row_index (int): row index on pdf
            matches (dict): all match for current team
        """
        i = 0  # index of image
        for _, match in matches.items():
            # draw the home image

            self.image(
                name=path(name=f"logos/{match['home']['logo']}"),
                x=self.img_x + (self.img_w + self.e) * i,
                y=self.img_y + (self.cell_h + self.e * 2) * row_index,
                w=self.img_w,
                h=self.img_h,
                alt_text=match[HOME]["name"],
                title=match[HOME]["name"],
                type="png",
            )  # image

            if i != 0:
                # move cursor to the next line to write the location
                self.cell(self.e, self.cell_h, "", border=self.border)
            # write first location(home)
            self.cell(self.cell_w, self.cell_h, HOME, border=self.border, align="C")

            i += 1  # increment for the next image(away)
            # draw the away image

            self.image(
                name=path(name=f"logos/{match[AWAY]['logo']}"),
                x=self.img_x + (self.img_w + self.e) * i,
                y=self.img_y + (self.cell_h + self.e * 2) * row_index,
                w=self.img_w,
                h=self.img_h,
                type="png",
                alt_text=match[AWAY]["name"],
                title=match[AWAY]["name"],
            )  # image

            # write the second loaction name (away)
            self.cell(self.e, self.cell_h, "", border=self.border)

            # draw the next space for next row
            self.cell(
                self.cell_w,
                self.cell_h,
                AWAY,
                border=self.border,
                align="C",
                ln=(
                    0 if i != 7 else 1
                ),  # write on the same row or the bottom of the las image
            )
            i += 1

    def generate(self):
        """make draw and generate pdf for draw mad

        Raises:
            Exception: if results of tirage is empty
        """
        # make draw and generate json file
        self.draw.make_draw()

        # set json file generate by draw class instance
        self.tirages = load_json(path=tirages_path_json)

        # compute total page for pdf
        self.total_pages = (
            int(len(self.tirages.keys()) / self.per_page)
            if len(self.tirages.keys()) % self.per_page == 0
            else int(len(self.tirages.keys()) / self.per_page) + 1
        )

        if not len(self.tirages):
            raise Exception("cannot generate PDF from empty draw")

        print("generate PDF...", end="\n")

        j = 0  # index of club

        for club, matches in self.tirages.items():
            j = self.__set_team_target_header(row_index=j, team_name=club)
            self.__set_team_opponents(row_index=j, matches=matches)
            j += 1

        print("pdf generated successfully!!!")
        print("exporting pdf...")
