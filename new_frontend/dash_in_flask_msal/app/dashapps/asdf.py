import plotly.graph_objects as go
labels=['human','rat','human-plasma','rat-plasma','human-plasma-no','rat-plasma-no'],
fig =go.Figure(go.Sunburst(
    # labels=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
    # parents=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
    # values=[10, 14, 12, 10, 2, 6, 6, 4, 4],
    labels=labels
    parents=['','','human','rat','human-plasma','rat-plasma'],
    values=[1 for i in range(len(labels))]
))
# Update layout for tight margin
# See https://plotly.com/python/creating-and-updating-figures/
fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))

fig.show()