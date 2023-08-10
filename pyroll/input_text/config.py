import pyroll.core as pr


@pr.config("PYROLL_IMPORT")
class Config:
    FACTORY_KEY = "__ctor__"
    """Defines the key used to store the name of the factory function used to construct an object when importing dicts."""