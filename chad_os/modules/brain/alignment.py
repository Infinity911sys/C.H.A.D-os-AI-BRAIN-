import json

from ...kernel.k1_alignment import K1ConsciousnessAlignment


class AlignmentModule:
    def __init__(self, k1: K1ConsciousnessAlignment):
        self.k1 = k1

    def evaluate_output(self, output: object) -> float:
        score = 0.0 if "forbidden" in json.dumps(output).lower() else 1.0
        self.k1.update_alignment(score)
        return score
