# Dataset

This folder contains dataset information.

Files to be added:
- Dataset Details
- Dataset Description
- Dataset Source
# Dataset

## Dataset Name
SpaceNet Dataset

## Source
SpaceNet / AWS Open Data

## Purpose
The dataset is used to develop and evaluate the
AI-based satellite image importance scoring and
intelligent storage lifecycle optimization system.

## Dataset Structure

- `raw/` - Original downloaded satellite images.
- `sample/` - Small subset used for development and testing.
- `processed/` - Images generated after preprocessing.

## Preprocessing

The preprocessing pipeline will include:

1. Image loading
2. Image validation
3. Resizing
4. Format conversion where required
5. Normalization
6. Saving processed images

## Usage

The sample dataset is used during development to
test the Vision Foundation Model and importance
scoring pipeline before scaling to a larger dataset.
