
parsec_param = {}
# each parsecm benchmark parameter has the following fields
# dir: directory where the benchmark source resides
# run_args: arguments to run (for different input size); %s should be replaced
# by thread num
# show_res: command to show the results (for different input size)

parsec_param['blackscholes'] = {
    'dir': 'pkgs/apps',
    'run_args': {
        'simdev'   : '%s in_16.txt  out.txt',
        'simsmall' : '%s in_4K.txt  out.txt',
        'simmedium': '%s in_16K.txt out.txt',
        'simlarge' : '%s in_64K.txt out.txt',
    },
    'show_res': {
        'simdev'   : 'wc -l out.txt; head out.txt; tail out.txt',
        'simsmall' : 'wc -l out.txt; head out.txt; tail out.txt',
        'simmedium': 'wc -l out.txt; head out.txt; tail out.txt',
        'simlarge' : 'wc -l out.txt; head out.txt; tail out.txt',
    },
}

parsec_param['streamcluster'] = {
    'dir': 'pkgs/kernels',
    'run_args': {
        'simdev'   : '3  10 3   16    16    10   none out.txt %s',
        'simsmall' : '10 20 32  4096  4096  1000 none out.txt %s',
        'simmedium': '10 20 64  8192  8192  1000 none out.txt %s',
        'simlarge' : '10 20 128 16384 16384 1000 none out.txt %s',
    },
    'show_res': {
        'simdev'   : 'wc -l out.txt; cat out.txt',
        'simsmall' : 'wc -l out.txt; cat out.txt',
        'simmedium': 'wc -l out.txt; cat out.txt',
        'simlarge' : 'wc -l out.txt; cat out.txt',
    },
}

parsec_param['fluidanimate'] = {
    'dir': 'pkgs/apps',
    'run_args': {
        'simdev'   : '%s 3 in_15K.fluid  out.fluid',
        'simsmall' : '%s 5 in_35K.fluid  out.fluid',
        'simmedium': '%s 5 in_100K.fluid out.fluid',
        'simlarge' : '%s 5 in_300K.fluid out.fluid',
    },
    'show_res': {
        'simdev'   : 'du -sh out.fluid',
        'simsmall' : 'du -sh out.fluid',
        'simmedium': 'du -sh out.fluid',
        'simlarge' : 'du -sh out.fluid',
    },
}

parsec_param['swaptions'] = {
    'dir': 'pkgs/apps',
    'run_args': {
        'simdev'   : '-ns 16 -sm 50    -nt %s', # change 3 to 16, enable 8 threads
        'simsmall' : '-ns 16 -sm 10000 -nt %s',
        'simmedium': '-ns 32 -sm 20000 -nt %s',
        'simlarge' : '-ns 64 -sm 40000 -nt %s',
    },
    'show_res': {
        'simdev'   : '',
        'simsmall' : '',
        'simmedium': '',
        'simlarge' : '',
    },
}

parsec_param['bodytrack'] = {
    'dir': 'pkgs/apps',
    'run_args': {
        # we use posix thread model (input arg = 2)
        'simdev'    : 'sequenceB_1 4 1 100  3 2 %s',
        'simsmall'  : 'sequenceB_1 4 1 1000 5 2 %s',
        'simmedium' : 'sequenceB_2 4 2 2000 5 2 %s',
        'simlarge'  : 'sequenceB_4 4 4 4000 5 2 %s',
    },
    'show_res': {
        'simdev'   : '',
        'simsmall' : '',
        'simmedium': '',
        'simlarge' : '',
    },
}

parsec_param['facesim'] = {
    'dir': 'pkgs/apps',
    'run_args': {
        # all input sizes are the same
        'simdev'    : '-timing -threads %s',
        'simsmall'  : '-timing -threads %s',
        'simmedium' : '-timing -threads %s',
        'simlarge'  : '-timing -threads %s',
    },
    'show_res': {
        'simdev'   : 'ls run/Storytelling/output',
        'simsmall' : 'ls run/Storytelling/output',
        'simmedium': 'ls run/Storytelling/output',
        'simlarge' : 'ls run/Storytelling/output',
    },
}

