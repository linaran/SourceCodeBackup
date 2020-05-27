#pragma once

class UnionFind 
{
public:
	UnionFind(int n);

	~UnionFind();

	void connect(int p, int q);

	bool areConnected(int p, int q);

	int maxInComponentHavingObject(int p);

private:
	int n;
	int* parentOf;
	int* sz;
	int* maxForRoot;

	int root(int p);

	void addRootToAnother(int p, int q);

};