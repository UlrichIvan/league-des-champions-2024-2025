from fpdf import FPDF


# Créer une classe qui hérite de FPDF
class PDF(FPDF):

    def __init__(self):
        # call super() function
        super().__init__()


pdf = PDF()

pdf.add_page("P")

pdf.set_font("helvetica", "BU", 20)

pdf.cell(0, 0, "Ligue des champions!", align="C")

pdf.output("data/a.pdf")
