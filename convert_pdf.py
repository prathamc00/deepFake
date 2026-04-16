# -*- coding: utf-8 -*-
import markdown
from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font('helvetica', size=12)

with open('Deepfake_Detection_Research_Paper.md', 'r', encoding='utf-8') as f:
    text = f.read()

replacements = {
    '–': '-',
    '—': '-',
    '“': '\"',
    '”': '\"',
    '’': '\'',
    '‘': '\'',
    'ö': 'o',
    'ß': 'ss',
}
for k, v in replacements.items():
    text = text.replace(k, v)

html = markdown.markdown(text, extensions=['tables'])

try:
    pdf.write_html(html)
    pdf.output('Deepfake_Detection_Research_Paper.pdf')
    print('PDF Created successfully.')
except Exception as e:
    print('Error:', e)