parsec_param['ferret'] = {
    'dir': 'pkgs/apps',
    'run_args': {
        'simdev'    : 'corel lsh queries 5   5 %s out.txt',
        'simsmall'  : 'corel lsh queries 10 20 %s out.txt',
        'simmedium' : 'corel lsh queries 10 20 %s out.txt',
        'simlarge'  : 'corel lsh queries 10 20 %s out.txt',
    },
    'show_res': {
        'simdev'   : 'cat out.txt',
        'simsmall' : 'cat out.txt',
        'simmedium': 'cat out.txt',
        'simlarge' : 'cat out.txt',
    },
}

parsec_param['x264'] = {
    'dir': 'pkgs/apps',
    'run_args': {
        'simdev'    : ('--quiet --qp 20 --partitions b8x8,i4x4 --ref 5 --direct auto --b-pyramid ' +
                       '--weightb --mixed-refs --no-fast-pskip --me umh --subme 7 --analyse b8x8,i4x4 ' +
                       '--threads %s -o x264_dev4.264 eledream_64x36_3.y4m')      ,
        'simsmall'  : ('--quiet --qp 20 --partitions b8x8,i4x4 --ref 5 --direct auto --b-pyramid ' +
                       '--weightb --mixed-refs --no-fast-pskip --me umh --subme 7 --analyse b8x8,i4x4 ' +
                       '--threads %s -o x264_small.264 eledream_640x360_8.y4m')   ,
        'simmedium' : ('--quiet --qp 20 --partitions b8x8,i4x4 --ref 5 --direct auto --b-pyramid ' +
                       '--weightb --mixed-refs --no-fast-pskip --me umh --subme 7 --analyse b8x8,i4x4 ' +
                       '--threads %s -o x264_medium.264 eledream_640x360_32.y4m') ,
        'simlarge'  : ('--quiet --qp 20 --partitions b8x8,i4x4 --ref 5 --direct auto --b-pyramid ' +
                       '--weightb --mixed-refs --no-fast-pskip --me umh --subme 7 --analyse b8x8,i4x4 ' +
                       '--threads %s -o x264_large.264 eledream_640x360_128.y4m') ,
    },
    'show_res': {
        'simdev'   : '',
        'simsmall' : '',
        'simmedium': '',
        'simlarge' : '',
    },
}

parsec_param['canneal'] = {
    'dir': 'pkgs/kernels',
    'run_args': {
        'simdev'   : '%s 100   300  100.nets    2',
        'simsmall' : '%s 10000 2000 100000.nets 32',
        'simmedium': '%s 15000 2000 200000.nets 64',
        'simlarge' : '%s 15000 2000 400000.nets 128',
    },
    'show_res': {
        'simdev'   : '',
        'simsmall' : '',
        'simmedium': '',
        'simlarge' : '',
    },
}

'''
parsec3_param['freqmine'] = {
        'dir'    : 'pkgs/apps',
        # freqmine.out will be removed in program
        'dev'    : 'T10I4D100K_1k.dat 3 freqmine.out %s'  ,
        'small'  : 'kosarak_250k.dat 220 freqmine.out %s' ,
        'medium' : 'kosarak_500k.dat 410 freqmine.out %s' ,
        'large'  : 'kosarak_990k.dat 790 freqmine.out %s' ,
        }

parsec3_param['vips'] = {
        'dir'    : 'pkgs/apps',
        # additional arg for thread num
        'dev'    : 'im_benchmark barbados_256x288.v vips_dev.v %s'        ,
        'small'  : 'im_benchmark pomegranate_1600x1200.v vips_small.v %s' ,
        'medium' : 'im_benchmark vulture_2336x2336.v vips_medium.v %s'    ,
        'large'  : 'im_benchmark bigben_2662x5500.v vips_large.v %s'      ,
        }

        '''

# parameter to run SPLASH2x
splash_param = {}

