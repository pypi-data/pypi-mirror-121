# nxtoascii

Convert a BLISS HDF5 file to SPEC, MULTISPEC, CSV or a generic ASCII columns file.

## Install

From source

```bash
python -m pip install .
```

## Usage

Convert a BLISS HDF5 file to a MULTISPEC file

```bash
nxtoascii /data/visitor/hg123/id00/hg123_id00.h5
```

Save each scan in a separate SPEC file

```bash
nxtoascii /data/visitor/hg123/id00/hg123_id00.h5 --format SPEC
```

Select scans with the word "exafs" in the title

```bash
nxtoascii ... --scans "*exafs*"
```

Make sure the first three columns are Emono, I0 and I1

```bash
nxtoascii ... --columns Emono I0 I1
```

Only save the columns Emono, I0 and I1

```bash
nxtoascii ... --columns Emono I0 I1 --only_columns
```

## Developers

```bash
python -m pip install -r requirements-dev.txt
pytest
```
