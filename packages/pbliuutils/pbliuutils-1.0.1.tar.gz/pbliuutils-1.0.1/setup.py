from setuptools import setup

setup(name='pbliuutils',
      version='1.0.1',
      description='A util for file operation',
      author='pbliu',
      author_email='sbpt123456@126.com',
      url='https://www.python.org/',
      license='MIT',
      keywords='simpleitk pickle',
      project_urls={
            'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
            'Funding': 'https://donate.pypi.org',
            'Source': 'https://github.com/pypa/sampleproject/',
            'Tracker': 'https://github.com/pypa/sampleproject/issues',
      },
      packages=['pbliu_utils'],
      install_requires=['SimpleITK'],
      python_requires='>=3'
     )
