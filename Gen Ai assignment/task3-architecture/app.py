import json
import os
from analyzer import analyze_requirement

def run():
    requirement = input("Enter high-level business requirement: ")

    architecture = analyze_requirement(requirement)

    os.makedirs("output", exist_ok=True)
    with open("output/architecture.json", "w") as f:
        json.dump(architecture, f, indent=2)

    print("\n✅ Generated Low-Level Architecture:\n")
    for key, value in architecture.items():
        print(f"{key.upper()}:")
        for item in value:
            print(f" - {item}")
        print()

if __name__ == "__main__":
    run()
