import setuptools

setuptools.setup(
    name='link',
    packages=setuptools.find_packages(),
    description="Link - Fetch's link to the rest of world",
    version='3.0.2',
    url='https://github.com/h4ck3rk3y/link',
    author='Fetch',
    author_email='hello@gofetch.io',
    keywords=[],
    install_requires=[
        "grequests>=0.6.0",
        "requests>=2.24.0",
    ],
)
