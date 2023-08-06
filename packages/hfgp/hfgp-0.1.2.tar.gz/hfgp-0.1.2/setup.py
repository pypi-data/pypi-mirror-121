from distutils.core import setup
from setuptools import setup, find_packages

 
setup(name = "hfgp",
    version = "0.1.2",
    description = "Huggingface GP 接入模块",
    author = "stellahong",
    author_email = "stellahong@fuzhi.a",
    #Name the folder where your packages live:
    #(If you have other packages (dirs) or modules (py files) then
    #put them into the package directory - they will be found recursively.)
    packages = find_packages(),
    #exclude_package_data = {'docs':['1.txt']},  #排除文件
    install_requires = [
        'gin-config==0.3.0',
        #'sentence-transformers==0.4.1.2'
        'sentence-transformers==0.4.1.2',
	'transformers==4.9.1'
    ],
    long_description = """Really long text here."""   
)
