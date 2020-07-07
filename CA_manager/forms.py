from django import forms


class UploadCertFileForm(forms.Form):
    title = forms.CharField(max_length=64)
    cert_file = forms.FileField()