
#include <assert.h>
#include <locale.h>
#include <stdio.h>
#include <stdlib.h>


#include <chrono>
#include <string>

#include "llvm/ADT/DenseMap.h"
#include <llvm/ADT/SmallSet.h>

using StepResTy = std::pair<int64_t,uint64_t>;
using StepMapTy = llvm::DenseMap<uint64_t,StepResTy>;

#define HEADER "index, steps, peak\n"

static StepResTy three_x_plus_one(uint64_t x,
                                  const StepMapTy& step_map,
                                  uint64_t lower_bound)
{
  unsigned steps = 0;
  llvm::SmallSet<uint64_t,32> visited;
  uint64_t maxval = x;

  while (true)
  {
    if (visited.count(x)) {
      return std::make_pair(-1,maxval);
    }
    visited.insert(x);

    unsigned zeros = __builtin_ctz(x);
    steps += zeros;
    x = x >> zeros;

    if (x == 1) {
      return std::make_pair(steps, maxval);
    }

    if (x < lower_bound) {
      auto prev = step_map.lookup(x);
      return std::make_pair(steps + prev.first, std::max(maxval, prev.second));
    }

    steps++;
    x = 3*x+1;
    maxval = std::max(maxval, x);
  }

  llvm_unreachable("Broke out of loop without returning?");
}

int main(int argc, char** argv)
{
  assert(argc == 5 && "Usage: tk-3x+1 <start> <stop> <map-in> <map-out>");

  // Parse args
  uint64_t start = atoll(argv[1]);
  uint64_t stop  = atoll(argv[2]);

  std::string MapInFileName  = argv[3];
  std::string MapOutFileName = argv[4];

  // Initialize step map
  printf("Initializing...\n");
  StepMapTy StepMap{};
  StepMap.reserve(stop);

  // Load input step map
  FILE* MapInFile = fopen(MapInFileName.c_str(), "r");
  uint64_t idx, steps, peak;
  auto ret = fscanf(MapInFile, HEADER);
  assert(ret == 0 && "Failed to read header");
  while (fscanf(MapInFile,"%llu, %llu, %llu", &idx, &steps, &peak) != EOF) {
    StepMap[idx] = std::make_pair(steps,peak);
  }
  fclose(MapInFile);

  // Run
  printf("Running...\n");
  auto tstart = std::chrono::high_resolution_clock::now();

  for (uint64_t i=start; i < stop; i += 2)
  {
    auto res = three_x_plus_one(i, StepMap, i);
    if (res.first < 0) {
      fprintf(stderr, "COUNTER FOUND: %llu", i);
      exit(-1);
    }
    StepMap[i] = res;
  }

  auto tend = std::chrono::high_resolution_clock::now();

  // Write output step map
  printf("Saving results...\n");
  FILE* MapOutFile = fopen(MapOutFileName.c_str(), "w");
  fprintf(MapOutFile, "%s", HEADER);
  for (uint64_t i=1; i < stop; i += 2) {
    fprintf(MapOutFile,"%llu, %lld, %llu\n",i,StepMap[i].first,StepMap[i].second);
  }
  fclose(MapOutFile);

  // Calculate & print metrics
  auto N = stop - start;
  std::chrono::duration<double, std::nano> TotalTime = tend - tstart;
  auto cps = N / TotalTime.count() * 1E9;

  setlocale(LC_NUMERIC, "");
  printf("\n");
  printf("Verification Time: %fs\n", TotalTime.count()/1E9);
  printf("Checks Per Second: %'.0f\n",cps);
  return 0;
}
