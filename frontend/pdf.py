from fpdf import FPDF
from utils import path


# Créer une classe qui hérite de FPDF
class PDF(FPDF):

    def __init__(self, tirages: dict):

        super().__init__()

        self.__tirages = tirages

        self.add_page("P")

    def header(self):
        # Select Arial bold 15
        self.set_font("helvetica", "Ib", 15)

        self.cell(0, 0, "Résults from champions league 2024-2025", align="C")

        self.ln(20)

    @property
    def tirages(self) -> dict:
        return self.__tirages

    @tirages.setter
    def tirages(self, value: dict) -> None:
        self.__tirages = value

    def export(self) -> None:
        self.output("data/tirages.pdf")
        print("export done successfully!!!")

    def generate(self):
        if not len(self.tirages):
            print("cannot generate PDF from empty tirage")

        

        self.tirages = {
            "Manchester City": {
                "pot_1": {
                    "home": {
                        "nom": "PSG",
                        "pays": "France",
                        "championnat": "Ligue 1",
                        "chapeau": 1,
                        "logo": "Paris_Saint-Germain.png",
                    },
                    "away": {
                        "nom": "FC Barcelone",
                        "pays": "Espagne",
                        "championnat": "La Liga",
                        "chapeau": 1,
                        "logo": "Logo_FC_Barcelona.png",
                    },
                },
                "pot_2": {
                    "home": {
                        "nom": "Club Bruges",
                        "pays": "Belgique",
                        "championnat": "Jupiler Pro League",
                        "chapeau": 2,
                        "logo": "Club_Brugge.png",
                    },
                    "away": {
                        "nom": "Juventus Turin",
                        "pays": "Italie",
                        "championnat": "Serie A",
                        "chapeau": 2,
                        "logo": "Juventus_FC.png",
                    },
                },
                "pot_3": {
                    "home": {
                        "nom": "Celtic",
                        "pays": "Écosse",
                        "championnat": "Scottish Premiership",
                        "chapeau": 3,
                        "logo": "Celtic_fc.png",
                    },
                    "away": {
                        "nom": "PSV Eindhoven",
                        "pays": "Pays-Bas",
                        "championnat": "Eredivisie",
                        "chapeau": 3,
                        "logo": "psv_eindhoven.png",
                    },
                },
                "pot_4": {
                    "home": {
                        "nom": "Sturm Graz",
                        "pays": "Autriche",
                        "championnat": "Bundesliga Autrichienne",
                        "chapeau": 4,
                        "logo": "SK_Sturm_Graz.png",
                    },
                    "away": {
                        "nom": "Slovan Bratislava",
                        "pays": "Slovaquie",
                        "championnat": "Fortuna Liga",
                        "chapeau": 4,
                        "logo": "Slovan_Bratislava.png",
                    },
                },
            },
            "Bayern Munich": {
                "pot_1": {
                    "home": {
                        "nom": "FC Barcelone",
                        "pays": "Espagne",
                        "championnat": "La Liga",
                        "chapeau": 1,
                        "logo": "Logo_FC_Barcelona.png",
                    },
                    "away": {
                        "nom": "PSG",
                        "pays": "France",
                        "championnat": "Ligue 1",
                        "chapeau": 1,
                        "logo": "Paris_Saint-Germain.png",
                    },
                },
                "pot_2": {
                    "home": {
                        "nom": "Benfica Lisbonne",
                        "pays": "Portugal",
                        "championnat": "Primeira Liga",
                        "chapeau": 2,
                        "logo": "SLB.png",
                    },
                    "away": {
                        "nom": "Shakhtar Donetsk",
                        "pays": "Ukraine",
                        "championnat": "Premyer-Liha",
                        "chapeau": 2,
                        "logo": "FC_Shakhtar_Donetsk.png",
                    },
                },
                "pot_3": {
                    "home": {
                        "nom": "Étoile Rouge de Belgrade",
                        "pays": "Serbie",
                        "championnat": "SuperLiga",
                        "chapeau": 3,
                        "logo": "crvena-zvezda.png",
                    },
                    "away": {
                        "nom": "Feyenoord Rotterdam",
                        "pays": "Pays-Bas",
                        "championnat": "Eredivisie",
                        "chapeau": 3,
                        "logo": "Feyenoord_Rotterdam.png",
                    },
                },
                "pot_4": {
                    "home": {
                        "nom": "Stade Brestois",
                        "pays": "France",
                        "championnat": "Ligue 1",
                        "chapeau": 4,
                        "logo": "SB29.png",
                    },
                    "away": {
                        "nom": "Bologne",
                        "pays": "Italie",
                        "championnat": "Serie A",
                        "chapeau": 4,
                        "logo": "Bologna_FC.png",
                    },
                },
            },
            "Real Madrid": {
                "pot_1": {
                    "home": {
                        "nom": "RB Leipzig",
                        "pays": "Allemagne",
                        "championnat": "Bundesliga",
                        "chapeau": 1,
                        "logo": "RB_Leipzig.png",
                    },
                    "away": {
                        "nom": "Liverpool",
                        "pays": "Angleterre",
                        "championnat": "Premier League",
                        "chapeau": 1,
                        "logo": "liverpool.png",
                    },
                },
                "pot_2": {
                    "home": {
                        "nom": "Bayer Leverkusen",
                        "pays": "Allemagne",
                        "championnat": "Bundesliga",
                        "chapeau": 2,
                        "logo": "Bayer_04_Leverkusen.png",
                    },
                    "away": {
                        "nom": "Club Bruges",
                        "pays": "Belgique",
                        "championnat": "Jupiler Pro League",
                        "chapeau": 2,
                        "logo": "Club_Brugge.png",
                    },
                },
                "pot_3": {
                    "home": {
                        "nom": "Lille",
                        "pays": "France",
                        "championnat": "Ligue 1",
                        "chapeau": 3,
                        "logo": "LOSC_Lille.png",
                    },
                    "away": {
                        "nom": "Celtic",
                        "pays": "Écosse",
                        "championnat": "Scottish Premiership",
                        "chapeau": 3,
                        "logo": "Celtic_fc.png",
                    },
                },
                "pot_4": {
                    "home": {
                        "nom": "Aston Villa",
                        "pays": "Angleterre",
                        "championnat": "Premier League",
                        "chapeau": 4,
                        "logo": "Aston_Villa.png",
                    },
                    "away": {
                        "nom": "Sturm Graz",
                        "pays": "Autriche",
                        "championnat": "Bundesliga Autrichienne",
                        "chapeau": 4,
                        "logo": "SK_Sturm_Graz.png",
                    },
                },
            },
            "PSG": {
                "pot_1": {
                    "home": {
                        "nom": "Bayern Munich",
                        "pays": "Allemagne",
                        "championnat": "Bundesliga",
                        "chapeau": 1,
                        "logo": "bayern_munich.png",
                    },
                    "away": {
                        "nom": "Manchester City",
                        "pays": "Angleterre",
                        "championnat": "Premier League",
                        "chapeau": 1,
                        "logo": "manchester-city.png",
                    },
                },
                "pot_2": {
                    "home": {
                        "nom": "Atlético de Madrid",
                        "pays": "Espagne",
                        "championnat": "La Liga",
                        "chapeau": 2,
                        "logo": "Logo_Atletico.png",
                    },
                    "away": {
                        "nom": "Bayer Leverkusen",
                        "pays": "Allemagne",
                        "championnat": "Bundesliga",
                        "chapeau": 2,
                        "logo": "Bayer_04_Leverkusen.png",
                    },
                },
                "pot_3": {
                    "home": {
                        "nom": "Dinamo Zagreb",
                        "pays": "Croatie",
                        "championnat": "Prva HNL",
                        "chapeau": 3,
                        "logo": "Dinamo_Zagreb.png",
                    },
                    "away": {
                        "nom": "Étoile Rouge de Belgrade",
                        "pays": "Serbie",
                        "championnat": "SuperLiga",
                        "chapeau": 3,
                        "logo": "crvena-zvezda.png",
                    },
                },
                "pot_4": {
                    "home": {
                        "nom": "Bologne",
                        "pays": "Italie",
                        "championnat": "Serie A",
                        "chapeau": 4,
                        "logo": "Bologna_FC.png",
                    },
                    "away": {
                        "nom": "Stuttgart",
                        "pays": "Allemagne",
                        "championnat": "Bundesliga",
                        "chapeau": 4,
                        "logo": "VfB_Stuttgart_1893.png",
                    },
                },
            },
            "Liverpool": {
                "pot_1": {
                    "home": {
                        "nom": "Real Madrid",
                        "pays": "Espagne",
                        "championnat": "La Liga",
                        "chapeau": 1,
                        "logo": "Real_madrid.png",
                    },
                    "away": {
                        "nom": "Borussia Dortmund",
                        "pays": "Allemagne",
                        "championnat": "Bundesliga",
                        "chapeau": 1,
                        "logo": "Borussia_Dortmund.png",
                    },
                },
                "pot_2": {
                    "home": {
                        "nom": "AC Milan",
                        "pays": "Italie",
                        "championnat": "Serie A",
                        "chapeau": 2,
                        "logo": "AC_Milan.png",
                    },
                    "away": {
                        "nom": "Atlético de Madrid",
                        "pays": "Espagne",
                        "championnat": "La Liga",
                        "chapeau": 2,
                        "logo": "Logo_Atletico.png",
                    },
                },
                "pot_3": {
                    "home": {
                        "nom": "PSV Eindhoven",
                        "pays": "Pays-Bas",
                        "championnat": "Eredivisie",
                        "chapeau": 3,
                        "logo": "psv_eindhoven.png",
                    },
                    "away": {
                        "nom": "RB Salzbourg",
                        "pays": "Autriche",
                        "championnat": "Bundesliga Autrichienne",
                        "chapeau": 3,
                        "logo": "FC_Salzburg_logo.png",
                    },
                },
                "pot_4": {
                    "home": {
                        "nom": "Stuttgart",
                        "pays": "Allemagne",
                        "championnat": "Bundesliga",
                        "chapeau": 4,
                        "logo": "VfB_Stuttgart_1893.png",
                    },
                    "away": {
                        "nom": "Gérone",
                        "pays": "Espagne",
                        "championnat": "La Liga",
                        "chapeau": 4,
                        "logo": "Logo_Girona_FC.png",
                    },
                },
            },
            "Inter Milan": {
                "pot_1": {
                    "home": {
                        "nom": "Borussia Dortmund",
                        "pays": "Allemagne",
                        "championnat": "Bundesliga",
                        "chapeau": 1,
                        "logo": "Borussia_Dortmund.png",
                    },
                    "away": {
                        "nom": "RB Leipzig",
                        "pays": "Allemagne",
                        "championnat": "Bundesliga",
                        "chapeau": 1,
                        "logo": "RB_Leipzig.png",
                    },
                },
                "pot_2": {
                    "home": {
                        "nom": "Shakhtar Donetsk",
                        "pays": "Ukraine",
                        "championnat": "Premyer-Liha",
                        "chapeau": 2,
                        "logo": "FC_Shakhtar_Donetsk.png",
                    },
                    "away": {
                        "nom": "Arsenal",
                        "pays": "Angleterre",
                        "championnat": "Premier League",
                        "chapeau": 2,
                        "logo": "arsenal.png",
                    },
                },
                "pot_3": {
                    "home": {
                        "nom": "Feyenoord Rotterdam",
                        "pays": "Pays-Bas",
                        "championnat": "Eredivisie",
                        "chapeau": 3,
                        "logo": "Feyenoord_Rotterdam.png",
                    },
                    "away": {
                        "nom": "Young Boys",
                        "pays": "Suisse",
                        "championnat": "Super League",
                        "chapeau": 3,
                        "logo": "Young_Boys.png",
                    },
                },
                "pot_4": {
                    "home": {
                        "nom": "Slovan Bratislava",
                        "pays": "Slovaquie",
                        "championnat": "Fortuna Liga",
                        "chapeau": 4,
                        "logo": "Slovan_Bratislava.png",
                    },
                    "away": {
                        "nom": "AS Monaco",
                        "pays": "France",
                        "championnat": "Ligue 1",
                        "chapeau": 4,
                        "logo": "AS_Monaco.png",
                    },
                },
            },
        }

        cell_w = 15
        cell_h = 35
        img_w = img_h = 15
        img_x = 10
        img_y = 40
        e = 10
        border = 1

        j = 0  # index of club

        for club, matches in self.tirages.items():

            self.set_font("helvetica", "b", 15)

            self.cell(0, e, club.upper(), border=border, ln=1)  # club

            i = 0  # index for image

            for _, match in matches.items():
                self.image(
                    name=path(name=f"logos/{match['home']['logo']}"),
                    x=img_x + (img_w + e) * i,
                    y=img_y + (cell_h + e) * j,
                    w=img_w,
                    h=img_h,
                    alt_text=match["home"]["nom"],
                    title=match["home"]["nom"],
                    type="png",
                )  # image

                if i != 0:
                    self.cell(e, cell_h, "", border=border)

                self.cell(cell_w, cell_h, "home", border=border, align="C")

                i += 1

                self.image(
                    name=path(name=f"logos/{match['away']['logo']}"),
                    x=img_x + (img_w + e) * i,
                    y=img_y + (cell_h + e) * j,
                    w=img_w,
                    h=img_h,
                    type="png",
                    alt_text=match["home"]["nom"],
                    title=match["home"]["nom"],
                )  # image

                self.cell(e, cell_h, "", border=border)

                self.cell(
                    cell_w,
                    cell_h,
                    "away",
                    border=border,
                    align="C",
                    ln=0 if i != 7 else 1,
                )

                i += 1
            j += 1
