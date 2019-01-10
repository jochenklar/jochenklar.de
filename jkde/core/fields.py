from django.utils import translation
from django.utils.translation import ugettext_lazy as _


class TranslatedField(object):

    note_template = '<p class="text-secondary">%s</p>'

    note_text_en = _('Sorry, this content is only available in English.')
    note_text_de = _('Sorry, this content is only available in German.')

    def __init__(self, field_name):
        self.field_name = field_name

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
        return getattr(instance, self.field_name)

    def get_de(self, instance):
        return getattr(instance, self.field_name + '_de')


class TranslatedTitleField(TranslatedField):

    def __get__(self, instance, owner):

        if self.is_en:
            return self.get_en(instance)
        elif self.is_de:
            return self.get_de(instance) or self.get_en(instance)
        else:
            raise RuntimeError('Language not supported.')


class TranslatedTextField(TranslatedField):

    def __get__(self, instance, owner):

        if self.is_en:
            en = self.get_en(instance)

            if en not in [None, '', '<p></p>']:
                return en
            else:
                return self.note_de + self.get_de(instance)

        elif self.is_de:
            de = self.get_de(instance)

            if de not in [None, '', '<p></p>']:
                return de
            else:
                return self.note_en + self.get_en(instance)

        else:
            raise RuntimeError('Language not supported.')


class TranslatedStreamField(TranslatedField):

    def __get__(self, instance, owner):

        if self.is_en:
            en = self.get_en(instance)

            if en:
                return en
            else:
                return self.get_de(instance)

        elif self.is_de:
            de = self.get_de(instance)

            if de:
                return de
            else:
                value = self.get_en(instance)

                # inject the tranlation note
                value.stream_data = [{
                    'type': 'richtext',
                    'value': self.note_de
                }] + value.stream_data

                return value

        else:
            raise RuntimeError('Language not supported.')
