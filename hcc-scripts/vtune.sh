source /opt/intel/oneapi/vtune/latest/env/vars.sh

vtune -collect hotspots -knob sampling-mode=sw -knob enable-stack-collection=true -result-dir result2 ./2DConvolution.exe

# https://www.intel.com/content/www/us/en/docs/vtune-profiler/installation-guide/2025-0/package-managers.html
# https://www.intel.com/content/www/us/en/docs/vtune-profiler/cookbook/2025-0/top-down-microarchitecture-analysis-method.html