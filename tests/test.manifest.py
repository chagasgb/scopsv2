from pathlib import Path
import pytest

from manifest import Manifest


YAML_EXEMPLO = """
camadas:
  backend:
    tecnologia: " Python "
    versao: "3.12"
  frontend:
    tecnologia: "VUE"
    versao: "3"

recursos:
  db_main:
    tipo: database
    porta: 5432
  api_users:
    tipo: api
    porta: 8000
    camada: backend

blueprints:
  gerar_api:
    recurso: api_users
    output: "src/api"
  gerar_db:
    recurso: db_main
    output: "infra/db"
"""


@pytest.fixture
def manifest_path(tmp_path: Path) -> Path:
    p = tmp_path / "manifesto.yml"
    p.write_text(YAML_EXEMPLO, encoding="utf-8")
    return p


def test_load_and_basic_blocks(manifest_path: Path):
    m = Manifest.load(str(manifest_path))
    assert "backend" in m.camadas
    assert "db_main" in m.recursos
    assert "gerar_api" in m.blueprints


def test_tecnologia_da_camada_normaliza(manifest_path: Path):
    m = Manifest.load(str(manifest_path))
    assert m.tecnologia_da_camada("backend") == "python"
    assert m.tecnologia_da_camada("frontend") == "vue"


def test_tecnologia_da_camada_inexistente(manifest_path: Path):
    m = Manifest.load(str(manifest_path))
    assert m.tecnologia_da_camada("nao_existe") is None


def test_camadas_por_tecnologia(manifest_path: Path):
    m = Manifest.load(str(manifest_path))
    assert m.camadas_por_tecnologia("python") == ["backend"]
    assert m.camadas_por_tecnologia("VUE") == ["frontend"]  # normaliza entrada também


def test_recurso_e_recursos_por_tipo(manifest_path: Path):
    m = Manifest.load(str(manifest_path))
    assert m.recurso("api_users")["porta"] == 8000
    assert set(m.recursos_por_tipo("api")) == {"api_users"}
    assert set(m.recursos_por_tipo("database")) == {"db_main"}
    assert m.recurso("nao_existe") is None


def test_blueprint_e_blueprints_do_recurso(manifest_path: Path):
    m = Manifest.load(str(manifest_path))
    assert m.blueprint("gerar_api")["output"] == "src/api"
    assert set(m.blueprints_do_recurso("api_users")) == {"gerar_api"}
    assert set(m.blueprints_do_recurso("db_main")) == {"gerar_db"}
    assert m.blueprint("nao_existe") is None


def test_yaml_vazio_nao_quebra(tmp_path: Path):
    p = tmp_path / "manifesto.yml"
    p.write_text("", encoding="utf-8")
    m = Manifest.load(str(p))
    assert m.camadas == {}
    assert m.recursos == {}
    assert m.blueprints == {}