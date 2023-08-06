from setuptools import setup

setup(
    name='discord_port',
    version='1.4',
    description='discord_port is a simple way to make auth with the Discord API!',
    license='MIT',
    long_description=open('README.md','r',encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='airbu',
    author_email='airbu.email@gmail.com',
    keywords=['discord','api','oauth'],
    packages=['discord_port'],
    install_requires=['requests'],
    package_dir={'discord_port': 'discord_port'},
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)