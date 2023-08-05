import pandas as pd

class jhu_extract:

    def __init__(self, kind):
        self.kind = kind
    
    def extract_data(self) -> pd.DataFrame:
        if self.kind == "cases":
            return pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv")
        elif self.kind == "deaths":
            return pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv")
        else:
            print("must select either cases or deaths when instantiating extract object...")