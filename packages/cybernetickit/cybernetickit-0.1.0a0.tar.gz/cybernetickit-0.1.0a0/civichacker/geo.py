'''
Copyright (C) 2021  Civic Hacker, LLC <opensource@civichacker.com>

This program is free software: you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation, either
version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this program.  If not, see
<http://www.gnu.org/licenses/>.
'''


from elasticsearch_dsl import Keyword, GeoShape, GeoPoint, Text, Double
from elasticsearch_dsl import Object, InnerDoc
from civichacker import AliasDocType, util


class Area(InnerDoc):
    land: float = Double()
    water: float = Double()


class State(AliasDocType):
    name: str = Keyword()
    abbr: str = Keyword()
    fips: str = Keyword()
    geometry = GeoShape()
    area = Object(Area)
    centroid = GeoPoint()

    class Index:
        name = 'state'
        doc_type = 'state'

    class Meta:
        doc_type = 'state'


class County(AliasDocType):
    name: str = Text()
    name_full: str = Text()
    fips: str = Keyword()
    state: str = Keyword()
    geometry = GeoShape()
    centroid = GeoPoint()
    area = Object(Area)

    class Index:
        name = 'county'
        doc_type = 'county'

    class Meta:
        doc_type = 'county'
