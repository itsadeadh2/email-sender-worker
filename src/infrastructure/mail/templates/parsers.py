from abc import ABC
from jinja2 import Environment, FileSystemLoader
import pathlib
from pydantic import BaseModel, HttpUrl, validator
from typing import Optional


# Schemas
class LinksModel(BaseModel):
    email: str
    github: HttpUrl
    website: HttpUrl
    linkedin: HttpUrl
    whatsapp: HttpUrl
    resume: Optional[str] = ""

    @validator('resume', pre=True, always=True)
    def set_default_resume(cls, v):
        return v or ""


class ContactInfoModel(BaseModel):
    greeting: str
    message: str
    links: LinksModel


# Parsers
class Parser(ABC):
    def __init__(self, template_name, file_system_path=None):
        path = file_system_path or pathlib.Path(__file__).parent.resolve()
        env = Environment(loader=FileSystemLoader(path))
        self.template = env.get_template(template_name)

    def get_html(self):
        pass

    def get_text(self):
        pass


class ContactInfoParser(Parser):

    default_contact_info = ContactInfoModel(
        greeting="Hi,",
        message="Thank you for reaching out to me. I'm excited to connect with you and provide you with all my relevant contact details. <br/>"
                "Below, you will find my contact information along with some additional details that might interest you. Additionally, I have attached my resume for your review.",
        links=LinksModel(
            email="itsadeadh2@gmail.com",
            github="https://github.com/itsadeadh2",
            website="https://itsadeadh2.com",
            linkedin="https://www.linkedin.com/in/barbosathiagodev/",
            whatsapp="https://api.whatsapp.com/send?phone=5569992219034",
            resume=""
        )
    )

    def __init__(self, data_override=None):
        if data_override is None:
            data_override = {}
        email_data = {**self.default_contact_info.model_dump(), **data_override}
        self.validated_data = ContactInfoModel(**email_data)
        super().__init__(template_name='contact_info.html')

    def get_html(self, data_override=None):
        if data_override is None:
            data_override = {}
        return self.template.render(email=self.validated_data.model_dump())

    def get_text(self, data_override=None):
        if data_override is None:
            data_override = {}
        dict_data = self.validated_data.model_dump()
        text = dict_data.get('greeting')
        text += '\n\n'
        text += dict_data.get('message')
        text += '\n\n'
        for key, value in dict_data.get('links').items():
            text += f'{key}: {value}\n'

        text += '\n'
        text += 'Thiago Barbosa'
        return text
