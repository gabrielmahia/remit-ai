"""Regression tests for the Gemini helper in app.py.

app.py runs Streamlit UI code at import, so these tests extract the real `gemini` function from the source with `ast` and execute just that function
against a fake HTTP layer. They exist because an inner `import ssl, urllib.error` once made `urllib` a local name, so every call raised
UnboundLocalError before reaching the `try` (the docstring said 'never raises'); a blind `except` elsewhere hid the symptom."""
import ast
import io
import json
import ssl
import urllib.error
import urllib.request
from pathlib import Path

APP = Path(__file__).resolve().parents[1] / "app.py"


def _load_gemini():
    tree = ast.parse(APP.read_text(encoding="utf-8"))
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "gemini")
    ns = {"json": json, "ssl": ssl, "urllib": urllib}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), str(APP), "exec"), ns)  # noqa: S102
    return ns["gemini"]


class _Resp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def test_gemini_returns_the_model_text(monkeypatch):
    body = json.dumps({"candidates": [{"content": {"parts": [{"text": "hello from the model"}]}}]}).encode()
    monkeypatch.setattr(urllib.request, "urlopen", lambda *a, **k: _Resp(body))
    assert _load_gemini()("hi", "KEY") == "hello from the model"


def test_gemini_reports_an_empty_response(monkeypatch):
    monkeypatch.setattr(urllib.request, "urlopen", lambda *a, **k: _Resp(json.dumps({"candidates": []}).encode()))
    assert "No response" in _load_gemini()("hi", "KEY")


def test_gemini_never_raises_on_an_http_error(monkeypatch):
    def boom(*a, **k):
        raise urllib.error.HTTPError("u", 404, "not found", {}, None)

    monkeypatch.setattr(urllib.request, "urlopen", boom)
    out = _load_gemini()("hi", "KEY")
    assert "AI unavailable" in out and "404" in out


def test_app_imports_urllib_at_module_level_not_inside_functions():
    # The root cause: a function-level import of urllib.error shadows the module-level name for the whole function body.
    tree = ast.parse(APP.read_text(encoding="utf-8"))
    for fn in (n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)):
        for node in ast.walk(fn):
            if isinstance(node, ast.Import):
                assert not any(a.name.split(".")[0] in ("urllib", "ssl", "json") for a in node.names), f"{fn.name} imports {[a.name for a in node.names]} locally"
