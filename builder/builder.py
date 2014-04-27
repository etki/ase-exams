#!/usr/bin/env python
# coding=utf-8

from sources.config import AseConfig
from sources.builder import AseBuilder
try:
    from config import CONFIG
    ase_config = AseConfig(CONFIG)
except ImportError:
    ase_config = AseConfig()

from sources.parser import AseParser

AseBuilder(ase_config).build()