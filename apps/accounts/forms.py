from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class TailwindMixin:
    base_input_classes = (
        "block w-full rounded-md border border-zinc-700 bg-zinc-900 "
        "px-3 py-2 text-sm text-zinc-100 placeholder-zinc-500 "
        "focus:border-brand-red focus:outline-none focus:ring-1 focus:ring-brand-red"
    )

    def _style_fields(self):
        for field in self.fields.values():
            classes = self.base_input_classes
            existing = field.widget.attrs.get("class")
            if existing:
                classes = f"{existing} {classes}"
            field.widget.attrs.update({"class": classes})


class LoginForm(TailwindMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class SignupForm(TailwindMixin, UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

