from sponsorcheck.domain.models import ClassificationResponse
from sponsorcheck.reports.html_renderer import HTMLRenderer
import pdfkit
import io

def generate_pdf(data: ClassificationResponse) -> bytes:
    html_renderer = HTMLRenderer()
    html_content = html_renderer.render(data)
    
    # Generate PDF from HTML string using wkhtmltopdf
    pdf_bytes = pdfkit.from_string(html_content, False)
    
    return pdf_bytes
