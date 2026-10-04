from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LicenseVerifier:
    license_id: str

    def verify(self) -> bool:
        return bool(self.license_id and not self.license_id.startswith('xxxx-'))

    def status(self) -> str:
        return 'verified' if self.verify() else 'unverified'
