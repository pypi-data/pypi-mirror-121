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

from typing import List
from datetime import datetime, date
from elasticsearch_dsl import Keyword, Nested, Date, Object, Text, InnerDoc, GeoPoint, Integer
from civichacker import AliasDocType


REPO_TYPES = [
    {'id': 'socrata', 'name': 'Socrata'},
    {'id': 'ckan', 'name': 'CKAN'},
    {'id': 'dkan', 'name': 'DKAN'},
    {'id': 'opendatasoft', 'name': 'OpenDataSoft'},
    {'id': 'oai', 'name': 'OpenArchives Initiative'},
    {'id': 'arcgis', 'name': 'ArcGIS'},
    {'id': 'web', 'name': 'Generic Web Datasource'},
    {'id': 'frictionless', 'name': 'Frictionless Data'},
    {'id': 'junar', 'name': 'Junar'},
    {'id': 'google', 'name': 'Google Datasource'}
]

class DataSourceType(InnerDoc):
    name: str = Keyword()
    identifier: str = Keyword()


class Repository(InnerDoc):
    name: str = Keyword()
    id: str = Keyword()
    version: str = Keyword()
    url: str = Keyword()


class DataHighlight(InnerDoc):
    name: str = Keyword()
    id: str = Keyword()
    version: str = Keyword()
    url: str = Keyword()
    modified: date = Date()
    created: date = Date()


class DataSource(AliasDocType):
    id: str = Keyword()
    url = Keyword()
    name: str = Text()
    level: str = Keyword()  # city, state, federal
    locality: List[str] = Keyword(multi=True)
    total: int = Integer()
    new = Object(DataHighlight)
    updated = Object(DataHighlight)
    location = GeoPoint()
    version: str = Keyword()
    type = Object(DataSourceType)

    class Index:
        name = 'datasource'
        doc_type = 'datasource'

    class Meta:
        doc_type = 'datasource'

    def add_updated(self, name, url, identifier, created, updated):
        self.updated.append(
            DataHighlight(name=name, url=url, id=identifier, created=created, updated=updated)
        )

    def add_new(self, name, url, identifier, created, updated=None):
        self.new.append(
            DataHighlight(name=name, url=url, id=identifier, created=created, updated=updated)
        )


class DataSourceDoc(InnerDoc):
    id: str = Keyword()
    url: str = Keyword()
    name: str = Text()
    level: str = Keyword()  # city, state, federal
    locality: List[str] = Keyword(multi=True)
    location = GeoPoint()
    version: str = Keyword()
    type = Object(DataSourceType)

    class Index:
        name = 'datasource'
        doc_type = 'datasource'

    class Meta:
        doc_type = 'datasource'


class PointOfContact(InnerDoc):
    fn: str = Keyword()
    ln: str = Keyword()
    email: str = Text()


class DataSet(AliasDocType):

    class Index:
        name = 'dataset'
        doc_type = 'dataset'

    class Meta:
        doc_type = 'dataset'

    name: str = Text()
    format: str = Keyword()
    description: str = Text()
    category: str = Keyword()
    type: str = Keyword()
    repository = Object(Repository)
    tags: List[str] = Keyword(multi=True)
    raw = Object()
    source = Object(DataSourceDoc)
    url: str = Keyword()
    odata: str = Keyword()
    identifier: str = Keyword()
    landing: str = Keyword()
    distribution = Object(properties={
        '@type': Keyword(),
        'downloadURL': Keyword(),
        'mediaType': Keyword(),
    })
    modified: date  = Date()
    created: date = Date()
    locality: List[str] = Keyword(multi=True)
    level: str = Keyword()
    contact = Object(PointOfContact)

    def add_distribution(self, download):
        self.distribution.append({
            '@type': download['@type'],
            'downloadURL': download['downloadURL'],
            'mediaType': download['mediaType']
        })


class Data(AliasDocType):
    locality: str = Keyword(multi=True)
    level: str = Keyword()
    identifier: str = Keyword()
    field = Object(properties={
        'name': Keyword(),
        'type': Keyword()})

    class Index:
        name = 'data'
        doc_type = 'data'
