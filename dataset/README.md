# Dataset and sample imagery

## Dataset used

IntelliArchive references SpaceNet satellite imagery for development and demonstration. Sample names shown in the application include RGB pan-sharpened Las Vegas tiles (AOI 2). SpaceNet is a family of datasets; imagery, labels, license terms, and citations vary by challenge and product.

SpaceNet is catalogued in the AWS Registry of Open Data and hosted in the public S3 bucket s3://spacenet-dataset/. The application uses image pixels as CLIP inputs. It does not train CLIP on SpaceNet labels, and its importance score is not a building/road detection result or supervised accuracy metric.

## What is included in this repository

On the current main branch, dataset/ contains this README but no checked-in raw/, sample/, or processed/ image assets. The application advertises ten sample GeoTIFFs, so verify where those files are supplied locally or in the deployment environment before saying the binaries are included in GitHub. Large imagery should not be committed without checking repository size and the exact product license.

The lifecycle simulation copies archived images into cloud_simulation/S3_STANDARD/, cloud_simulation/S3_STANDARD_IA/, or cloud_simulation/S3_GLACIER/. It records decisions in results/lifecycle_log.csv and results/importance_scores.csv. These are local prototype artifacts, not durable S3 lifecycle transitions.

## Source and licensing

- SpaceNet dataset catalog: https://spacenet.ai/datasets/
- AWS Open Data Registry entry: https://registry.opendata.aws/spacenet/
- Check the exact challenge/product page for license and attribution requirements. SpaceNet's catalog lists varying licenses; do not assume all subsets share the same terms.

Suggested citation; update the access date when submitting:

> SpaceNet on Amazon Web Services (AWS). “Datasets.” The SpaceNet Catalog. https://spacenet.ai/datasets/. Accessed 26 October 2026.

## Image handling in this project

1. Load a supported GeoTIFF or image through the analysis flow.
2. Validate it and prepare a display preview. Contrast stretching is for visualization, not radiometric calibration.
3. Convert to RGB and resize the model input to 224 × 224 for CLIP ViT-B/32.
4. Use the output probabilities to calculate the prototype importance score and category.
5. If lifecycle simulation is selected, copy the file into a local simulated tier and update the CSV ledgers.

## Reproducibility record

For every sample used in a result or screenshot, record:

| Field | What to record |
| --- | --- |
| Filename | Exact input filename |
| Product | SpaceNet challenge/product and release |
| AOI or location | Only when confirmed by source metadata |
| Source | Exact dataset URL or S3 key |
| License | Terms for that exact product |
| Checksum | SHA-256 of the exact file used |
| Processing | Contrast/resize settings and relevant library versions |
| Inference | CLIP model ID, text prompts, and thresholds |

Do not publish dataset counts or model-performance claims without a sample manifest and evaluation procedure.
