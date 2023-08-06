from .config import configuration
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
import sys

model = declarative_base()


class _domain(type):
    domainList = {}

    def __getattr__(self, name):
        if name not in _domain.domainList:
            module = getattr(__import__("{service}.{name}".format(service=configuration.domain_path.replace(configuration.appPath, "").lstrip("/").replace("/", "."), name=name)), name)
            d = getattr(module, name)
            _domain.domainList[name] = d
        return _domain.domainList[name]

class domain(metaclass=_domain):
    model = model

    class table:
        id = Column(Integer, primary_key=True)

        @staticmethod
        def string(len):
            return Column(String(len))

        @staticmethod
        def number():
            return Column(Integer)
