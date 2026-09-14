cd tests/

# 1. RAM Footprint Benchmarks
python src/load.py ISCAS85 --dump 
python src/load.py ISCAS89 --dump 
python src/load.py EPFL_parsed --dump
python src/load.py EPFL_large_parsed --dump
python src/load.py EPFL_mammoth_parsed --dump
python src/load.py IWLS2005/itc99 --dump 
python src/load.py IWLS2005/opencores --dump 
python src/load.py IWLS2005/faraday --dump

python src/benchmark.py ISCAS85 --optimize --vector 10000 --warmup 10 --dump 
python src/benchmark.py EPFL_parsed --optimize --vector 10000 --warmup 10 --dump 
# 3. Sequential Simulation Benchmarks
python src/benchmark_89.py ISCAS89 --optimize --no-engine --vector 10000 --warmup 10 --dump 
python src/benchmark_iwls.py IWLS2005/itc99 --optimize --no-engine --no-rx-oop --no-rx-sweep --vector 10000 --warmup 10 --dump 
python src/benchmark_iwls.py IWLS2005/opencores --optimize --no-engine --no-rx-oop --no-rx-sweep --vector 10000 --warmup 10 --dump 
python src/benchmark_iwls.py IWLS2005/faraday --optimize --no-engine --no-rx-oop --no-rx-sweep --vector 10000 --warmup 10 --dump 
# 2. Combinational Simulation Benchmarks

python src/benchmark.py EPFL_large_parsed --optimize --vector 500 --warmup 10 --no-engine --dump 
python src/benchmark.py EPFL_mammoth_parsed --optimize --vector 50 --warmup 10 --no-engine --dump 


# 4. Topological Geometry Analysis
python geometry.py ISCAS85 --dump
python geometry.py ISCAS89 --dump
python geometry.py EPFL_parsed --dump
# python geometry.py EPFL_large_parsed --dump
# python geometry.py EPFL_mammoth_parsed --dump
# python geometry.py IWLS2005/itc99/ --dump
# python geometry.py IWLS2005/opencores/ --dump
# python geometry.py IWLS2005/faraday/ --dump

# 5. Multi-Engine Hardware Profiling (Linux perf)
# python src/perf.py iscas85 --vectors 5000
# python src/perf.py iwls --vectors 10000 --limit 15

# 6. Master Unified 3-in-1 Benchmarks (Load, Verification & Hardware Profiling)
# python master_test.py iwls --vectors 10000 --limit 5
# python master_test.py iscas85 --vectors 10000
# python master_test.py iscas89 --vectors 10000 --limit 5


python tests/master_test.py tests/ISCAS85 --skip-verify
python tests/master_test.py tests/EPFL_parsed --skip-verify
python tests/master_test.py tests/EPFL_large_parsed --vectors 500 --no-engine --skip-verify

python tests/master_test.py tests/ISCAS89 --skip-verify
python tests/master_test.py tests/IWLS2005/itc99 --no-engine --skip-verify
python tests/master_test.py tests/IWLS2005/opencores --no-engine --skip-verify
python tests/master_test.py tests/IWLS2005/faraday --no-engine --skip-verify