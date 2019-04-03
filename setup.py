from setuptools import setup

setup(
    name='simple_NER',
    version='0.1.8',
    packages=['simple_NER', 'simple_NER.rules', 'simple_NER.annotators',
              'simple_NER.annotators.utils'],
    url='https://github.com/JarbasAl/simple_NER',
    license='MIT',
    author='jarbasAI',
    install_requires=["padaos", "fann2==1.0.7", "padatious", "nltk",
                      "requests"],
    author_email='jarbasai@mailfence.com',
    description='rule based NER'
)
