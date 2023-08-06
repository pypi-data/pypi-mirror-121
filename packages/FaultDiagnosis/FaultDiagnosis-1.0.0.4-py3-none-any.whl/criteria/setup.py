from setuptools import setup, find_packages

setup(
name='FaultPredict', # 패키지 이름
version='1.0.0.1',
description='Sunghan Fault Disgnosis',
author='SungHan',
autoor_email='shbems777@gmail.com',
url='https://github.com/tathata21/moon',
license='SH', # 성한에서 정한 라이센스에 따른다.
py_modules=['noraml_model'], # 패키지에 포함되는 모듈
python_requires='>=3',
install_requires=['pymssql'], # 패키지 사용을 위해 필요한 추가 설치 패키지
packages=['criteria'] # 패키지가 들어있는 폴더들
)
