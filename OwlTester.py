import os
import argparse
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

def save_results(axioms, output_file):
    """Saves extracted axioms to a file."""
    output_dir = os.path.dirname(output_file)

    if output_dir:  # Prevents FileNotFoundError when output file is just a filename
        os.makedirs(output_dir, exist_ok=True)

    with open(output_file, "w") as f:
        f.write("🔍 Extracted Axioms:\n")
        for axiom in axioms:
            f.write(f"{axiom}\n")

    print(f"📂 Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ontology Tester CLI for Axiom Extraction")
    parser.add_argument("ontology", help="Path to the OWL ontology file")
    parser.add_argument("-o", "--output", default=RESULTS_FILE, help="Path to save results")
    args = parser.parse_args()

    onto = load_ontology(args.ontology)
    if onto:
        axioms = extract_axioms(onto)
        save_results(axioms, args.output)
    else:
        print("❌ Ontology processing failed. Check your file.")
