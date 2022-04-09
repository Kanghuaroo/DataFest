import pandas as pd

df = pd.read_csv("data/player-6607011.csv")

p = df[df['event_id'] == 911]
p = p.dropna(axis=1, how='all')
p.to_csv("people_minigame.csv")
