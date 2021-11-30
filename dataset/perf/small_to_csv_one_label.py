import json
import os
import sys
import csv


if len(sys.argv) <= 1:
    print("Usage: python3 to_csv_one_label.py <label_name>")
    print("sample usage: python3 to_csv_one_label.py math")
    sys.exit(-1)

label_name = sys.argv[1]

features = [
    "branch-misses_FEATURE_CONFIG",
    "branch-misses_FEATURE_TYPE",
    "branch-misses_INTERCEPT",
    "branch-misses_R-VAL",
    "branches_FEATURE_CONFIG",
    "branches_FEATURE_TYPE",
    "branches_INTERCEPT",
    "branches_R-VAL",
    "context-switches_FEATURE_CONFIG",
    "context-switches_FEATURE_TYPE",
    "context-switches_INTERCEPT",
    "context-switches_R-VAL",
    "cpu-migrations_FEATURE_CONFIG",
    "cpu-migrations_FEATURE_TYPE",
    "cpu-migrations_INTERCEPT",
    "cpu-migrations_R-VAL",
    "cycles_FEATURE_CONFIG",
    "cycles_FEATURE_TYPE",
    "cycles_INTERCEPT",
    "cycles_R-VAL",
    "instructions_FEATURE_CONFIG",
    "instructions_FEATURE_TYPE",
    "instructions_INTERCEPT",
    "instructions_R-VAL",
    "page-faults_FEATURE_CONFIG",
    "page-faults_FEATURE_TYPE",
    "page-faults_INTERCEPT",
    "page-faults_R-VAL",
    "stalled-cycles-frontend_FEATURE_CONFIG",
    "stalled-cycles-frontend_FEATURE_TYPE",
    "stalled-cycles-frontend_INTERCEPT",
    "stalled-cycles-frontend_R-VAL",
    "task-clock_FEATURE_CONFIG",
    "task-clock_FEATURE_TYPE",
    "task-clock_INTERCEPT",
    "task-clock_R-VAL",
    "label",
]

dataset = []

with open("../../../rafPipeline/dataset_metadata/labels/labels.json") as f:
    labels = json.load(f)

for root, dirs, files in os.walk("../../../TheOutputsCodeforces/processed/atomic_perf/results_code/"):
    for name in files:
        if name != "PROCESSED.RAF":
            continue
        problem = os.path.join(root, name).split("/")[-2]
        with open(os.path.join(root, name), 'r') as f:
            j = json.load(f)
            if not j.get("metrics", None):
                continue

        new_entry = []
        for feature in features:
            if feature == "label":
                l = labels[problem.split("_", 1)[0]]
                if label_name in l:
                    new_entry.append(1)
                else:
                    new_entry.append(0)
                print(problem, label_name in l)
            else:
                new_entry.append(j["metrics"][feature.split("_", 1)[0]][feature.split("_", 1)[1]])
        dataset.append(new_entry)

with open(f'small_{label_name}_dataset.csv', 'w') as f:
    write = csv.writer(f)

    write.writerow(features)
    counter = 200
    for data in dataset:
        if counter > 100 and data[-1] == 0:
            write.writerow(data)
            counter = counter - 1
        elif counter > 0 and counter <= 100 and data[-1] == 1:
            write.writerow(data)
            counter = counter - 1