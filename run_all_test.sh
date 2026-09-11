python tests/load.py tests/ISCAS85 --dump 
python tests/load.py tests/EPFL_parsed --dump
python tests/load.py tests/EPFL_large_parsed --dump
python tests/load.py tests/EPFL_mammoth_parsed --dump

python tests/benchmark.py tests/ISCAS85 --optimize --vector 50000 --warmup 10 --dump 
python tests/benchmark.py tests/EPFL_parsed --optimize --vector 50000 --warmup 10 --dump 
python tests/benchmark.py tests/EPFL_large_parsed --optimize --vector 500 --warmup 10 --no-engine --dump 
python tests/benchmark.py tests/EPFL_mammoth_parsed --optimize --vector 50 --warmup 10 --no-engine --dump 

python tests/benchmark_89.py tests/ISCAS89 --optimize --vector 50000 --warmup 10 --dump 

python tests/geometry.py tests/ISCAS85 --dump
python tests/geometry.py tests/ISCAS89 --dump
python tests/geometry.py tests/EPFL_parsed --dump
python tests/geometry.py tests/EPFL_large_parsed --dump
python tests/geometry.py tests/EPFL_mammoth_parsed --dump
