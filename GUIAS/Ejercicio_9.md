# Ejercicio 9 · Promoción controlada entre dos planes

**Ampliación opcional del taller final.** Continúa el mismo laboratorio después del ejercicio 8. Trabajarás en tu copia personal, con los archivos y las validaciones que ya construiste.

## Tu punto de acceso

Abre esta guía en el repositorio original del curso y tu **propia copia** en otra pestaña. Las copias creadas anteriormente no reciben automáticamente las guías nuevas: no vuelvas a clonar ni pierdas tus cambios. Si trabajas en VS Code local, abre el clon que ya utilizas y comprueba con `git remote -v` que `origin` apunta a tu repositorio personal, no a `b-regina/iac-ia-laboratorio-demo`.

## Antes de empezar: qué problema resolvemos

En el caso ficticio Nexo Portal ya tienes dos planes que pasan por separado las políticas del ejercicio 8: uno para `pruebas` y otro para `integracion`. Un cambio de nombre como `portal-ensayo` en integración cumple la convención `portal-` y puede superar **ambas políticas individuales**, pero no corresponde al nombre `portal-interno` previsto para promocionar. Necesitamos comparar los dos resultados y comprobar la decisión de promoción.

**Resultado:** el workflow seguirá ejecutando `fmt`, `validate`, ambos `plan` y ambas políticas. Después ejecutará una revisión adicional que lee los dos planes JSON temporales y un criterio JSON versionado. Mostrarás un caso verde, uno rojo por nombre no aprobado y la corrección verde. Todo son fichas `terraform_data` ficticias; no se ejecuta `apply`, no se guardan estados persistentes ni se despliega infraestructura.

**Requisitos:** tu propia copia del repositorio con el ejercicio 8 terminado y su último commit verde. Navegador con GitHub.com y github.dev; IA en una segunda pestaña. No necesitas instalar nada. Si tienes VS Code local autorizado, puedes editar allí tu misma copia y seguir usando Actions.

## 1. Identifica el punto de partida

1. En GitHub.com abre **tu repositorio personal**, selecciona la rama donde terminaste el ejercicio 8 y verifica en Actions su último commit verde. No abras la plantilla inicial `main` pensando que contiene los ocho ejercicios.
2. Comprueba que existen `escenario-integracion.tfvars`, `politica_plan.py`, `modulo_ficha/` y `.github/workflows/validacion.yml`. En el `.tfvars` debe figurar `nombre_aplicacion = "portal-interno"`.
3. Crea una rama nueva **en tu repositorio** llamada `ejercicio-9-promocion` a partir de esa versión verde. Confirma el nombre de la rama antes de editar.
4. Cambia `github.com` por `github.dev` en la URL de **tu repositorio y esa rama**. Puede abrirse `vscode.dev`. Si pide permisos, revisa la cuenta. Si el editor está bloqueado, usa los iconos de edición de archivos en GitHub.com.

**Punto de control:** crear una rama de trabajo no crea otro repositorio. Tu historial de los ejercicios 1 a 8 sigue en tu copia personal.

## 2. Define el criterio de promoción

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

## 3. Diseña el revisor de planes con IA y verifica cada regla

Antes de programar, escribe una tabla de decisiones pequeña. **Caso A:** en pruebas `portal-demo` e integración `portal-interno`, ambos con sus responsables correctos: aprobar. **Caso B:** integración `portal-ensayo` y responsable correcto: rechazar **solo en la comparación**, aunque sus políticas individuales pasen. **Caso C:** falta la ficha de ayuda o cambia de nombre: rechazar. Explica por qué una política que acepta cualquier nombre `portal-` no basta para la decisión de promoción.

Crea `revision_promocion.py` en la **raíz** de tu copia. Recibirá tres argumentos en este orden: ruta del plan JSON de pruebas, ruta del plan JSON de integración y ruta de `criterio-promocion.json`. Usará únicamente `json` y `sys` de Python 3. Diseña funciones pequeñas con estos contratos:

| Función | Qué recibe | Qué debe comprobar y devolver |
| --- | --- | --- |
| `rechazar(motivo)` | Texto | Imprime `PROMOCIÓN RECHAZADA: <motivo>` y termina con código 1. |
| `leer(ruta)` | Ruta | Lee un JSON; si falta o es inválido, rechaza con una causa. |
| `extraer(plan, escenario)` | Plan JSON y nombre de escenario | Exige exactamente dos `resource_changes`, las direcciones de portal y ayuda, tipo `terraform_data`, acción `create`, `input` con `nombre`, `entorno`, `etiquetas`; devuelve las dos fichas indexadas por dirección. Rechaza claves ausentes, tipos erróneos y direcciones duplicadas. |
| `principal()` | Tres argumentos | Lee ambos planes y el criterio; exige cinco claves de texto no vacío; compara entornos, etiquetas, responsables y nombres. Imprime `PROMOCIÓN APTA: dos planes ficticios coherentes con el criterio versionado` al aprobar. |

Las direcciones de portal y ayuda son `module.fichas["portal"].terraform_data.ficha` y `module.fichas["ayuda"].terraform_data.ficha`. El criterio permite únicamente origen `pruebas` y destino `integracion`. En cada plan comprueba que `etiquetas.entorno` coincide con `input.entorno`; que `etiquetas.proyecto` no cambia entre escenarios; que el responsable de origen es `equipo-lab` y el de destino coincide con `responsable_destino`. El portal de origen y destino debe coincidir con `nombre_portal_origen` y `nombre_portal_destino`; el nombre de ayuda no debe cambiar. Comprueba `tipo`, `acción` y claves antes de acceder a campos para que el script explique el error en vez de terminar con `KeyError`.

