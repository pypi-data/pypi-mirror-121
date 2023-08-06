from setuptools import setup

VERSION = "0.2.0"

install_requires = [
    'websocket-client',
    'netifaces'
]

setup(
    name="vmilabs",
    version=VERSION,
    description="official SDK for vmilabs product pillar",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author="vmilabs",
    author_email="kern_zhous@163.com",
    license="Apache-2.0",
    url="https://github.com/openvmi/sdk.sandbox.python.git",
    python_requires='>=3.6',
    keywords="vmilabs SDK",
    install_requires=install_requires,
    packages=["vmilabs"],
)
