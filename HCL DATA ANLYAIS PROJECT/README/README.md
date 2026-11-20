# IPL Data Analysis Using Python (Sample Data Analyst Project)

A beginner-friendly data analysis project for **B.Tech 1st Year - Data Analyst** learners.
It analyses match results, team performance and player output of a T20 cricket league using Python, pandas, matplotlib and seaborn.

> **The dataset is SAMPLE data.** Every row is tagged `Data_Type = SAMPLE` and player names are placeholders (`Player 001` ...). It is **not real IPL data**, so the findings describe this sample only.

## Business problem
A cricket analytics team wants to understand what influences match results, team performance and player output.

## Questions answered
1. How are scores and winning margins distributed?
2. Does winning the toss help? Do teams prefer to bat or field?
3. Which teams and venues perform best?
4. How do team season stats (wins, net run rate, total runs) relate to each other?
5. Who are the top run-scorers and wicket-takers in the sample?

## Dataset
`data/raw/IPL_Sample_Data_Raw.xlsx` - 3 sheets (Matches 105 rows, Team_Stats 103, Player_Stats 103 before cleaning; 100 each after):

| Sheet | Columns |
|---|---|
| Matches | Match_ID, Season, Date, Team_1, Team_2, Venue_City, Toss_Winner, Toss_Decision, Team_1_Score, Team_2_Score, Winner, Run_Difference, Data_Type |
| Team_Stats | Season, Team, Matches, Wins, Losses, Points, Net_Run_Rate, Total_Runs, Data_Type |
| Player_Stats | Player, Team, Season, Matches, Innings, Runs, Average, Strike_Rate, Fifties, Wickets, Data_Type |

The raw file **intentionally has duplicates, missing values, impossible values (a score of 1000, 9999 runs) and inconsistent text** (BAT / bat, chennai / Chennai) so you can practise cleaning. It was created from the tidy template in `data/reference/` by `scripts/generate_raw_data.py`; each problem is recoverable, so missing values are recalculated from other columns (e.g. Winner from the scores) instead of guessed.

## Project structure
```
IPL_Data_Analysis_Project/
├── data/
│   ├── raw/IPL_Sample_Data_Raw.xlsx             (messy file used by the notebook)
│   ├── reference/IPL_Sample_Data_Template.xlsx  (original tidy template)
│   ├── processed/                               (ipl_clean.xlsx + 3 clean CSV files)
│   └── generated/                               (optional: output of generate_data.py)
├── notebooks/ipl_data_analysis.ipynb
├── images/                                      (4 charts saved by the notebook)
├── scripts/
│   ├── generate_data.py                         (creates a NEW synthetic dataset from scratch)
│   ├── generate_raw_data.py                     (makes the messy raw file from the template)
│   └── run_analysis.py                          (same analysis as a plain Python script)
├── IPL_Data_Analysis_Presentation.pptx
├── requirements.txt
├── .gitignore
└── README.md
```

## Generate your own data (optional)
`python scripts/generate_data.py` (run from the `scripts/` folder) creates a brand-new synthetic dataset with the same 3 sheets in `data/generated/` (a tidy file and a messy raw file). To analyse it, point the notebook to `../data/generated/IPL_Sample_Data_Raw.xlsx` (and `IPL_Sample_Data_Tidy.xlsx` for the final check). The numbers in this README and the slides come from the given template, so they will differ for generated data.

## How to run
```bash
git clone https://github.com/<your-username>/ipl-data-analysis.git
cd ipl-data-analysis
pip install -r requirements.txt
jupyter notebook notebooks/ipl_data_analysis.ipynb
```
Or run the script version: `cd scripts && python run_analysis.py`

## Steps followed
1. Load and inspect data  2. Clean data (duplicates, text, impossible values, missing values, logic checks)  3. Create new columns (Toss_Winner_Won_Match, Total_Runs_In_Match, Margin_Band, Batting_First_Won, Win_Pct, Player_Role)  4. Exploratory analysis with charts  5. Insights and recommendations

## Key findings (from this sample only)
- Average total runs in a match is about 353; average winning margin is about 37 runs.
- Toss winners won 45% of matches. With 100 matches this is within chance, so there is no evidence the toss helps.
- Teams chose to bat after winning the toss 54% of the time.
- Highest win % in the Matches sheet: Chennai Super Kings (72%); lowest: Punjab Kings (33%). Each team played only 15-28 matches, so this is indicative only.
- Highest-scoring city: Hyderabad (about 378 runs per match); lowest: Delhi (about 330).
- In Team_Stats, Wins have only a weak relationship with Total_Runs (-0.20) and Net_Run_Rate (0.11).

## Charts
![Overall](images/01_overall_performance.png)
![Toss and teams](images/02_toss_and_teams.png)
![Correlation](images/03_correlation.png)
![Groups](images/04_group_comparison.png)

## Assumptions and limitations
- `Team_1` is assumed to be the team that batted first (the template does not say so).
- Sample data only; sheets are independent samples, so Matches and Team_Stats need not agree.
- Correlation does not prove causation.

## Tools
Python 3 · pandas · NumPy · matplotlib · seaborn · Jupyter Notebook · Git and GitHub

## Author
Your Name - B.Tech 1st Year (replace with your details)
