# Ejercicio 6  Una política automática para revisar el plan

**Tiempo orientativo:** 110 a 140 minutos. **Punto de partida:** tu propia copia del laboratorio con el ejercicio 5 terminado. **Ruta principal:** navegador, github.dev y GitHub Actions. La IA se consulta en otra pestaña si está disponible. No se instalan aplicaciones, no se usan servicios cloud ni se ejecuta `tofu apply`.

## Qué vas a aprender y por qué

El equipo ficticio Nexo Portal ya ha creado un módulo reutilizable para el portal y la ficha de ayuda. Una persona revisora pide una comprobación más: **antes de aceptar un plan, ambas fichas deben estar en el mismo entorno**. También deben ser exactamente dos, usar solo `terraform_data` y respetar los nombres del laboratorio.

En el ejercicio 3 añadiste validaciones de variables; en el 4 aprendiste a leer el pipeline; en el 5 reutilizaste el módulo. Ahora escribirás una **política didáctica** que lee el plan que produce OpenTofu y rechaza cambios que el formato y la sintaxis no detectan. Seguirás en el mismo proyecto; solo añadirás `politica_plan.py` a la raíz y ampliarás el workflow existente.

**Resultado observable:** una ejecución verde con dos planes aprobados, otra roja en la que `tofu validate` y `tofu plan` pasan pero la política detecta entornos distintos, y una tercera verde tras corregir el cambio. Conservarás los tres enlaces y explicarás el motivo del fallo. Esta práctica profundiza en estandarización, controles previos y gobierno del temario.

| Comprobación | Pregunta que responde |
| --- | --- |
| `tofu fmt -check -diff -recursive` | ¿Está formateado el código de la raíz y del módulo? |
| `tofu validate` | ¿Es coherente la configuración de OpenTofu? |
| `tofu plan` | ¿Qué cambios calcula OpenTofu para este escenario? |
| `politica_plan.py` | ¿Cumple ese plan las reglas del laboratorio? |

Una validación verde no equivale por sí sola a una aprobación de gobierno. La política mira los **valores previstos** del plan, no solo si el archivo HCL se puede leer.

## Antes de escribir  abre tu copia y predice el resultado

1. Abre `https://github.com/TU_USUARIO/TU_COPIA` e inicia sesión. Debes ver el `modulo_ficha` del ejercicio 5, el `main.tf` con `module "portal"` y `module "ayuda"`, los dos escenarios y el resumen de Actions del ejercicio 4. No trabajes en el repositorio de la docente.
2. Desde la rama que contiene tu ejercicio 5, crea `politica-ejercicio-6`. Si el ejercicio 5 ya quedó integrado en tu `main`, selecciona `main` antes de crearla. Conserva los cinco ejercicios anteriores en esta nueva rama.
3. Cambia `github.com` por `github.dev` en la URL de **tu copia y de esa rama**. Puede abrirse `vscode.dev`. Comprueba el nombre de la rama en la esquina inferior. Abre una segunda pestaña con Copilot Chat en GitHub.com o ChatGPT, solo si tu organización lo permite.
4. Lee `main.tf` y predice los valores de ambos planes. Con la configuración correcta, el portal y la ayuda están en `pruebas` por defecto y en `integracion` en el segundo escenario. No modifiques aún el módulo.

**Mapa mínimo:** `main.tf` y `modulo_ficha/` siguen igual; `politica_plan.py` será el único archivo nuevo. Se edita `.github/workflows/validacion.yml` y, al final, se añade una explicación breve al `README.md`. Los archivos `.tfplan` existirán solo durante la ejecución del runner y ya están excluidos por `.gitignore`.

## Paso 1  Define la regla antes de codificarla

Escribe en dos frases qué debería aprobar la política. La respuesta esperada es: exactamente `module.portal.terraform_data.ficha` y `module.ayuda.terraform_data.ficha`; ambas son altas ficticias, usan nombres que empiezan por `portal-`, la ayuda se llama `portal-ayuda` y sus entornos son iguales y pertenecen al conjunto `desarrollo`, `pruebas`, `integracion`.

