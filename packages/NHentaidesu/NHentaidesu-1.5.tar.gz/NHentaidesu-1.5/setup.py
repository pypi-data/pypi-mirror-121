from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='NHentaidesu',
    version='1.5',
    description='NHentai API wrapper with hybrid runtime.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url='https://github.com/rushkii/NHentaidesu',
    author='Kiizuha',
    author_email='riskimuhammmad1@gmail.com',
    keywords='nhentai nhentaidesu nhentai-python nhentai python nhentai api',
    license='MIT',
    packages=find_packages(exclude=['downloads', 'example.py']),
    install_requires=[
        'aiofiles',
        'bs4',
        'aiohttp',
        'img2pdf',
        'dateparser',
        'python-magic',
        'python-magic-bin==0.4.14'
    ],
    include_package_data=True,
    zip_safe=False
)