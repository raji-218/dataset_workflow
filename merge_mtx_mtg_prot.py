#mgx+mtx
import pandas as pd

# ============================================
# Load datasets
# ============================================

mgx = pd.read_csv("HMP2_Genus_Filtered.csv")
mtx = pd.read_csv("MTX_SelectedFeatures.csv")

# ============================================
# Remove technical replicate samples
# ============================================

mgx = mgx[
    ~mgx["SampleID"].str.endswith("_TR", na=False)
]

mgx = mgx[
    ~mgx["SampleID"].str.endswith("_P", na=False)
]

print("=" * 60)
print("Cleaned MGX Dataset")
print("=" * 60)

print("Shape:", mgx.shape)
print("Participants:", mgx["Participant ID"].nunique())

dup = mgx.duplicated(
    subset=["Participant ID", "visit_num"],
    keep=False
)

print("Duplicate visits:", dup.sum())

# ============================================
# Save cleaned MGX dataset
# ============================================

mgx.to_csv(
    "MGX_SelectedFeatures.csv",
    index=False
)

print("Saved: MGX_SelectedFeatures.csv")

# ============================================
# Metadata columns
# ============================================

mgx_meta = [
    "SampleID",
    "Participant ID",
    "diagnosis",
    "visit_num",
    "sex",
    "BMI",
    "Age at diagnosis",
    "is_inflamed"
]

mtx_meta = [
    "Participant ID",
    "visit_num",
    "diagnosis",
    "MET",
    "MGX",
    "MTX",
    "PROT"
]

# ============================================
# Prefix feature columns only
# ============================================

mgx = mgx.rename(
    columns={
        c: "GENUS_" + c
        for c in mgx.columns
        if c not in mgx_meta
    }
)

mtx = mtx.rename(
    columns={
        c: "MTX_" + c
        for c in mtx.columns
        if c not in mtx_meta
    }
)

# ============================================
# Merge datasets
# ============================================

merged = mgx.merge(
    mtx,
    on=[
        "Participant ID",
        "visit_num",
        "diagnosis"
    ],
    how="inner"
)

print("\n" + "=" * 60)
print("MGX + MTX Dataset")
print("=" * 60)

print("Shape:", merged.shape)

print("\nDiagnosis")
print(merged["diagnosis"].value_counts())

print("\nParticipants")
print(merged["Participant ID"].nunique())

print("\nUnique rows")
print(len(merged))

# ============================================
# Save merged dataset
# ============================================

merged.to_csv(
    "MGX_MTX_SelectedFeatures.csv",
    index=False
)

print("\nSaved: MGX_MTX_SelectedFeatures.csv")

#prot+mtx
import pandas as pd

# ============================================
# Load datasets
# ============================================

prot = pd.read_csv("Proteomics_SelectedFeatures.csv")
mtx = pd.read_csv("MTX_SelectedFeatures.csv")

# ============================================
# Metadata columns
# ============================================

prot_meta = [
    "SampleID",
    "Participant ID",
    "diagnosis",
    "visit_num"
]

mtx_meta = [
    "Participant ID",
    "visit_num",
    "diagnosis",
    "MET",
    "MGX",
    "MTX",
    "PROT"
]

# ============================================
# Prefix feature columns
# ============================================

prot = prot.rename(
    columns={
        c: "PROT_" + c
        for c in prot.columns
        if c not in prot_meta
    }
)

mtx = mtx.rename(
    columns={
        c: "MTX_" + c
        for c in mtx.columns
        if c not in mtx_meta
    }
)

# ============================================
# Merge
# ============================================

merged = prot.merge(
    mtx,
    on=[
        "Participant ID",
        "visit_num",
        "diagnosis"
    ],
    how="inner"
)

print("=" * 60)
print("PROT + MTX Dataset")
print("=" * 60)

print("Shape:", merged.shape)

print("\nDiagnosis")
print(merged["diagnosis"].value_counts())

print("\nParticipants")
print(merged["Participant ID"].nunique())

print("\nUnique rows")
print(len(merged))

merged.to_csv(
    "PROT_MTX_SelectedFeatures.csv",
    index=False
)

print("\nSaved: PROT_MTX_SelectedFeatures.csv")

#mgx+mtx+prot
import pandas as pd

# ============================================
# Load datasets
# ============================================

mgx = pd.read_csv("MGX_SelectedFeatures.csv")
prot = pd.read_csv("Proteomics_SelectedFeatures.csv")
mtx = pd.read_csv("MTX_SelectedFeatures.csv")

# ============================================
# Metadata
# ============================================

mgx_meta = [
    "SampleID",
    "Participant ID",
    "diagnosis",
    "visit_num",
    "sex",
    "BMI",
    "Age at diagnosis",
    "is_inflamed"
]

prot_meta = [
    "SampleID",
    "Participant ID",
    "diagnosis",
    "visit_num"
]

mtx_meta = [
    "Participant ID",
    "visit_num",
    "diagnosis",
    "MET",
    "MGX",
    "MTX",
    "PROT"
]

# ============================================
# Prefix features
# ============================================

mgx = mgx.rename(
    columns={
        c: "GENUS_" + c
        for c in mgx.columns
        if c not in mgx_meta
    }
)

prot = prot.rename(
    columns={
        c: "PROT_" + c
        for c in prot.columns
        if c not in prot_meta
    }
)

mtx = mtx.rename(
    columns={
        c: "MTX_" + c
        for c in mtx.columns
        if c not in mtx_meta
    }
)

# ============================================
# MGX + PROT
# ============================================

merged = mgx.merge(
    prot,
    on=[
        "Participant ID",
        "visit_num",
        "diagnosis"
    ],
    how="inner"
)

# ============================================
# + MTX
# ============================================

merged = merged.merge(
    mtx,
    on=[
        "Participant ID",
        "visit_num",
        "diagnosis"
    ],
    how="inner"
)

print("=" * 60)
print("MGX + PROT + MTX Dataset")
print("=" * 60)

print("Shape:", merged.shape)

print("\nDiagnosis")
print(merged["diagnosis"].value_counts())

print("\nParticipants")
print(merged["Participant ID"].nunique())

print("\nUnique rows")
print(len(merged))

merged.to_csv(
    "MGX_PROT_MTX_SelectedFeatures.csv",
    index=False
)

print("\nSaved: MGX_PROT_MTX_SelectedFeatures.csv")
