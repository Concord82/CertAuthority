from enum import Enum


class ReasonFlags(Enum):
    """An enumeration for CRL reasons.
    This enumeration is a copy of ``cryptography.x509.ReasonFlags``. We create a copy because any change
    in the enumeration would trigger a database migration, so up/downgrading cryptography might cause problems
    with your Django project.
    """

    unspecified = "unspecified"
    key_compromise = "keyCompromise"
    ca_compromise = "cACompromise"
    affiliation_changed = "affiliationChanged"
    superseded = "superseded"
    cessation_of_operation = "cessationOfOperation"
    certificate_hold = "certificateHold"
    privilege_withdrawn = "privilegeWithdrawn"
    aa_compromise = "aACompromise"
    remove_from_crl = "removeFromCRL"