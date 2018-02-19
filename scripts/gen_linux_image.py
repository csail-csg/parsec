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
args = parser.parse_args()

# riscy dirs
build_linux_script = os.path.join(os.environ['RISCY_HOME'],
                                  'tools', 'build-linux.py')
bbl_path = os.path.join(os.environ['RISCY_TOOLS'], 'build-pk', 'bbl')

# dirs for benchmarks
root_dir = os.environ['xxPARSECDIRxx']
out_dir = os.path.abspath(args.out_dir)
test_dir = os.path.join(out_dir, 'test')

# parsec
for bench, param in parsec_param.iteritems():
    print ''
    print '========================================='
    print 'Generating parsec benchmark {} ...'.format(bench)
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

    for size in ['simsmall', 'simmedium', 'simlarge']:
        # sub dir for this input size
        test_size_dir = os.path.join(test_dir, size)
        os.makedirs(test_size_dir)

        # copy inputs
        input_tar = os.path.join(root_dir, param['dir'], bench,
                                 'inputs', 'input_' + size + '.tar')
        if os.path.isfile(input_tar):
            subprocess.check_call(['tar', '-xf', input_tar,
                                   '-C', test_size_dir])

        # write run_SIZE.sh: $1 to run_SIZE.sh is thread num
        # run_SIZE.sh is outside test_size_dir
        run_sh = os.path.join(test_dir, 'run_{}.sh'.format(size))
        if os.path.isfile(run_sh):
            raise Exception('run.sh already exists!')
        with open(run_sh, 'w') as fp:
            fp.write('#!/bin/ash\n')
            fp.write('if [ $# -ne 1 ]; then\n')
            fp.write('  echo "Usage: ./run.sh THREAD_NUM"\n')
            fp.write('  exit\n')
            fp.write('fi\n')
            fp.write('cd {}\n'.format(size))
            run_args = param['run_args'][size] % '$1'
            fp.write('../{} {}\n'.format(bench, run_args))
        os.chmod(run_sh, int('0777', 8))

        # write show_SIZE.sh (show result)
        # show_SIZE.sh is outside test_size_dir
        show_sh = os.path.join(test_dir, 'show_{}.sh'.format(size))
        if os.path.isfile(show_sh):
            raise Exception('show.sh already exists!')
        with open(show_sh, 'w') as fp:
            fp.write('#!/bin/ash\n')
            fp.write('cd {}\n'.format(size))
            fp.write(param['show_res'][size] + '\n')
        os.chmod(show_sh, int('0777', 8))

    # compile and copy linux (bbl)
    subprocess.check_call([build_linux_script,
                           '--jobs', str(args.jobs),
                           '--testdir', test_dir])
    shutil.copy(bbl_path,
                os.path.join(out_dir,
                             '_'.join(['bbl', 'parsec', bench])))

