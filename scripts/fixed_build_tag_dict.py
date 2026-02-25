#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModel, AutoProcessor


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build label JSON and normalized text embedding .npy for SigLIP2 tag dictionary."
    )
    parser.add_argument(
        "--labels-json",
        required=True,
        help="Input labels JSON path (array of strings)",
    )
    parser.add_argument(
        "--output-labels",
        default="style.json",
        help="Output labels JSON path",
    )
    parser.add_argument(
        "--output-embs",
        default="style_embs.npy",
        help="Output embeddings .npy path",
    )
    parser.add_argument(
        "--model-id",
        default="google/siglip2-base-patch16-224",
        help="Hugging Face model id",
    )
    parser.add_argument(
        "--max-length",
        type=int,
        default=64,
        help="Max token length",
    )
    parser.add_argument(
        "--device",
        default="cpu",
        help="Torch device (cpu, cuda, mps)",
    )
    return parser.parse_args()


def load_labels(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list) or not all(isinstance(x, str) for x in data):
        raise ValueError("labels JSON must be an array of strings")
    return data


def main() -> None:
    args = parse_args()

    labels_path = Path(args.labels_json)
    out_labels = Path(args.output_labels)
    out_embs = Path(args.output_embs)

    labels = load_labels(labels_path)

    device = args.device
    print(f"Loading model: {args.model_id} on {device}")
    processor = AutoProcessor.from_pretrained(args.model_id)
    model = AutoModel.from_pretrained(args.model_id, torch_dtype=torch.float32).to(device)
    model.eval()

    inputs = processor(
        text=labels,
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=args.max_length,
    ).to(device)

    with torch.no_grad():
        txt = model.get_text_features(input_ids=inputs["input_ids"])

    txt = txt / txt.norm(dim=-1, keepdim=True)

    out_embs.parent.mkdir(parents=True, exist_ok=True)
    out_labels.parent.mkdir(parents=True, exist_ok=True)

    np.save(out_embs, txt.cpu().numpy())
    with out_labels.open("w", encoding="utf-8") as f:
        json.dump(labels, f, ensure_ascii=False, indent=2)

    print(f"DONE: labels={len(labels)}, dim={txt.shape[-1]}")
    print(f"Saved labels: {out_labels}")
    print(f"Saved embs: {out_embs}")


if __name__ == "__main__":
    main()
