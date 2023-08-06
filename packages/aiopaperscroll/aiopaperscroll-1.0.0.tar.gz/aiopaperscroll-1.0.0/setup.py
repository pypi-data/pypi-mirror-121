from setuptools import setup, find_packages

setup(
    name='aiopaperscroll',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'loguru',
        'asyncio',
        'aiohttp'],
    url='https://github.com/old-pinky/AioPaperScroll-SDK'
)

