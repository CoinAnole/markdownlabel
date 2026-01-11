# Fulcrum → markdownlabel handoff

This file is meant to let us resume work in a new window / new conversation working directly in `external/markdownlabel/`.

## Context

Fulcrum embeds a vendored copy of Kivy Garden MarkdownLabel at `external/markdownlabel/`. We hit `Clock.max_iteration` warnings while rendering medium/complex Markdown (nested lists + tables + code blocks) in the chat feed.

The warning is not necessarily a “true infinite loop”; it can also be “layout convergence takes >60 passes in a frame”, especially with deep widget trees and many coupled size bindings.

## What we did in Fulcrum before this handoff

### 1) Pragmatic guardrail in the app

We increased `Clock.max_iteration` at app startup:

- File: `fulcrum/main.py`
- Change: `Clock.max_iteration = 120`
- Rationale: reduces spurious warnings during heavy layout, but does not fix actual cycles.

### 2) markdownlabel binding-cycle fixes (vendored copy)

We made several safety changes inside the vendored `markdownlabel`:

- **`kivy_garden/markdownlabel/rendering.py`**
  - `apply_text_size_binding()` now binds `texture_size -> height` **only when `label.size_hint_y is None`**.
  - Previously the code effectively bound `texture_size -> height` unconditionally, which can fight layout-driven heights.

- **`kivy_garden/markdownlabel/kivy_renderer.py`**
  - List marker changed from `size_hint_y=1` to `size_hint_y=None`, and marker height is bound to the list content column height.
  - Removed per-widget bindings in a couple places (code blocks / truncation placeholder) to avoid duplicated binding passes; MarkdownLabel already does a global pass via `_update_text_size_bindings_in_place(content)`.

Even with these fixes, the full “stress test” markdown could still trip `Clock.max_iteration` in widget mode on this machine. Minimal list-only and code-only cases did **not** trigger the warning, suggesting the full document is at the “slow convergence” edge rather than a single obvious cycle.

## Repro scripts copied into markdownlabel

Added under `external/markdownlabel/repro/`:

- `repro/reproduce_issue.py`: the original stress test (lists + tables + code)
- `repro/min_list_only.py`: minimal list-only
- `repro/min_code_only.py`: minimal fenced-code-only

Run from within the markdownlabel repo:

```bash
python repro/reproduce_issue.py
python repro/min_list_only.py
python repro/min_code_only.py
```

## What to do next (in the markdownlabel repo)

1. **Get test dependencies installed** (Hypothesis in particular).
   - When we tried running markdownlabel’s tests inside Fulcrum’s env, pytest failed to import `hypothesis`.
2. **Run the markdownlabel test suite** focusing on text sizing / rendering:
   - `kivy_garden/markdownlabel/tests/test_text_properties.py`
   - `kivy_garden/markdownlabel/tests/test_sizing_behavior.py`
   - Any performance / rebuild-contract tests relevant to size bindings.
3. **If `repro/reproduce_issue.py` still warns with default `Clock.max_iteration=60`**:
   - Decide whether to treat it as acceptable “heavy layout” (and document that users should raise max_iteration for very complex markdown), OR
   - Add a mitigation:
     - heuristic switch to `render_mode='texture'` for large ASTs / deep nesting, OR
     - reduce widget churn (e.g., fewer intermediate BoxLayouts / fewer bindings).

## Notes

- In widget mode, the ScrollView + dynamic-height children pattern amplifies layout work. If we need to fully eliminate warnings, texture mode (single Image) is likely the most robust path for very complex markdown.

