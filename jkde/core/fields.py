from django.utils import translation
from django.utils.translation import ugettext_lazy as _


class TranslatedField(object):

    def __init__(self, field_name):
        self.field_name = field_name

    @property
    def is_de(self):
        return translation.get_language() == 'de'

    def get_en(self, instance):
        return getattr(instance, self.field_name)

    def get_de(self, instance):
        return getattr(instance, self.field_name + '_de')


class TranslatedTitleField(TranslatedField):

    def __get__(self, instance, owner):

        if self.is_de:
            return self.get_de(instance) or self.get_en(instance)
        else:
            return self.get_en(instance) or self.get_de(instance)


class TranslatedTextField(TranslatedField):

    note_en = _('Sorry, this content is only available in English.')
    note_de = _('Sorry, this content is only available in German.')

    def __get__(self, instance, owner):

        if self.is_de:
            value = self.get_de(instance)
            if value in [None, '', '<p></p>']:
                return '<p class="text-secondary">%s</p>%s' % (self.note_en, self.get_en(instance))
            else:
                return value
        else:
            value = self.get_en(instance)
            if value in [None, '', '<p></p>']:
                return '<p class="text-secondary">%s</p>%s' % (self.note_de, self.get_de(instance))
            else:
                return value
