import pandas as pd
from pandas import DataFrame
import plotly.express as px
from plotly.graph_objects import Figure


def get_jump_goals() -> DataFrame:
    """
    Returns a DataFrame of premade jump goals and/or custom goals added by user.
    In the future will likely refactor to get goals from db.
    """
    df_jump_goal_dict = {'jump goal measurements': {0: 'net height',
                                                    1: 'top of antenna over net height',
                                                    2: 'comfortably dunking height',
                                                    3: 'rim height'},
                         'value': {0: 243.0, 1: 322.0, 2: 320.04, 3: 304.8},
                         'unit': {0: 'cm', 1: 'cm', 2: 'cm', 3: 'cm'}}

    df_jump_goals = DataFrame.from_dict(df_jump_goal_dict)
    return df_jump_goals


def get_personal_measurements() -> DataFrame:
    """
    Returns a DataFrame of users height and standing reach to later calculate vertical jump height.
    In the future will likely refactor to get goals from db.
    """
    df_personal_measurements_dict = {'personal measurements': {0: 'height', 1: 'standing reach'},
                                     'value': {0: 176.53, 1: 222.25},
                                     'unit': {0: 'cm', 1: 'cm'}}

    df_personal_measurements = DataFrame.from_dict(df_personal_measurements_dict)
    return df_personal_measurements


def get_highest_jumps() -> DataFrame:
    """
    Returns a DataFrame of users past jumps (now labeled 'spike approach reach'). Edits date field
    to be a Pandas data dtype.
    In the future will likely refactor to get goals from db.
    """
    df_spike_height_dict = {'jump measurements': {1: 'spike approach reach',
                                                  3: 'spike approach reach',
                                                  5: 'spike approach reach',
                                                  7: 'spike approach reach'},
                            'value': {1: 299.3, 3: 305.8, 5: 304.8, 7: 308.3},
                            'unit': {1: 'cm', 3: 'cm', 5: 'cm', 7: 'cm'},
                            'date': {1: '1/5/2022', 3: '3/17/2022', 5: '4/7/2022', 7: '4/10/2022'}}

    df_spike_height_raw = DataFrame.from_dict(df_spike_height_dict)
    df_spike_height = df_spike_height_raw.loc[df_spike_height_raw["jump measurements"] == "spike approach reach"]
    df_spike_height["date"] = pd.to_datetime(df_spike_height["date"], format='%m/%d/%Y', errors='ignore')
    return df_spike_height


# show difference between jump and goals - graph
def graph_jump_progress(df_spike_height: DataFrame, df_jump_goals: DataFrame) -> Figure:
    spike_height_progress = px.line(
        x=df_spike_height["date"],
        y=df_spike_height["value"],
        range_x=["2022-01-01", "2022-12-31"],
        range_y=[200, 350],
        markers=True
    )

    for goal_name, goal_value in zip(df_jump_goals["jump goal measurements"].values, df_jump_goals["value"].values):
        spike_height_progress.add_hline(goal_value, annotation_text=goal_name)

    return spike_height_progress


# show difference between jump and goals - numbers
def get_latest_spike_height(df_spike_height: DataFrame) -> float:
    latest_reach_float = df_spike_height.sort_values(by="date").tail(1)["value"].values[0]
    return latest_reach_float


def get_differences_from_goals(latest_spike_height: float, df_jump_goals: DataFrame) -> DataFrame:
    df_jump_goals["goal difference"] = df_jump_goals["value"] - latest_spike_height
    df_jump_goals["achieved"] = 1
    df_jump_goals.loc[df_jump_goals["goal difference"] > 0, "achieved"] = 0
    return df_jump_goals


# show increase in jump over time (e.g. compare to about 1 inch gain per month being good)

# show increase in vert over time (e.g. compare to about 1 inch gain per month being good)

# estimate time to reach next goal (1. based on past performance / 2. based on about 2cm gain per month)
def get_months_to_next_goal(df_differences: DataFrame) -> DataFrame:
    """
    Using a heuristic for now to calculate the time to get to the next goal.
    Currently taking the difference between the next jump goal and the current highest jump
    and dividing by 2.54 cm (1 inch) as a metric of how many cm you should gain per month
    and therefore how many months until you achieve your next goal.
    In the future may refactor to use other methods (linear/log reg, ml?) to estimate time.
    """
    next_goal_df = df_differences.loc[(df_differences["achieved"] == 0)].min()
    next_goal_df["months to goal"] = next_goal_df["goal difference"] / 2.54
    return next_goal_df
