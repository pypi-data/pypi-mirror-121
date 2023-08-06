import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='nacispreloader',
    version='0.2.4',
    author='Steven Beale',
    author_email='steven.beale@woodplc.com',
    description='Preloader of nacis natural earth shapefiles',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',
    project_urls = {
        "Repo": "https://bitbucket.org/amecfwmetocean/nacis/"
    },
    license='MIT',
    packages=['nacis'],
    install_requires=['cartopy', 'requests>=2.26.0', 'boto3>=1.18.47'],
)
