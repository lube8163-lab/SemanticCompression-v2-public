#!/usr/bin/env python3
import argparse
from pathlib import Path

import coremltools as ct
import torch
from transformers import SiglipVisionModel


class SigLIP2VisionWrapper(torch.nn.Module):
    def __init__(self, model: SiglipVisionModel):
        super().__init__()
        self.model = model

    def forward(self, pixel_values: torch.Tensor) -> torch.Tensor:
        out = self.model(pixel_values=pixel_values)
        return out.pooler_output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export SigLIP2 vision encoder (CLS/pooler output) to Core ML."
    )
    parser.add_argument(
        "--model-id",
        default="google/siglip2-base-patch16-224",
        help="Hugging Face model id",
    )
    parser.add_argument(
        "--output",
        default="SigLIP2_Base_VisionCLS.mlpackage",
        help="Output .mlpackage path",
    )
    parser.add_argument(
        "--image-size",
        type=int,
        default=224,
        help="Input image size (square)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Loading model: {args.model_id}")
    vision_model = SiglipVisionModel.from_pretrained(
        args.model_id,
        torch_dtype=torch.float32,
    )
    vision_model.eval()

    wrapper = SigLIP2VisionWrapper(vision_model)

    dummy = torch.randn(1, 3, args.image_size, args.image_size)

    print("Tracing Torch model...")
    with torch.no_grad():
        traced = torch.jit.trace(wrapper, dummy)

    print("Converting to CoreML...")
    mlmodel = ct.convert(
        traced,
        convert_to="mlprogram",
        inputs=[
            ct.TensorType(
                name="pixel_values",
                shape=dummy.shape,
            )
        ],
        compute_precision=ct.precision.FLOAT16,
    )

    mlmodel.save(str(output_path))
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