El plan se guardará temporalmente con `tofu plan -out=...`. `tofu show -json -plan=...` lo convertirá en JSON para leer las propiedades `resource_changes`, `address`, `change.actions` y `change.after.input`. La política devuelve **código 0** cuando aprueba y **código 1** cuando rechaza; GitHub Actions utiliza ese resultado para marcar el paso verde o rojo. No hay que aprender todo el formato JSON: en esta práctica solo usamos esas claves.

## Paso 2  Crea el archivo de política

En el Explorador de github.dev, selecciona la **raíz del repositorio**, pulsa **New File** y escribe exactamente `politica_plan.py`. No lo crees dentro de `modulo_ficha` ni de `.github`. Copia el código siguiente y guarda con `Ctrl+S`:

```python
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
```

**Qué hace cada bloque:** las constantes definen qué se permite; `json.load` recibe la representación del plan; `resource_changes` contiene los recursos previstos; el bucle revisa cada tipo, acción y entrada; la última condición compara los dos entornos. La función `rechazar` explica el motivo y hace fallar el paso. Si falta la lista de cambios o aparecen entradas desconocidas, la política también rechaza el plan.

**Punto de control:** comprueba la indentación de Python. Las líneas dentro de `if`, `try`, `except`, `for` y `def` llevan cuatro espacios. No cambies `main.tf` todavía.

## Paso 3  Amplía el workflow existente

Abre `.github/workflows/validacion.yml`. No crees otro workflow. Haz estos cambios concretos:

1. Bajo `tofu_version: 1.13.9`, añade al mismo nivel `tofu_wrapper: false`. Esto deja la salida JSON del comando disponible tal como la espera Python.
2. Sustituye las dos líneas `run: tofu plan ...` de los pasos existentes por las que siguen. Conserva sus nombres e identificadores `id`:

```yaml
        run: tofu plan -input=false -no-color -out=plan-predeterminado.tfplan
```

```yaml
        run: >-
          tofu plan -input=false -no-color
          -var-file=escenario-integracion.tfvars
          -out=plan-integracion.tfplan
```

En YAML, `>-` une esas tres líneas en un único comando para el runner. Respeta los espacios de indentación: `run` queda bajo el paso y las tres líneas del comando quedan más adentro.

3. **Inmediatamente después** del plan predeterminado, añade este paso nuevo, con la misma indentación que las demás líneas `- name:`:

```yaml
      - name: Politica del plan predeterminado
        id: politica_predeterminado
        run: tofu show -json -plan=plan-predeterminado.tfplan | python3 politica_plan.py
```

4. **Inmediatamente después** del plan de integración, añade este paso:

```yaml
      - name: Politica del plan de integracion
        id: politica_integracion
        run: tofu show -json -plan=plan-integracion.tfplan | python3 politica_plan.py
```

5. En el bloque **Resumir comprobaciones**, añade una fila detrás de cada plan para que el resumen indique también el resultado de la política:

```yaml
            echo "| Política predeterminada | ${{ steps.politica_predeterminado.outcome }} |"
            echo "| Política de integración | ${{ steps.politica_integracion.outcome }} |"
```

Coloca cada línea de `echo` tras el plan que le corresponde. Conserva `if: ${{ always() }}` en el resumen y la publicación de `evidencia.txt`. No añadas `apply`, tokens ni secretos. El workflow completo resuelto está en la rama docente; usa esta guía para construir el tuyo, no para sustituir el ejercicio por una copia de la solución.

**Punto de control:** ahora hay **dos pasos de plan y dos de política**. El primer archivo se llama `plan-predeterminado.tfplan` en sus dos referencias; el segundo, `plan-integracion.tfplan`. Estos archivos se crean en el runner y no se adjuntan como artefactos. `evidencia.txt` contiene solo el resumen.

