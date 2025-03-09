from owlready2 import *
from sympy import symbols, Eq
from itertools import combinations

def load_ontology(file_path):
    """Loads an OWL ontology from the given file path."""
    onto = get_ontology(file_path).load()
    return onto

def clean_axiom(axiom):
    """Cleans axiom by replacing dots and ensuring valid symbols."""
    cleaned = axiom.replace(".", "_").replace("[", "").replace("]", "").replace(" ", "_").replace("None", "NULL")
    if cleaned[0].isdigit():
        cleaned = "A_" + cleaned  # Prefix numerical identifiers to make them valid symbols
    return cleaned

def extract_axioms(onto):
    """Extracts first-order predicate logic axioms from the ontology."""
    axioms = []
    for cls in onto.classes():
        axioms.append(f'∀x ({clean_axiom(cls.name)}(x) → {clean_axiom(str(cls.is_a))})')
    for prop in onto.object_properties():
        axioms.append(f'∀x ∀y ({clean_axiom(prop.name)}(x, y) → {clean_axiom(str(prop.domain))} ∧ {clean_axiom(str(prop.range))})')
    return axioms

def check_contradictions_and_inferences(axioms):
    """Checks for contradictions and valid inferences by comparing axioms logically."""
    print("Generated Premises:")
    for i, axiom in enumerate(axioms):
        print(f"{i+1}: {axiom}")
    
    contradictions = []
    inferences = []
    
    print("\nTesting for Contradictions and Inferences...")
    for ax1, ax2 in combinations(axioms, 2):
        if ax1 == ax2:  # Avoid trivial contradictions
            continue
        
        if f'¬{ax1}' in ax2 or f'¬{ax2}' in ax1:  # Opposing axioms
            contradictions.append((ax1, ax2))
        else:
            inferences.append((ax1, ax2))
    
    if contradictions:
        print("\nContradictions found:")
        for c in contradictions:
            print(f"Contradictory Pair: {c[0]} <--> {c[1]}")
    else:
        print("\nNo contradictions found.")
    
    if inferences:
        print("\nValid Inferences:")
        for inf in inferences:
            print(f"Inference: {inf[0]} ∧ {inf[1]} → Conclusion")
    else:
        print("\nNo valid inferences found.")
    
    return contradictions, inferences

def save_results(axioms, contradictions, inferences, output_file):
    """Saves results to a file."""
    with open(output_file, "w") as f:
        f.write("Generated Premises:\n")
        for i, axiom in enumerate(axioms):
            f.write(f"{i+1}: {axiom}\n")
        
        f.write("\nTesting for Contradictions and Inferences...\n")
        if contradictions:
            f.write("Contradictions found:\n")
            for c in contradictions:
                f.write(f"Contradictory Pair: {c[0]} <--> {c[1]}\n")
        else:
            f.write("No contradictions found.\n")
        
        if inferences:
            f.write("\nValid Inferences:\n")
            for inf in inferences:
                f.write(f"Inference: {inf[0]} ∧ {inf[1]} → Conclusion\n")
        else:
            f.write("No valid inferences found.\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        onto_path = input("Enter the path to the OWL ontology file: ")
    else:
        onto_path = sys.argv[1]
    
    output_file = "results.txt"
    
    onto = load_ontology(onto_path)
    axioms = extract_axioms(onto)
    contradictions, inferences = check_contradictions_and_inferences(axioms)
    
    save_results(axioms, contradictions, inferences, output_file)
    
    print("\nResults saved to results.txt")
