from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Validate DNA coding strand sequence
def DNA(DNAseq):
    nucleotide = {"G", "C", "A", "T", "g", "c", "a", "t"}
    for n in DNAseq:
        if n not in nucleotide:
            return False
    return True

# Encode DNA coding strand to DNA template strand
def DNAtemplate_strand(DNAseq):
    DNAtemp = list(DNAseq.upper()) # Convert string to list
    for n in range(len(DNAtemp)):
        if DNAtemp[n] == "G":
            DNAtemp[n] = "C"
        elif DNAtemp[n] == "C":
            DNAtemp[n] = "G"
        elif DNAtemp[n] == "A":
            DNAtemp[n] = "T"
        elif DNAtemp[n] == "T":
            DNAtemp[n] = "A"
    DNAtemp = "".join(DNAtemp) # Convert list back to string
    return DNAtemp

# DNA transcription (to mRNA)
def mRNA(DNAseq):
    mRNAseq = list(DNAseq.upper()) # Convert string to list
    for n in range(len(DNAseq)):
        if mRNAseq[n] == "T":
            mRNAseq[n] = "U"
    mRNAseq = "".join(mRNAseq) # Convert list back to string
    return mRNAseq

# Translate mRNA sequence to amino acid codons (starting from start codon and ends when encountering stop codon)
def aminoacid(DNAseq):
    aminoacid = {
      "AAA":"K", "AAC":"N", "AAG":"K", "AAU":"N", 
      "ACA":"T", "ACC":"T", "ACG":"T", "ACU":"T", 
      "AGA":"R", "AGC":"S", "AGG":"R", "AGU":"S", 
      "AUA":"I", "AUC":"I", "AUG":"M", "AUU":"I", 
      "CAA":"Q", "CAC":"H", "CAG":"Q", "CAU":"H", 
      "CCA":"P", "CCC":"P", "CCG":"P", "CCU":"P", 
      "CGA":"R", "CGC":"R", "CGG":"R", "CGU":"R", 
      "CUA":"L", "CUC":"L", "CUG":"L", "CUU":"L", 
      "GAA":"E", "GAC":"D", "GAG":"E", "GAU":"D", 
      "GCA":"A", "GCC":"A", "GCG":"A", "GCU":"A", 
      "GGA":"G", "GGC":"G", "GGG":"G", "GGU":"G", 
      "GUA":"V", "GUC":"V", "GUG":"V", "GUU":"V",
      "UAC":"Y", "UAU":"Y", "UCA":"S", "UCC":"S",
      "UCG":"S", "UCU":"S", "UGC":"C", "UGG":"W",
      "UGU":"C", "UUA":"L", "UUC":"F", "UUG":"L",
      "UUU":"F", "UAA":"-", "UAG":"-", "UGA":"-"}
    
    mRNAseq = mRNA(DNAseq)

    if len(mRNAseq) < 3:
        return None, None
    
    else:
        protein = ""
        mRNAseq_startcodon = ""
        protein_startcodon = ""

        for p in range(0, len(mRNAseq), 3):
            codon = mRNAseq[p:p+3]
            if len(codon) < 3:
                break
            else:
                protein += aminoacid.get(codon)

        startcodon = "AUG"
        startcodon_index = mRNAseq.find(startcodon)

        if startcodon_index:
            for t in range(startcodon_index, len(mRNAseq), 3):
                newcodon = mRNAseq[t:t+3]
                if len(newcodon) < 3:
                    break
                else:
                    mRNAseq_startcodon += newcodon
                    protein_startcodon += aminoacid.get(newcodon)

        return protein, mRNAseq_startcodon, protein_startcodon    # Return the results as a tuple

# Flask route to handle form submission and process DNA sequence
@app.route("/process", methods=["POST"])
def process_dna():
    DNAseq = request.json.get("DNAseq", "")

    if not DNA(DNAseq):
        return jsonify(error="Invalid DNA sequence. Please try again!")
    
    result = {
        "DNAseq": DNAseq.upper(),
        "template_strand": DNAtemplate_strand(DNAseq),
        "mrna_seq": mRNA(DNAseq),
        "protein": None,
        "mRNAseq_startcodon": None,
        "protein_start": None
    }
    protein, mRNAseq_startcodon, protein_start = aminoacid(DNAseq)
    result["protein"] = protein
    result["mRNAseq_startcodon"] = mRNAseq_startcodon
    result["protein_start"] = protein_start
    return jsonify(result)

# Flask route for the index.html page
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
