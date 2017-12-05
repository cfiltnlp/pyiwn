from setuptools import setup

setup(name='pyiwn',
      version='0.3',
      description='IndoWordNet Library (IWNL) is an API for accessing linked lexical knowledge base of wordnets of 18 scheduled languages of India, viz., Assamese, Bangla, Bodo, Gujarati, Hindi, Kannada, Kashmiri, Konkani, Malayalam, Meitei (Manipuri), Marathi, Nepali, Odia, Punjabi, Sanskrit, Tamil, Telugu and Urdu. It also provides functionality beyond data access, such as relationship discovery, word similarity and relatednes measures and morphological processing.',
      url='https://github.com/riteshpanjwani/pyiwn',
      author='Ritesh Panjwani',
      author_email='riteshpanjwani@gmail.com',
      download_url = 'https://github.com/riteshpanjwani/pyiwn/archive/0.1.tar.gz',
      license='MIT',
      packages=['pyiwn'],
      zip_safe=False,
      keywords = ['wordnet', 'IndoWordNet', 'nlp', 'python', 'API']
      )