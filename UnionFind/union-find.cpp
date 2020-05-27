#include "union-find.h"
#include <algorithm>

UnionFind::UnionFind(int n)
	: n(n)
	, parentOf(new int[n]) 
	, sz(new int[n]) 
	, maxForRoot(new int[n])
{
	for (int i = 0; i < n; ++i) 
	{
		parentOf[i] = i;
		maxForRoot[i] = i;
		sz[i] = 1;
	}
}

UnionFind::~UnionFind() 
{
	delete[] parentOf;
	delete[] sz;
	delete[] maxForRoot;
}

int UnionFind::root(int p)
{
	while (parentOf[p] != p) {
		parentOf[p] = parentOf[parentOf[p]]; // path compression
		p = parentOf[p];
	}

	return p;
}

void UnionFind::addRootToAnother(int p, int q)
{
	parentOf[p] = q;
	sz[q] += sz[p];
	maxForRoot[q] = std::max(maxForRoot[p], maxForRoot[q]);
}

void UnionFind::connect(int p, int q)
{
	const int rootP = root(p);
	const int rootQ = root(q);
	if (sz[rootP] <= sz[rootQ]) 
	{
		addRootToAnother(rootP, rootQ);
	}
	else
	{
		addRootToAnother(rootQ, rootP);
	}
}

bool UnionFind::areConnected(int p, int q)
{
	return root(p) == root(q);
}

int UnionFind::maxInComponentHavingObject(int p)
{
	return maxForRoot[root(p)];
}
