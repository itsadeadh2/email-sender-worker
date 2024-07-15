import pdfkit


class ResumeProvider:
    def __init__(self, logger):
        self.__logger = logger

    def retrieve(self) -> tuple:
        resume_path = '/tmp/resume.pdf'
        self.__logger.info(f"Downloading resume from {resume_path}")
        resume_page = "https://resume.itsadeadh2.com"
        pdfkit_config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
        pdfkit.from_url(resume_page, resume_path, configuration=pdfkit_config)

        return 'resume.pdf', open(resume_path, 'rb')


if __name__ == "__main__":
    ResumeProvider(None).retrieve()
