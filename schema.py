# schema.py (for Pydantic v2+)

from pydantic import BaseModel, ValidationError
from typing import List, Optional
import json
import os

# ✅ Define Pydantic schema
class DesignSpec(BaseModel):
    type: str
    material: List[str]
    color: Optional[str] = None
    purpose: Optional[str] = None

# ✅ Structured outputs
structured_outputs = [
    {
        "type": "robotic arm",
        "material": ["aluminum"],
        "color": None,
        "purpose": "factory use"
    },
    {
        "type": "gearbox",
        "material": ["steel"],
        "color": "red",
        "purpose": "automotive"
    },
    {
        "type": "throne",
        "material": ["wood"],
        "color": None,
        "purpose": "fantasy game"
    }
]

# ✅ Output directory
output_dir = "spec_outputs"
os.makedirs(output_dir, exist_ok=True)

# ✅ Validate and save each spec
for i, raw in enumerate(structured_outputs, start=1):
    try:
        spec = DesignSpec(**raw)
        filename = os.path.join(output_dir, f"spec_{i}.json")
        with open(filename, "w") as f:
            # ✅ Use model_dump_json in Pydantic v2
            f.write(spec.model_dump_json(indent=4))
        print(f"✅ Saved validated JSON to: {filename}")
    except ValidationError as e:
        print(f"❌ Validation error for spec {i}:\n{e}")
    except Exception as e:
        print(f"❌ Other error in spec {i}:\n{e}")
