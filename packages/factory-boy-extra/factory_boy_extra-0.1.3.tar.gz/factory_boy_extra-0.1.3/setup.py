# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['factory_boy_extra']

package_data = \
{'': ['*']}

install_requires = \
['factory-boy>=3.2.0,<4.0.0']

setup_kwargs = {
    'name': 'factory-boy-extra',
    'version': '0.1.3',
    'description': '',
    'long_description': '# Extra factories for factory_boy\n\nThis library contains 2 base factories.\n* AsyncSQLAlchemyModelFactory\n* TortoiseModelFactory\n\n\n## TortoiseModelFactory\nIs made to use it with tortoise-orm.\n\n### Usage\n\nIt works aout of the box, if you have already initialized \ntortoise-orm for testing.\n\nYou can check how to do this in [tortoise docs](https://tortoise-orm.readthedocs.io/en/latest/contrib/unittest.html#py-test).\n\n```python\nimport factory\nfrom tortoise import fields, models\nfrom factory_boy_extra.tortoise_factory import TortoiseModelFactory\n\n\nclass TargetModel(models.Model):\n    name = fields.CharField(max_length=200)\n\n\nclass TargetModelFactory(TortoiseModelFactory):\n    name = factory.Faker("word")\n\n    class Meta:\n        model = TargetModel\n```\n\nThat\'s it. Now you can use it in your tests, E.G.\n\n```python\n@pytest.mark.asyncio\nasync def test_factories():\n    targets = TargetModelFactory.create_batch(10)\n    actual_models = await TargetModel.all()\n    assert len(actual_models) == 10\n```\n\n## AsyncSQLAlchemyModelFactory\n\n### Usage\nAt your conftest.py initialize your factories\nwith AsyncSession.\n\n```python\n@pytest.fixture(autouse=True)\ndef init_factories(dbsession: AsyncSession) -> None:\n    """Init factories."""\n    BaseFactory.session = dbsession\n```\n\nThe dbsession factory can be obtained in [pytest-async-sqlalchemy](https://pypi.org/project/pytest-async-sqlalchemy/) library,\nor you can add it by yourself:\n\n```python\nimport pytest\nfrom sqlalchemy.ext.asyncio import create_async_engine, AsyncSession\nfrom sqlalchemy.orm import sessionmaker\n\n\n@pytest.fixture()\nasync def dbsession():\n    """\n    Fixture that returns a SQLAlchemy session with a SAVEPOINT, and the rollback to it\n    after the test completes.\n    """\n    engine = create_async_engine(database_url) # You must provide your database URL.\n    connection = await engine.connect()\n    trans = await connection.begin()\n\n    Session = sessionmaker(connection, expire_on_commit=False, class_=AsyncSession)\n    session = Session()\n\n    try:\n        yield session\n    finally:\n        await session.close()\n        await trans.rollback()\n        await connection.close()\n        await engine.dispose()\n```\n\nNow you can create factories and use them in your tests.\n\n```python\nfrom factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory\n\nclass TargetModel(Base):\n\n    __tablename__ = "targetmodel"\n\n    name = Column(String(length=120), nullable=False)  # noqa: WPS432\n\n\nclass TargetModelFactory(AsyncSQLAlchemyModelFactory):\n    name = factory.Faker("word")\n\n    class Meta:\n        model = TargetModel\n```\n\nIn tests it wil look like this:\n```python\nimport pytest\n\nfrom sqlalchemy.ext.asyncio import AsyncSession\nfrom sqlalchemy import select\n\n\n@pytest.mark.asyncio\nasync def test_successful_notification(dbsession: AsyncSession) -> None:\n    TargetModelFactory.create_batch(10)\n    actual_models = (await dbsession.execute(select(TargetModel))).fetchall()\n    assert len(actual_models) == 10\n```',
    'author': 'Pavel Kirilin',
    'author_email': 'win10@list.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/s3rius/factory_boy_extra',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.7,<4.0.0',
}


setup(**setup_kwargs)
