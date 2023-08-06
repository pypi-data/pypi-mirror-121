import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='usefulmath',  
     version='1.0',
     scripts=['usefulmath'] ,
     author="DynPyDev",
     author_email="dynpydev@gmail.com",
     description="A repository which excecutes long/complex calculations",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/DynPyDev/usefulmath",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )