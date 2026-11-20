# Cloud-Based Business Data Analytics and Decision Support System

**Student project package**

**Student:** Parminder Singh Bhari  
**Enrolment Number:** 024BCA110806  
**Programme:** BCA, Semester 5

## Project overview
This Streamlit application analyses the supplied DataServe India client dataset and compares its cloud analytics KPIs with Competitor Alpha and Competitor Beta. It includes an executive overview, company benchmarking, regional analysis, cloud service model analysis, data-quality checks, segment analysis, recommendations and a dataset explorer.

## Project structure
```text
Cloud_Based_Business_Analytics_Project/
├── app.py
├── requirements.txt
├── README.md
└── data/
    ├── client_dataset.xlsx
    ├── competitor_alpha.xlsx
    └── competitor_beta.xlsx
```

## Run locally
1. Install Python 3.10 or newer.
2. Extract the project ZIP.
3. Open a terminal in the project folder.
4. Create and activate a virtual environment (recommended).
5. Install dependencies:
   `pip install -r requirements.txt`
6. Start the dashboard:
   `streamlit run app.py`
7. Open the local URL shown in the terminal (normally `http://localhost:8501`).

## Deploy on Streamlit Community Cloud
1. Create a GitHub repository and upload `app.py`, `requirements.txt`, `README.md`, and the `data` folder.
2. Sign in to Streamlit Community Cloud using GitHub.
3. Select **New app**, choose the repository and branch, and set the main file path to `app.py`.
4. Deploy the app. Keep the Excel files in the `data` folder so the application can load them.

## KPI calculation notes
- Average query time, uptime, data quality, conversion, optimisation, decision effectiveness and satisfaction are arithmetic means of their respective dataset columns.
- Cost per GB is calculated as `SUM(Cloud_Cost_INR) / SUM(Data_Volume_GB)`.
- Regional and service-model views use grouped averages for the client dataset.
- The recommendations are decision-support suggestions based on observed differences; the dataset does not establish causal explanations.

## Limitations
The datasets are treated as supplied academic case material. Before using this application for a real business decision, confirm KPI definitions, time periods, workload comparability, access controls and data governance requirements.
