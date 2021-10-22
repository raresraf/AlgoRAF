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
    "Average resident set size_FEATURE_CONFIG",
    "Average resident set size_FEATURE_TYPE",
    "Average resident set size_INTERCEPT",
    "Average resident set size_R-VAL",

    "Average shared text size_FEATURE_CONFIG",
    "Average shared text size_FEATURE_TYPE",
    "Average shared text size_INTERCEPT",
    "Average shared text size_R-VAL",

    "Average stack size_FEATURE_CONFIG",
    "Average stack size_FEATURE_TYPE",
    "Average stack size_INTERCEPT",
    "Average stack size_R-VAL",

    "Average total size_FEATURE_CONFIG",
    "Average total size_FEATURE_TYPE",
    "Average total size_INTERCEPT",
    "Average total size_R-VAL",

    "File system inputs_FEATURE_CONFIG",
    "File system inputs_FEATURE_TYPE",
    "File system inputs_INTERCEPT",
    "File system inputs_R-VAL",

    "File system outputs_FEATURE_CONFIG",
    "File system outputs_FEATURE_TYPE",
    "File system outputs_INTERCEPT",
    "File system outputs_R-VAL",

    "Involuntary context switches_FEATURE_CONFIG",
    "Involuntary context switches_FEATURE_TYPE",
    "Involuntary context switches_INTERCEPT",
    "Involuntary context switches_R-VAL",

    "Major (requiring I/O) page faults_FEATURE_CONFIG",
    "Major (requiring I/O) page faults_FEATURE_TYPE",
    "Major (requiring I/O) page faults_INTERCEPT",
    "Major (requiring I/O) page faults_R-VAL",

    "Maximum resident set size_FEATURE_CONFIG",
    "Maximum resident set size_FEATURE_TYPE",
    "Maximum resident set size_INTERCEPT",
    "Maximum resident set size_R-VAL",

    "Minor (reclaiming a frame) page faults_FEATURE_CONFIG",
    "Minor (reclaiming a frame) page faults_FEATURE_TYPE",
    "Minor (reclaiming a frame) page faults_INTERCEPT",
    "Minor (reclaiming a frame) page faults_R-VAL",

    "Signals delivered_FEATURE_CONFIG",
    "Signals delivered_FEATURE_TYPE",
    "Signals delivered_INTERCEPT",
    "Signals delivered_R-VAL",

    "Socket messages received_FEATURE_CONFIG",
    "Socket messages received_FEATURE_TYPE",
    "Socket messages received_INTERCEPT",
    "Socket messages received_R-VAL",

    "Socket messages sent_FEATURE_CONFIG",
    "Socket messages sent_FEATURE_TYPE",
    "Socket messages sent_INTERCEPT",
    "Socket messages sent_R-VAL",

    "Swaps_FEATURE_CONFIG",
    "Swaps_FEATURE_TYPE",
    "Swaps_INTERCEPT",
    "Swaps_R-VAL",

    "System time_FEATURE_CONFIG",
    "System time_FEATURE_TYPE",
    "System time_INTERCEPT",
    "System time_R-VAL",

    "User time_FEATURE_CONFIG",
    "User time_FEATURE_TYPE",
    "User time_INTERCEPT",
    "User time_R-VAL",

    "Voluntary context switches_FEATURE_CONFIG",
    "Voluntary context switches_FEATURE_TYPE",
    "Voluntary context switches_INTERCEPT",
    "Voluntary context switches_R-VAL",

    "label",
]


dataset = []

with open("../../../rafPipeline/dataset_metadata/labels/labels.json") as f:
    labels = json.load(f)

for root, dirs, files in os.walk("../../../TheOutputsCodeforces/processed/atomic_time/results_code/"):
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

with open(f'{label_name}_dataset.csv', 'w') as f:
    write = csv.writer(f)

    write.writerow(features)
    write.writerows(dataset)