#include <unordered_set>
#include <utility>
#include <vector>
#include <algorithm>
#include <stack>

using Grid = std::vector<std::vector<int>>;

namespace std {
	template<>
	struct hash<std::pair<int, int>> {
		size_t operator()(const std::pair<int, int>& k) const {
			std::hash<int> intHash;

			size_t hash = 17;
			hash = intHash(k.first) + 31 * hash;
			hash = intHash(k.second) + 31 * hash;

			return hash;
		}
	};
}

bool isInGrid(const Grid& grid, int i, int j) {
	const int rowCount = grid.size();
	const int colCount = grid[0].size();

	return i >= 0 && i < rowCount && j >= 0 && j < colCount;
}

void addToListIfInGrid(const Grid& grid, int i, int j, std::vector<std::pair<int, int>>& list) {
	if (isInGrid(grid, i, j)) {
		list.emplace_back(i, j);
	}
}

std::vector<std::pair<int, int>> neighboursOf(const Grid& grid, int i, int j) {
	std::vector<std::pair<int, int>> neighbours;

	addToListIfInGrid(grid, i + 1, j, neighbours);
	addToListIfInGrid(grid, i - 1, j, neighbours);
	addToListIfInGrid(grid, i, j + 1, neighbours);
	addToListIfInGrid(grid, i, j - 1, neighbours);

	return neighbours;
}

// Recursive variant
size_t countOfConnectedElementsFromRec(const Grid& grid, int i, int j, std::unordered_set<std::pair<int, int>>& visited) {
	size_t retValue = 1;
	int nodeValue = grid[i][j];
	std::vector<std::pair<int, int>> neighbours = neighboursOf(grid, i, j);

	visited.emplace(i, j);

	for (const std::pair<int, int>& elem : neighbours) {
		if (visited.find(elem) != visited.end()) continue;

		int neighbourValue = grid[elem.first][elem.second];
		if (neighbourValue == nodeValue) {
			retValue += countOfConnectedElementsFromRec(grid, elem.first, elem.second, visited);
		}
	}

	return retValue;
}

// Non-recursive variant
size_t countOfConnectedElementsFrom(const Grid& grid, int i, int j, std::unordered_set<std::pair<int, int>>& visited) {
	size_t retValue = 0;
	
	std::stack<std::pair<int, int>> unprocessedNodes;
	unprocessedNodes.emplace(i, j);
	
	std::pair<int, int> currentNode;
	std::vector<std::pair<int, int>> neighboursOfCurrent;
	while (!unprocessedNodes.empty()) {
		currentNode = unprocessedNodes.top();
		unprocessedNodes.pop();

		// Node processing
		retValue += 1;
		visited.emplace(currentNode.first, currentNode.second);

		neighboursOfCurrent = neighboursOf(grid, currentNode.first, currentNode.second);
		for (const std::pair<int, int>& elem : neighboursOfCurrent) {
			if (visited.find(elem) != visited.end()) continue;

			int neighbourValue = grid[elem.first][elem.second];
			int currentNodeValue = grid[currentNode.first][currentNode.second];

			if (neighbourValue == currentNodeValue) {
				unprocessedNodes.push(elem);
			}
		}
	}

	return retValue;
}

size_t maxCountOfConnectedElements(const Grid& grid) {
	size_t retValue = 0;

	if (grid.size() == 0) return retValue;
	if (grid[0].size() == 0) return retValue;

	std::unordered_set<std::pair<int, int>> visited;

	for (int i = 0; i < grid.size(); ++i) {
		for (int j = 0; j < grid[0].size(); ++j) {
			if (visited.find({ i, j }) != visited.end()) continue;
			retValue = std::max(countOfConnectedElementsFrom(grid, i, j, visited), retValue);
		}
	}

	return retValue;
}