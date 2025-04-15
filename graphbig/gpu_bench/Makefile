SUBDIR = gpu_BetweennessCentr \
         gpu_BFS \
         gpu_ConnectedComp \
         gpu_DegreeCentr \
         gpu_GraphColoring \
         gpu_kCore \
         gpu_SSSP \
         gpu_TriangleCount

all:
	@for dir in $(SUBDIR); do \
	    echo "Entering $$dir"; \
	    $(MAKE) -C $$dir; \
	    echo "Leaving $$dir"; \
	done

clean:
	@for dir in $(SUBDIR); do \
	    echo "Entering $$dir"; \
	    $(MAKE) -C $$dir clean; \
	    echo "Leaving $$dir"; \
	done