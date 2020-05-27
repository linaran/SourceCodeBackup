#include "union-find.h"
#include <cstdio>

int main() 
{
	UnionFind unionFind(10);
	printf("Max in component having object 2: %d\n", unionFind.maxInComponentHavingObject(2));

	unionFind.connect(0, 1);
	printf("Max in component having object 1: %d\n", unionFind.maxInComponentHavingObject(1));
	unionFind.connect(5, 6);
	unionFind.connect(0, 5);
	unionFind.connect(2, 1);
	
	printf("Is 1 and 5 connected: %d\n", unionFind.areConnected(1, 5));
	printf("Max in component having object 2: %d\n", unionFind.maxInComponentHavingObject(2));
	return 0;
}