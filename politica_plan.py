"""Política didáctica para el plan ficticio leído desde la entrada estándar."""

import json
import sys


ESPERADOS = {
    "module.portal.terraform_data.ficha",
    "module.ayuda.terraform_data.ficha",
}
ENTORNOS = {"desarrollo", "pruebas", "integracion"}


def rechazar(motivo):
    print(f"POLÍTICA RECHAZADA: {motivo}")
    raise SystemExit(1)


try:
    plan = json.load(sys.stdin)
except (ValueError, UnicodeError):
    rechazar("no se pudo leer el plan JSON")

cambios = plan.get("resource_changes")
if not isinstance(cambios, list):
    rechazar("el plan no contiene una lista de cambios")

direcciones = [c.get("address") for c in cambios if isinstance(c, dict)]
if len(cambios) != 2 or set(direcciones) != ESPERADOS:
    rechazar("se esperan exactamente las fichas portal y ayuda")

valores = {}
for cambio in cambios:
    direccion = cambio["address"]
    if cambio.get("mode") != "managed" or cambio.get("type") != "terraform_data":
        rechazar(f"tipo de recurso no permitido en {direccion}")

    detalle = cambio.get("change", {})
    if detalle.get("actions") != ["create"]:
        rechazar(f"solo se permiten altas ficticias en {direccion}")
    if detalle.get("after_unknown", {}).get("input"):
        rechazar(f"entradas desconocidas en {direccion}")
    if detalle.get("after_sensitive", {}).get("input"):
        rechazar(f"entradas sensibles en {direccion}")

    entrada = detalle.get("after", {}).get("input")
    if not isinstance(entrada, dict) or set(entrada) != {"nombre", "entorno"}:
        rechazar(f"entradas inesperadas en {direccion}")

    nombre, entorno = entrada["nombre"], entrada["entorno"]
    if not isinstance(nombre, str) or not nombre.startswith("portal-"):
        rechazar(f"nombre fuera de la convención en {direccion}")
    if not isinstance(entorno, str) or entorno not in ENTORNOS:
        rechazar(f"entorno no permitido en {direccion}")
    valores[direccion] = entrada

if valores["module.ayuda.terraform_data.ficha"]["nombre"] != "portal-ayuda":
    rechazar("la ficha de ayuda debe llamarse portal-ayuda")
if len({entrada["entorno"] for entrada in valores.values()}) != 1:
    rechazar("portal y ayuda deben pertenecer al mismo entorno")

print("POLÍTICA APROBADA: dos fichas ficticias, mismo entorno y sin operaciones reales")
