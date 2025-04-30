from flask import Flask, request, render_template
import os
from OwlTester import load_ontology, extract_axioms, check_reasoner_inconsistencies, check_contradictions_and_inferences, save_results

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
RESULTS_FILE = "static/results.txt"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    """Handles file upload and analysis."""
    if request.method == "POST":
        file = request.files["ontology"]
        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            
            onto = load_ontology(file_path)
            axioms = extract_axioms(onto)
            inconsistencies = check_reasoner_inconsistencies(onto)
            contradictions, inferences = check_contradictions_and_inferences(axioms)
            
            save_results(axioms, contradictions, inferences, inconsistencies, RESULTS_FILE)
            
            return render_template("result.html", file=RESULTS_FILE)

    return render_template("index.html")

@app.route("/results")
def results():
    """Displays saved results."""
    with open(RESULTS_FILE, "r") as f:
        content = f.read()
    return f"<pre>{content}</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
