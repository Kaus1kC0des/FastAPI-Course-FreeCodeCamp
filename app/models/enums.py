from sqlalchemy.dialects.postgresql import ENUM
import enum


class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"
    prefer_not_to_say = "prefer_not_to_say"
    other = "other"
