
This tool combines a classical gene set analysis with a local large language model to provide a robust yet interpretable set of gene set analysis results.

You can try this tool out in a public instance at [TO BE DETERMINED]

You can also install the tool locally if you want to run it yourself.

## Installation

### Pre-requisites

To install this tool you will need to have

* A recent version of [python](https://python.org)

* A recent version of [R](https://cran.r-project.org)

* An installation of [Ollama](https://ollama.com/) into which the [gpt-oss:20b](https://ollama.com/library/gpt-oss) model has been loaded.  This will require a GPU with 16GB of VRAM in order to run.

### Code installation

Assuming you have the pre-requisites above installed and available in your path then the installation of the code will be:

```
git clone https://github.com/s-andrews/gsea_llm.git

cd gsea_llm/WebFrontEnd

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

Rscript install_packages.R

cd www

flask --app webapp.py run

```

This will start the web server on localhost on port 5000.  You can see the other options for changing ports or activating development modes [here](https://flask.palletsprojects.com/en/stable/cli/).  For production use you should use a production flask server such as [waitress](https://flask.palletsprojects.com/en/stable/deploying/waitress/)

If your Ollama instance isn't running on the default port on localhost then you should set the ```OLLAMA_HOST``` environment variable to give the base URL for the API.