## Paso 4  Revisa con IA sin entregar datos sensibles

En la segunda pestaña escribe este prompt, usando solo los fragmentos ficticios del laboratorio:

> Revisa esta política didáctica de OpenTofu. El plan JSON llega por entrada estándar después de `tofu show -json -plan=...`. Debo permitir solo dos recursos `terraform_data` llamados `module.portal.terraform_data.ficha` y `module.ayuda.terraform_data.ficha`, ambos en el mismo entorno, con nombres `portal-`; la ayuda debe llamarse `portal-ayuda`. Explica en lenguaje sencillo cómo `resource_changes`, `change.actions` y `change.after.input` sostienen esas reglas. Predice qué pasará si la ayuda usa `desarrollo` y el portal usa `pruebas`. Señala un límite de esta política como control de producción. No propongas desplegar ni usar proveedores cloud.

Contrasta la respuesta con el código y luego con Actions. No pegues planes JSON de un entorno real en una IA: podrían contener valores sensibles. En este laboratorio solo hay datos inventados.

## Paso 5  Confirma y verifica la ejecución verde

1. En **Source Control**, comprueba que aparece el archivo nuevo y el workflow modificado. Escribe `Ejercicio 6: política sobre el plan` y usa **Commit & Push**. Si tu editor presenta Commit y Sync por separado, completa los dos. Comprueba que GitHub.com muestra el commit en `politica-ejercicio-6`.
2. En **Actions** de tu copia, abre **Validacion IaC** para ese commit y el trabajo **comprobar**. Espera a que termine. Deben pasar formato, validación, plan predeterminado, política predeterminada, plan de integración y política de integración.
3. Abre cada política y busca `POLÍTICA APROBADA: dos fichas ficticias, mismo entorno y sin operaciones reales`. En los planes busca `Plan: 2 to add, 0 to change, 0 to destroy` y los nombres y entornos del ejercicio 5.
4. Comprueba el resumen de seis resultados. Guarda el enlace de la ejecución verde. El artefacto `evidencia-iac-...` sigue siendo un archivo de texto de resumen con retención de siete días, no el plan JSON.

**Interpretación:** el runner instala OpenTofu y dispone de Python; no has instalado ninguna de las dos herramientas en tu equipo. El archivo `.tfplan` guarda el plan solo en ese runner temporal. `tofu show -json` puede mostrar datos sensibles en proyectos reales, por lo que aquí se utiliza exclusivamente información inventada y no se publica el JSON.

## Paso 6  Introduce un error de gobierno que sí valida

En **tu rama de ejercicio**, abre el `main.tf` de la raíz y localiza `module "ayuda"`. Cambia solamente `entorno = var.entorno` por `entorno = "desarrollo"`. Antes del commit, predice: ¿pasará `tofu validate`?, ¿mostrará un plan de dos fichas?, ¿aprobará la política del escenario predeterminado? Confirma con `Prueba: ayuda en entorno diferente` y abre su nueva ejecución de Actions.

Debes observar **formato verde, validación verde, plan predeterminado verde y política predeterminada roja**. Su mensaje es `POLÍTICA RECHAZADA: portal y ayuda deben pertenecer al mismo entorno`. Como los pasos están en serie, el plan de integración y su política quedarán omitidos. El resumen y la publicación de la evidencia pueden quedar verdes gracias a `always()`, pero el **trabajo completo es rojo**.

Si el primer fallo ocurre en formato o en Python por un error de copia, localiza ese paso y corrígelo antes de evaluar la regla. No afirmes que probaste una política si el código ni siquiera llegó al plan.

## Paso 7  Corrige y entrega el cambio revisado

