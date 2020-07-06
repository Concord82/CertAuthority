from django.db import models

from cryptography import x509
from cryptography.hazmat.backends import default_backend


from django.core.exceptions import ValidationError

from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.translation import gettext_lazy as _

from .constants import ReasonFlags
# Create your models here.


def validate_past(value):
    if value > timezone.now():
        raise ValidationError(_('Date must be in the past!'))


class X509Certificat(models.Model):
    # reasons are defined in http://www.ietf.org/rfc/rfc3280.txt
    REVOCATION_REASONS = (
        (ReasonFlags.aa_compromise.name, _('Attribute Authority compromised')),
        (ReasonFlags.affiliation_changed.name, _('Affiliation changed')),
        (ReasonFlags.ca_compromise.name, _('CA compromised')),
        (ReasonFlags.certificate_hold.name, _('On Hold')),
        (ReasonFlags.cessation_of_operation.name, _('Cessation of operation')),
        (ReasonFlags.key_compromise.name, _('Key compromised')),
        (ReasonFlags.privilege_withdrawn.name, _('Privilege withdrawn')),
        (ReasonFlags.remove_from_crl.name, _('Removed from CRL')),
        (ReasonFlags.superseded.name, _('Superseded')),
        (ReasonFlags.unspecified.name, _('Unspecified')),
    )

    common_name = models.CharField(_('Common name'), max_length=128)
    serial = models.CharField(max_length=64)

    pub = models.TextField(_('Public Key'))
    private = models.TextField(_('Private Key'))

    created = models.DateTimeField(auto_now=True)
    valid_from = models.DateTimeField(blank=False)
    expires = models.DateTimeField(null=False, blank=False)

    #revocation info
    revoked = models.BooleanField(default=False)
    revoked_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Revoked on'),
                                        validators=[validate_past])
    revoked_reason = models.CharField(
        max_length=32, blank=True, default='', verbose_name=_('Reason for revokation'),
        choices=REVOCATION_REASONS)

    _x509 = None

    class Meta:
        abstract = True

    @property
    def x509(self):
        if self._x509 is None:
            backend = default_backend()
            self._x509 = x509.load_pem_x509_certificate(force_bytes(self.pub), backend)

        return self._x509






class CertificationAuthorities(models.Model):
    name = models.CharField(max_length=32)
    default_set = models.BooleanField(default=False)