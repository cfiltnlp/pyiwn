from setuptools import setup

setup(name='pyiwn',
      version='1.0',
      description='pyiwn -- A Python based API to access Indian language WordNets -- This API gives access to synsets, glosses, examples, lexico-semantic relations between synsets, ontology nodes for 18 Indian languages, viz., Assamese, Bangla, Bodo, Gujarati, Hindi, Kannada, Kashmiri, Konkani, Malayalam, Meitei (Manipuri), Marathi, Nepali, Odia, Punjabi, Sanskrit, Tamil, Telugu and Urdu. In future, it will also provide access to speech data for words, glosses examples in Hindi WordNet.',
      url='https://github.com/riteshpanjwani/pyiwn',
      author='Ritesh Panjwani',
      author_email='riteshpanjwani@gmail.com',
      license='MIT',
      packages=['pyiwn'],
      zip_safe=False,
      keywords = ['wordnet', 'IndoWordNet', 'nlp', 'python', 'API'],
      install_requires=[line.replace('\n', '') for line in open('requirements.txt').readlines()]
      )