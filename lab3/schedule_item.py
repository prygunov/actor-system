from dataclasses import dataclass
from lab3.order_entity import OrderEntity

@dataclass
class ScheduleItem:
    """
    Класс записи расписания
    """
    order: OrderEntity
    rec_type: str
    start_time: int
    end_time: int
    point_from: Point
    point_to: Point
    cost: float
    all_params: dict
    