from setuptools import setup, find_packages

setup(
    name="mkdocs-oceanbase-test",
    version='0.0.1',
    url='',
    license='',
    description='oceanbase static site theme',
    author='zhouzi',
    author_email='3222676446@qq.com',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'mkdocs.themes': [
            'oceanbase_theme_test = oceanbase_theme_test',
        ]
    },
    zip_safe=False
)
