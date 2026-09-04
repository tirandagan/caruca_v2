## Command

`{{command}}`

## Syntax specification

```python
{{syntax_spec}}
```

## Value types and the values they stand for

```json
{{probe_values}}
```

## Bounds

- A repeatable argument may appear at most {{max_arity}} time(s).
- At most {{max_count}} optional flags may be combined in a single invocation.
- These flags are excluded entirely: {{skip_flags}}
- Standard input variation: {{stdin_variation}}. File content variation: {{content_variation}}.

## Now produce the output

One JSON object per line, in the format given above, for `{{command}}`.
