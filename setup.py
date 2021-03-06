#/* +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#   Copyright (c) 2011-2016 The plumed team
#   (see the PEOPLE file at the root of the distribution for a list of names)
#
#   See http://www.plumed.org for more information.
#
#   This file is part of plumed, version 2.
#
#   plumed is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   plumed is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with plumed.  If not, see <http://www.gnu.org/licenses/>.
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
#
# This python routine builds an interface between plumed and python using cython
#
from setuptools import setup
#from distutils.core import setup
from distutils.extension import Extension
import subprocess
import os
import sys

plumedname = os.getenv("plumed_program_name")
if plumedname is None:
    plumedname = "plumed"

plumedversion = os.getenv("plumed_version")
if plumedversion is None:
    plumedversion = subprocess.check_output(['grep','-v','#','./VERSION']).decode("utf-8")

print( "Module name " + plumedname )
print( "Version number " + plumedversion )

extra_compile_args=['-D__PLUMED_HAS_DLOPEN','-D__PLUMED_WRAPPER_LINK_RUNTIME=1','-D__PLUMED_WRAPPER_CXX=1','-D__PLUMED_WRAPPER_IMPLEMENTATION=1','-D__PLUMED_WRAPPER_EXTERN=0','-D__PLUMED_WRAPPER_CXX_DEFAULT_INVALID=1'] 

defaultkernel=os.getenv("plumed_default_kernel")
if defaultkernel is not None:
    extra_compile_args.append("-D__PLUMED_DEFAULT_KERNEL=" + os.path.abspath(defaultkernel))
    print( "Hardcoded PLUMED_KERNEL " + os.path.abspath(defaultkernel))

try:
    import numpy
except:
    print('Error: building ' + plumedname + ' requires numpy. Please install it first with pip install numpy')
    sys.exit(-1)

try:
    from Cython.Build import cythonize
except:
    print('Error: building ' + plumedname + ' requires cython. Please install it first with pip install cython')
    sys.exit(-1)

include_dirs=[numpy.get_include()]

try:
    include_dirs.append(os.environ["plumed_include_dir"])
except:
    include_dirs.append(".")

setup(
  name=plumedname,
  version=plumedversion,
  description='Python interface to PLUMED',
  author='Gareth A. Tribello',
  author_email='plumed-users@googlegroups.com',
  url='http://www.plumed.org',
  zip_safe= False,
  ext_modules = cythonize([
                  Extension( name=plumedname,
                             sources=["plumed.pyx"],
                             language="c++",
                             include_dirs=include_dirs,
                             extra_compile_args=extra_compile_args
                           )
                          ])
)
