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

DEFAULT_RIGHT_MARGIN = 10
DEFAULT_LEFT_MARGIN = 15
DEFAULT_TOP_MARGIN = 10
DEFAULT_BOTTOM_MARGIN = 5
DEFAULT_LEADING = 14

NORMAL_FONT_SIZE = 9

RIGHT_HEADER_STYLE_FONT_SIZE = 8

BOLD_FONT_SIZE = 12
BOLD_LEADING = 18

LIST_STYLE_FONT_SIZE = 12
LIST_STYLE_SPACE_AFTER = 2
LIST_STYLE_SPACE_BEFORE = 2
LIST_STYLE_LIST_INDENT = 12
LIST_STYLE_BULLET_FONT_SIZE = 9
LIST_STYLE_BULLET_INDENT = 7


class BaseDocPortraitTemplate(SimpleDocTemplate):
    def __init__(
        self,
        filename,
        right_margin=DEFAULT_RIGHT_MARGIN,
        left_margin=DEFAULT_LEFT_MARGIN,
        top_margin=DEFAULT_TOP_MARGIN,
        bottom_margin=DEFAULT_BOTTOM_MARGIN,
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
    styles = getSampleStyleSheet()

    def __init__(self, buffer):
        self.buffer = buffer
        self.__create_styles()

    def __create_styles(self):
        self.NORMAL_STYLE = ParagraphStyle(
            name='doc_header',
            fontName='OpenSans',
            fontSize=NORMAL_FONT_SIZE,
            leading=DEFAULT_LEADING,
        )
        self.BOLD_STYLE = ParagraphStyle(
            name='BOLD_STYLE',
            fontName='OpenSans-Bold',
            fontSize=BOLD_FONT_SIZE,
            leading=BOLD_LEADING,
        )
        self.RIGHT_HEADER_STYLE = ParagraphStyle(
            name='Header',
            fontName='OpenSans',
            fontSize=RIGHT_HEADER_STYLE_FONT_SIZE,
            leading=DEFAULT_LEADING,
            alignment=TA_RIGHT,
        )
        self.LIST_STYLE = ParagraphStyle(
            name='ListStyle',
            fontName='OpenSans',
            fontSize=LIST_STYLE_FONT_SIZE,
            leading=DEFAULT_LEADING,
            spaceAfter=LIST_STYLE_SPACE_AFTER,
            spaceBefore=LIST_STYLE_SPACE_BEFORE,
            leftIndent=LIST_STYLE_LIST_INDENT,
            bulletAnchor='start',
            bulletFontSize=LIST_STYLE_BULLET_FONT_SIZE,
            bulletIndent=LIST_STYLE_BULLET_INDENT,
        )

    @abstractmethod
    def get_pdf(self):
        pass
