import os
import argparse
from itertools import combinations
from owlready2 import *

# Default results file
RESULTS_FILE = "results.txt"

def load_ontology(file_path):
    """Loads an OWL ontology and runs Pellet reasoner."""
    if not os.path.exists(file_path):
        print(f"❌ Error: Ontology file '{file_path}' not found.")
        return None

    try:
        onto = get_ontology(file_path).load()
        print("✅ Ontology successfully loaded.")
        
        with onto:
            sync_reasoner_pellet()
            print("🔍 Pellet Reasoner completed.")

        return onto
    except Exception as e:
        print(f"❌ Ontology loading failed: {e}")
        return None

def extract_axioms(onto):
    """Extracts class definitions and object property axioms."""
    axioms = []

    # Extract class axioms
    for cls in onto.classes():
        axioms.append(f'∀x ({cls.name}(x) → owl.Thing)')

    # Extract object property axioms
    for prop in onto.object_properties():
        domain = prop.domain[0] if prop.domain else "?"
        range_ = prop.range[0] if prop.range else "?"
        axioms.append(f'∀x ∀y ({prop.name}(x, y) → {domain} ∧ {range_})')

    print(f"📝 Extracted {len(axioms)} axioms.")
    return axioms

def check_reasoner_inconsistencies(onto):
    """Detects inconsistencies from the reasoner, such as owl:Nothing classifications or disjoint violations."""
    inconsistencies = []

    # Check for owl:Nothing classifications
    for cls in onto.classes():
        if owl.Nothing in cls.is_a:
            inconsistencies.append(f"❌ Contradiction: {cls.name} is inferred as owl:Nothing (logical inconsistency).")

    # Check disjoint class violations
    for cls1 in onto.classes():
        if hasattr(cls1, "disjoint_with"):
            for cls2 in cls1.disjoint_with:
                for individual in cls1.instances():
                    if individual in cls2.instances():
                        inconsistencies.append(f"⚠️ Violation: {individual} is both {cls1.name} and {cls2.name}, violating disjoint constraint.")

    print(f"⚠️ Found {len(inconsistencies)} inconsistencies.")
    return inconsistencies

def check_contradictions(axioms):
    """Detects contradictions in axioms by analyzing negations and conflicting statements."""
    contradictions = []

    for ax1, ax2 in combinations(axioms, 2):
        if f'¬{ax1}' in ax2 or f'¬{ax2}' in ax1:
            contradictions.append((ax1, ax2))

    print(f"⚠️ Found {len(contradictions)} contradictions.")
    return contradictions

def save_results(axioms, inconsistencies, contradictions, output_file):
    """Saves extracted axioms, inconsistencies, and contradictions to a file."""
    output_dir = os.path.dirname(output_file)

    if output_dir:  # Prevents FileNotFoundError when output file is a simple filename
        os.makedirs(output_dir, exist_ok=True)

    with open(output_file, "w") as f:
        f.write("🔍 Extracted Axioms:\n")
        for axiom in axioms:
            f.write(f"{axiom}\n")

        f.write("\n⚠️ Ontology Inconsistencies:\n")
        for inc in inconsistencies:
            f.write(f"{inc}\n")

        f.write("\n❌ Contradictions Detected:\n")
        for c in contradictions:
            f.write(f"Contradictory Pair: {c[0]} <--> {c[1]}\n")

    print(f"📂 Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ontology Tester CLI for Axiom Extraction, Contradictions & Inconsistencies")
    parser.add_argument("ontology", help="Path to the OWL ontology file")
    parser.add_argument("-o", "--output", default=RESULTS_FILE, help="Path to save results")
    args = parser.parse_args()

    onto = load_ontology(args.ontology)
    if onto:
        axioms = extract_axioms(onto)
        inconsistencies = check_reasoner_inconsistencies(onto)
        contradictions = check_contradictions(axioms)
        save_results(axioms, inconsistencies, contradictions, args.output)
    else:
        print("❌ Ontology processing failed. Check your file.")
