// Fitness step of the evolution. One thread = one individual: it decodes the chromosome into a
// schedule and writes the cost of that schedule.
//
// Chromosome: permutation with repetition of job numbers. The k-th occurrence of a job is its
// k-th recipe step, so every permutation is a schedule that keeps the recipe order.
//
// params (int[13]): 0 individuals, 1 genes, 2 jobs, 3 machines, 11 tardiness scale.
// cost = tardiness scale * sum(weight * tardiness) + makespan.
#define MAX_JOBS 512
#define MAX_MACHINES 64

extern "C" __global__ void kernel(const int* population, const int* job_op_offset, const int* op_machine_type, const int* op_minutes, const int* job_arrival, const int* job_due, const int* job_weight, const int* type_machine_offset, const int* params, int n, int* cost)
{
    int idx = threadIdx.x + blockIdx.x * blockDim.x;
    if (idx >= params[0])
    {
        return;
    }

    int genes = params[1];
    int jobs = params[2];
    int machines = params[3];
    int job_next[MAX_JOBS];
    int job_ready[MAX_JOBS];
    int machine_free[MAX_MACHINES];
    for (int job = 0; job < jobs; ++job)
    {
        job_next[job] = job_op_offset[job];
        job_ready[job] = job_arrival[job];
    }
    for (int machine = 0; machine < machines; ++machine)
    {
        machine_free[machine] = 0;
    }

    const int* chromosome = population + (size_t)idx * genes;
    int weighted_tardiness = 0;
    int makespan = 0;
    for (int gene = 0; gene < genes; ++gene)
    {
        int job = chromosome[gene];
        int op = job_next[job]++;
        int type = op_machine_type[op];
        int ready = job_ready[job];

        // The machine that starts the step soonest; among equals the one idle for the shortest time.
        int best_machine = type_machine_offset[type];
        int best_start = 2147483647;
        int best_free = -1;
        for (int machine = type_machine_offset[type]; machine < type_machine_offset[type + 1]; ++machine)
        {
            int free_at = machine_free[machine];
            int start = free_at > ready ? free_at : ready;
            if (start < best_start || (start == best_start && free_at > best_free))
            {
                best_machine = machine;
                best_start = start;
                best_free = free_at;
            }
        }

        int end = best_start + op_minutes[op];
        machine_free[best_machine] = end;
        job_ready[job] = end;
        if (job_next[job] == job_op_offset[job + 1])
        {
            int tardiness = end - job_due[job];
            if (tardiness > 0)
            {
                weighted_tardiness += job_weight[job] * tardiness;
            }
            if (end > makespan)
            {
                makespan = end;
            }
        }
    }
    cost[idx] = params[11] * weighted_tardiness + makespan;
}
