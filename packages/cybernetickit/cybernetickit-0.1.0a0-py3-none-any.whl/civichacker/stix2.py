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

from datetime import datetime
import uuid
from typing import List, Optional, Dict

from stix2.datastore import DataSink, DataSource

from civichacker import CoreModel


class StixMetaObject(CoreModel):
    type: str
    spec_version: str
    id: str
    created_by_ref: str
    created: datetime
    modified: datetime
    revoked: Optional[bool]
    labels: Optional[List[str]]
    confidence: Optional[int]
    lang: Optional[str]
    external_references: Optional[List[str]]
    object_marking_refs: Optional[List[str]]
    granular_markings: Optional[List[str]]
    defanged: Optional[bool]
    extensions: Optional[Dict]


    class Index:
        name = "stix-*"


class StixCore(CoreModel):
    type: str
    spec_version: str
    id: str
    created_by_ref: Optional[str]
    created: datetime
    modified: datetime
    revoked: Optional[bool]
    labels: Optional[List[str]]
    confidence: Optional[int]
    lang: Optional[str]
    external_references: Optional[List[str]]
    object_marking_refs: Optional[List[str]]
    granular_markings: Optional[List[str]]
    defanged: Optional[bool]
    extensions: Optional[Dict]

    @classmethod
    def from_stix(stix_instance: Dict):
        pass

    class Index:
        name = "stix-*"


class ElasticSink(DataSink):

    id = uuid.uuid4()

    def add(stix_objs: List[StixModel]):
        pass


class ElasticSource(DataSource):

    id = uuid.uuid4()

    def get(stix_id:str) -> StixModel:
        pass

    def all_versions(stix_id:str) -> List[StixModel]:
        pass

    def query() -> List[StixModel]:
        pass
