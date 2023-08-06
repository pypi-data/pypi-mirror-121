from setuptools import setup
import os
import sys

if sys.version_info[0] < 3:
    with open('README.md') as f:
        long_description = f.read()
else:
    with open('README.md', encoding='utf-8') as f:
        long_description = f.read()

# version = {}
# with open(os.path.join('appyweather', 'version.py')) as f:
#     exec(f.read(), version)

setup(
    name='appyweather',
    packages=['appyweather'],
    version='1.0.1',
    license='MIT',
    description='24h Weather Forecast Data',
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    author='Kostas Deligiannis',
    author_email='pr0fil3r@gmail.com',
    url='https://example.com',
    keywords=['weather', 'forecast', 'openweather'],
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
