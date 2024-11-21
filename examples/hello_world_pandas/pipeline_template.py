"""Template pipeline.

Some set function serve as interface points for general integration purposes. Other
nodes are marked abstract as the implementations will change (e.g. different  logic
for different business needs).

The idea is that you create placeholder nodes to restrict implementation needs and
domain expertise.
"""

from typing import Any

import numpy as np
import pandas as pd
import plotly.express as px
from hamilton.function_modifiers import tag
from plotly.graph_objs import Figure


def some_SQL_query(my_data: str) -> str:
    """This could be the actual SQL query as input straight from the data analyst.

    Alternatively, company wants to have an abstract layer like a data warehouse.
    """
    if my_data == "spending_budget":
        return "my_database"
    else:
        return "some_other_data"


def raw_data(some_SQL_query: str) -> dict:
    """Getting the correct data.

    This can be a non-trivial operation that not everyone knows how to do.
    """
    db = {
        "my_database": {
            "signups": pd.Series([1, 10, 50, np.nan, 200, 400]),
            "spend": pd.Series([np.nan, 10, 20, 40, 40, 50]) * 1e6,
        },
        "some_other_data": {
            "other_data_foo": pd.Series([0, 0, 0, 0, 0]),
            "other_data_bar": pd.Series([0, 0, 0, 0, 0]),
        },
    }

    return db[some_SQL_query]


# HERE: WOULD REALLY LIKE TO DO SOMETHING LIKE
# def pre_process(UPSTREAM[raw_data]: dict) -> ABSTRACT[pd.DataFrame]:
@tag(node_type="abstract", return_type="pd.DataFrame")
def pre_process(raw_data: dict) -> Any:
    """Placeholder.

    We can think of here that data cleaning use cases will vary and want to keep this
    flexible. E.G. remove rows vs replace NaN with 0.
    """
    pass


def initial_df(pre_process: pd.DataFrame) -> pd.DataFrame:
    """This is the starting point for another domain.

    Lets say that we need some healthy check on the data. This would be an interface
    point into the pipeline that guarantees access.
    """
    return pre_process


def save_initial_df(initial_df: pd.DataFrame) -> None:
    """Upload to database."""
    pass


# HERE: WOULD REALLY LIKE TO DO SOMETHING LIKE
# def final_df(UPSTREAM[initial_df]: pd.DataFrame) -> ABSTRACT[pd.DataFrame]:
@tag(node_type="abstract", return_type="pd.DataFrame")
def final_df(initial_df: pd.DataFrame) -> Any:
    """Placeholder.

    This is the implementation for business specific logic. This node should be replaced
    by a whole subdag with the end node being final df. Since it is abstract the input
    will be overriden anyways and it is here so that it displays nicely in the DAG.
    """
    pass


def save_final_df(final_df: pd.DataFrame) -> None:
    """Upload to database."""
    pass


@tag(node_type="abstract", return_type="pd.DataFrame")
def spending_metrics(final_df: pd.DataFrame) -> Any:
    """Placeholder.

    This is the implementation for business specific logic. This node should be replaced
    by a whole subdag with the end node being final df. Since it is abstract the input
    will be overriden anyways and it is here so that it displays nicely in the DAG.
    """
    pass


@tag(node_type="abstract", return_type="pd.DataFrame")
def signup_metrics(final_df: pd.DataFrame) -> Any:
    """Placeholder.

    This is the implementation for business specific logic. This node should be replaced
    by a whole subdag with the end node being final df. Since it is abstract the input
    will be overriden anyways and it is here so that it displays nicely in the DAG.
    """
    pass


def dashboard_spending(spending_metrics: pd.DataFrame) -> Figure:
    """Display metrics w.r.t. spending as independent variable."""
    df = spending_metrics.set_index("spend")
    return px.scatter(df, y=df.columns[0], title="Spending Metrics")


def dashboard_signups(signup_metrics: pd.DataFrame) -> Figure:
    """Display metrics w.r.t. signups as independent variable."""
    df = signup_metrics.set_index("signups")
    return px.scatter(df, y=df.columns[0], title="Signup Metrics")