Pide ayuda a la IA **por partes**, solo con datos ficticios:

> Quiero construir en Python 3 un revisor didáctico que compare dos planes JSON de OpenTofu, ya revisados individualmente por `politica_plan.py`. Recibe tres rutas: plan de pruebas, plan de integración y criterio JSON. Diseña primero las funciones `rechazar`, `leer` y `extraer` según esta tabla de requisitos [pega la tabla]. No escribas despliegues, proveedores ni dependencias externas. Explica cómo evitas duplicados y errores por claves ausentes. Devuélveme código solo después del pseudocódigo.

Después solicita `principal` con las comparaciones detalladas del párrafo anterior. Pide a la IA que señale qué parte **no** es una aprobación real. Revisa el código propuesto línea por línea y comprueba que el mensaje para el caso B sea exactamente `PROMOCIÓN RECHAZADA: nombre del portal de destino no aprobado`. El nombre del archivo, de los argumentos y del mensaje deben coincidir con el workflow del siguiente paso.

**Punto de control:** `revision_promocion.py` está junto a `politica_plan.py` y `criterio-promocion.json`, sin datos reales. No modifiques la política individual para convertirla en comparador. Tu revisor se ejecutará **después** de ambas políticas, como control adicional.

## 4. Conecta la revisión al workflow existente

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

## 5. Revisión crítica de la IA

En una **segunda pestaña** de Copilot o ChatGPT, pega únicamente este prompt y, si lo necesitas, fragmentos del código ficticio:

> Estoy revisando un laboratorio IaC ficticio con dos planes `terraform_data`. Las dos políticas individuales pueden aceptar `portal-ensayo` porque empieza por `portal-`, pero el criterio de promoción exige `portal-interno` en integración. Explícame la diferencia entre validar un escenario y comparar dos escenarios. Señala tres casos de error y cómo ver el primer paso rojo en GitHub Actions. No sugieras servicios cloud, credenciales, `apply`, datos empresariales reales ni afirmar que hubo un despliegue.

Anota una afirmación de la IA y el dato concreto del plan o del log con el que la comprobarás. Si la IA llama a esto “detección de drift”, corrige la explicación: **sin estado real no estamos detectando drift**; solo comparamos dos planes simulados. También verifica que el programa no declare apta una comparación si el criterio JSON está vacío o si la ficha de ayuda se duplicó.

## 6. Publica y comprueba el caso correcto

En Source Control revisa que cambian **dos archivos nuevos** (`criterio-promocion.json` y `revision_promocion.py`) y **un archivo existente** (`validacion.yml`). Guarda, confirma con `Ejercicio 9: revisar promocion entre escenarios` y haz Push/Sync. En GitHub.com abre Actions del **mismo commit**; entra en `Validacion IaC` → trabajo `comprobar`.

Debes ver formato, validación, planes, políticas y `Revisar promocion entre escenarios` verdes. En el nuevo paso busca `PROMOCIÓN APTA: dos planes ficticios coherentes con el criterio versionado`. Ambos planes siguen mostrando `Plan: 2 to add, 0 to change, 0 to destroy` porque cada ejecución parte de un runner sin estado. Copia el enlace de esta ejecución.

## 7. Provoca un rechazo controlado

En **tu misma rama**, cambia solo la segunda línea de `escenario-integracion.tfvars` a:

```hcl
nombre_aplicacion = "portal-ensayo"
```

Conserva `entorno` y `responsable`. Haz un commit `Prueba: nombre no aprobado para integracion` y Push/Sync. Predice el resultado antes de abrir Actions: `tofu validate` y ambos planes deben pasar; las dos políticas individuales también, porque `portal-ensayo` sigue la convención. El **primer paso rojo** debe ser `Revisar promocion entre escenarios` con `PROMOCIÓN RECHAZADA: nombre del portal de destino no aprobado`. El trabajo queda rojo. Copia el enlace.

Si falla antes el formato, un plan o la política individual, lee ese primer fallo y corrígelo: todavía no has probado la revisión de promoción. No cambies el criterio JSON para “hacer verde” el error; perderías la prueba de la regla acordada.

## 8. Corrige y entrega

Devuelve `nombre_aplicacion = "portal-interno"` a `escenario-integracion.tfvars`. Publica `Correccion: restaurar nombre aprobado` y verifica una **nueva** ejecución verde. En el README **de tu copia personal**, escribe en tres o cuatro frases qué comparaste, por qué la política individual aceptó el cambio erróneo, qué hizo fallar la revisión conjunta y por qué no hubo despliegue. Confirma ese README y comprueba también su ejecución.

Entrega enlaces a tu rama, tres ejecuciones (verde, roja, verde) y una explicación de la afirmación de la IA que verificaste. Si abres un pull request de tu rama hacia la rama donde terminó el 8, hazlo **dentro de tu copia personal** y revisa que el diff final ya no contiene `portal-ensayo`.

## Revisión de gobernanza y evidencia

Explica a un compañero cómo un autor podría cambiar a la vez el nombre del portal y el criterio JSON para hacer verde un caso no aprobado. Pide a la IA dos controles de producción que reduzcan ese riesgo y clasifícalos como decisiones organizativas, no como funciones de este script. No los implantes en el laboratorio. En tu entrega distingue: plan técnicamente válido, política individual aprobada, comparación apta y autorización humana real.

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
