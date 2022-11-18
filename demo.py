# simple_demo.py
from fpdf import FPDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Welcome to Python!", align="C")
pdf.output("simple_demo.pdf")