'''
splash_param['barnes'] = {
        'dev'      : '-f input.template' ,
        'small'    : '-f input.template' ,
        'medium'   : '-f input.template' ,
        'large'    : '-f input.template' ,
        'template' : True
        }

splash_param['fmm'] = {
        'dev'      : '-f input.template' ,
        'small'    : '-f input.template' ,
        'medium'   : '-f input.template' ,
        'large'    : '-f input.template' ,
        'template' : True
        }

splash_param['ocean_cp'] = {
        'dev'      : '-n258 -p%s -e1e-07 -r20000 -t28800'  ,
        'small'    : '-n514 -p%s -e1e-07 -r20000 -t28800'  ,
        'medium'   : '-n1026 -p%s -e1e-07 -r20000 -t28800' ,
        'large'    : '-n2050 -p%s -e1e-07 -r20000 -t28800' ,
        'template' : False
        }

splash_param['ocean_ncp'] = {
        'dev'      : '-n258 -p%s -e1e-07 -r20000 -t28800'  ,
        'small'    : '-n514 -p%s -e1e-07 -r20000 -t28800'  ,
        'medium'   : '-n1026 -p%s -e1e-07 -r20000 -t28800' ,
        'large'    : '-n2050 -p%s -e1e-07 -r20000 -t28800' ,
        'template' : False
        }

splash_param['radiosity'] = {
        'dev'      : '-bf 1.5e-1 -batch -room -p %s' ,
        'small'    : '-bf 1.5e-1 -batch -room -p %s' ,
        'medium'   : '-bf 1.5e-2 -batch -room -p %s' ,
        'large'    : '-bf 1.5e-3 -batch -room -p %s' ,
        'template' : False
        }

splash_param['raytrace'] = {
        'dev'      : '-s -p%s -a4 teapot.env' ,
        'small'    : '-s -p%s -a8 teapot.env' ,
        'medium'   : '-s -p%s -a2 balls4.env' ,
        'large'    : '-s -p%s -a8 balls4.env' ,
        'template' : False
        }

splash_param['volrend'] = {
        'dev'      : '%s head-scaleddown4 4'   ,
        'small'    : '%s head-scaleddown4 20'  ,
        'medium'   : '%s head-scaleddown2 50'  ,
        'large'    : '%s head-scaleddown2 100' ,
        'template' : False
        }

splash_param['water_nsquared'] = {
        'dev'      : 'input.template' ,
        'small'    : 'input.template' ,
        'medium'   : 'input.template' ,
        'large'    : 'input.template' ,
        'template' : True
        }

splash_param['water_spatial'] = {
        'dev'      : 'input.template' ,
        'small'    : 'input.template' ,
        'medium'   : 'input.template' ,
        'large'    : 'input.template' ,
        'template' : True
        }

splash_param['cholesky'] = {
        'dev'      : '-p%s tk14.O' ,
        'small'    : '-p%s tk29.O' ,
        'medium'   : '-p%s tk29.O' ,
        'large'    : '-p%s tk29.O' ,
        'template' : False
        }

splash_param['fft'] = {
        'dev'      : '-m18 -p%s' ,
        'small'    : '-m20 -p%s' ,
        'medium'   : '-m22 -p%s' ,
        'large'    : '-m24 -p%s' ,
        'template' : False
        }

splash_param['lu_cb'] = {
        'dev'      : '-p%s -n512 -b16'  ,
        'small'    : '-p%s -n512 -b16'  ,
        'medium'   : '-p%s -n1024 -b16' ,
        'large'    : '-p%s -n2048 -b16' ,
        'template' : False
        }

splash_param['lu_ncb'] = {
        'dev'      : '-p%s -n512 -b16'  ,
        'small'    : '-p%s -n512 -b16'  ,
        'medium'   : '-p%s -n1024 -b16' ,
        'large'    : '-p%s -n2048 -b16' ,
        'template' : False
        }

splash_param['radix'] = {
        'dev'      : '-p%s -r4096 -n262144 -m524288'       ,
        'small'    : '-p%s -r4096 -n4194304 -m2147483647'  ,
        'medium'   : '-p%s -r4096 -n16777216 -m2147483647' ,
        'large'    : '-p%s -r4096 -n67108864 -m2147483647' ,
        'template' : False
        }
        '''
