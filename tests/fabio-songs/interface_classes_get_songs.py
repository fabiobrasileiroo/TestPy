# referencia do site json to parser: https://json2csharp.com/code-converters/json-to-python
from typing import List
from typing import Any
from dataclasses import dataclass
import json
@dataclass
class Datum:
    id: str
    name: str
    artists: str
    isExplicit: bool
    durationMs: int
    albumName: str
    albumReleaseDate: str

    @staticmethod
    def from_dict(obj: Any) -> 'Datum':
        _id = str(obj.get("id"))
        _name = str(obj.get("name"))
        _artists = str(obj.get("artists"))
        _isExplicit = 
        _durationMs = int(obj.get("durationMs"))
        _albumName = str(obj.get("albumName"))
        _albumReleaseDate = str(obj.get("albumReleaseDate"))
        return Datum(_id, _name, _artists, _isExplicit, _durationMs, _albumName, _albumReleaseDate)

@dataclass
class Root:
    data: List[Datum]

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _data = [Datum.from_dict(y) for y in obj.get("data")]
        return Root(_data)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)