'''
Created on 09-07-2019

:author: Leandro (Cerberus1746) Benedet Garcia
'''
import pytest

from .. import data_core
from ..custom_exceptions import DuplicatedModelTypeName
from ..model import Model


class TestClass(object):
	model_type_name = "model_type_name"
	second_model_type_name = "second_model_type_name"
	model_with_init_name = "model_with_init_name"
	creation_test_name = "creation_test_name"

	default_test_field_name = "name"
	default_test_field_content = "name_content"

	yaml_content = f"""
data:
    - {default_test_field_name}: {default_test_field_content}
""".strip()

	instance_error = "The class wansn't instanced correctly, check __new__ in ModelMixin class"

	@staticmethod
	def create_test_model(model_name):
		test_model = data_core.get_model_type(model_name, default=False)
		if not test_model:
			class TestModel(Model, model_name=model_name):
				name: str

			test_model = TestModel

		return test_model

	@pytest.fixture
	def model(self):
		return self.create_test_model(self.model_type_name)

	@pytest.fixture
	def model_with_init(self):
		test_model = data_core.get_model_type(self.model_with_init_name, default=False)
		if not test_model:
			class TestModelWithInit(Model, model_name=self.model_with_init_name):
				name: str

				def __init__(self):
					self.name = TestClass.default_test_field_content

			test_model = TestModelWithInit

		return test_model

	@pytest.fixture
	def second_model(self):
		return self.create_test_model(self.second_model_type_name)

	def test_check_if_equal(self, model):
		assert data_core.get_model_type(self.model_type_name) == model

	@staticmethod
	def test_check_if_unequal(model, second_model, model_with_init):
		assert model != second_model != model_with_init

	def test_direct_instance_dataclass(self, model):
		model_type = data_core.get_model_type(self.model_type_name)
		instanced = model_type(self.default_test_field_content)

		assert isinstance(instanced, model), self.instance_error
		assert getattr(instanced, self.default_test_field_name) == self.default_test_field_content

		instanced = model_type(name=self.default_test_field_content)
		assert instanced.name == self.default_test_field_content

	def test_instance_dataclass_with_init(self, model_with_init):
		model_type = data_core.get_model_type(self.model_with_init_name)
		instanced = model_type()

		assert isinstance(instanced, model_with_init), self.instance_error
		assert getattr(instanced, self.default_test_field_name) == self.default_test_field_content

	def test_load_from_file(self, tmpdir, model):
		tmp_dir =  tmpdir.mkdir("raws")
		yaml_file = tmp_dir.join("test.yaml")
		yaml_file_path = str(yaml_file.realpath())

		yaml_file.write(self.yaml_content)

		instanced = model(db_file=yaml_file_path)
		assert isinstance(instanced, model), self.instance_error
		assert getattr(instanced, self.default_test_field_name) == self.default_test_field_content

	def test_assert_model_is_unique(self, model):
		assert model
		with pytest.raises(DuplicatedModelTypeName):
			class TestModel(Model, model_name=self.model_type_name):
				name: str
