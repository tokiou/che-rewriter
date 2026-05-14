# 002 - Dataset Format

## Objective

Define the JSONL format used to train Che Rewriter.

## Scope

The dataset must represent rewriting examples from neutral Spanish into Rioplatense Spanish.

Each example must include:

- system instruction
- user rewriting request
- assistant completion

## Format

Each line must be a valid JSON object.

Required fields:

- `prompt`
- `completion`

`prompt` must be a list of chat messages.
`completion` must be a list of chat messages.

Each chat message must include:

- `role`
- `content`

Allowed roles:

- `system`
- `user`
- `assistant`

## Example

```json
{"prompt":[{"role":"system","content":"Sos un reescritor rioplatense."},{"role":"user","content":"Reescribí: Hola, ¿cómo estás?"}],"completion":[{"role":"assistant","content":"Hola, ¿cómo andás?"}]}