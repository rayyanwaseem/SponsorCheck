from jinja2 import Environment, FileSystemLoader
import os
from sponsorcheck.domain.models import ClassificationResponse

class HTMLRenderer:
    def __init__(self):
        templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.env = Environment(loader=FileSystemLoader(templates_dir))
        
    def render(self, data: ClassificationResponse) -> str:
        template = self.env.get_template('report.html')
        return template.render(data=data)
