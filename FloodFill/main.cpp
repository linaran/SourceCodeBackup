#include "FloodFill.h"
#include <cstdio>

int main() {
	Grid grid{
		{0, 0, 1, 2},
		{0, 1, 2, 1},
		{2, 1, 1, 1}
	};

	printf("Result %zu\n", maxCountOfConnectedElements(grid));

	return 0;
}