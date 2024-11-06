from fpdf import FPDF


# Créer une classe qui hérite de FPDF
class PDF(FPDF):

    def __init__(self):
        super().__init__()

        self.add_page("P")

        self.set_font("helvetica", "BU", 20)

        self.cell(0, 0, "Résultats de la Ligue des champions 2024-2025", align="C")

    def export(self) -> None:
        self.output("data/tirages.pdf")
        print("export done successfully!!!")
