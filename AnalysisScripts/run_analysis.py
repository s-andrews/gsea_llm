#!/usr/bin/env python3
# This script takes in a job id and runs the different steps of the analysis
#
# run_gene_set_analysis.R to do the initia GSEA
#
# ??????? to extract the Gene Ontology text from the GO IDs
#
# ??????? to run the LLM to summarise the terms
#
# Then it can write out the analysis.complete flag so the web
# app knows that everything is finished.

import sys
import subprocess
from pathlib import Path

def main():
    job_id = sys.argv[1]

    job_folder = Path(__file__).parent / "WebFrontEnd/Jobs/"+job_id

    log_file = job_folder / "analysis_log.txt"
    error_file = job_folder / "analysis_errors.txt"

    with open(log_file, "a") as out, open(error_file, "a") as err:
        subprocess.Popen(
            [sys.executable, "other_script.py"],  # Run with same Python interpreter
            stdout=out,  # Redirect stdout to file
            stderr=err   # Redirect stderr to file
        )

    


if __name__ == "__main__":
    main()
