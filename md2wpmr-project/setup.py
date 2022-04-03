from setuptools import setup, find_packages

setup(
    name="mkdocsexporttoweasyprintmatrixrobots",
    version="0.1",
    packages=["md2wpmr"],
    # include_package_data=True,
    entry_points={
        'mkdocs.plugins': [
            'md2wpmr = md2wpmr.plugin:Export'
        ]
    }
)