1. Restituye `entorno = var.entorno` en `module "ayuda"`, guarda y publica `Corrección: ayuda comparte entorno`. Abre **la nueva ejecución** y comprueba que ambos planes y ambas políticas vuelven a verde. Guarda el enlace rojo y el de corrección.
2. Añade al `README.md` de tu copia una sección `## Política del laboratorio`. Explica con tus palabras qué se permite, por qué validación y política responden a preguntas distintas, dónde se ven los resultados y por qué este ejemplo no despliega infraestructura ni demuestra gobierno de producción. Confirma el README.
3. Abre un **Pull request en tu propia copia**. Usa como base la rama que contiene el ejercicio 5, o tu `main` si ya lo fusionaste, y como compare `politica-ejercicio-6`. Revisa **Files changed** y deja el PR en borrador si esperas comentarios de la docente.
4. En la descripción del PR incluye los tres enlaces de Actions, tu predicción antes del fallo, el mensaje exacto de rechazo, una observación contrastada de la IA y una limitación de la política. No enlaces el PR al repositorio de la docente.

## Si algo falla  usa este diagnóstico

| Síntoma | Qué mirar |
| --- | --- |
| `No such file` para `.tfplan` | El plan anterior no se completó o el nombre del archivo no coincide entre `-out` y `-plan`. |
| `no se pudo leer el plan JSON` | Revisa `tofu_wrapper: false`, `tofu show -json -plan=...` y que el plan previo terminó en verde. |
| Error YAML o el workflow no arranca | Revisa que cada `- name` esté dentro de `steps` con la misma indentación y que las expresiones `${{ ... }}` permanezcan intactas. |
| Error `IndentationError` en Python | Compara espacios y bloques del archivo con la guía. |
| Política rechazada en el primer commit | Comprueba que `main.tf` aún usa `var.entorno` en ambos módulos; mira el mensaje específico de rechazo. |
| Plans verdes y trabajo rojo | Abre las etapas de política; un plan calculable puede incumplir una regla. |
| No puedes abrir github.dev | Edita los archivos desde GitHub.com, con el lápiz y **Commit changes**, si tu política de acceso lo permite. |
| Actions está bloqueado en tu organización | Usa la demostración docente y registra la ejecución individual como pendiente. |

## Plan B  VS Code instalado en tu equipo

Si tu equipo ya tiene VS Code y Git, o permite instalarlos, abre **la misma copia** del repositorio localmente y crea `politica-ejercicio-6` desde tu rama del ejercicio 5. Edita `politica_plan.py` y el mismo workflow, confirma y publica la rama. No hace falta OpenTofu o Python local: GitHub Actions ejecuta ambas herramientas. Si ya tienes esas herramientas autorizadas, puedes probar los comandos localmente para aprender, pero la evidencia de entrega sigue siendo la ejecución en Actions y el PR de tu copia. Si el equipo corporativo no permite ni la web ni instalaciones, la docente podrá mostrar las ejecuciones comprobadas y anotará la limitación; no se atribuye al alumno una prueba que no ejecutó.

## Preguntas finales y reto

1. ¿Qué comprobación admite el cambio a `"desarrollo"` en la ayuda y cuál lo rechaza? ¿Por qué?
2. ¿Qué representa `resource_changes` y por qué la política exige exactamente dos direcciones?
3. ¿Qué ocurre con los pasos posteriores cuando la primera política falla? ¿Por qué el resumen puede seguir apareciendo?
4. ¿Qué archivos efímeros produce `-out` y por qué no se publican ni se comparten con una IA?
5. ¿Por qué una política editable en la misma rama necesita revisión humana y permisos más estrictos antes de convertirse en control real?

**Reto autónomo:** en otra rama de tu copia cambia solo el nombre de la ficha de ayuda a `portal-asistencia`. Mantén el resto correcto. Predice si las validaciones y el plan pasarán y qué texto dará la política. Compruébalo, registra el enlace del fallo y vuelve a la configuración correcta. Usa solo datos ficticios.

**Límite profesional:** esta política es didáctica. En producción harían falta reglas protegidas, aprobaciones independientes, cobertura de más recursos, secretos, costes y permisos. Un plan aprobado aquí no autoriza un despliegue real.
