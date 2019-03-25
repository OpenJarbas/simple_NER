from setuptools import setup

setup(
    name='simple_NER',
    version='0.1.1',
    packages=['simple_NER', 'simple_NER.rules'],
    url='https://github.com/JarbasAl/simple_NER',
    license='MIT',
    author='jarbasAI',
    install_requires=["padaos"],
    author_email='jarbasai@mailfence.com',
    description='rule based NER'
)
