import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='naver-dbcore',  
     version='0.0.3',
     packages=['naver_dbcore'] ,
     author="Jose Cuevas",
     author_email="jose.cuevas.cv@gmail.com",
     description="A DB Persistence Ancestor Library",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/jacr6/naver-dbcore", 
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )