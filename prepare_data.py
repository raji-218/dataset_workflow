import pandas as pd

# load taxonomic abundance table
df = pd.read_csv("taxonomic_profiles.tsv", sep="\t")
taxonomy_col = df.columns[0]

print("original shape:", df.shape)

# extract genus-level abundance
genus = df[
    df[taxonomy_col].str.contains(r"\|g__", regex=True)
    & ~df[taxonomy_col].str.contains(r"\|s__", regex=True)
].copy()

genus[taxonomy_col] = genus[taxonomy_col].str.extract(r"g__([^|]+)")
genus.rename(columns={taxonomy_col: "Genus"}, inplace=True)

# transpose genus table
genus = genus.set_index("Genus").T
genus.reset_index(inplace=True)
genus.rename(columns={"index": "SampleID"}, inplace=True)

genus.to_csv("HMP2_Genus_Transposed.csv", index=False)

# extract species-level abundance
species = df[df[taxonomy_col].str.contains(r"\|s__", regex=True)].copy()
species[taxonomy_col] = species[taxonomy_col].str.extract(r"s__([^|]+)")
species.rename(columns={taxonomy_col: "Species"}, inplace=True)

species = species.set_index("Species").T
species.reset_index(inplace=True)
species.rename(columns={"index": "SampleID"}, inplace=True)

species.to_csv("HMP2_Species_Transposed.csv", index=False)

# load metadata
meta = pd.read_excel("hmp2_metadata_2018-08-20.xlsx")

# keep only metagenomic samples
meta = meta[meta["data_type"] == "metagenomics"].copy()

# keep useful metadata columns
meta = meta[
    [
        "External ID",
        "Participant ID",
        "diagnosis",
        "visit_num",
        "sex",
        "BMI",
        "Age at diagnosis",
        "is_inflamed",
    ]
]

# merge abundance with metadata
merged = genus.merge(
    meta,
    left_on="SampleID",
    right_on="External ID",
    how="inner",
)

merged.drop(columns="External ID", inplace=True)

print("merged shape:", merged.shape)

merged.to_csv("HMP2_Genus_ML_Dataset.csv", index=False)
