# Week 6 AI Lab - Graded Submission

This folder contains the completed graded work for **Tasks 1-5** and the required Streamlit GUI. Tasks 6-7 were explicitly labeled ungraded in the task document and are intentionally excluded.

## Contents

- `week6_Tasks_solution.ipynb` - completed and executed notebook with outputs and highlighted NetworkX solution paths.
- `app.py` - deployment-ready Streamlit application for GBFS and A* on the hospital graph.
- `searchAlgos.py` - shared hospital graph, Euclidean heuristic, GBFS, and A* implementations.
- `streamlit_app_solution_template1.py` - completed single-file version of the first supplied template.
- `streamlit_app_solution_template2.py` - completed modular version of the second supplied template.
- `requirements.txt` - dependencies for Streamlit Community Cloud.
- `SUBMISSION_CHECKLIST.md` - exact final submission steps.

## Run the app locally

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Create a GitHub repository and upload every file in this folder.
2. In Streamlit Community Cloud, create an app from that repository.
3. Set the main file path to `app.py` and deploy.
4. Copy the repository URL and deployed app URL into `SUBMISSION_CHECKLIST.md` and submit both with the executed notebook to GCR.

