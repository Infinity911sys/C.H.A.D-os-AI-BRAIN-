from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass
class IdentityRegistry:
    control_token: str

    def authorize(self, headers: Mapping[str, str]) -> bool:
        auth = headers.get('Authorization', '')
        if auth.startswith('Bearer '):
            return auth.removeprefix('Bearer ').strip() == self.control_token
        api_key = headers.get('X-API-Key', '')
        return api_key == self.control_token
