import yaml
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List


@dataclass
class Manifest:
    data: dict

    # =========================
    # Construtor único (somente path)
    # =========================
    @classmethod
    def load(cls, path: str) -> "Manifest":
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
        return cls(data=data)

    # =========================
    # Acessos básicos
    # =========================
    @property
    def camadas(self) -> dict:
        return self.data.get("camadas", {}) or {}

    @property
    def recursos(self) -> dict:
        return self.data.get("recursos", {}) or {}

    @property
    def blueprints(self) -> dict:
        return self.data.get("blueprints", {}) or {}

    # =========================
    # Helpers Camadas
    # =========================
    def tecnologia_da_camada(self, nome: str) -> Optional[str]:
        camada = self.camadas.get(nome)
        if not camada:
            return None
        tech = camada.get("tecnologia")
        return tech.strip().lower() if isinstance(tech, str) else None

    def camadas_por_tecnologia(self, tech: str) -> List[str]:
        t = tech.strip().lower()
        return [
            nome
            for nome in self.camadas
            if self.tecnologia_da_camada(nome) == t
        ]

    # =========================
    # Helpers Recursos
    # =========================
    def recurso(self, nome: str) -> Optional[dict]:
        return self.recursos.get(nome)

    def recursos_por_tipo(self, tipo: str) -> List[str]:
        return [
            nome
            for nome, dados in self.recursos.items()
            if dados.get("tipo") == tipo
        ]

    # =========================
    # Helpers Blueprints
    # =========================
    def blueprint(self, nome: str) -> Optional[dict]:
        return self.blueprints.get(nome)

    def blueprints_do_recurso(self, recurso_nome: str) -> List[str]:
        return [
            nome
            for nome, dados in self.blueprints.items()
            if dados.get("recurso") == recurso_nome
        ]


# =========================
# Uso
# =========================

manifest = Manifest.load("manifesto.yml")

print("Camadas:")
print(manifest.camadas)

print("\nRecursos:")
print(manifest.recursos)

print("\nBlueprints:")
print(manifest.blueprints)

print("\nRecursos do tipo 'api':")
print(manifest.recursos_por_tipo("api"))

print("\nBlueprints do recurso api_users:")
print(manifest.blueprints_do_recurso("api_users"))