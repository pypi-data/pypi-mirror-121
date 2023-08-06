from setuptools import setup, find_packages

with open('README.md','r') as f:
	long_description = f.read()

setup(name='SimpleMaze_JJAP', # 패키지 명

version='1.0.0.5',

description='Simple Maze Module, made by JJAPDABOTTEAM',

author='Seol7523',

author_email='seolchaehwan@naver.com',

url='https://github.com/Seol7523/SimpleMaze',

license='MIT', # MIT에서 정한 표준 라이센스 따른다

py_modules=['maze'], # 패키지에 포함되는 모듈

packages=['SimpleMaze_JJAP'],

python_requires='>=3',

install_requires=[], # 패키지 사용을 위해 필요한 추가 설치 패키지

long_description=long_description,

long_description_content_type='text/markdown'
)