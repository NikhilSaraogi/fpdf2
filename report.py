from fpdf import FPDF
from datetime import datetime ,timezone
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

title = 'Maintenance Report'

class PDF(FPDF):       
    def header(self):
        # Logo
        #self.image('pulse.png', 180, 8, 25)
        self.set_font('helvetica', 'B', 18)
       
        # Calculate width of title and position
        title_w = self.get_string_width(title) + 6
       
        #doc_w = self.w 
        #self.set_x((doc_w - title_w) / 2) # fixing title into center
        # colors of frame, background, and text
        self.set_draw_color(255, 255, 255) # border = black
        self.set_fill_color(255, 255, 255) # background = white
        self.set_text_color(0, 0, 0) # text = white
        # Thickness of frame (border)
        #self.set_line_width(0.5)
        # Title
        self.cell(title_w, 10, title, border=1, ln=1, align='C', fill=1)
        self.cell(90, 10, " ", 0, 2, 'C')
        #line between two points.
        #self.set_font('helvetica', '', 8)
        self.set_draw_color(0,0,0) # border = black
        self.line(0, 35, 220, 35)
        # Line break
        self.ln(15)
    
    # Page footer
    def footer(self):
        # Set position of the footer
        self.set_y(-15)
        # set font
        self.set_font('helvetica', '', 8)
        self.set_fill_color(224,224,224)
        self.line(0, 265, 220, 265)
        # Set font color grey
        self.set_text_color(0, 0, 0) #color-Black
        # Page number
        self.cell(0, 10, f'Page No: {self.page_no()}', align='R')
        self.cell(-200)
        #fetching date and time
        current_datetime = datetime.now()
        # current_datetime = datetime.now(timezone.utc)
        # print(current_datetime)
        # self.creation_date = current_datetime.strftime('%x %X')
        date_string=current_datetime.strftime('%x %X')
        # print(current_datetime)
        self.cell(0,10,f'Report Generated on {date_string} (UTC Time)',align='L')
    
    def will_page_break(self, height):
        #Returns: a boolean indicating if a page break would occur
        return (
            # ensure that there is already some content on the page:
            self.y > self.t_margin
            and self.y + height > self.page_break_trigger
            and not self.in_footer
            and self.accept_page_break
        )

#to generate the table from dataset
def output_df_to_pdf(pdf, df):
    # A cell is a rectangular area, possibly framed, which contains some text
    # Set the width and height of cell
    table_cell_width = 28
    table_cell_height = 8
    cols = df.columns
    render_table_header(df)
    # Loop over to print each data in the table
    for row in df.itertuples():
        if pdf.will_page_break(table_cell_height):
            render_table_header(df)
        for col in cols:
            pdf.set_font('Arial', '', 5)
            value = str(getattr(row, col))
            pdf.cell(table_cell_width, table_cell_height, value, align='C', border=1)
        pdf.ln(table_cell_height)


def render_table_header(df):
    table_cell_width = 28
    table_cell_height = 8
    # Select a font as Arial, bold, 10
    pdf.set_font('Arial', 'B', 8)
    
    # Loop over to print column names
    cols = df.columns
    for col in cols:
        pdf.cell(table_cell_width, table_cell_height, col, align='C', border=1)
    # Line break
    pdf.ln(table_cell_height)


# Create a PDF object
pdf = PDF('P', 'mm', 'Letter')

# get total page numbers
pdf.alias_nb_pages()

# Set auto page break
pdf.set_auto_page_break(auto = True, margin = 15)

# Add Page
pdf.add_page()

# Remember to always put one of these at least once.
pdf.set_font('Times','',10.0) 
 
# Effective page width, or just epw
epw = pdf.w - 2*pdf.l_margin
 
# Set column width to 1/4 of effective page width to distribute content 
# evenly across table and page
col_width = epw/4


th = pdf.font_size
 
pdf.set_font('Times','B',14.0) 
pdf.cell(epw, 10 , 'INCIDENT REPORT', align='C')
pdf.set_font('Times','',10.0) 
pdf.ln(10)
 
df = pd.DataFrame({"A":np.random.randint(0,100,size=1000),"B":np.random.randint(0,100,size=1000),"C":np.random.randint(0,100,size=1000),"D":np.random.randint(0,100,size=1000)})

vals = df.values
data=vals.tolist()

df = pd.DataFrame(np.random.randint(0,1000,size=(100, 4)), columns=list('ABCD'))
df.columns = ['A', 'B', 'C', 'D']

output_df_to_pdf(pdf, df)


# Here we add more padding by passing 2*th as height
for row in data:
    for datum in row:
        # Enter data in colums
        pdf.cell(col_width, 2*th, str(datum), border=1)
 
    pdf.ln(2*th)



pdf.ln(10)
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

pdf.ln(20)
pdf.set_font('Times','B',14.0) 
pdf.cell(epw, 5 , 'My plots', align='C')
pdf.cell(50, 10, "", 0, 2, 'C')
pdf.image('1.area.png', x = 40, y = 80,  w=150, h=100)



pdf.ln(10)
pdf.set_font('Times','B',14.0) 
pdf.cell(epw, 5 , 'My plots', align='C')
pdf.cell(30, 5, " ", 0, 2, 'C')
pdf.ln(10)
df.plot.area()
plt.savefig('1.area.png')
# pdf.image('chart.png', x = 40, y = 80, w=150, h=100)
pdf.image('1.area.png',  w=200, h=100)



pdf.ln(10)
pdf.set_font('Times','B',14.0) 
pdf.cell(epw, 5 , 'My plots', align='C')
pdf.cell(30, 5, " ", 0, 2, 'C')
pdf.ln(10)
df.plot()
plt.savefig('2.plot.png')
pdf.image('2.plot.png',  w=200, h=100)

pdf.ln(10)
pdf.set_font('Times','B',14.0) 
pdf.cell(epw, 5 , 'My plots', align='C')
pdf.cell(30, 5, " ", 0, 2, 'C')
pdf.ln(10)
df.sum().plot.bar()
plt.savefig('3.sum.png')
pdf.image('3.sum.png',  w=200, h=100)




pdf.output('Report.pdf')

