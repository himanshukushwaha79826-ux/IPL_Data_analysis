"""Generate a SYNTHETIC IPL-style dataset (3 sheets) for learning purposes.
No real IPL data is used; every row is tagged Data_Type = SAMPLE and players are placeholders.
Creates two files in data/generated/:
  IPL_Sample_Data_Tidy.xlsx  - clean, consistent data (the 'answer key')
  IPL_Sample_Data_Raw.xlsx   - same data with realistic problems added for the cleaning exercise
Run from the scripts/ folder:  python generate_data.py"""
import os
import numpy as np, pandas as pd

rng = np.random.default_rng(42)
TEAMS = {'Chennai Super Kings': 'Chennai', 'Mumbai Indians': 'Mumbai', 'Royal Challengers Bengaluru': 'Bengaluru',
         'Kolkata Knight Riders': 'Kolkata', 'Delhi Capitals': 'Delhi', 'Rajasthan Royals': 'Jaipur',
         'Punjab Kings': 'Mohali', 'Sunrisers Hyderabad': 'Hyderabad', 'Gujarat Titans': 'Ahmedabad',
         'Lucknow Super Giants': 'Lucknow'}
names = list(TEAMS)
SEASONS = list(range(2017, 2027))

# ---------------- Matches (100 rows) ----------------
n = 100
rows = []
for i in range(n):
    t1, t2 = rng.choice(names, 2, replace=False)
    season = int(rng.choice(SEASONS))
    date = pd.Timestamp(season, 3, 22) + pd.Timedelta(days=int(rng.integers(0, 70)))
    s1 = int(np.clip(rng.normal(176, 30), 120, 230)); s2 = int(np.clip(rng.normal(172, 30), 120, 230))
    if s1 == s2: s1 += 1                                   # no ties
    rows.append({'Match_ID': i + 1, 'Season': season, 'Date': date, 'Team_1': t1, 'Team_2': t2,
                 'Venue_City': TEAMS[t1],                  # Team_1 plays at home
                 'Toss_Winner': str(rng.choice([t1, t2])),
                 'Toss_Decision': str(rng.choice(['bat', 'field'], p=[.54, .46])),
                 'Team_1_Score': s1, 'Team_2_Score': s2,
                 'Winner': t1 if s1 > s2 else t2, 'Run_Difference': abs(s1 - s2), 'Data_Type': 'SAMPLE'})
matches = pd.DataFrame(rows)

# ---------------- Team_Stats (10 teams x 10 seasons) ----------------
rows = []
for season in SEASONS:
    for team in names:
        wins = int(np.clip(round(rng.normal(7.3, 2.4)), 3, 11))
        rows.append({'Season': season, 'Team': team, 'Matches': 14, 'Wins': wins, 'Losses': 14 - wins,
                     'Points': 2 * wins, 'Net_Run_Rate': round(float(rng.normal(0, .55)), 3),
                     'Total_Runs': int(np.clip(rng.normal(1920, 230), 1500, 2300)), 'Data_Type': 'SAMPLE'})
teams = pd.DataFrame(rows)

# ---------------- Player_Stats (100 placeholder players) ----------------
rows = []
for i in range(100):
    m = int(rng.integers(6, 17)); inn = int(rng.integers(max(3, m - 5), m + 1))
    runs = int(np.clip(rng.normal(350, 185), 50, 700))
    rows.append({'Player': f'Player {i + 1:03d}', 'Team': str(rng.choice(names)), 'Season': int(rng.choice(SEASONS)),
                 'Matches': m, 'Innings': inn, 'Runs': runs, 'Average': round(runs / inn, 2),
                 'Strike_Rate': round(float(np.clip(rng.normal(148, 27), 100, 200)), 2),
                 'Fifties': int(rng.integers(0, min(7, runs // 60) + 1)), 'Wickets': int(rng.integers(0, 26)),
                 'Data_Type': 'SAMPLE'})
players = pd.DataFrame(rows)

os.makedirs('../data/generated', exist_ok=True)
with pd.ExcelWriter('../data/generated/IPL_Sample_Data_Tidy.xlsx') as w:
    matches.to_excel(w, sheet_name='Matches', index=False)
    teams.to_excel(w, sheet_name='Team_Stats', index=False)
    players.to_excel(w, sheet_name='Player_Stats', index=False)

# ---------------- Introduce realistic data-quality problems (all recoverable) ----------------
m, t, p = matches.copy(), teams.copy(), players.copy()

def pick(size, k, used):
    free = np.setdiff1d(np.arange(size), list(used))
    idx = rng.choice(free, k, replace=False); used.update(idx.tolist()); return idx

used = set()
m.loc[pick(len(m), 4, used), 'Winner'] = np.nan            # missing winner
m.loc[pick(len(m), 4, used), 'Run_Difference'] = np.nan    # missing margin
m.loc[pick(len(m), 3, used), 'Team_2_Score'] = np.nan      # missing score
m.loc[pick(len(m), 2, used), 'Team_1_Score'] = 1000        # impossible score
i = pick(len(m), 8, set())                                 # inconsistent text
m.loc[i, 'Toss_Decision'] = [[v.upper(), v.capitalize() + ' ', ' ' + v, v.upper()][j % 4] for j, v in enumerate(m.loc[i, 'Toss_Decision'])]
i = pick(len(m), 8, set())
m.loc[i, 'Venue_City'] = [v.lower() if j % 2 else ' ' + v + ' ' for j, v in enumerate(m.loc[i, 'Venue_City'])]
m = pd.concat([m, m.sample(5, random_state=1)], ignore_index=True)   # 5 duplicate rows

used = set()
t.loc[pick(len(t), 4, used), 'Wins'] = np.nan
t.loc[pick(len(t), 3, used), 'Losses'] = np.nan
t.loc[pick(len(t), 4, used), 'Points'] = np.nan
i = pick(len(t), 6, set())
t.loc[i, 'Team'] = [v.upper() if j % 2 else ' ' + v.lower() for j, v in enumerate(t.loc[i, 'Team'])]
t = pd.concat([t, t.sample(3, random_state=2)], ignore_index=True)

used = set()
p.loc[pick(len(p), 5, used), 'Average'] = np.nan
p.loc[pick(len(p), 3, used), 'Runs'] = np.nan
p.loc[pick(len(p), 2, used), 'Runs'] = 9999                # impossible runs
i = pick(len(p), 5, set())
p.loc[i, 'Team'] = [v.upper() if j % 2 else v.lower() + ' ' for j, v in enumerate(p.loc[i, 'Team'])]
p = pd.concat([p, p.sample(3, random_state=3)], ignore_index=True)

with pd.ExcelWriter('../data/generated/IPL_Sample_Data_Raw.xlsx') as w:
    m.to_excel(w, sheet_name='Matches', index=False)
    t.to_excel(w, sheet_name='Team_Stats', index=False)
    p.to_excel(w, sheet_name='Player_Stats', index=False)
print('Tidy :', matches.shape, teams.shape, players.shape)
print('Raw  :', m.shape, t.shape, p.shape)
