from django import forms

from .models import User, Client, Domain, Payment, Invoice
from .mixins import FormControlMixin


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        )
    )

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = User.objects.filter(username=username, is_active=True).first()
        if user == None or not user.check_password(password):
            raise forms.ValidationError("Incorrect username or password")
        return self.cleaned_data


class ClientForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            "name",
            "paid_until",
            "contact_person",
            "contact_number",
            "email",
            "schema_name",
            "primary_domain_name",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["paid_until"].widget.attrs.update(
            {"class": "form-control datetimepicker"}
        )

        self.fields["primary_domain_name"].widget.attrs.update({"readonly": "readonly"})
        self.fields["contact_number"].widget.attrs.update({"maxlength": 10})
        self.fields["schema_name"].label = "Sub Domain"


class DomainForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Domain
        fields = ["domain", "is_display_domain"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["domain"].widget.attrs.update({"class": "form-control"})


class UserForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("User with this email address already exists")
        return email


class PaymentForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Payment
        exclude = (
            "deleted_at",
            "user",
            "active_status",
            "campaign_id",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["enroll_date"].widget.attrs.update(
            {"class": "form-control datepicker"}
        )

        self.fields["payment_due_date"].widget.attrs.update(
            {"class": "form-control datepicker"}
        )


class InvoiceForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Invoice
        exclude = ("deleted_at", "updated_at", "created_at", "user")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["next_payment_due_date"].widget.attrs.update(
            {"class": "form-control datepicker"}
        )
