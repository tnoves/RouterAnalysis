Python script to find patterns in downtime of my home router.
This worked by providing a .csv log file acquired from the router and then flagging the time and date where certain keywords appeared.
Log files are not included in this repository due to privacy concerns, instead .png images showing some findings are included.

This project is unstructured as it was only to help identify if there were any patterns in internet dropouts which I could then show to my ISP.
The following files worked as such:
- main.py : Produces 2 aggregated heatmaps for instances where the router reported the DSL link going down and also going up over the course of a day.
- DSL_Down_Heatmap.py : Same as for main.py but only showing DSL link down instances.
- DSL_Down_Grid.py : Produces a grid showing instances the router reported the DSL ling going down listed hourly.
