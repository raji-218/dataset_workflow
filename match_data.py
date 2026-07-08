import pandas as pd

matched = pd.read_csv("Matched_Sample_IDs.csv")

mtx_samples = (
    matched["MTX"]
    .dropna()
    .astype(str)
    + "_Abundance-RPKs"
)

print("Matched MTX samples:", len(mtx_samples))
print(mtx_samples.head())

header = pd.read_csv(
    "genefamilies.tsv",
    sep="\t",
    nrows=0
)

available = [c for c in mtx_samples if c in header.columns]

print("Matched columns found:", len(available))
print("Missing columns:", len(mtx_samples) - len(available))

missing = sorted(set(mtx_samples) - set(available))

print("\nFirst 10 missing:")
print(missing[:10])

header = pd.read_csv(
    "genefamilies.tsv",
    sep="\t",
    nrows=0
)

header_cols = header.columns.tolist()

for sample in missing[:10]:
    base = sample.replace("_Abundance-RPKs", "")

    matches = [c for c in header_cols if base in c]

    print("\n", base)
    print(matches[:5])

import pandas as pd

# load matched sample ids
matched = pd.read_csv("Matched_Sample_IDs.csv")

mtx = (
    matched["MTX"]
    .dropna()
    .astype(str)
    + "_Abundance-RPKs"
).tolist()

# read only header
header = pd.read_csv(
    "genefamilies.tsv",
    sep="\t",
    nrows=0
)

available = [c for c in mtx if c in header.columns]

print("Matched MTX samples:", len(available))

usecols = ["# Gene Family"] + available

chunksize = 50000

first = True

for chunk in pd.read_csv(
    "genefamilies.tsv",
    sep="\t",
    usecols=usecols,
    chunksize=chunksize
):

    # remove stratified rows
    chunk = chunk[
        ~chunk["# Gene Family"].str.contains("|", regex=False)
    ]

    # remove HUMAnN summary rows
    chunk = chunk[
        ~chunk["# Gene Family"].isin(
            ["UNMAPPED", "UNINTEGRATED"]
        )
    ]

    if first:
        chunk.to_csv(
            "MTX_155_Unstratified.tsv",
            sep="\t",
            index=False
        )
        first = False
    else:
        chunk.to_csv(
            "MTX_155_Unstratified.tsv",
            sep="\t",
            mode="a",
            header=False,
            index=False
        )

print("Finished!")
