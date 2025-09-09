#!/usr/bin/env python3

from flask import Flask, request, render_template, make_response
import random
from urllib.parse import quote_plus
from pathlib import Path
import string

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

    if (job_folder / "job_complete.flag").exists():
        # We need to read in the various parts of the results.

        # AI summary
        ai_summary = "This is where the ai summary will go"

        # GSEA results
        gsea_headers = []
        gsea_results = []

        with open(job_folder/"cluster_profiler_result.tsv") as infh:
            gsea_headers = infh.readline().strip().split("\t")

            for line in infh:
                sections = line.strip().split("\t")

                for i in range(0,len(sections)):
                    try:
                        number = float(sections[i])
                        sections[i] = str(round(number,2))
                    except ValueError:
                        pass

                gsea_results.append(sections)


        return render_template("results.html", headers=gsea_headers, ai_summary=ai_summary, hits=gsea_results)
    
    else:
        # TODO: Put up a proper holding page
        return ("Job running")



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



