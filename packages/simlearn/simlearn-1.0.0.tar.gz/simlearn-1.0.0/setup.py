import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name         = 'simlearn',
    version      = '1.0.0',
    author       = 'Alexander D. Kazakov',
    author_email = 'alexander.d.kazakov@gmail.com',
    description  = 'Simlearn is a way how to teach/learn about simulations with a joy. PyStar is a main application of it.',
    license      = 'GNU',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url          = 'https://gitlab.com/alexander.d.kazakov/pystar',
    packages     =  setuptools.find_packages(),
    keywords     = ['simulations', "molecular dynamics", "LJ", "CG"],
    classifiers=[
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.8',
      'Programming Language :: Python :: 3.9',
      ],
    python_requires='>=3.8',
    install_requires=[
        'pyqt5-sip',
        'pyqt5-tools',
        'pyqt5',
        'pyqtgraph',
        'numpy',
        'matplotlib',
        'PyOpenGL',
      ],
)

