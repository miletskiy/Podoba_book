
from .util import get_groups  # get_current_language

def groups_processor(request):
    return {'GROUPS':get_groups(request)}
    # return {'GROUPS':['1','2','3']}

# def lang_processor(request):
#     return {'LANGS':get_current_language(request)}


# django.middleware.locale.LocaleMiddleware

# from django.middleware.locale import LocaleMiddleware