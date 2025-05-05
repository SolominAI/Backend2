from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room


class RoomsRepositories(BaseRepository):
    model = RoomsOrm
    schema = Room

