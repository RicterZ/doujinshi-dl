# coding: utf-8
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Iterator, Tuple


@dataclass
class GalleryMeta:
    id: str
    name: str
    pretty_name: str
    img_id: str
    ext: list
    pages: int
    info: Dict[str, Any] = field(default_factory=dict)
    extra: Dict[str, Any] = field(default_factory=dict)  # plugin-private data

    def to_dict(self) -> dict:
        d = {
            'id': self.id,
            'name': self.name,
            'pretty_name': self.pretty_name,
            'img_id': self.img_id,
            'ext': self.ext,
            'pages': self.pages,
        }
        d.update(self.info)
        d.update(self.extra)
        return d


class BaseParser(ABC):
    @abstractmethod
    def fetch(self, gallery_id: str) -> GalleryMeta: ...

    @abstractmethod
    def search(self, keyword: str, sorting: str = 'date', page=None, **kwargs) -> List[Dict]: ...

    def artist(self, artist_name: str, sorting: str = 'date', page=None, **kwargs) -> List[Dict]:
        return self.search(f'artist:{artist_name}', sorting=sorting, page=page, **kwargs)

    def favorites(self, page=None) -> List[Dict]:
        return []

    def configure(self, args): ...


class BaseModel(ABC):
    @abstractmethod
    def iter_tasks(self) -> Iterator[Tuple[str, str]]: ...
    # yields (url, filename) tuples


class BaseSerializer(ABC):
    @abstractmethod
    def write_all(self, meta: GalleryMeta, output_dir: str): ...

    def finalize(self, output_dir: str) -> None:
        pass


class BasePlugin(ABC):
    name: str

    @abstractmethod
    def create_parser(self) -> BaseParser: ...

    @abstractmethod
    def create_model(self, meta: GalleryMeta, name_format: str = '[%i][%a][%t]') -> BaseModel: ...

    @abstractmethod
    def create_serializer(self) -> BaseSerializer: ...

    def register_args(self, argparser): pass

    def check_auth(self) -> None:
        pass

    def print_results(self, results) -> None:
        pass
