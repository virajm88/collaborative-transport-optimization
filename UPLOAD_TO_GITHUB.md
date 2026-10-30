# Upload and run this repository

Suggested repository name: **`collaborative-transport-optimization`**.

Suggested description:

> Reproducible transport MILP with exact cooperative cost allocation, coalition
> stability analysis and explicit Benders decomposition in Python / HiGHS.

## 1. Extract first

Unzip the download and open the `collaborative-transport-optimization` folder.
It contains `README.md`, `collab_transport/`, `tests/`, `data/`, `docs/`,
`examples/`, `requirements.txt` and the other repository files.

Upload the **contents of this folder**, not the ZIP and not an extra outer folder.
`README.md` should appear at the root of your GitHub repository.

## 2. Browser upload

1. On GitHub, create a new repository with the suggested name. Choose public if
   you want recruiters and supervisors to inspect it without access requests.
2. Leave initial README, licence and gitignore options blank; all are included here.
3. Choose **uploading an existing file** (or **Add file → Upload files**).
4. Drag the extracted folder's contents into the upload area, then commit.
5. Open `README.md` and check that the network and allocation images render.

The archive includes `.gitignore` and `.github/workflows/ci.yml`. These may be
hidden by your file browser. On macOS, `Command + Shift + .` toggles hidden files;
on Windows, enable hidden items in File Explorer. Include them in the upload.
If your browser does not upload the workflow folder, use Git below or create
`.github/workflows/ci.yml` through GitHub's file editor and paste its supplied content.

## 3. Git upload (alternative)

Create an empty GitHub repository first. In a terminal inside the extracted project:

```bash
git init
git add .
git commit -m "Add transport optimisation and cooperative allocation study"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/collaborative-transport-optimization.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual username. GitHub may request
authentication. No GitHub account information is embedded in this project.

## 4. Check it locally

On macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m collab_transport demo
```

Open `outputs/demo/report.md`. To regenerate all experiments, run:

```bash
python reproduce.py
```

You can inspect the included reference plots and results on GitHub before
installing Python. The commands produce fresh outputs in `outputs/`, which is
excluded from Git by default. Deliberately copy selected rerun results into a
new `examples/` folder if you want to publish your own experiment record.

## 5. Before using it in an application

Work through `docs/LEARNING_GUIDE.md` and make one documented extension or analysis.
Be precise about which parts you understand, which changes you made, and where
you used assistance. A repository supports a skills claim most strongly when
you can explain its assumptions, algorithm and results yourself.

The GitHub Actions workflow is included but has not run on your GitHub account
until you upload. Its checks are available under the repository's **Actions** tab.

