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

import typing
from collections import namedtuple
from datetime import datetime, date
from itertools import filterfalse

from civichacker.util import is_attr_required

from elasticsearch_dsl import Document, Date, Text, Keyword, Integer


def simple_mapping(anno):
    if anno == str:
        return Keyword()
    elif anno == int:
        return Integer()
    else:
        return Text()


class ElasticModel(Document):

    pk: str = Text(fields={'raw': Keyword()})
    inserted_at: date = Date()

    @classmethod
    def alias(cls):
        return cls.Index.name

    @classmethod
    def setup(cls, alias, pattern):
        index_template = cls._index.as_template(alias, pattern)
        index_template.save()
        # if not cls._index.exists():
        #    cls.migrate(alias, pattern, move_data=False)

    @classmethod
    def migrate(cls, alias, pattern, move_data=True, update_alias=True):
        next_index = pattern.replace('*', datetime.now().strftime('%Y.%m.%d'))
        es = connections.get_connection()
        es.indices.create(index=next_index)
        if move_data:
            # move data from current alias to the new index
            es.reindex(
                body={"source": {"index": alias}, "dest": {"index": next_index}},
                request_timeout=3600
            )
            # refresh the index to make the changes visible
            es.indices.refresh(index=next_index)
        if update_alias:
            # repoint the alias to point to the newly created index
            es.indices.update_aliases(body={
                'actions': [
                    {"remove": {"alias": alias, "index": pattern}},
                    {"add": {"alias": alias, "index": next_index}},
                ]
            })


AliasDocType = ElasticModel

class CoreModel(ElasticModel):
    def __init__(self, *args, **kwargs):
        hints = typing.get_type_hints(type(self))
        required = filterfalse(lambda key: is_attr_required(hints[key]), hints.keys())
        namedtuple("klass", required)(**kwargs)
        return super(ElasticModel, self).__init__(*args, **kwargs)
