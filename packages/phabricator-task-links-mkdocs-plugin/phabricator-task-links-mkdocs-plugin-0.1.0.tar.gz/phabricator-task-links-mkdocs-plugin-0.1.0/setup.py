import io
from setuptools import setup

from pathlib import Path

readme_path = Path(__file__).parent / "README.md"

with io.open(readme_path, encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="phabricator-task-links-mkdocs-plugin",
    version="0.1.0",
    packages=["phabricator_task_links"],
    url="https://github.com/theskumar/autolink-references-mkdocs-plugin",
    license="MIT",
    author="Daniel Palstra",
    author_email="noreply@danielpalstra.github.com",
    description="This plugin will create links when using Phabricator task numbers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["mkdocs"],
    # The following rows are important to register your plugin.
    # The format is "(plugin name) = (plugin folder):(class name)"
    # Without them, mkdocs will not be able to recognize it.
    entry_points={
        "mkdocs.plugins": [
            "phabricator_task_links = phabricator_task_links:PhabricatorTaskLinks",
        ]
    },
)
