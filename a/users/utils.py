from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import shutil

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        write_bytesio_to_file("out.pdf", pdf)
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

# Initialie our BytesIO

def write_bytesio_to_file(filename, bytesio):
    """
    Write the contents of the given BytesIO to a file.
    Creates the file or overwrites the file if it does
    not exist yet.
    """
    with open(filename, "wb") as outfile:
        outfile.write(bytesio.getbuffer())
