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

from elasticsearch_dsl import Keyword, Nested, Date, Object, Text
from civichacker import CoreModel
from typing import List, Optional


class Preprint(CoreModel):
    title: str = Text()
    description: str = Text(multi=True)
    identifier: str = Keyword(multi=True)
    oai_id: str = Keyword()
    publisher: str = Keyword()
    set: List[dict] = Object(properties={
                 'code': Keyword(),
                 'name': Keyword()
                 }, multi=True)
    creator: List[str] = Text(multi=True)
    subject: List[str] = Keyword(multi=True)
    type: str = Keyword()
    date: List[str] = Date(multi=True)
    uploaded_at = Date()
    format: str = Keyword()
    source: str = Keyword()
    language: str = Keyword()
    rights: Optional[List[str]] = Keyword(multi=True)
    repository: dict = Object(properties={
                        'id': Keyword(),
                        'name': Keyword()})

    class Meta:
        index = 'preprint'
        doc_type = 'preprint'

    class Index:
        name = 'preprint'


class Repository(CoreModel):
    name: str = Text()
    description: str = Text()
    topic: str = Keyword()
    type: str = Keyword()
    tags: List[str] = Keyword(multi=True)
    city: Optional[str] = Keyword()  # blank for state and federal datasets
    state: Optional[str] = Keyword()  # blank for federal datasets
    administrative_level: str = Keyword()  # city, state, federal
    institution: str = Text()
    agency: str = Text()
    base_url: str = Keyword()
    formats = Nested(properties={
                        'name': Keyword(),
                        'schema': Keyword(),
                        'url': Keyword()
                        })
    version: str = Keyword()
    emails: List[str] = Keyword(multi=True)

    sets = Nested(properties={
                        'namespace': Keyword(),
                        'name': Keyword()
                    })

    class Meta:
        index = 'repository'
        doc_type = 'repository'

    class Index:
        name = 'repository'
