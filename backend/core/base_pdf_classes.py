from abc import ABC, abstractmethod

from django.conf import settings
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.styles import (
    TA_RIGHT,
    ParagraphStyle,
    getSampleStyleSheet,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate


class BaseDocPortraitTemplate(SimpleDocTemplate):
    def __init__(
        self,
        filename,
        right_margin=10,
        left_margin=15,
        top_margin=10,
        bottom_margin=5,
        pagesize=portrait(A4),
        **kw,
    ):
        super().__init__(filename, **kw)
        self.rightMargin = right_margin
        self.leftMargin = left_margin
        self.topMargin = top_margin
        self.bottomMargin = bottom_margin
        self.pagesize = pagesize

        pdfmetrics.registerFont(
            TTFont(
                'OpenSans',
                settings.BASE_DIR / 'static/fonts/OpenSans-Regular.ttf',
            )
        )
        pdfmetrics.registerFont(
            TTFont(
                'OpenSans-Bold',
                settings.BASE_DIR / 'static/fonts/OpenSans-Bold.ttf',
            )
        )


class BaseDocsPDF(ABC):
    COLORS_BLACK_COLOR = (0, 0, 0)
    styles = getSampleStyleSheet()

    def __init__(self, buffer):
        self.buffer = buffer
        self.__create_styles()

    def __create_styles(self):
        self.NORMAL_STYLE = ParagraphStyle(
            name='doc_header',
            fontName='OpenSans',
            fontSize=9,
            leading=14,
        )
        self.BOLD_STYLE = ParagraphStyle(
            name='BOLD_STYLE',
            fontName='OpenSans-Bold',
            fontSize=12,
            leading=18,
        )
        self.RIGHT_HEADER_STYLE = ParagraphStyle(
            name='Header',
            fontName='OpenSans',
            fontSize=8,
            leading=14,
            alignment=TA_RIGHT,
        )
        self.LIST_STYLE = ParagraphStyle(
            name='ListStyle',
            fontName='OpenSans',
            fontSize=10,
            leading=14,
            spaceAfter=2,
            spaceBefore=2,
            leftIndent=12,
            bulletAnchor='start',
            bulletFontSize=9,
            bulletIndent=7,
        )

    @abstractmethod
    def get_pdf(self):
        pass
