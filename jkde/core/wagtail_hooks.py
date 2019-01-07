import wagtail.admin.rich_text.editors.draftail.features as draftail_features

from wagtail.core import hooks
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineStyleElementHandler,
    BlockElementHandler
)


@hooks.register('register_rich_text_features')
def register_strikethrough_feature(features):

    feature_name = 'strikethrough'
    feature_type = 'STRIKETHROUGH'
    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature({
            'type': feature_type,
            'description': 'Strikethrough'
        })
    )
    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {
            's': InlineStyleElementHandler(feature_type)
        },
        'to_database_format': {
            'style_map': {
                feature_type: 's'
            }
        }
    })
    features.default_features.append('strikethrough')


@hooks.register('register_rich_text_features')
def register_code_feature(features):

    feature_name = 'code'
    feature_type = 'CODE'
    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature({
            'type': feature_type,
            'description': 'Code'
        })
    )
    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {
            'code': InlineStyleElementHandler(feature_type)
        },
        'to_database_format': {
            'style_map': {
                feature_type: 'code'
            }
        }
    })
    features.default_features.append('code')


@hooks.register('register_rich_text_features')
def register_blockquote_feature(features):

    feature_name = 'blockquote'
    feature_type = 'blockquote'
    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.BlockFeature({
            'type': feature_type,
            'label': '"',
            'description': 'Blockquote',
            'element': 'blockquote'
        })
    )
    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {
            'blockquote': BlockElementHandler(feature_type)
        },
        'to_database_format': {
            'block_map': {
                feature_type: 'blockquote'
            }
        }
    })
    features.default_features.append('blockquote')
