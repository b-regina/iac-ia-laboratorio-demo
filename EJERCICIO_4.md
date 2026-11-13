# Ejercicio 4. Una automatización que explica sus resultados

## La historia y la finalidad

El equipo ficticio de `portal-demo` ya escribe su configuración IaC, usa variables para dos escenarios y revisa los cambios antes de incorporarlos. Ahora una compañera pregunta: «Si el pipeline falla, ¿dónde veo qué comprobación falló y cómo guardo la evidencia?». Vas a mejorar **el mismo workflow** de tu copia personal para que muestre una tabla de resultados y adjunte un archivo de texto descargable. Después provocarás un fallo controlado y comprobarás que el resumen ayuda a encontrarlo.

**Objetivo técnico:** comprender un archivo YAML de GitHub Actions, relacionar cada paso con su resultado y registrar evidencias tanto en ejecuciones correctas como incorrectas. **Resultado esperado:** una ejecución verde, una roja y otra verde, todas con resumen y artefacto `evidencia.txt`.

**Duración orientativa:** 100 a 120 minutos. **Punto de partida:** tu **misma copia personal**, con los ejercicios 1, 2 y 3 terminados y las dos validaciones del ejercicio 3 incorporadas en `main`. No crees otro repositorio. El trabajo es público y usa únicamente nombres y datos ficticios. La [plantilla docente](https://github.com/b-regina/iac-ia-laboratorio-demo) es solo una referencia: **todos tus commits van a tu copia**.

No necesitas instalar software. Trabaja con GitHub.com y github.dev en el navegador, y usa la IA en una segunda pestaña. Si tienes VS Code local autorizado, la ruta alternativa está al final. No añadas secretos, datos corporativos, proveedores cloud ni `tofu apply`.

## Mapa rápido: ¿qué parte hace qué?

| Elemento del archivo `.github/workflows/validacion.yml` | Significado en esta práctica |
| --- | --- |
| `on: push`, `pull_request`, `workflow_dispatch` | Cuándo se inicia: al publicar un commit, al abrir/actualizar una propuesta o manualmente desde GitHub. |
| `permissions: contents: read` | Permiso de lectura del código para el trabajo; no autoriza escribir en el repositorio. |
| `jobs: comprobar` y `runs-on: ubuntu-latest` | Un trabajo que usa temporalmente un ejecutor de GitHub. |
| `steps`, `uses` y `run` | Pasos ordenados: una acción reutilizable o un comando ejecutado en el runner. |
| `id` y `steps.<id>.outcome` | Un nombre interno para consultar si un paso acabó en `success`, `failure` o `skipped`. |
| `if: ${{ always() }}` | Permite intentar el resumen y la publicación del archivo incluso después de un fallo previo. |
| `$GITHUB_STEP_SUMMARY` | Archivo especial: lo escrito en él aparece en el resumen de la ejecución de Actions. |
| `evidencia.txt` | Archivo de texto **generado durante la ejecución**, no una carpeta nueva del proyecto. |

**Punto de control inicial:** abre tu copia en GitHub.com y entra en `.github/workflows/validacion.yml`. Localiza las dos líneas `tofu plan`: una usa los valores predeterminados y otra lee `escenario-integracion.tfvars`. Comprueba en `variables.tf` que las reglas del ejercicio 3 siguen presentes. Explica con una frase por qué se consulta un plan antes de cualquier despliegue. Aquí **solo se planifica**: no existe un paso de aplicación.

## Paso 1. Abre una rama de trabajo

1. En GitHub.com, entra en **tu repositorio personal**, no en la plantilla de `b-regina`. Elige `main` en el selector de ramas, escribe `automatizacion-ejercicio-4` y usa **Create branch**. Según la interfaz, quizá debas abrir **View all branches → New branch**.
2. Abre la URL de **esa rama** y cambia `github.com` por `github.dev` en la barra del navegador. Puede abrirse en `vscode.dev`. En el borde inferior comprueba que la rama es `automatizacion-ejercicio-4`.
3. En el explorador de archivos despliega `.github`, después `workflows`, y abre `validacion.yml`. Si no ves `.github`, comprueba que estás en la raíz del repositorio y no en otra carpeta. El archivo empieza por `name: Validacion IaC`.

**Por qué una rama:** el error de prueba quedará aislado y no romperá la rama principal de tu proyecto. El resultado final se revisará con un pull request, igual que en el ejercicio 3.

## Paso 2. Da un identificador a las cuatro comprobaciones

En el workflow localiza los siguientes pasos y añade **solo la línea `id:`** inmediatamente debajo de cada `name:`. Conserva las líneas `run:` y los dos espacios adicionales de sangría que ya tienen los campos del paso:

```yaml
      - name: Comprobar formato
        id: formato
        run: tofu fmt -check -diff
      - name: Validar
        id: validar
        run: tofu validate -no-color
      - name: Plan con valores por defecto
        id: plan_predeterminado
        run: tofu plan -input=false -no-color
      - name: Plan del escenario integracion
        id: plan_integracion
        run: tofu plan -input=false -no-color -var-file=escenario-integracion.tfvars
```

`name` es el título visible del paso; `id` es su nombre interno, sin espacios, para leer el resultado más adelante. Los pasos **Obtener codigo**, **Instalar OpenTofu** e **Inicializar** se conservan. Tampoco cambies `on`, `permissions` ni `runs-on`.

## Paso 3. Añade el resumen y el archivo de evidencia

Al final de la lista `steps:`, justo **después** del paso `Plan del escenario integracion`, pega este bloque completo. Copia también sus sangrías: cada `- name:` empieza a la misma altura que los pasos anteriores.

```yaml
      - name: Resumir comprobaciones
        if: ${{ always() }}
        run: |
          {
            echo "## Resultados del laboratorio"
            echo ""
            echo "Commit analizado: $GITHUB_SHA"
            echo ""
            echo "| Comprobación | Resultado |"
            echo "| --- | --- |"
            echo "| Formato | ${{ steps.formato.outcome }} |"
            echo "| Validación | ${{ steps.validar.outcome }} |"
            echo "| Plan predeterminado | ${{ steps.plan_predeterminado.outcome }} |"
            echo "| Plan de integración | ${{ steps.plan_integracion.outcome }} |"
          } | tee evidencia.txt >> "$GITHUB_STEP_SUMMARY"
      - name: Publicar evidencia
        if: ${{ always() }}
        uses: actions/upload-artifact@v7
        with:
          name: evidencia-iac-${{ github.run_id }}-${{ github.run_attempt }}
          path: evidencia.txt
          if-no-files-found: error
          retention-days: 7
```

El signo `|` detrás de `run:` indica que siguen varias líneas de comandos. Las llaves `{ ... }` agrupan los `echo`. `tee` escribe **la misma información** en `evidencia.txt` y en el resumen de GitHub. `upload-artifact` adjunta el archivo a esta ejecución; el nombre incluye el número de ejecución e intento para evitar confusiones. La retención es de **7 días**: guarda el enlace a la ejecución para la entrega; si necesitas conservar el archivo más tiempo, descárgalo dentro de ese plazo. No subas el plan completo ni información sensible como artefacto.

**Comprueba antes del commit:** el archivo sigue teniendo un solo `jobs:`, un solo trabajo `comprobar`, los pasos antiguos y los dos pasos nuevos. `if:` debe estar alineado con `run:` o `uses:` dentro de cada paso. `path: evidencia.txt` coincide exactamente con el archivo creado por `tee`.

Guarda con `Ctrl+S`. En **Source Control** revisa el cambio: debería verse **solo** `.github/workflows/validacion.yml`. Escribe `Ejercicio 4: resumir y conservar evidencias` y confirma con **Commit & Push**; si aparecen dos botones separados, haz primero **Commit** y después **Push/Sync**.

## Paso 4. Lee una ejecución correcta

1. Vuelve a GitHub.com en **tu copia**. Entra en **Actions → Validacion IaC**. Abre la ejecución vinculada al commit anterior; puede tardar unos segundos en aparecer.
2. Abre el trabajo **comprobar**. Comprueba que **Comprobar formato**, **Validar**, **Plan con valores por defecto**, **Plan del escenario integracion**, **Resumir comprobaciones** y **Publicar evidencia** están en verde. `tofu init` e instalación también deben haber terminado correctamente.
3. Regresa a la página de esa ejecución. Busca el recuadro **Resultados del laboratorio** con cuatro `success`. Debajo, en **Artifacts**, debe aparecer `evidencia-iac-...`. Descárgalo y abre `evidencia.txt`: el commit y los cuatro estados deben coincidir con el resumen. Si el navegador descarga un ZIP, abre el archivo de texto que contiene.
4. Copia el enlace de la ejecución verde. El archivo `evidencia.txt` **no** debe aparecer entre los archivos del repositorio: se generó en el runner temporal y se conserva asociado a esa ejecución.

**Qué has demostrado:** el pipeline realiza comprobaciones automáticas y deja una evidencia legible. Un resultado verde significa que pasaron **esas comprobaciones concretas**; no representa aprobación para desplegar en una nube real.

## Paso 5. Pide una revisión a la IA y contrástala

Antes de abrir la segunda pestaña, responde tú: «¿Qué ocurre con el paso Resumir comprobaciones si falla Plan del escenario integracion?». Después abre **GitHub Copilot Chat en GitHub.com** o **ChatGPT** en otra pestaña. No dependas del agente integrado en VS Code Web. Usa este prompt con **solo el fragmento ficticio** del workflow:

> Estoy aprendiendo GitHub Actions con un laboratorio IaC ficticio. Mi workflow ejecuta OpenTofu `init`, `fmt`, `validate` y dos `plan`. Tiene pasos con `id`, un resumen con `if: ${{ always() }}` que lee `steps.<id>.outcome`, y publica `evidencia.txt` con `actions/upload-artifact@v7`. Explícame en lenguaje sencillo qué ocurrirá si falla el segundo plan, qué comprobaré en los logs y por qué ni el resumen ni el artefacto implican que el despliegue haya sido aprobado. Indica incertidumbres. No sugieras `tofu apply`, credenciales ni servicios cloud.

Contrasta la respuesta con el YAML y luego con la ejecución real. Si la IA afirma que `always()` convierte un fallo en éxito, anota que es incorrecto: un paso anterior fallido mantiene el trabajo en rojo. No pegues información de la empresa ni tokens en una herramienta de IA.

## Paso 6. Provoca un fallo controlado y localízalo

Trabaja **solo en `automatizacion-ejercicio-4`**. En la línea `run:` de **Plan del escenario integracion**, cambia temporalmente el nombre del archivo a uno inexistente:

```yaml
        run: tofu plan -input=false -no-color -var-file=escenario-inexistente.tfvars
```

No crees ese archivo. Guarda, confirma y publica el commit `Prueba: ruta de escenario inexistente`.

En Actions abre **la ejecución de este commit**. El trabajo debe estar **rojo**. Abre el paso **Plan del escenario integracion** y busca el mensaje de que el archivo de variables indicado no existe. Observa que los pasos previos pasaron, que el paso del plan falló y que **Resumir comprobaciones** y **Publicar evidencia** se ejecutaron. En el resumen y en el archivo descargado, **Plan de integración** debe decir `failure`. Anota el enlace, el nombre del paso fallido y el mensaje del log.

**Interpretación:** cambiamos una ruta en el pipeline, no un valor de OpenTofu. El fallo es deliberado y está aislado en la rama de trabajo. Las comprobaciones posteriores con `always()` ayudan a diagnosticarlo; **no borran el fallo**.

## Paso 7. Corrige, revisa y prepara la siguiente práctica

1. Restaura la ruta correcta `-var-file=escenario-integracion.tfvars`. Publica `Corregir ruta de escenario` y abre la nueva ejecución. Verifica cuatro `success`, trabajo verde y un nuevo artefacto. Guarda también este enlace.
2. En GitHub.com abre **Pull requests → New pull request** de **tu copia**. Comprueba `base: main` y `compare: automatizacion-ejercicio-4`, ambos bajo **tu cuenta**, nunca bajo la plantilla docente. En **Files changed** el cambio final debe incluir los cuatro `id` y los dos pasos nuevos, **sin** la ruta incorrecta del ensayo. El historial sí conserva el commit del fallo y su corrección.
3. Titula el PR `Ejercicio 4: evidencias del pipeline`. Describe: qué automatizaste, enlace a ejecución verde, enlace a ejecución roja, por qué `always()` no oculta errores y qué decisión requiere todavía revisión humana. Comprueba la ejecución automática del PR y, si todo está correcto, fusiona **en tu propia `main`**.
4. Comprueba una ejecución verde de `main` tras la fusión. Conserva tu repositorio y la rama principal: el ejercicio siguiente continuará sobre este mismo proyecto.

**Entrega:** cuatro enlaces de **tu cuenta**: repositorio, PR, ejecución roja y ejecución verde corregida. Añade una frase sobre qué muestra `evidencia.txt` y otra sobre qué no demuestra.

## Ruta B: VS Code local autorizado

Si la política de tu equipo **permite** VS Code y Git, abre **tu misma copia** localmente, realiza **Pull** antes de empezar, crea `automatizacion-ejercicio-4` desde `main`, modifica el mismo `validacion.yml`, confirma los cambios y usa **Push**. Consulta Actions y crea el PR en GitHub.com igual que en la ruta del navegador. OpenTofu sigue ejecutándose en GitHub Actions: para este ejercicio no hace falta instalarlo localmente. Si no tienes Git o VS Code autorizados, utiliza íntegramente github.dev; GitHub Actions y github.dev son servicios web y **no se instalan** en el ordenador.

## Si algo no sale como esperabas

| Lo que observas | Qué comprobar y cómo recuperarte |
| --- | --- |
| No aparece la ejecución | Comprueba que hiciste **Push**, que miras **tu repositorio** y que el commit está en la rama correcta. Refresca Actions. |
| El workflow no llega a comenzar | Revisa con cuidado el YAML: sangría, `- name`, dos puntos y `run: |`. Una sintaxis YAML inválida puede impedir que exista un trabajo con logs. |
| El paso de resumen no aparece | Comprueba que está **dentro de `steps:`** del trabajo `comprobar` y que `if: ${{ always() }}` está bajo su `- name:`. |
| El trabajo es rojo, pero el resumen dice `success` en algunos pasos | Mira **qué fila** tiene `failure`. Los pasos anteriores pudieron pasar; el trabajo completo sigue fallido. |
| No sale el artefacto | Abre **Publicar evidencia** en los logs; confirma `path: evidencia.txt` y que el paso de resumen generó el archivo. Revisa si la política de tu cuenta bloquea artefactos. |
| El PR apunta a `b-regina` | Antes de crearlo, cambia **base** y **compare** para que ambos sean ramas de **tu copia**. |
| No puedes usar Actions o github.dev desde el equipo corporativo | Haz la lectura de la guía y observa la demo docente; registra el bloqueo concreto para revisarlo en clase. No introduzcas credenciales corporativas ni busques servicios de pago. |

## Preguntas para comprobar que lo has comprendido

1. ¿Qué diferencia hay entre un disparador `on: push` y un paso `run:`?
2. ¿Para qué sirve un `id` en un paso y qué significa `steps.plan_integracion.outcome`?
3. ¿Por qué se genera `evidencia.txt` incluso cuando falla el segundo plan? ¿Por qué el trabajo sigue rojo?
4. ¿Dónde se consulta un log y dónde se descarga un artefacto? ¿Por cuánto tiempo se conserva el de esta práctica?
5. ¿Qué peligro tendría subir un plan real con secretos como artefacto público?
6. ¿Qué partes de una automatización así serían conceptualmente reutilizables en Jenkins o Azure DevOps, aunque cambie la sintaxis?

**Reto autónomo, después de la entrega:** sin cambiar el resultado del pipeline, mejora en tu rama el texto del título `## Resultados del laboratorio` para que un compañero identifique el escenario. Comprueba el nuevo resumen con otro commit y explica por qué ese cambio de presentación no altera `tofu plan`.
