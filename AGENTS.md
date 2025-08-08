# Repository Guidelines

## Project Structure & Module Organization
- `scripts/`: Blender Python scripts (e.g., `fuzzy_sphere.py`, `studio_geometric_shapes.py`). Each script is self‑contained and declares an “Artistic Parameters” block at the top.
- `output/`: Rendered images and frames. Prefer small PNGs for previews; avoid committing large TIFFs unless required.
- `PROJECT_RULES.md`, `USER_RULES.md`: Domain context and usage rules.

## Build, Test, and Development Commands
- Requirements: Blender 4.x with Cycles. Run from the Blender UI (Scripting workspace) or headless.
- Run headless (no render): `blender -b -P scripts/fuzzy_sphere.py`
- Render a still (frame 1 → PNG): `blender -b -P scripts/fuzzy_sphere.py -o //output/fuzzyball2 -F PNG -f 1`
- Alternate scene: `blender -b -P scripts/studio_geometric_shapes.py`
- Quick smoke check: `blender -b --python-expr "import bpy; print(bpy.app.version_string)"`

## Coding Style & Naming Conventions
- Language: Python for Blender API. Use 4‑space indentation, `snake_case` for functions/variables, and `UPPER_SNAKE_CASE` for tunable constants (e.g., `LIGHT_INTENSITY`).
- File naming: descriptive, lower_snake (e.g., `new_effect_name.py`). Keep scripts in `scripts/` and avoid absolute paths.
- Structure: keep a clear parameters section, grouped helper functions (materials, lighting, camera), and a `main()` entry guarded by `if __name__ == "__main__":`.
- Formatting: prefer `black -l 100` and `ruff`/`flake8` if available; don’t introduce tooling that isn’t already configured.

## Testing Guidelines
- No unit test framework is used. Validate via headless runs that complete without errors and (when applicable) write outputs to `output/`.
- Suggested check: render a single frame at low samples and verify the file exists in `output/`.

## Commit & Pull Request Guidelines
- Commits: imperative, concise, and scoped. Examples: “Increase `SHADOW_SOFTNESS` for softer shadows”, “Refactor lighting setup for clarity”.
- PRs: include a clear description, key parameter changes, and a small preview image (PNG) saved under `output/`. Link related issues and note any breaking render differences.
- Assets: avoid committing very large binaries; keep previews optimized.

## Security & Configuration Tips
- Use relative paths (e.g., `//output/...`) and write only under `output/`.
- Keep sample counts/render sizes modest by default; document heavy settings so contributors can adjust locally.
