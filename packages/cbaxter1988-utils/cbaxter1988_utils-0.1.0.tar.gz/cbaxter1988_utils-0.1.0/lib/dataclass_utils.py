from dataclasses import asdict, is_dataclass


def dataclass_to_dict(data_class):
    if is_dataclass(data_class):
        return asdict(data_class)
