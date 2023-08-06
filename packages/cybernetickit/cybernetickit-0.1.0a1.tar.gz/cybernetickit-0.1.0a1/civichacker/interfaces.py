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

from abc import ABCMeta, abstractmethod
from typing import Any

from civichacker import CoreModel


class Repository(metaclass=ABCMeta):

    def __init__(self, model: CoreModel):
        pass

    @abstractmethod
    def create(self, model: CoreModel) -> CoreModel:
        model.save()

    @abstractmethod
    def get(self, id: Any) -> CoreModel:
        return model.get(id)

    @abstractmethod
    def delete(self, id: Any) -> CoreModel:
        pass

    @abstractmethod
    def update(self, model: CoreModel) -> CoreModel:
        pass

    @abstractmethod
    def update(self, id: Any, fields: dict) -> CoreModel:
        pass
