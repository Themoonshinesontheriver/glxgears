"""llvm

Tool-specific initialization for LLVM

"""

#
# Copyright (c) 2009 VMware, Inc.
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

import os
import os.path
import sys

import SCons.Errors
import SCons.Util


def generate(env):
    try:
        llvm_dir = os.environ['LLVM']
    except KeyError:
        # Do nothing -- use the system headers/libs
        llvm_dir = None
    else:
        if not os.path.isdir(llvm_dir):
            raise SCons.Errors.InternalError, "Specified LLVM directory not found"

        if env['debug']:
            llvm_subdir = 'Debug'
        else:
            llvm_subdir = 'Release'

        llvm_bin_dir = os.path.join(llvm_dir, llvm_subdir, 'bin')
        if not os.path.isdir(llvm_bin_dir):
            llvm_bin_dir = os.path.join(llvm_dir, 'bin')
            if not os.path.isdir(llvm_bin_dir):
                raise SCons.Errors.InternalError, "LLVM binary directory not found"

        env.PrependENVPath('PATH', llvm_bin_dir)

    if env['msvc']:
        # XXX: There is no llvm-config on Windows, so assume a standard layout
        if llvm_dir is not None:
            env.Prepend(CPPPATH = [os.path.join(llvm_dir, 'include')])
            env.Prepend(LIBPATH = [os.path.join(llvm_dir, 'lib')])
            env.Prepend(LIBS = [
                'LLVMBitWriter',
                'LLVMCore',
                'LLVMSupport',
                'LLVMSystem',
                'LLVMSupport',
                'LLVMSystem',
                'LLVMCore',
                'LLVMCodeGen',
                'LLVMSelectionDAG',
                'LLVMAsmPrinter',
                'LLVMBitReader',
                'LLVMBitWriter',
                'LLVMTransformUtils',
                'LLVMInstrumentation',
                'LLVMScalarOpts',
                'LLVMipo',
                'LLVMHello',
                'LLVMLinker',
                'LLVMAnalysis',
                'LLVMipa',
                'LLVMX86CodeGen',
                'LLVMX86AsmPrinter',
                'LLVMExecutionEngine',
                'LLVMInterpreter',
                'LLVMJIT',
                'LLVMTarget',
                'LLVMAsmParser',
                'LLVMDebugger',
                'LLVMArchive',
                'imagehlp',
                'psapi',
            ])
            env['LLVM_VERSION'] = '2.5'
        return
    elif env.Detect('llvm-config'):
        version = env.backtick('llvm-config --version').rstrip()

        try:
            env.ParseConfig('llvm-config --cppflags')
            env.ParseConfig('llvm-config --libs jit interpreter nativecodegen bitwriter')
            env.ParseConfig('llvm-config --ldflags')
        except OSError:
            print 'llvm-config version %s failed' % version
        else:
            if env['platform'] == 'windows':
                env.Append(LIBS = ['imagehlp', 'psapi'])
            env['LINK'] = env['CXX']
            env['LLVM_VERSION'] = version

def exists(env):
    return True

# vim:set ts=4 sw=4 et:
