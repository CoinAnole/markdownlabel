# Test Suite Deviations

Deviations from [TESTING.md](TESTING.md) guidelines.

## kivy_garden/markdownlabel/tests/test_kivy_renderer_blocks.py
- Line 502-508: Test naming that doesn't match assertions (claims stores alt text but doesn't verify content)

## kivy_garden/markdownlabel/tests/test_kivy_renderer_tables.py
- Line 140-155: Testing private method `_render_table_cell` without documented exception
- Line 211-225: Testing private method `_render_table_cell` without documented exception
- Line 254-297: Test naming does not match assertions (claims verification of table_head/table_body structures with alignments but only asserts GridLayout type)

## kivy_garden/markdownlabel/tests/test_rebuild_scheduling.py
- Line 73: Docstring incorrectly classifies mixed changes (including style-only font_name) as "structure property changes"
- Line 85: Inline comment incorrectly labels property changes including font_name as "structure property changes"
- Line 182-211: Testing private _rebuild_trigger attribute without listed documented exception

## kivy_garden/markdownlabel/tests/test_serialization.py
- Line 718: Testing private method `_serialize_token` without documented exception
- Line 754: Testing private method `_serialize_list_item` without documented exception
- Line 765: Testing private method `_serialize_list_item` without documented exception

## kivy_garden/markdownlabel/tests/test_texture_render_mode.py
- Line 513-517: Monkeypatching private _render_as_texture without documented exception
- Line 544-548: Monkeypatching private _render_as_texture without documented exception

All other test files have no deviations.