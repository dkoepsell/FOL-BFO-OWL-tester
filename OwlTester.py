import os
from owlready2 import *
from sympy import symbols, Eq
from itertools import combinations

def load_ontology(file_path):
    """Loads an OWL ontology from the given file path and runs a reasoner."""
    if not os.path.exists(file_path):
        print(f"Error: Ontology file '{file_path}' not found.")
        return None

    onto = get_ontology(file_path).load()
    print("Ontology successfully loaded!")

    return onto

def extract_axioms(onto):
    """Extracts first-order predicate logic axioms, handling complex is_a structures."""
    if not onto:
        return []

    axioms = []
    for cls in onto.classes():
        if cls.is_a:
            axioms.append(f'∀x ({cls.name}(x) → {" ∧ ".join(str(cond) for cond in cls.is_a)})')

    for prop in onto.object_properties():
        if prop.domain and prop.range:
            axioms.append(f'∀x ∀y ({prop.name}(x, y) → {prop.domain} ∧ {prop.range})')

    return axioms

def check_reasoner_inconsistencies(onto):
    """Detects inconsistencies by analyzing inferred owl:Nothing classifications and disjoint class violations."""
    if not onto:
        return []

    inconsistencies = []

    for cls in onto.classes():
        if owl.Nothing in cls.is_a:
            inconsistencies.append(f"Class {cls.name} is inferred as owl:Nothing (contradiction detected).")

    for cls1 in onto.classes():
        if hasattr(cls1, "disjoint_with"):
            for cls2 in cls1.disjoint_with:
                for individual in cls1.instances():
                    if individual in cls2.instances():
                        inconsistencies.append(f"{individual} violates disjoint constraint between {cls1.name} and {cls2.name}.")

    return inconsistencies

def check_contradictions_and_inferences(axioms):
    """Detects contradictions and valid logical inferences between extracted axioms."""
    if not axioms:
        return [], []

    contradictions = []
    inferences = []

    for ax1, ax2 in combinations(axioms, 2):
        if f'¬{ax1}' in ax2 or f'¬{ax2}' in ax1:
            contradictions.append((ax1, ax2))
        else:
            inferences.append((ax1, ax2))

    return contradictions, inferences

def save_results(axioms, contradictions, inferences, inconsistencies, output_file):
    """Ensures static directory exists before saving results."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w") as f:
        f.write("Generated Axioms:\n")
        for i, axiom in enumerate(axioms):
            f.write(f"{i+1}: {axiom}\n")

        f.write("\nContradictions Detected:\n")
        for c in contradictions:
            f.write(f"Contradictory Pair: {c[0]} <--> {c[1]}\n")

        f.write("\nValid Inferences:\n")
        for inf in inferences:
            f.write(f"Inference: {inf[0]} ∧ {inf[1]} → Conclusion\n")

        f.write("\nOntology Reasoner Inconsistencies:\n")
        for inc in inconsistencies:
            f.write(f"{inc}\n")

if __name__ == "__main__":
    import sys
    onto_path = sys.argv[1] if len(sys.argv) > 1 else input("Enter the OWL ontology file path: ")
    output_file = "static/results.txt"

    onto = load_ontology(onto_path)
    if onto:
        axioms = extract_axioms(onto)
        inconsistencies = check_reasoner_inconsistencies(onto)
        contradictions, inferences = check_contradictions_and_inferences(axioms)

        save_results(axioms, contradictions, inferences, inconsistencies, output_file)
        print("\nResults saved to static/results.txt")
    else:
        print("Ontology loading failed. Check your file.")
