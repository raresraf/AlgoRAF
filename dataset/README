# HOW TO GENERATE THE DATASET

- [TheOutputsCodeforces](https://github.com/raresraf/TheOutputsCodeforces): Run raw process: 

`python3 process_raw.py atomic_perf/results_code perf`

- [TheOutputsCodeforces](https://github.com/raresraf/TheOutputsCodeforces): Run aggregations: 

`python3 run_aggregations.py processed/`

- [rafPipeline](https://github.com/raresraf/rafPipeline): generate the r-Complexity embeddings

`python3 rComplexity/tailor.py ../TheOutputsCodeforces/processed/`

# HOW TO EXTEND THE DATASET

- [TheInputsCodeforces](https://github.com/raresraf/TheInputsCodeforces): Write the generator in TheInputsCodeforces for the new problem.

- [TheInputsCodeforces](https://github.com/raresraf/TheInputsCodeforces): Generate syntetic inputs for the problem.

- [rafPipeline](https://github.com/raresraf/rafPipeline): Profile the code by dynamically running it against the syntetic inputs generated above.

`python3 run_on_demand <problemID> perf`

- Generate the dataset. (steps above)
