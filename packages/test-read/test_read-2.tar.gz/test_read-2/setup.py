import setuptools

setuptools.setup(
    name='test_read',
    version='2',
    packages=setuptools.find_packages(),
    description='test_read',
    include_package_data=True,
    package_data={"": ["*.json"]}
)
    