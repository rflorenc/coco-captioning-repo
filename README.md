# coco-captioning-repo
Image Caption Generation using COCO dataset 


Uses a subset of the [COCO "Common Objects in Context"](https://cocodataset.org/#home) dataset for image caption generation.  
Demonstrates transfer learning from a pretrained [ResNet152](https://docs.pytorch.org/vision/main/models/generated/torchvision.models.resnet152.html) on the ImageNet dataset.  Compares prediction results using BLEU score and cosine similarity.  

## What's here

| File | Purpose |
|---|---|
| `nb_ImageCaptionGeneration_COCO.ipynb` | everything: getting the data, EDA → ResNet152 features → caption vocabulary → LSTM decoder → BLEU / cosine evaluation |
| `datasets/coco/images/metadata/coco_subset_meta.csv` | metadata of the 5,029-image subset |

The images, annotations and ResNet152 weights are **not** in this repository (about 1.2 GB). The
notebook's **"Get the data"** section fetches them (and installs `nltk`), so a clone takes seconds.

## Run it on OpenShift AI

Prepared by the workshop setup (`lab-setup`): a shared, read-only `datasets` bucket holding the image
subset, the COCO 2017 annotations and the ResNet152 weights, and a connection to it in your project.

1. Create a workbench: image **Jupyter | PyTorch | CUDA | Python 3.12**, a hardware profile with **1 GPU**,
   memory request 16 GiB / limit 24 GiB, connection **`datasets (shared, read-only)`** attached.
2. Clone this repository (Git button).
3. Open `nb_ImageCaptionGeneration_COCO.ipynb` and run it from the top. "Get the data" fetches
   everything from the shared bucket (~15 seconds inside the cluster); re-running skips what is there.

## Run it elsewhere

Without the workshop connection, "Get the data" downloads the same files from their public copies, and
torchvision downloads the ResNet152 weights on first use. Needs a PyTorch environment (a GPU helps for
the feature extraction).

COCO images and annotations are licensed under [CC BY 4.0](https://cocodataset.org/#termsofuse).
