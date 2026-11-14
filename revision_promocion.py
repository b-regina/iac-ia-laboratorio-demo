"""Compara dos planes ficticios con un criterio versionado de promoción."""

import json
import sys


PORTAL = 'module.fichas["portal"].terraform_data.ficha'
AYUDA = 'module.fichas["ayuda"].terraform_data.ficha'
CLAVES_CRITERIO = {
    "origen", "destino", "nombre_portal_origen",
    "nombre_portal_destino", "responsable_destino",
}


def rechazar(motivo):
    print(f"PROMOCIÓN RECHAZADA: {motivo}")
    raise SystemExit(1)


def leer(ruta):
    try:
        with open(ruta, encoding="utf-8") as archivo:
            return json.load(archivo)
    except (OSError, ValueError, UnicodeError):
        rechazar(f"no se pudo leer JSON: {ruta}")


def extraer(plan, escenario):
    cambios = plan.get("resource_changes") if isinstance(plan, dict) else None
    if not isinstance(cambios, list) or len(cambios) != 2:
        rechazar(f"{escenario}: se esperan dos fichas en el plan")
    fichas = {}
    for cambio in cambios:
        if not isinstance(cambio, dict) or cambio.get("address") not in {PORTAL, AYUDA}:
            rechazar(f"{escenario}: dirección no admitida")
        if cambio.get("type") != "terraform_data":
            rechazar(f"{escenario}: tipo no admitido")
        detalle = cambio.get("change")
        if not isinstance(detalle, dict) or detalle.get("actions") != ["create"]:
            rechazar(f"{escenario}: solo se admiten altas ficticias")
        despues = detalle.get("after")
        entrada = despues.get("input") if isinstance(despues, dict) else None
        if not isinstance(entrada, dict) or set(entrada) != {"nombre", "entorno", "etiquetas"}:
            rechazar(f"{escenario}: entrada incompleta")
        etiquetas = entrada["etiquetas"]
        if not isinstance(etiquetas, dict) or set(etiquetas) != {"proyecto", "entorno", "responsable"}:
            rechazar(f"{escenario}: etiquetas incompletas")
        if not all(isinstance(valor, str) for valor in (entrada["nombre"], entrada["entorno"], *etiquetas.values())):
            rechazar(f"{escenario}: valores no textuales")
        fichas[cambio["address"]] = entrada
    if set(fichas) != {PORTAL, AYUDA}:
        rechazar(f"{escenario}: fichas duplicadas o ausentes")
    return fichas


def principal():
    if len(sys.argv) != 4:
        rechazar("uso: revision_promocion.py PLAN_ORIGEN PLAN_DESTINO CRITERIO")
    origen = extraer(leer(sys.argv[1]), "origen")
    destino = extraer(leer(sys.argv[2]), "destino")
    criterio = leer(sys.argv[3])
    if not isinstance(criterio, dict) or set(criterio) != CLAVES_CRITERIO:
        rechazar("el criterio debe declarar exactamente sus cinco campos")
    if not all(isinstance(valor, str) and valor for valor in criterio.values()):
        rechazar("el criterio solo admite textos no vacíos")
    if (criterio["origen"], criterio["destino"]) != ("pruebas", "integracion"):
        rechazar("solo se revisa pruebas → integracion")

    for clave in (PORTAL, AYUDA):
        a, b = origen[clave], destino[clave]
        if a["entorno"] != criterio["origen"] or b["entorno"] != criterio["destino"]:
            rechazar(f"entorno incorrecto en {clave}")
        if a["etiquetas"]["entorno"] != a["entorno"] or b["etiquetas"]["entorno"] != b["entorno"]:
            rechazar(f"etiqueta de entorno incoherente en {clave}")
        if a["etiquetas"]["proyecto"] != b["etiquetas"]["proyecto"]:
            rechazar(f"el proyecto cambió en {clave}")
        if a["etiquetas"]["responsable"] != "equipo-lab":
            rechazar(f"responsable de origen incorrecto en {clave}")
        if b["etiquetas"]["responsable"] != criterio["responsable_destino"]:
            rechazar(f"responsable de destino no aprobado en {clave}")

    if origen[PORTAL]["nombre"] != criterio["nombre_portal_origen"]:
        rechazar("nombre del portal de origen no aprobado")
    if destino[PORTAL]["nombre"] != criterio["nombre_portal_destino"]:
        rechazar("nombre del portal de destino no aprobado")
    if origen[AYUDA]["nombre"] != destino[AYUDA]["nombre"]:
        rechazar("la ficha de ayuda cambió entre entornos")
    print("PROMOCIÓN APTA: dos planes ficticios coherentes con el criterio versionado")


if __name__ == "__main__":
    principal()
