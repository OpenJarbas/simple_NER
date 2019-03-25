from setuptools import setup

setup(
    name='simple_NER',
    version='0.1.3',
    packages=['simple_NER', 'simple_NER.rules', 'simple_NER.annotators',
              'simple_NER.annotators.utils'],
    url='https://github.com/JarbasAl/simple_NER',
    license='MIT',
    author='jarbasAI',
    install_requires=["padaos"],
    author_email='jarbasai@mailfence.com',
    description='rule based NER'
)
