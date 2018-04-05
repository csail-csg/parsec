#!/usr/bin/python
import argparse
import subprocess
import os
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('--ipfile', required=True,
                    metavar = 'IP_LIST_FILE', dest = 'ip_file')
parser.add_argument('--riscy', required = True,
                    metavar = 'RISCY_DIR', dest = 'riscy_dir')
parser.add_argument('--exe', required = True,
                    metavar = 'UBUNTU_EXE', dest = 'exe')
parser.add_argument('--outdir', required = True,
                    metavar = 'OUTPUT_DIR', dest = 'out_dir')
parser.add_argument('--bbldir', required = False,
                    metavar = 'BBL_DIR', dest = 'bbl_dir',
                    default = '/efs/szzhang/run/parsec_bbls')
parser.add_argument('--input', required = True,
                    metavar = 'INPUT_SIZE', dest = 'input_size',
                    choices = ['simsmall', 'simmedium', 'simlarge'])
parser.add_argument('--thread', required = True,
                    metavar = 'THREAD_NUM', dest = 'thread')
parser.add_argument('--mem', required = False,
                    metavar = 'MEM_SIZE_MB', dest = 'mem_size', default = 2048)
# AWS fpga image global id, e.g., --agfi agfi-XXX
parser.add_argument('--agfi', required = True,
                    metavar = 'agfi-XXX', dest = 'agfi')
# We send command to Linux after it boots, but we need to insert a delay here,
# because Linux will ask for stdin before it finishes booting. 60s works for
# me.
parser.add_argument('--delay', required = False,
                    metavar = 'DELAY_SEC', dest = 'delay', default = 60)
args = parser.parse_args()

benchmarks = [
    ['blackscholes'],
    ['facesim'],
    ['ferret'],
    ['fluidanimate'],
    ['swaptions'],
    ['freqmine'],
    ['streamcluster'],
]

ip_addrs = []
with open(args.ip_file, 'r') as fp:
    for line in fp:
        ip_addrs.append(line.rstrip('\n'))

if len(ip_addrs) < len(benchmarks):
    raise Exception('Not enough IPs')

# run the benchmarks
proc_shell_cmd = ("'cd test; ls; " +
                  'echo ===Start===; ' +
                  './run.sh ' + str(args.thread) + '; ' +
                  'echo ===End===; ' +
                  'ls; ./show.sh; ' +
                  "cd; ./terminate'")
for i, bench_list in enumerate(benchmarks):
    # get IP
    ip = ip_addrs[i]
    # get commands on F1
    aws_cmd = 'cd ' + args.riscy_dir + '; source setup.sh; '
    for bench in bench_list:
        bbl_path = os.path.join(args.bbl_dir,
                                'bbl_spec_{}_{}'.format(bench, args.input_size))
        aws_cmd += ('mkdir -p ' + os.path.join(args.out_dir, bench) + '; ' +
                    'cd ' + os.path.join(args.out_dir, bench) + '; ' +
                    'sudo fpga-load-local-image -S 0 -I ' + args.agfi + '; ' +
                    args.exe + ' --just-run' +
                    ' --core-num ' + str(args.thread) +
                    ' --mem-size ' + str(args.mem_size) +
                    ' --deadlock-check-after 10000000000' +
                    ' --shell-cmd ' + proc_shell_cmd + ' ' + str(args.delay) +
                    ' --perf-file ' + os.path.join(bench + '.perf') +
                    ' -- ' + bbl_path +
                    ' &> ' + os.path.join(bench + '.out') + '; sleep 20; ');
    aws_cmd += 'sudo shutdown -h now'
    # overall ssh cmd
    ssh_cmd = ('ssh -oStrictHostKeyChecking=no -i ~/aws-csail.pem ' +
               'ubuntu@{} '.format(ip_addrs[i]) +
               '"screen -dmS ' + '.'.join(bench_list) + ' bash -c \\"' + aws_cmd + '\\""')
    print ssh_cmd
    #subprocess.check_call(ssh_cmd, shell = True)
