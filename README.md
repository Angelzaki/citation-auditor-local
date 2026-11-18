<div align="center">

# citation-auditor-local

**Auditor de citas RAG** · Angel Salazar

`answer + citations → ¿existen? ¿soportan?`

</div>

---

### `$ whoami`

No basta citar un `doc_id`. Verifico que el documento exista y que el texto de la respuesta esté respaldado.

---

### `$ ./audit.sh`

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
pytest
python -m citation_auditor
```

---

Hecho en Lima · Angel Salazar · CIP 404730
