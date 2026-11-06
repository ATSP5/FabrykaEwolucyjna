// Survivor step of the evolution. One thread = one cell: the child takes the cell only when it is
// no worse than the cell's individual, so the best schedule found is never lost (elitism in every
// cell) and an equal child lets the search drift across plateaus.
//
// params (int[13]): 0 individuals, 1 genes.
extern "C" __global__ void kernel(const int* population, const int* cost, const int* children, const int* children_cost, const int* params, int n, int* next_population, int* next_cost)
{
    int cell = threadIdx.x + blockIdx.x * blockDim.x;
    if (cell >= params[0])
    {
        return;
    }

    int genes = params[1];
    bool child_wins = children_cost[cell] <= cost[cell];
    const int* source = (child_wins ? children : population) + (size_t)cell * genes;
    int* target = next_population + (size_t)cell * genes;
    for (int gene = 0; gene < genes; ++gene)
    {
        target[gene] = source[gene];
    }
    next_cost[cell] = child_wins ? children_cost[cell] : cost[cell];
}
