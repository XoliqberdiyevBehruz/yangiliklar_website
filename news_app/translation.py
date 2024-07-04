from modeltranslation.translator import register, TranslationOptions, translator
from .models import News, Cotegory


class NewsTranslation(TranslationOptions):
    fields = ('title', 'body')
translator.register(News, NewsTranslation)

