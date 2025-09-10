#!/usr/bin/env python3

from flask import Flask, request, render_template, make_response
import random
from urllib.parse import quote_plus
from pathlib import Path
import string
import os
import subprocess
import sys

base_folder = Path(__file__).parent.parent / "Jobs"

app = Flask(__name__)


@app.route("/")
def index():

    # You'll need to pull data from the database.  Here were just 
    # hard coding a dataset, but the principle is the same
    data = [
        {"name":"Simon", "value":10},
        {"name": "Bob", "value": 20},
        {"name": "Alice", "value": 30}
    ]

    return render_template("index.html", data=data)


@app.route("/jobs/<jobid>")
def jobs(jobid):
    job_folder = Path(base_folder) / jobid

    if (job_folder / "analysis.complete").exists():
        # We need to read in the various parts of the results.

        # AI summary
        ai_summary = ""

        with open(job_folder/"LLMresponse.txt") as infh:
            for line in infh:
                ai_summary += line
                ai_summary += "\n"

        # GSEA results
        gsea_headers = []
        gsea_results = []

        headers_to_remove = ["RichFactor","zScore","pvalue","qvalue","geneID","Count"]

        headers_to_keep = []


        with open(job_folder/"cluster_profiler_result.tsv") as infh:
            gsea_headers = infh.readline().strip().split("\t")

            for header in gsea_headers:
                if not header in headers_to_remove:
                    headers_to_keep.append(header)

            for line in infh:
                sections = line.strip().split("\t")

                sections_to_keep = []

                for i in range(0,len(sections)):
                    if gsea_headers[i] in headers_to_remove:
                        continue
                    try:
                        number = float(sections[i])
                        sections_to_keep.append(str(round(number,2)))
                    except ValueError:
                        sections_to_keep.append(sections[i])

                gsea_results.append(sections_to_keep)


        return render_template("results.html", job_id=job_folder.name,headers=headers_to_keep, ai_summary=ai_summary, hits=gsea_results)
    
    else:
        # Read in the text from the log files and send them to the holding page.

        log_text = ""
        error_text = ""

        if (job_folder/"analysis_log.txt").exists():
            with open(job_folder/"analysis_log.txt","rt", encoding="utf8") as infh:
                for line in infh:
                    log_text += line

        if (job_folder/"analysis_errors.txt").exists():
            with open(job_folder/"analysis_errors.txt","rt", encoding="utf8") as infh:
                for line in infh:
                    error_text += line

        return render_template("holding.html", job_id=job_folder.name,log_text=log_text, error_text=error_text)



@app.route("/runanalysis", methods=["POST"])
def runanalysis():

    # We'll have a form with species, query and background
    # lists in it.  We'll make a directory for the data 
    # and put this information into it.  We can then redirect
    # to the output url and we're done.  Everything else will
    # be picked up by the analysis code.

    form = get_form()

    id = generate_random_folder()

    with open(id / "species.txt","wt", encoding="utf8") as out:
        out.write(form["species"])

    with open(id / "query_genes.txt","wt", encoding="utf8") as out:
        out.write(form["query"])

    with open(id / "background_genes.txt","wt", encoding="utf8") as out:
        out.write(form["background"])


    # Start a detached process to run the analysis
    with open(id/"analysis_log.txt", "wt", encoding="utf8") as out:
        subprocess.Popen(
            [sys.executable, id.parent.parent.parent / "AnalysisScripts/run_analysis.py", id.name],
            stdout=out,                # redirect stdout to file
            stderr=out,                # redirect stderr to same file
            stdin=subprocess.DEVNULL,  # detach from parent stdin
            preexec_fn=os.setsid       # start new session (detached)
        )


    return id.name


def generate_random_folder():

    attempts = 0
    while True:
        attempts += 1

        id = ""
        for _ in range(10):
            id += string.ascii_lowercase.upper()[random.randint(0,25)]


        if (base_folder / id).exists():
            if attempts == 10:
                id = ""
                break
            continue

        else:
            break

    if id:
        id = base_folder / id
        id.mkdir()
        return id
    
    raise Exception("Couldn't make new folder - failed 10 times!")



def get_form():

    if request.method == "GET":
        form = request.args.to_dict(flat=True)
        return form

    elif request.method == "POST":
        form = request.form.to_dict(flat=True)
        return form



