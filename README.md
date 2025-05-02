# FOL-BFO-OWL-tester
[OWL Ontology Checker](https://owl-tester-service-davidkoepsell.replit.app/)
Overview
This script analyzes an OWL ontology, extracts logical axioms, detects contradictions, and validates inferences using logical reasoning. It also checks for ontology inconsistencies using the Pellet reasoner.
Features
✔ Ontology Loading – Reads an OWL ontology file and processes it with the Pellet reasoner.
✔ Axiom Extraction – Translates ontology relationships into first-order predicate logic.
✔ Logical Consistency Checks – Detects contradictions and reasoner-inferred inconsistencies.
✔ Inference Detection – Identifies logical inferences from extracted axioms.
✔ Results Saving – Outputs analysis to a text file for review.
Dependencies
Before running the script, ensure you have the following dependencies installed:
Required Packages
- Python 3.12+
- Owlready2 (pip install owlready2) – For OWL ontology handling.
- SymPy (pip install sympy) – For symbolic logic processing.

Additional Requirements
- Java Runtime Environment (default-jre) – Required for running the Pellet reasoner. Install it using:sudo apt install default-jre


Installation & Setup
1. Install Dependencies
Run the following command:
pip install owlready2 sympy


If you're on a Debian-based system, Python's environment might be externally managed. In that case, use:
sudo apt install python3-venv
python3 -m venv myenv
source myenv/bin/activate
pip install owlready2 sympy


2. Prepare an OWL Ontology File
Ensure you have an OWL ontology (.owl file) available for analysis.
3. Run the Script
Execute the script with:
python OwlChecker.py path/to/ontology.owl


Replace path/to/ontology.owl with the actual location of your ontology file.
4. Review Results
Results are stored in a file called results.txt. Open it to check the detected axioms, contradictions, inferences, and ontology inconsistencies.
Troubleshooting
- Java Not Found? Ensure Java is installed (java -version). If missing, install it (sudo apt install default-jre).
- Ontology File Issues? Make sure your .owl file exists and is properly formatted.
- Pellet Reasoner Errors? Check that Pellet dependencies are installed and accessible.
- No Contradictions Found? Consider extending contradiction detection logic within the script.

License
This script is free to use and modify for ontology analysis and logical validation.
