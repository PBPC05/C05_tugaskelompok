from django.forms import ModelForm
from apps.forums.models import Forums, ForumsReplies
from django.utils.html import strip_tags


class ForumsForm(ModelForm):
    class Meta:
        model = Forums
        fields = ["title", "content"]

    def clean_title(self):
        title = self.cleaned_data["title"]
        return strip_tags(title)

    def clean_content(self):
        content = self.cleaned_data["content"]
        return strip_tags(content)
    
    
class ForumsRepliesForm(ModelForm):
    class Meta:
        model = ForumsReplies
        fields = ["replies_content"]

    def clean_content(self):
        replies_content = self.cleaned_data["replies_content"]
        return strip_tags(replies_content)
