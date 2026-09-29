import logging


class LicenseVerifier:
    def __init__(self, license_id: str):
        self.license_id = license_id

    def verify(self) -> bool:
        if not self.license_id or self.license_id.startswith("xxxx-"):
            logging.warning("Using placeholder license; treat as unverified in production.")
            return False
        return True

    def get_status(self) -> str:
        return "verified" if self.verify() else "unverified"
