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
from enum import Enum
from typing import Optional

from elasticsearch_dsl import Date, Text, Keyword, Integer

from civichacker import CoreModel

class DispositionEnum(str, Enum):
    enforced = 'enforce'
    report = 'report'


class CSPViolationReport(CoreModel):
    created_at: datetime = Date()
    document_uri: str = Text()
    referrer: str = Text()
    disposition: DispositionEnum = Keyword()
    effective_directive: str = Text()
    original_policy: str = Text()
    script_sample: str = Text()
    status_code: int = Integer()
    violated_directive: str = Text()
    line_number: int = Integer()
    client_ip: str = Keyword()

    class Index:
        name = "csp-*"

    async def save(self, **kwargs):
        today = datetime.utcnow().strftime('%Y.%m.%d')
        self.meta.index = f'csp-{today}'
        return await super().save(**kwargs)
