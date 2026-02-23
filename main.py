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
    # Geração de ENV
    # =========================
    def gerar_env_tecnologias(self, output_path: str) -> None:
        linhas = []

        for nome, dados in self.camadas.items():
            tech = dados.get("tecnologia")
            if isinstance(tech, str):
                tech = tech.strip().lower()
                chave = f"{nome.upper()}_TECNOLOGIA"
                linhas.append(f"{chave}={tech}")

        conteudo = "\n".join(linhas) + "\n"

        Path(output_path).write_text(conteudo, encoding="utf-8")

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

manifest.gerar_env_tecnologias(".env")


print("\nBlueprints do recurso api_users:")
print(manifest.blueprints_do_recurso("api_users"))


import typer

app = typer.Typer()

manifest: Manifest | None = None


@app.callback()
def main(manifest_path: str = typer.Option("manifesto.yml")):
    global manifest
    manifest = Manifest.load(manifest_path)


@app.command()
def listar_camadas():
    print(manifest.camadas)


@app.command()
def listar_recursos():
    print(manifest.recursos)


if __name__ == "__main__":
    app()