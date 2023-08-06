__version__ = "0.1.0"

import click
import os
import re
from PyPDF2 import PdfFileReader, PdfFileWriter


@click.command()
@click.argument("input_file", nargs=1, type=click.File("rb"))
@click.argument("output_path", nargs=-1, type=click.Path(exists=True))
def split_pdf(input_file, output_path):
    if output_path:
        output_path = output_path[0]
    else:
        output_path = os.path.dirname(input_file.name)
    identifier_regex = os.getenv("SPLITPDF_IDENTIFIER_REGEX")
    if identifier_regex:
        identifier_regex = r"{0}".format(identifier_regex)
        identifier_pattern = re.compile(identifier_regex, re.IGNORECASE)
    fname = os.path.splitext(os.path.basename(input_file.name))[0]
    pdf = PdfFileReader(input_file)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))
        if identifier_regex:
            page_text = pdf.getPage(page).extractText()
            match = identifier_pattern.search(page_text)
            identifier = "{}_".format(match.group().strip())
        else:
            identifier = ""
        output_filename = "{}_{}page_{}.pdf".format(fname, identifier, page + 1)
        output_file_path = os.path.join(click.format_filename(output_path), output_filename)
        with open(output_file_path, "wb") as out:
            pdf_writer.write(out)
        print("Created: {}".format(output_file_path))


if __name__ == "__main__":
    split_pdf()
