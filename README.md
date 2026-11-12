# coco-captioning-repo
Image Caption Generation using COCO dataset 


Uses a subset of the [COCO "Common Objects in Context"](https://cocodataset.org/#home) dataset for image caption generation.  
Demonstrates transfer learning from a pretrained [ResNet152](https://docs.pytorch.org/vision/main/models/generated/torchvision.models.resnet152.html) on the ImageNet dataset.  Compares prediction results using BLEU score and cosine similarity.  

## What's here

| File | Purpose |
|---|---|
| `nb_ImageCaptionGeneration_COCO.ipynb` | the notebook: EDA → ResNet152 features → caption vocabulary → LSTM decoder → BLEU / cosine evaluation |
| `fetch_coco_data.py` | puts the data and the ResNet152 weights where the notebook expects them (see below) |
| `requirements.txt` | packages on top of a PyTorch image (`nltk`) |
| `datasets/coco/images/metadata/coco_subset_meta.csv` | metadata of the 5,029-image subset |

The images, annotations and weights are **not** in this repository (about 1.2 GB). `fetch_coco_data.py`
fetches them, so a clone takes seconds.

## Run it on OpenShift AI

Prepared by the workshop setup (`lab-setup`): a shared, read-only `datasets` bucket holding the image
subset, the COCO 2017 annotations and the ResNet152 weights, and a connection to it in your project.

1. Create a workbench: image **Jupyter | PyTorch | CUDA | Python 3.12**, a hardware profile with **1 GPU**,
   memory request 16 GiB / limit 24 GiB, connection **`datasets (shared, read-only)`** attached.
2. Clone this repository (Git button, or `git clone` in a terminal).
3. In a terminal:
   ```bash
   cd coco-captioning-repo
   python fetch_coco_data.py      # ~1–2 min: images, annotations, metadata, ResNet152 weights
   pip install -r requirements.txt
   ```
4. Open `nb_ImageCaptionGeneration_COCO.ipynb` and run it section by section.

After step 3:
- `datasets/coco/images/` holds the 5,029 images
- `datasets/coco/annotations/` holds `captions_train2017.json` and `instances_train2017.json`
- `~/.cache/torch/hub/checkpoints/resnet152-f82ba261.pth` is used by torchvision instead of a download

## Run it elsewhere

Without the bucket, place the same files yourself before running the notebook:
- images: the subset listed in `coco_subset_meta.csv` (from [cocodataset.org](https://cocodataset.org/#download), train2017) in `datasets/coco/images/`
- annotations: `annotations_trainval2017.zip` from cocodataset.org, extracted into `datasets/coco/`
- the ResNet152 weights download automatically on first use

COCO images and annotations are licensed under [CC BY 4.0](https://cocodataset.org/#termsofuse).
