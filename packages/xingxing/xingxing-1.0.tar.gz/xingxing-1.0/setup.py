from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
extensions=[Extension('bCurveReconstruct',['bCurveReconstruct.py'])]
setup(name="xingxing",version='1.0',description="仅供测试参考",author="吴龙，邢温豪",ext_modules=cythonize(extensions))