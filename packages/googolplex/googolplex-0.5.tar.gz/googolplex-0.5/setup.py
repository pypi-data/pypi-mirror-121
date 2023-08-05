import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'googolplex',         
  packages = ['googolplex'],   
  version = '0.5',     
  license='MIT',        
  description = 'Useful for Data Manipulation', 
  long_description=long_description,
  long_description_content_type='text/markdown'  ,
  author = 'SALMAN_FAROZ',                   
  author_email = 'farozsts@gmail.com',      
  url = 'https://github.com/stsfaroz/pictures',  
  keywords = ["googolplex"],   
  install_requires=["pillow","ipython"],
  classifiers=[
    'Development Status :: 4 - Beta',      
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3.7',
  ],
)
