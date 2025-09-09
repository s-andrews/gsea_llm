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

def run_step(command, log_file, error_file, cwd=None):

    """Run a shell command and log output/errors. Raise error and stop p[ipeline if it fails."""
    with open(log_file, "a") as out, open(error_file, "a") as err:
        result = subprocess.run(
            command,
            stdout=out,
            stderr=err,
            cwd=cwd,
            text=True
        )
    if result.returncode != 0:
        raise RuntimeError(f"Step failed: {' '.join(command)}")


def main():
    job_id = sys.argv[1]
    project_root = Path(__file__).parent.parent
    job_folder = project_root / "WebFrontEnd" / "Jobs" / job_id
    job_folder.mkdir(parents=True, exist_ok=True) 

    log_file = job_folder / "analysis_log.txt"
    error_file = job_folder / "analysis_errors.txt"

    print(f"Starting analysis for job: {job_id}")

    r_script_path = project_root / "AnalysisScripts" / "run_gene_set_analysis.R"
    # r_cwd = project_root / "WebFrontEnd"
    try:
        # run gsea in r
        print("Running GSEA..")
        run_step(
            ["Rscript", str(r_script_path), str(job_folder)],
            log_file,
            error_file,
            cwd = project_root
        )

        # extract GO text from GO ids

        go_script_path = project_root / "AnalysisScripts" / "go_to_description.py"
        print("Extrcating GO text...")
        run_step(
            [sys.executable, str(go_script_path), job_id],
            log_file,
            error_file,
            cwd = project_root
        )

        run_llm_path = project_root / "AnalysisScripts" / "summarise_terms.py"

        #run llm to summarise terms
        print("Running LLM....")
        run_step(
            [sys.executable, str(run_llm_path), job_id],
            log_file,
            error_file,
            cwd = project_root
        )

        complete_flag = job_folder / "analysis.complete"
        complete_flag.touch()
        print("Pipeline complete!")

    except Exception as e:
        with open(error_file, "a") as err:
            err.write(f"Pipeline failed: {str(e)}\n")
        print(f"Error: {e}")
        sys.exit(1)

    


if __name__ == "__main__":
    main()
