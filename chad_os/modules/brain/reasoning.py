from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from chad_os.kernel.integrity import CognitiveIntegrity
from chad_os.modules.brain.memory import MemoryModule


@dataclass
class ReasoningModule:
    memory: MemoryModule
    integrity: CognitiveIntegrity

    def reason(self, prompt: str) -> dict[str, Any]:
        chain = [
            f'received:{prompt}',
            'classify intent',
            'apply safe portfolio constraints',
            'return minimal actionable response',
        ]
        valid = self.integrity.validate_reasoning_chain(chain)
        answer = {
            'prompt': prompt,
            'answer': f'Stub answer to: {prompt}',
            'valid': valid,
            'chain': chain,
        }
        self.memory.store({'type': 'reasoning', 'data': answer})
        return answer
