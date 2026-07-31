from dataclasses import asdict, dataclass


@dataclass
class DTO:
    def to_dict(obj):
        return asdict(obj, dict_factory=lambda x: {k: v for (k, v) in x if v is not None})
