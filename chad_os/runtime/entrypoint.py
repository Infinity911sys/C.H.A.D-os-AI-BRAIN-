import logging

from .bootstrap import BrainConfig, ChadOSBrain


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    brain = ChadOSBrain(BrainConfig.from_env())
    brain.boot()
    logging.info("C.H.A.D-os brain running. Type 'exit' to quit.")
    while True:
        try:
            prompt = input("You> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if prompt.lower() in {"exit", "quit"}:
            break
        brain.process_prompt(prompt)


if __name__ == "__main__":
    main()
