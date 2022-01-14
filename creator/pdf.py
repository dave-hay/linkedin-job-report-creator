from fpdf import FPDF

"""
d = today
t = title
c = company
lo = location
xp = text filepath
n = file name
cwdir = files cwd
"""


class PDF(FPDF):
    def header(self):
        # Setting font: helvetica bold 15
        self.set_font("helvetica", "B", 15)

    def footer(self):
        # Setting position at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "I", 8)
        # Setting text color to gray:
        self.set_text_color(128)
        # Printing page number
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def job_title(self, d, t, c, lo):
        self.set_font("helvetica", "B", 8)
        self.cell(0, 6, f'Date: {d}', 0, 1, 'R')
        self.ln(1)
        self.set_font("helvetica", "B", 15)
        self.cell(0, 6, f'Role: {t}', 0, 1, 'C')
        self.ln(4)
        self.cell(0, 6, f'Company: {c}', 0, 1, 'C')
        self.ln(4)
        self.cell(0, 6, f'Location: {lo}', 0, 1, 'C')
        self.ln(4)

    def job_body(self, xp, n, cwdir):
        with open(f"{cwdir}/{xp}", "rb") as fp:
            txt = fp.read().decode("latin-1")
        self.set_font('helvetica', size=12)
        self.multi_cell(0, 7, txt)
        self.ln()
        self.image(f'{cwdir}/docs/{n}.png', x=27, w=150)
        self.image(f'{cwdir}/docs/verb_{n}.png', x=27, w=150)
        self.image(f'{cwdir}/docs/noun_{n}.png', x=27, w=150)

    def print_job(self, d, t, c, lo, xp, n, cwdir):
        self.add_page()
        self.job_title(d, t, c, lo)
        self.job_body(xp, n, cwdir)


