# Ejercicio 9 · Promoción controlada entre dos planes

**Ampliación opcional del taller final · 90–120 minutos.** El temario original suma 25 horas y termina en el ejercicio 8. Este ejercicio amplía ese mismo laboratorio si queda tiempo o se programa una sesión adicional; no sustituye ni altera las 25 horas acordadas.

## Antes de empezar: qué problema resolvemos

En el caso ficticio Nexo Portal ya tienes dos planes que pasan por separado las políticas del ejercicio 8: uno para `pruebas` y otro para `integracion`. Un cambio de nombre como `portal-ensayo` en integración cumple la convención `portal-` y puede superar **ambas políticas individuales**, pero no corresponde al nombre `portal-interno` previsto para promocionar. Necesitamos comparar los dos resultados y comprobar la decisión de promoción.

**Resultado:** el workflow seguirá ejecutando `fmt`, `validate`, ambos `plan` y ambas políticas. Después ejecutará una revisión adicional que lee los dos planes JSON temporales y un criterio JSON versionado. Mostrarás un caso verde, uno rojo por nombre no aprobado y la corrección verde. Todo son fichas `terraform_data` ficticias; no se ejecuta `apply`, no se guardan estados persistentes ni se despliega infraestructura.

**Requisitos:** tu propia copia del repositorio con el ejercicio 8 terminado y su último commit verde. Navegador con GitHub.com y github.dev; IA en una segunda pestaña. No necesitas instalar nada. Si tienes VS Code local autorizado, puedes editar allí tu misma copia y seguir usando Actions.

## 1. Identifica el punto de partida · 10 minutos

1. En GitHub.com abre **tu repositorio personal**, selecciona la rama con la solución del ejercicio 8 y verifica en Actions su último commit verde. No abras la plantilla inicial `main` pensando que contiene los ocho ejercicios.
2. Comprueba que existen `escenario-integracion.tfvars`, `politica_plan.py`, `modulo_ficha/` y `.github/workflows/validacion.yml`. En el `.tfvars` debe figurar `nombre_aplicacion = "portal-interno"`.
3. Crea una rama nueva **en tu repositorio** llamada `ejercicio-9-promocion` a partir de esa versión verde. Confirma el nombre de la rama antes de editar.
4. Cambia `github.com` por `github.dev` en la URL de **tu repositorio y esa rama**. Puede abrirse `vscode.dev`. Si pide permisos, revisa la cuenta. Si el editor está bloqueado, usa los iconos de edición de archivos en GitHub.com.

**Punto de control:** crear una rama de trabajo no crea otro repositorio. La rama docente `ejercicio-9-inicio` solo sirve como referencia. Tu historial de los ejercicios 1 a 8 sigue en tu copia personal.

## 2. Define el criterio de promoción · 10 minutos

Crea en la raíz `criterio-promocion.json`. No crees una carpeta nueva. Copia exactamente:

```json
{
  "origen": "pruebas",
  "destino": "integracion",
  "nombre_portal_origen": "portal-demo",
  "nombre_portal_destino": "portal-interno",
  "responsable_destino": "equipo-integracion"
}
```

**Qué expresa:** los dos escenarios comparados, el nombre de la ficha `portal` antes y después, y el equipo que debe asumir la integración. La ficha `ayuda` mantiene el mismo nombre. Este archivo es un criterio **didáctico**, editable en tu rama: no equivale a una autorización corporativa ni a una aprobación independiente.

**Punto de control:** cinco claves y cinco valores de texto, sin comentarios ni coma después del último campo. Guarda con `Ctrl+S`.

## 3. Añade el revisor de planes · 30 minutos

Crea en la raíz `revision_promocion.py`. El programa recibe **tres rutas**: plan de origen, plan de destino y criterio. No necesita librerías externas. Copia el código completo que sigue y después recórrelo por bloques:

```python
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
```

**Lectura guiada:** `leer` informa si falta un JSON; `extraer` exige exactamente dos fichas `terraform_data` con acción `create`; `principal` comprueba entornos, etiquetas, nombres y responsable. El mensaje `PROMOCIÓN APTA` significa únicamente que estos dos **planes previstos** coinciden con el criterio versionado. No se ha producido una promoción real.

**Punto de control:** el archivo se llama `revision_promocion.py` en la raíz, al lado de `politica_plan.py`. Respeta la sangría Python. No pegues código de una cuenta corporativa ni datos sensibles en la IA.

## 4. Conecta la revisión al workflow existente · 15 minutos

Abre `.github/workflows/validacion.yml`. **No crees otro workflow.** Justo después de `Politica del plan de integracion`, añade este paso con el mismo nivel de sangría que los demás `- name`:

```yaml
      - name: Revisar promocion entre escenarios
        id: promocion
        run: |
          tofu show -json -plan=plan-predeterminado.tfplan > "$RUNNER_TEMP/plan-origen.json"
          tofu show -json -plan=plan-integracion.tfplan > "$RUNNER_TEMP/plan-destino.json"
          python3 revision_promocion.py \
            "$RUNNER_TEMP/plan-origen.json" \
            "$RUNNER_TEMP/plan-destino.json" \
            criterio-promocion.json
```

Se crean dos JSON **temporales dentro del runner**. No los subas al repositorio ni al artefacto. En el paso existente `Resumir comprobaciones`, dentro de la lista de líneas `echo "| ... |"`, añade después de `Política de integración`:

```yaml
            echo "| Revisión de promoción | ${{ steps.promocion.outcome }} |"
```

