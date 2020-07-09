# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Dict
import math
from pandas import DataFrame
from lib.data_source import DataSource
from lib.time import datetime_isoformat
import  datetime
from lib.cast import safe_int_cast

class LibyaHumdataDataSource(DataSource):
   
    def parse_dataframes(
        self, dataframes: Dict[str, DataFrame], aux: Dict[str, DataFrame], **parse_opts
    ) -> DataFrame:

        # Rename the appropriate columns
        data = (
            dataframes[0]
            .rename(
                columns={
                    "Location": "subregion1_name",
                    "Confirmed Cases": "total_confirmed",
                    "Deaths": "total_deceased",
                    "Recoveries": "total_recovered",
                    "Date": "date",  # is already in format "%Y-%m-%d"
                }
            )
            .drop(columns=["Active"])
        )

        # The first row is metadata info about column names - discard it
        data = data[data.subregion1_name != '#loc+name']
      
        # Convert string numbers to int
        # Parse integers
        for column in ("total_confirmed", "total_deceased", "total_recovered"):
            data[column] = data[column].apply(lambda x: safe_int_cast(str(x).replace(",", "")))
        
        # Make sure all records have the country code
        data["country_code"] = "LY"

        # Output the results
        return data
