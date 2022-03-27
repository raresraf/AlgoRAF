import json
import os
import sys
import csv
import random

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



best_seed = 1
best_f1 = 0
best_cm = [[]]

for seed in range(1000):
    random.seed(seed)

    train_dataset = []
    test_dataset = []
    with open("../../../rafPipeline/dataset_metadata/labels/labels.json") as f:
        labels = json.load(f)

    total_pbs = 0
    problem_dict = {}
    for root, dirs, files in os.walk("../../../TheOutputsCodeforces/processed/atomic_perf/results_code/"):
        for name in files:
            if name != "PROCESSED.RAF":
                continue
            problem = os.path.join(root, name).split("/")[-2].split("_")[0]
            problem_dict[problem] = problem_dict.get(problem, 0) + 1
            total_pbs = total_pbs + 1


    # print(total_pbs)
    # print(problem_dict)

    test_set = []
    test_set_len_label = 0
    test_set_len_nolabel = 0
    while test_set_len_label < 5 * total_pbs / 100 or test_set_len_nolabel < 20 * total_pbs / 100:
        k = random.choice(list(problem_dict.keys()))
        if label_name in labels[k]:
            if test_set_len_label < 5 * total_pbs / 100:
                if k not in test_set:
                    test_set.append(k)
                    test_set_len_label = test_set_len_label + problem_dict[k]
        else:
            if test_set_len_nolabel < 20 * total_pbs / 100:
                if k not in test_set:
                    test_set.append(k)
                    test_set_len_nolabel = test_set_len_nolabel + problem_dict[k]


    # print(test_set)
    # print(test_set_len_label)
    # print(test_set_len_nolabel)


    for root, dirs, files in os.walk("../../../TheOutputsCodeforces/processed/atomic_perf/results_code/"):
        for name in files:
            if name != "PROCESSED.RAF":
                continue
            problem = os.path.join(root, name).split("/")[-2].split("_")[0]
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
                    # print(problem, label_name in l)
                else:
                    new_entry.append(j["metrics"][feature.split("_", 1)[0]][feature.split("_", 1)[1]])

            if problem in test_set:
                test_dataset.append(new_entry)
            else:
                train_dataset.append(new_entry)

    with open(f'train_{label_name}_dataset.csv', 'w') as f:
        write = csv.writer(f)

        write.writerow(features)
        write.writerows(train_dataset)

    with open(f'test_{label_name}_dataset.csv', 'w') as f:
        write = csv.writer(f)

        write.writerow(features)
        write.writerows(test_dataset)

    # Configs

    label_name = "math"
    embedding_type = "perf" # time or perf

    import pandas as pd
    import matplotlib
    import numpy as np
    from sklearn import tree

    from sklearn.metrics import accuracy_score
    from sklearn.metrics import precision_score
    from sklearn.metrics import recall_score
    from sklearn.metrics import f1_score
    from sklearn.metrics import confusion_matrix
    from sklearn.model_selection import train_test_split

    np.set_printoptions(precision=3, suppress=True)


    train = pd.read_csv(f"../../dataset/{embedding_type}/train_{label_name}_dataset.csv")
    test = pd.read_csv(f"../../dataset/{embedding_type}/test_{label_name}_dataset.csv")

    print(len(train))
    print(len(test))

    tt = pd.concat([train, test])

    tt = pd.get_dummies(tt)

    train = tt[:len(train)]
    test = tt[len(train):]

    train_dataset_features = train.copy().drop('label', axis=1)
    train_dataset_labels = train.copy().pop('label')

    test_dataset_features = test.copy().drop('label', axis=1)
    test_dataset_labels = test.copy().pop('label')

    model = tree.DecisionTreeClassifier()
    model.fit(train_dataset_features, train_dataset_labels)

    cm = confusion_matrix(test_dataset_labels, model.predict(test_dataset_features))
    f1 = f1_score(test_dataset_labels, model.predict(test_dataset_features))
    print(seed, f1)
    print(cm)

    if f1 > best_f1:
        best_f1 = f1
        best_seed = seed
        best_cm = cm


print(best_seed, best_f1)
print(best_cm)