#!/usr/bin/python

import os
import shutil
import subprocess
import argparse
from benchmarks import parsec_param
from benchmarks import splash_param

parser = argparse.ArgumentParser()
parser.add_argument('--outdir', dest = 'out_dir', required = True)
parser.add_argument('--jobs', dest = 'jobs', required = False, default = 1)
parser.add_argument('--depld', dest = 'depld', action = 'store_true',
                    help = 'add fence between dependent loads')
args = parser.parse_args()

# riscy dirs
build_linux_script = os.path.join(os.environ['RISCY_HOME'],
                                  'tools', 'build-linux.py')
bbl_path = os.path.join(os.environ['RISCY_TOOLS'], 'build-pk', 'bbl')

# dirs for benchmarks
root_dir = os.environ['xxPARSECDIRxx']

# dir to build linux
out_dir = os.path.abspath(args.out_dir)
test_dir = os.path.join(out_dir, 'test') # build initramfs for this benchmark

# bodytrack needs shared libs
#bodytrack_libs = ['ld-linux-riscv64-lp64d.so.1',
#                  'libstdc++.so.6',
#                  'libpthread.so.0',
#                  'libm.so.6',
#                  'libc.so.6',
#                  'libgcc_s.so.1']

# parsec
for bench, param in parsec_param.iteritems():
    for size in ['simsmall', 'simmedium', 'simlarge', 'native']:
        print ''
        print '========================================='
        print 'Generating parsec benchmark {} size {} ...'.format(bench, size)
        print '========================================='
        print ''

        # clean up test dir
        if os.path.isdir(test_dir):
            shutil.rmtree(test_dir)
        os.makedirs(test_dir)

        # copy binary
        binary = os.path.join(root_dir, param['dir'], bench,
                              'inst', 'amd64-linux.gcc', 'bin', bench)
        shutil.copy(binary, test_dir)

        # copy inputs
        input_tar = os.path.join(root_dir, param['dir'], bench,
                                 'inputs', 'input_' + size + '.tar')
        if os.path.isfile(input_tar):
            subprocess.check_call(['tar', '-xf', input_tar, '-C', test_dir])

        # write run.sh: $1 to run.sh is thread num
        run_sh = os.path.join(test_dir, 'run.sh')
        if os.path.isfile(run_sh):
            raise Exception('run.sh already exists!')
        with open(run_sh, 'w') as fp:
            fp.write('#!/bin/ash\n')
            fp.write('if [ $# -ne 1 ]; then\n')
            fp.write('  echo "Usage: ./run.sh THREAD_NUM"\n')
            fp.write('  exit\n')
            fp.write('fi\n')
            # for facesim, create output dir
            if bench == 'facesim':
                fp.write('mkdir -p Storytelling/output\n')
            # for freqmine thread num is in OMP_NUM_THREADS
            if bench == 'freqmine':
                fp.write('export OMP_NUM_THREADS=$1\n')
                run_args = param['run_args'][size]
            else:
                run_args = param['run_args'][size] % '$1'
            fp.write('time ./{} {}\n'.format(bench, run_args))
        os.chmod(run_sh, int('0777', 8))

        # write show.sh (show result)
        show_sh = os.path.join(test_dir, 'show.sh')
        if os.path.isfile(show_sh):
            raise Exception('show.sh already exists!')
        with open(show_sh, 'w') as fp:
            fp.write('#!/bin/ash\n')
            fp.write(param['show_res'][size] + '\n')
        os.chmod(show_sh, int('0777', 8))

        # compile and copy linux (bbl)
        cmd = [build_linux_script,
               '--jobs', str(args.jobs),
               '--testdir', test_dir]
        if args.depld:
            cmd.append('--depld')
        subprocess.check_call(cmd)
        shutil.copy(bbl_path,
                    os.path.join(out_dir,
                                 '_'.join(['bbl', 'parsec', bench, size])))

