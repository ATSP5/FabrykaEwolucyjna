// Variation step of the evolution. One thread = one cell of the toroidal grid: it picks a mate
// from the cell's neighbourhood (tournament of two), crosses the cell's chromosome with it (POX)
// and mutates the child (swaps of nearby genes).
//
// params (int[13]): 0 individuals, 1 genes, 4 grid side, 5 generation, 6 seed, 7 neighbourhood
// radius, 8 mutation chance per mille, 9 most swaps per child, 10 swap window, 12 crossover chance
// per mille.
static __device__ __forceinline__ unsigned int pcg_hash(unsigned int value)
{
    unsigned int state = value * 747796405u + 2891336453u;
    unsigned int word = ((state >> ((state >> 28u) + 4u)) ^ state) * 277803737u;
    return (word >> 22u) ^ word;
}

static __device__ __forceinline__ unsigned int next_random(unsigned int* state)
{
    *state = pcg_hash(*state);
    return *state;
}

static __device__ __forceinline__ int pick_neighbour(int x, int y, int side, int radius, unsigned int* rng)
{
    int span = 2 * radius + 1;
    int dx = (int)(next_random(rng) % (unsigned int)span) - radius;
    int dy = (int)(next_random(rng) % (unsigned int)span) - radius;
    if (dx == 0 && dy == 0)
    {
        dx = 1;
    }
    return ((y + dy + side) % side) * side + (x + dx + side) % side;
}

// Precedence-preserving crossover: genes of a random subset of jobs keep their places from the
// parent, the gaps take the remaining genes in the mate's order. The child is always a valid
// permutation with repetition, because both parents hold each job equally many times.
static __device__ __forceinline__ void cross_pox(const int* parent, const int* mate, int genes, unsigned int subset_seed, int* child)
{
    int mate_gene = 0;
    for (int gene = 0; gene < genes; ++gene)
    {
        int job = parent[gene];
        if (pcg_hash((unsigned int)job + subset_seed) & 1u)
        {
            child[gene] = job;
        }
        else
        {
            while (pcg_hash((unsigned int)mate[mate_gene] + subset_seed) & 1u)
            {
                ++mate_gene;
            }
            child[gene] = mate[mate_gene];
            ++mate_gene;
        }
    }
}

extern "C" __global__ void kernel(const int* population, const int* cost, const int* params, int n, int* children)
{
    int cell = threadIdx.x + blockIdx.x * blockDim.x;
    if (cell >= params[0])
    {
        return;
    }

    int genes = params[1];
    int side = params[4];
    int radius = params[7];
    int swap_window = params[10];
    unsigned int rng = pcg_hash((unsigned int)params[6] ^ pcg_hash((unsigned int)params[5] * 2654435761u + (unsigned int)cell));

    int x = cell % side;
    int y = cell / side;
    int first = pick_neighbour(x, y, side, radius, &rng);
    int second = pick_neighbour(x, y, side, radius, &rng);
    int mate_cell = cost[first] <= cost[second] ? first : second;

    const int* parent = population + (size_t)cell * genes;
    const int* mate = population + (size_t)mate_cell * genes;
    int* child = children + (size_t)cell * genes;
    if ((int)(next_random(&rng) % 1000u) < params[12])
    {
        cross_pox(parent, mate, genes, next_random(&rng), child);
    }
    else
    {
        for (int gene = 0; gene < genes; ++gene)
        {
            child[gene] = parent[gene];
        }
    }

    if ((int)(next_random(&rng) % 1000u) < params[8])
    {
        int swaps = 1 + (int)(next_random(&rng) % (unsigned int)params[9]);
        for (int swap = 0; swap < swaps; ++swap)
        {
            int left = (int)(next_random(&rng) % (unsigned int)genes);
            int right = left + 1 + (int)(next_random(&rng) % (unsigned int)swap_window);
            if (right >= genes)
            {
                right = genes - 1;
            }
            int kept = child[left];
            child[left] = child[right];
            child[right] = kept;
        }
    }
}
