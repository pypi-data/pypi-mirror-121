'''
Cybernetic Kit
Copyright (C) 2021  Civic Hacker, LLC

This program is free software: you can redistribute it and/or modify
it under the terms of the Lesser GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
Lesser GNU General Public License for more details.

You should have received a copy of the Lesser GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from datetime import date, datetime, time
from typing import List

from elasticsearch_dsl import Object, Document, InnerDoc, GeoShape, Percolator
from elasticsearch_dsl import Keyword, Float, Date, Text, Integer, GeoPoint

from civichacker import AliasDocType, geo

POLLUTANTS = [
    {'name': 'nitric oxide', 'parameter': 'NO', 'units': 'PPB'},
    {'name': 'nitrogen oxides', 'parameter': 'NOX', 'units': 'PPB'},
    {'name': 'total reactive nitrogen', 'parameter': 'NOY', 'units': 'PPB'},
    {'name': 'nitrogen dioxide', 'parameter': 'NO2T', 'units': 'PPB'},
    {'name': 'nitrogen dioxide, computed', 'parameter': 'NO2', 'units': 'PPB'},
    {'name': 'nitrogen dioxide, computed', 'parameter': 'NO2Y', 'units': 'PPB'},
    {'name': 'nitrate, not adjusted for ammonium ion', 'parameter': 'NO3', 'units': 'UG/M3'},
    {'name': 'sulfate, not adjusted for ammonium ion', 'parameter': 'SO4', 'units': 'UG/M3'},
    {'name': 'sulfur dioxide, conventional', 'parameter': 'SO2', 'units': 'PPB'},
    {'name': 'sulfur dioxide, 24-hr average', 'parameter': 'SO2-24HR', 'units': 'PPB'},
    {'name': 'sulfur dioxide, trace levels', 'parameter': 'SO2T', 'units': 'PPB'},
    {'name': 'carbon monoxide, conventional', 'parameter': 'CO', 'units': 'PPM'},
    {'name': 'carbon monoxide, 8-hr average', 'parameter': 'CO-8HR', 'units': 'PPM'},
    {'name': 'carbon monoxide, trace levels', 'parameter': 'COT', 'units': 'PPM'},
    {'name': 'elemental carbon, PM2.5', 'parameter': 'EC', 'units': 'UG/M3'},
    {'name': 'organic carbon, not adjusted for oxygen and hydrogen, PM2.5', 'parameter': 'OC', 'units': 'UG/M3'},
    {'name': 'black carbon at 880 nm', 'parameter': 'BC', 'units': 'UG/M3'},
    {'name': 'second channel of Aethalometer at 370 nm', 'parameter': 'UV-AETH', 'units': 'UG/M3'},
    {'name': 'PM2.5 mass', 'parameter': 'PM2.5', 'units': 'UG/M3'},
    {'name': 'PM10 mass', 'parameter': 'PM10', 'units': 'UG/M3'},
    {'name': 'PM2.5 mass 24-hr average', 'parameter': 'PM2.5-24HR', 'units': 'UG/M3'},
    {'name': 'PM10 mass 24-hr average', 'parameter': 'PM10-24HR', 'units': 'UG/M3'},
    {'name': 'ozone', 'parameter': 'OZONE', 'units': 'PPB'},
    {'name': 'peak ozone 8-hr average', 'parameter': 'OZONE-8HR', 'units': 'PPB'},
    {'name': 'peak ozone 1-hr maxmium', 'parameter': 'OZONE-1HR', 'units': 'PPB'},
    {'name': 'ambient temperature', 'parameter': 'TEMP', 'units': 'C'},
    {'name': 'wind speed', 'parameter': 'WS', 'units': 'M/S'},
    {'name': 'wind direction', 'parameter': 'WD', 'units': 'DEGREES'},
    {'name': 'relative humidity', 'parameter': 'RHUM', 'units': 'PERCENT'},
    {'name': 'barometric pressure', 'parameter': 'BARPR', 'units': 'MILLIBAR'},
    {'name': 'solar radiation', 'parameter': 'SRAD', 'units': 'WATTS/M2'},
    {'name': 'precipitation', 'parameter': 'PRECIP', 'units': 'MM'},
]


class Agency(InnerDoc):
    name: str = Text()
    id: str = Keyword()


class Site(AliasDocType):
    id: str = Keyword()
    code = Keyword()
    name = Text()
    website = Text()
    status = Keyword()
    type = Keyword()
    start_time = Date()
    end_time = Date()
    agency = Object(Agency)
    use = Keyword()
    outputs = Keyword(multi=True)
    inputs = Keyword(multi=True)
    region = Keyword()
    location = GeoPoint()
    elevation = Keyword()
    state = Object(geo.State)
    county = Object(geo.County)

    class Index:
        name = 'site'

    class Meta:
        doc_type = 'site'


class Pollutant(InnerDoc):
    parameter: str = Keyword()
    name: str = Text()
    units: str = Keyword()


class GeoPercolate(AliasDocType):
    geometry = GeoShape()
    query = Percolator()

    class Index:
        name = 'perc'


class AirQualityPercolate(GeoPercolate):
    location = GeoPoint()
    sitename: str = Keyword()
    aqsid: str = Keyword()

    class Index:
        name = 'airquality-perc'
        doc_type = 'airquality-perc'

    class Meta:
        doc_type = 'airquality-perc'


class AirQuality(AliasDocType):
    date: datetime = Date()
    time: str = Keyword()
    aqsid: str = Keyword()
    sitename: str = Text()
    site = Object(Site)
    offset: str = Keyword()
    pollutant = Object(Pollutant)
    units: str = Keyword()
    concentration: float = Float()
    datasource: str = Keyword()
    locality: List[str] = Keyword(multi=True)
    state: str = Keyword()
    county: str = Keyword()
    aqi: int = Integer()

    class Index:
        name = 'airquality'
        doc_type = 'airquality'

    class Meta:
        doc_type = 'airquality'
