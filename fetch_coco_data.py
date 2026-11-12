"""
COCO data for nb_ImageCaptionGeneration_COCO.ipynb. Run once, from a workbench terminal:
    python fetch_coco_data.py [path-to-this-repo]        default: the folder this script is in
(It can also be pasted as a first notebook cell.)

Gets the data from the shared, read-only `datasets` bucket instead of Git LFS, and the ResNet152
weights from the same bucket instead of download.pytorch.org. Needs the workbench connection
"datasets (shared, read-only)" attached (AWS_* environment variables). Idempotent: skips what is
already there, so re-running the notebook is cheap.

If the clone already has the zips (an image with git-lfs downloads them on clone), they are used as
they are; otherwise they come from the bucket. Result, relative to the repository root (the paths the
notebook already uses):
  datasets/coco/images/<5,029 jpg>              from coco/coco_subset_images.zip
  datasets/coco/images/metadata/coco_subset_meta.csv
  datasets/coco/annotations/{captions,instances}_train2017.json   (only the two the notebook reads)
  ~/.cache/torch/hub/checkpoints/resnet152-f82ba261.pth          (ResNet152_Weights.DEFAULT; PyTorch's
                                                                  default cache, so torchvision finds it by itself)
"""
import os, sys, zipfile, pathlib
import boto3

REPO = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).parent).resolve()   # this repo
COCO = REPO / "datasets" / "coco"
# PyTorch's default cache (or $TORCH_HOME if set): torchvision looks here before downloading
TORCH_HOME = pathlib.Path(os.environ.get("TORCH_HOME", pathlib.Path.home() / ".cache" / "torch"))

from botocore import UNSIGNED
from botocore.config import Config
if os.environ.get("AWS_ACCESS_KEY_ID", "anonymous") == "anonymous":   # shared bucket: anonymous read-only policy
    s3 = boto3.client("s3", endpoint_url=os.environ["AWS_S3_ENDPOINT"], config=Config(signature_version=UNSIGNED),
                      region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))
else:
    s3 = boto3.client("s3", endpoint_url=os.environ["AWS_S3_ENDPOINT"],
                      aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
                      aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
                      region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))
BUCKET = os.environ.get("AWS_S3_BUCKET", "datasets")

def fetch(key, dest):
    dest = pathlib.Path(dest)
    if dest.exists() and dest.stat().st_size > 0:
        print(f"have {dest}"); return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"downloading s3://{BUCKET}/{key} ..."); s3.download_file(BUCKET, key, str(dest)); return dest

def extract(zip_path, target, only=None):
    with zipfile.ZipFile(zip_path) as z:
        names = [n for n in z.namelist()
                 if not n.startswith("__MACOSX/") and not n.endswith(".DS_Store") and not n.endswith("/")
                 and (only is None or n in only)]
        todo = [n for n in names if not (target / n).exists()]
        for n in todo: z.extract(n, target)
        print(f"{zip_path.name}: {len(names) - len(todo)} present, {len(todo)} extracted")

def zip_source(key, in_clone, tmp_name):
    """Use the zip from the clone if Git LFS already downloaded it (a real zip, not a pointer file),
    otherwise download it from the bucket."""
    if in_clone.exists() and zipfile.is_zipfile(in_clone):
        print(f"using {in_clone.relative_to(REPO)} from the clone (Git LFS)"); return in_clone
    return fetch(key, REPO / ".coco-download" / tmp_name)

extract(zip_source("coco/coco_subset_images.zip", COCO / "images" / "coco_subset_images.zip", "coco_subset_images.zip"), COCO)
extract(zip_source("coco/annotations_trainval2017.zip", COCO / "annotations" / "annotations_trainval2017.zip", "annotations_trainval2017.zip"), COCO,
        only={"annotations/captions_train2017.json", "annotations/instances_train2017.json"})
fetch("coco/coco_subset_meta.csv", COCO / "images" / "metadata" / "coco_subset_meta.csv")
fetch("torch/hub/checkpoints/resnet152-f82ba261.pth", TORCH_HOME / "hub" / "checkpoints" / "resnet152-f82ba261.pth")
print(f"COCO data ready under {COCO}; ResNet152 weights in {TORCH_HOME / 'hub' / 'checkpoints'}")
