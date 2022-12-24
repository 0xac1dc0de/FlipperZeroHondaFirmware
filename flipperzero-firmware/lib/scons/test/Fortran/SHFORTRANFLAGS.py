#!/usr/bin/env python
#
# __COPYRIGHT__
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

import TestSCons

_python_ = TestSCons._python_
_obj   = TestSCons._shobj
obj_   = TestSCons.shobj_

test = TestSCons.TestSCons()
test.file_fixture(['fixture', 'myfortran_flags.py'])

test.write('SConstruct', """
env = Environment(SHFORTRAN = r'%(_python_)s myfortran_flags.py fortran')
env.Append(SHFORTRANFLAGS = '-x')
env.SharedObject(target = 'test01', source = 'test01.f')
env.SharedObject(target = 'test02', source = 'test02.F')
env.SharedObject(target = 'test03', source = 'test03.for')
env.SharedObject(target = 'test04', source = 'test04.FOR')
env.SharedObject(target = 'test05', source = 'test05.ftn')
env.SharedObject(target = 'test06', source = 'test06.FTN')
env.SharedObject(target = 'test07', source = 'test07.fpp')
env.SharedObject(target = 'test08', source = 'test08.FPP')
""" % locals())

test.write('test01.f',   "This is a .f file.\n#fortran\n")
test.write('test02.F',   "This is a .F file.\n#fortran\n")
test.write('test03.for', "This is a .for file.\n#fortran\n")
test.write('test04.FOR', "This is a .FOR file.\n#fortran\n")
test.write('test05.ftn', "This is a .ftn file.\n#fortran\n")
test.write('test06.FTN', "This is a .FTN file.\n#fortran\n")
test.write('test07.fpp', "This is a .fpp file.\n#fortran\n")
test.write('test08.FPP', "This is a .FPP file.\n#fortran\n")

test.run(arguments = '.', stderr = None)

test.must_match(obj_ + 'test01' + _obj, " -c -x\nThis is a .f file.\n")
test.must_match(obj_ + 'test02' + _obj, " -c -x\nThis is a .F file.\n")
test.must_match(obj_ + 'test03' + _obj, " -c -x\nThis is a .for file.\n")
test.must_match(obj_ + 'test04' + _obj, " -c -x\nThis is a .FOR file.\n")
test.must_match(obj_ + 'test05' + _obj, " -c -x\nThis is a .ftn file.\n")
test.must_match(obj_ + 'test06' + _obj, " -c -x\nThis is a .FTN file.\n")
test.must_match(obj_ + 'test07' + _obj, " -c -x\nThis is a .fpp file.\n")
test.must_match(obj_ + 'test08' + _obj, " -c -x\nThis is a .FPP file.\n")

fc = 'f77'
fortran = test.detect_tool(fc)

if fortran:

    directory = 'x'
    test.subdir(directory)

    test.file_fixture('wrapper.py')

    test.write('SConstruct', """
foo = Environment(SHFORTRAN = '%(fc)s')
shfortran = foo.Dictionary('SHFORTRAN')
bar = foo.Clone(SHFORTRAN = r'%(_python_)s wrapper.py ' + shfortran)
bar.Append(SHFORTRANFLAGS = '-I%(directory)s')
foo.SharedLibrary(target = 'foo/foo', source = 'foo.f')
bar.SharedLibrary(target = 'bar/bar', source = 'bar.f')
""" % locals())

    test.write('foo.f', r"""
      PROGRAM FOO
      PRINT *,'foo.f'
      STOP
      END
""")

    test.write('bar.f', r"""
      PROGRAM BAR
      PRINT *,'bar.f'
      STOP
      END
""")


    test.run(arguments = 'foo', stderr = None)

    test.must_not_exist('wrapper.out')

    import sys
    if sys.platform[:5] == 'sunos':
        test.run(arguments = 'bar', stderr = None)
    else:
        test.run(arguments = 'bar')

    test.must_match('wrapper.out', "wrapper.py\n")

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4: