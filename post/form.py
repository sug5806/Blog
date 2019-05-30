from django.forms.models import modelform_factory
from .models import Post

class Post_form():
    modelform_factory(Post)