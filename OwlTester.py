import os
import argparse
from owlready2 import *

# Default results file
RESULTS_FILE = "static/results.txt"

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
    """Extracts axioms from ontology."""
    axioms = []
    if onto:
        for cls in onto.classes():
            axioms.append(f'∀x ({cls.name}(x) → {" ∧ ".join(str(cond) for cond in cls.is_a)})')
    print(f"📝 Extracted {len(axioms)} axioms.")
    return axioms

def check_reasoner_inconsistencies(onto):
    """Checks ontology for inconsistencies."""
    inconsistencies = []
    if onto:
        for cls in onto.classes():
            if owl.Nothing in cls.is_a:
                inconsistencies.append(f"❌ Contradiction: {cls.name} inferred as owl:Nothing.")
    print(f"⚠️ Found {len(inconsistencies)} inconsistencies.")
    return inconsistencies

def save_results(axioms, inconsistencies, output_file):
    """Saves results to a file."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as f:
        f.write("🔍 Axioms Extracted:\n")
        for axiom in axioms:
            f.write(f"{axiom}\n")

        f.write("\n⚠️ Ontology Inconsistencies:\n")
        for inc in inconsistencies:
            f.write(f"{inc}\n")
    
    print(f"📂 Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OWL Tester CLI for Ontology Analysis")
    parser.add_argument("ontology", help="Path to the OWL ontology file")
    parser.add_argument("-o", "--output", default=RESULTS_FILE, help="Path to save results")
    args = parser.parse_args()

    onto = load_ontology(args.ontology)
    if onto:
        axioms = extract_axioms(onto)
        inconsistencies = check_reasoner_inconsistencies(onto)
        save_results(axioms, inconsistencies, args.output)
    else:
        print("❌ Ontology processing failed. Check your file.")
