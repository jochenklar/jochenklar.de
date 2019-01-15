from django.utils import translation
from django.utils.translation import ugettext_lazy as _


class TranslatedField(object):

    note_template = '<p class="text-secondary">%s</p>'

    note_text_en = _('Sorry, this content is only available in English.')
    note_text_de = _('Sorry, this content is only available in German.')

    def __init__(self, field_name, note=False):
        self.field_name = field_name
        self.note = note

    @property
    def is_en(self):
        return translation.get_language() == 'en'

    @property
    def is_de(self):
        return translation.get_language() == 'de'

    @property
    def note_en(self):
        return self.note_template % self.note_text_en

    @property
    def note_de(self):
        return self.note_template % self.note_text_de

    def get_en(self, instance):
        en = getattr(instance, self.field_name)
        if en in [None, '', '<p></p>']:
            return None
        else:
            return en

    def get_de(self, instance):
        de = getattr(instance, self.field_name + '_de')
        if de in [None, '', '<p></p>']:
            return None
        else:
            return de


class TranslatedTextField(TranslatedField):

    def __get__(self, instance, owner):

        if self.is_en:
            en = self.get_en(instance)

            if en:
                return en
            elif self.note:
                return self.note_de + self.get_de(instance)
            else:
                return self.get_de(instance)

        elif self.is_de:
            de = self.get_de(instance)

            if de:
                return de
            elif self.note:
                return self.note_en + self.get_en(instance)
            else:
                return self.get_en(instance)

        else:
            raise RuntimeError('Language not supported.')


class TranslatedStreamField(TranslatedField):

    def __get__(self, instance, owner):

        if self.is_en:
            en = self.get_en(instance)

            if en:
                return en
            elif self.note:
                # inject the translation note into StreamValue.render_as_block
                de = self.get_de(instance)
                de.render_as_block = lambda context=None: self.note_de + \
                    de.stream_block.render(de, context=context)

                return de
            else:
                return self.get_de(instance)

        elif self.is_de:
            de = self.get_de(instance)

            if de:
                return de
            elif self.note:
                # inject the translation note into StreamValue.render_as_block
                en = self.get_en(instance)
                en.render_as_block = lambda context=None: self.note_en + \
                    en.stream_block.render(en, context=context)

                return en
            else:
                return self.get_en(instance)

        else:
            raise RuntimeError('Language not supported.')
