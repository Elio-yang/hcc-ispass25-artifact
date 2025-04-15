#!/bin/bash

PIN=/shared/pin/pin/pin
traceso=/shared/pin/pin/source/tools/SimpleExamples/obj-intel64/trace.so
$PIN -t $traceso -o trace.txt -- $1


# https://software.intel.com/sites/landingpage/pintool/docs/98869/Pin/doc/html/index.html#EXAMPLES
# https://www.intel.com/content/www/us/en/developer/articles/tool/pin-a-dynamic-binary-instrumentation-tool.html