**Punto de control:** el nuevo paso se ejecuta solo si las comprobaciones anteriores llegan a él; el `Summary` registra `success`, `failure` o `skipped`. El artefacto `evidencia.txt` no contiene el plan JSON. Ni el script ni el workflow llaman a `tofu apply`.

## 5. Revisión asistida por IA · 10 minutos

En una **segunda pestaña** de Copilot o ChatGPT, pega únicamente este prompt y, si lo necesitas, fragmentos del código ficticio:

> Estoy revisando un laboratorio IaC ficticio con dos planes `terraform_data`. Las dos políticas individuales pueden aceptar `portal-ensayo` porque empieza por `portal-`, pero el criterio de promoción exige `portal-interno` en integración. Explícame la diferencia entre validar un escenario y comparar dos escenarios. Señala tres casos de error y cómo ver el primer paso rojo en GitHub Actions. No sugieras servicios cloud, credenciales, `apply`, datos empresariales reales ni afirmar que hubo un despliegue.

Anota una afirmación de la IA y el dato concreto del plan o del log con el que la comprobarás. Si la IA llama a esto “detección de drift”, corrige la explicación: **sin estado real no estamos detectando drift**; solo comparamos dos planes simulados.

## 6. Publica y comprueba el caso correcto · 10 minutos

En Source Control revisa que cambian **dos archivos nuevos** (`criterio-promocion.json` y `revision_promocion.py`) y **un archivo existente** (`validacion.yml`). Guarda, confirma con `Ejercicio 9: revisar promocion entre escenarios` y haz Push/Sync. En GitHub.com abre Actions del **mismo commit**; entra en `Validacion IaC` → trabajo `comprobar`.

Debes ver formato, validación, planes, políticas y `Revisar promocion entre escenarios` verdes. En el nuevo paso busca `PROMOCIÓN APTA: dos planes ficticios coherentes con el criterio versionado`. Ambos planes siguen mostrando `Plan: 2 to add, 0 to change, 0 to destroy` porque cada ejecución parte de un runner sin estado. Copia el enlace de esta ejecución.

## 7. Provoca un rechazo controlado · 10 minutos

En **tu misma rama**, cambia solo la segunda línea de `escenario-integracion.tfvars` a:

```hcl
nombre_aplicacion = "portal-ensayo"
```

Conserva `entorno` y `responsable`. Haz un commit `Prueba: nombre no aprobado para integracion` y Push/Sync. Predice el resultado antes de abrir Actions: `tofu validate` y ambos planes deben pasar; las dos políticas individuales también, porque `portal-ensayo` sigue la convención. El **primer paso rojo** debe ser `Revisar promocion entre escenarios` con `PROMOCIÓN RECHAZADA: nombre del portal de destino no aprobado`. El trabajo queda rojo. Copia el enlace.

Si falla antes el formato, un plan o la política individual, lee ese primer fallo y corrígelo: todavía no has probado la revisión de promoción. No cambies el criterio JSON para “hacer verde” el error; perderías la prueba de la regla acordada.

## 8. Corrige y entrega · 10 minutos

Devuelve `nombre_aplicacion = "portal-interno"` a `escenario-integracion.tfvars`. Publica `Correccion: restaurar nombre aprobado` y verifica una **nueva** ejecución verde. En el README **de tu copia personal**, escribe en tres o cuatro frases qué comparaste, por qué la política individual aceptó el cambio erróneo, qué hizo fallar la revisión conjunta y por qué no hubo despliegue. Confirma ese README y comprueba también su ejecución.

Entrega enlaces a tu rama, tres ejecuciones (verde, roja, verde) y una explicación de la afirmación de la IA que verificaste. Si abres un pull request de tu rama hacia la rama donde terminó el 8, hazlo **dentro de tu copia personal** y revisa que el diff final ya no contiene `portal-ensayo`.

## Incidencias y límites

| Observas | Revisa |
| --- | --- |
| No aparece la ejecución | Comprueba Push/Sync, rama y SHA del commit. |
| JSON inválido | Revisa comas, comillas dobles y las cinco claves de `criterio-promocion.json`. |
| `No such file` | Nombres exactos de los archivos y ubicación en la raíz. |
| `IndentationError` | Sangría de `revision_promocion.py`; no pegues tabuladores mezclados. |
| `PROMOCIÓN RECHAZADA` en el caso correcto | Compara nombre y responsable del plan de integración con el criterio JSON. |
| Paso de promoción `skipped` | Lee el primer paso rojo anterior; un paso omitido no demuestra el control. |
| VS Code Web no permite editar | Usa el lápiz de GitHub.com o VS Code local autorizado; Actions ejecuta OpenTofu igualmente. |

**Límites:** el criterio y el script son modificables en la misma rama. En un entorno real harían falta revisión humana independiente, protección de ramas, permisos, estado protegido, secretos, control de costes y un procedimiento de reversión. El éxito de este ejercicio solo acredita la comparación didáctica de dos planes ficticios, no una aprobación formal, detección de drift ni promoción de recursos.

**Preguntas de cierre:** ¿por qué pasaron ambas políticas individuales en el caso rojo? ¿Qué valor de integración esperaba el criterio? ¿Qué paso ofrece la primera evidencia del fallo? ¿Qué se tendría que proteger para que un autor no pudiera cambiar simultáneamente el código y el criterio? ¿Por qué `Plan: 2 to add` no implica dos despliegues?
