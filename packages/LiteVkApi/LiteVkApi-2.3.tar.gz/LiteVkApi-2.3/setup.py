from setuptools import setup


long_description = """
# LiteVkApi
Бот в Вк? Легко!

Из-за некорректного отображения документации в PyPI, она была полностью перемещена на гитхаб - https://github.com/Ma-Mush/LiteVkApi/
"""


setup(
    name="LiteVkApi",
    version="2.3",
    description="Библиотека для лекгого написания ботов ВК!",
    packages=["LiteVkApi"],
    author_email="ma_mush@mail.ru",
    zip_safe=False,
    python_requires=">=3.6",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires= "vk-api==11.9.1"
)
