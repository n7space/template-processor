"""

Markdown to DOCX conversion module extracted from md2docx-python project.

Project address: https://github.com/shloktech/md2docx-python/
Project LICENSE: LICENSE.MD2DOCX

The reason for extraction is to align the API and features with the needs.
Changes:
- input is text, not file
- markdown2 is used instead of markdown
- table support is added via markdown2 extras and additional HTML processing

"""

import markdown2
from docx import Document
from bs4 import BeautifulSoup


def markdown_to_word(markdown_source, word_file_path):
    # Converting Markdown to HTML
    html_content = markdown2.markdown(markdown_source, extras=["tables", "wiki-tables"])

    # Creating a new Word Document
    doc = Document()

    # Converting HTML to text and add it to the Word Document
    soup = BeautifulSoup(html_content, "html.parser")

    # Adding content to the Word Document
    for element in soup:
        if element.name == "h1":
            doc.add_heading(element.text, level=1)
        elif element.name == "h2":
            doc.add_heading(element.text, level=2)
        elif element.name == "h3":
            doc.add_heading(element.text, level=3)
        elif element.name == "p":
            paragraph = doc.add_paragraph()
            for child in element.children:
                if child.name == "strong":
                    paragraph.add_run(child.text).bold = True
                elif child.name == "em":
                    paragraph.add_run(child.text).italic = True
                else:
                    paragraph.add_run(child)
        elif element.name == "ul":
            for li in element.find_all("li"):
                doc.add_paragraph(li.text.strip(), style="List Bullet")
        elif element.name == "ol":
            for li in element.find_all("li"):
                doc.add_paragraph(li.text.strip(), style="List Number")
        elif element.name == "table":
            rows_data = []
            for row in element.find_all("tr"):
                cells = row.find_all(["th", "td"])
                row_data = [cell.get_text(strip=True) for cell in cells]
                if row_data:
                    rows_data.append(row_data)

            if rows_data:
                columns_count = len(rows_data[0])
                table = doc.add_table(rows=len(rows_data), cols=columns_count)
                table.style = "Table Grid"

                for row_index, row_data in enumerate(rows_data):
                    for column_index, cell_text in enumerate(row_data):
                        if column_index < columns_count:
                            table.rows[row_index].cells[column_index].text = cell_text

                # Make the first row bold if it is a header
                first_row = element.find("tr")
                if first_row and first_row.find("th"):
                    for cell in table.rows[0].cells:
                        for paragraph in cell.paragraphs:
                            for run in paragraph.runs:
                                run.bold = True

    doc.save(word_file_path)
