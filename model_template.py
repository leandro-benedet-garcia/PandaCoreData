'''
Created on 2019-04-26

@author: Leandro (Cerberu1746) Benedet Garcia
'''

from core_data.model_mixin import ModelMixin
from dataclasses import dataclass
from . import data_core


class ModelTemplate(ModelMixin):


	def __init__(self, mod, db_file):
		super().__init__(mod, db_file)
