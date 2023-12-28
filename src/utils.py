import us
from plotly.subplots import make_subplots


def add_iso2_to_dataframe(dataframe, col):
    dataframe["code"] = dataframe[col].apply(lambda x: us.states.lookup(x).abbr if us.states.lookup(x) else None)
    return dataframe


season_mapping = {
    "December": 'Winter',
    "January": 'Winter',
    "February": 'Winter',
    "March": 'Spring',
    "April": 'Spring',
    "May": 'Spring',
    "June": 'Summer',
    "July": 'Summer',
    "August": 'Summer',
    "September": 'Autumn',
    "October": 'Autumn',
    "November": 'Autumn'
}


month_order = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]


update_layout_fig = dict(
    template="simple_white",
    paper_bgcolor="white",
    plot_bgcolor="white"
)



