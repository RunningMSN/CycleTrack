# CycleTrack

CycleTrack is a medical school application tracking system available publicly and for free
[here](https://cycletrack.docs2be.org). We aim to fulfill the following objectives:
1. Provide an organizational tool for keeping track of the status of each application.
2. Allow applicants to easily visualize their own application cycle through graphs and maps that they can also download 
and share with friends. This is an expansion of our previous project, 
[CycleVis](https://github.com/toofastdan117/Med_School_Cycle_Analyzer).
3. Increase transparency of the medical school application process by crowdsourcing data and displaying publicly in an 
easy-to-digest manner.
4. As future data is collected, use this data to help applicants generate school lists calibrated to their individual
characteristics and needs.

## Application Tracking
The functional unit of our application tracking system is a cycle. Inside the dashboard, applicants can add a new
application cycle based on the year they plan to matriculate. Each cycle includes a settings page where statistics
(e.g. GPA, MCAT) and demographics (e.g. gender, residence) can be optionally added. Additionally, each cycle contains a
school list. New MD and DO schools can be added manually through the school selection menu or imported from an existing
excel or google spreadsheet. As the cycle progresses, the school list can be edited insert the date of admissions
actions such as the date an application was completed, interview was received, etc. The school list is displayed as a
for easy access to all schools and judging to-do items.

## Cycle Visualization
CycleTrack contains a number of options for visualizing application cycles that have been logged in the system.
Visualizations are generated from data inserted into the school list. Current visualization options include:
1. Line Graph: The line graph displays the running total of each admission action over time.
2. Bar Graph: The bar graph also displays running totals of admission actions over time, but makes it easier to visualize
what proportion of all actions each action makes up.
3. Map: The map shows the current admission status of each school along with the location of each school on a map of the
United States.
4. Dot Graph: The dot graph shows what admission actions have occurred for each school over time.
5. Sankey Diagram: The sankey diagram shows the flow of admissions actions from one status to the other at the current
time point in the application cycle.

## Data Crowdsourcing
Data collected from school lists is displayed via the [school explorer](https://cycletrack.docs2be.org/explorer). The
main page displays all schools for which data has been tracked along with basic information about them. Clicking a
school within the explorer will display an individual school page. Each school page presents more details information
about the school such as the state of admissions actions over the current application cycle as well as historic
information about applicants interviewed/accepted to that particular school. We recognize that there is likely
additional information about schools that you may like displayed. If so, please contact us and if feasible, we will work
to add this in.