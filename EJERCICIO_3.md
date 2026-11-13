# Ejercicio 3. Revisar y gobernar un cambio de IaC

## Para qué sirve esta práctica

En el ejercicio 2 dejaste una misma configuración ficticia preparada para los escenarios `pruebas` e `integracion`. Ahora el equipo ficticio quiere evitar que alguien escriba por error un entorno no aprobado o un nombre fuera de la convención `portal-`. Antes de incorporar un cambio, otra persona debe poder leer qué regla se propone y qué ha comprobado el pipeline.

Añadirás dos reglas de validación en `variables.tf`, observarás un plan fallido y su corrección, usarás la IA para **revisar** el cambio y abrirás un **pull request** en tu propio repositorio. Esta es una forma sencilla de practicar una política escrita como código y la revisión humana. No representa un control de seguridad corporativo completo. No hay credenciales, proveedores cloud ni `tofu apply`.

**Duración orientativa:** 90 a 120 minutos. **Punto de partida:** tu copia del ejercicio 2, con `entorno = "pruebas"` como valor predeterminado, `escenario-integracion.tfvars` y un workflow que muestra dos planes. Si terminaste el reto opcional del ejercicio 2 con `portal-equipo`, puedes conservar ese nombre: cumple la convención `portal-`.

## Paso 1. Lee lo que ya protege el proyecto

En GitHub.com, abre **tu copia personal**. No crees un tercer repositorio ni modifiques la plantilla docente.

1. Abre `.github/workflows/validacion.yml`: `permissions: contents: read` concede al workflow solo lectura del contenido para esta práctica. No cambies los permisos ni añadas secretos.
2. Abre `.gitignore`: excluye estados, planes, claves y archivos `.tfvars` en general, pero permite **solo** `escenario-integracion.tfvars` porque tiene valores ficticios. `.gitignore` no oculta los archivos que ya se publicaron ni convierte un repositorio público en privado.
3. Abre `variables.tf` y `escenario-integracion.tfvars`. Comprueba que los valores predeterminados y el escenario actual pertenecen al laboratorio. Pregúntate qué pasaría si alguien pusiera `produccion` en el escenario.

**Punto de control:** puedes explicar por qué hay un archivo de escenario visible, por qué no se deben subir credenciales y dónde se ven los permisos del workflow.

## Paso 2. Crea una rama para la propuesta

En el selector de ramas de GitHub.com, crea una rama llamada `revision-ejercicio-3` **a partir de `main` de tu copia**. Puedes usar **View all branches → New branch**; la interfaz puede mostrar **New branch** directamente. Abre la URL de esa rama con `github.dev` sustituyendo el dominio, o usa el lápiz de GitHub.com si el editor web está bloqueado. Comprueba en la esquina inferior del editor que trabajas en `revision-ejercicio-3`, no en `main` ni en `b-regina`.

## Paso 3. Define dos reglas claras

En `variables.tf`, **dentro** del bloque `variable "entorno"`, debajo de `default`, añade:

```hcl
  validation {
    condition     = contains(["desarrollo", "pruebas", "integracion"], var.entorno)
    error_message = "El entorno debe ser desarrollo, pruebas o integracion."
  }
```

Dentro de `variable "nombre_aplicacion"`, debajo de su `default`, añade:

```hcl
  validation {
    condition     = startswith(var.nombre_aplicacion, "portal-")
    error_message = "El nombre debe comenzar por portal-."
  }
```

Conserva el cierre `}` de cada variable. El archivo seguirá teniendo **dos bloques `variable`** y cada uno tendrá **un bloque `validation`**. `contains` comprueba la lista de entornos; `startswith` exige el prefijo del nombre. Las reglas verifican valores, no sustituyen la revisión de permisos, costes o secretos.

Guarda con `Ctrl+S`. En **Source Control** revisa que solo cambió `variables.tf`. Publica un commit llamado `Ejercicio 3: validar entorno y nombre`. Abre **Actions** en tu repositorio y comprueba que los planes por defecto y de integración continúan en verde.

**Antes de preguntarle a la IA:** escribe con tus palabras qué aceptará cada regla. En una segunda pestaña de Copilot Chat o ChatGPT, usa este prompt con **solo el código ficticio**:

> Actúa como revisor de una configuración OpenTofu de laboratorio. Hay dos validaciones: `contains(["desarrollo", "pruebas", "integracion"], var.entorno)` y `startswith(var.nombre_aplicacion, "portal-")`. El workflow solo ejecuta `init`, `fmt`, `validate` y dos planes con permisos de lectura. Explica qué errores evitan, qué errores NO evitan y qué comprobarías antes de aprobar un pull request. No propongas credenciales, despliegues cloud ni `tofu apply`. Señala cualquier afirmación que deba verificarse en los logs.

Comprueba sus respuestas tú mismo. Una sugerencia de la IA no es aprobación técnica.

## Paso 4. Provoca un fallo controlado y corrígelo

Continúa **en la rama `revision-ejercicio-3` de tu copia**.

1. En `escenario-integracion.tfvars`, cambia temporalmente solo `entorno = "integracion"` por `entorno = "produccion"`. Es una palabra ficticia para probar la regla: no se desplegará ningún entorno. Publica el commit `Prueba: entorno no permitido`.
2. En **Actions**, abre la ejecución de ese commit. `Inicializar`, `Comprobar formato`, `Validar` y el **plan con valores por defecto** pueden salir verdes. El **plan del escenario integracion** debe fallar y mostrar `El entorno debe ser desarrollo, pruebas o integracion.`. Anota el enlace de esa ejecución y el paso que falló.
3. Repón `entorno = "integracion"`, publica `Corregir entorno de integracion` y comprueba que la siguiente ejecución completa los dos planes en verde.

**¿Por qué no falló antes?** `tofu validate` comprueba la configuración; no usa los valores concretos de ese archivo `.tfvars`. El segundo comando `tofu plan -var-file=escenario-integracion.tfvars` sí los carga y aplica la regla al valor `produccion`. Esto no es un despliegue ni una prueba con una cuenta cloud.

## Paso 5. Abre y revisa tu propuesta

En GitHub.com, dentro de tu repositorio, pulsa **Compare & pull request** si aparece el aviso tras publicar la rama. Si no, entra en **Pull requests → New pull request**, elige **base: main** y **compare: revision-ejercicio-3** de **tu misma cuenta**. Antes de crear el PR, mira **Files changed**: el cambio final debería ser la incorporación de dos validaciones en `variables.tf`. El historial también mostrará el ensayo fallido y su corrección.

Pon como título `Ejercicio 3: validar entorno y nombre`. En la descripción escribe: objetivo, dos reglas, enlace a la ejecución roja, enlace a la ejecución verde y una frase sobre lo que aún requiere revisión humana. Crea el pull request. Si GitHub ejecuta de nuevo el workflow para el PR, espera a que termine y lee sus comprobaciones.

**Lista de revisión antes de fusionar:**

- ¿El diff final contiene las dos reglas y mantiene los valores ficticios válidos?
- ¿El workflow conserva `permissions: contents: read` y no contiene `tofu apply`?
- ¿No aparecen contraseñas, claves, tokens ni información de la empresa?
- ¿El plan falló con el valor no permitido y volvió a verde tras corregirlo?
- ¿La explicación de la IA coincide con el código y los logs?

Si todo coincide, pulsa **Merge pull request** en tu propia copia. Comprueba que `main` contiene las validaciones y tiene una ejecución verde. No abras un PR hacia la plantilla docente. En una clase con revisión por parejas, otra persona puede comentar tu PR público; no es necesario darle acceso de administración.

## Ruta B y problemas habituales

Si usas VS Code local autorizado, haz **Pull** antes de empezar, crea la rama desde `main`, edita `variables.tf`, confirma y publica los commits con **Push**. Abre y revisa el PR desde GitHub.com. OpenTofu sigue ejecutándose en Actions; no requiere instalación en el equipo.

| Lo que ves | Qué comprobar |
| --- | --- |
| Error de sintaxis o formato | Revisa que `validation` esté dentro del `variable` correcto, que las llaves cierren y que `condition` y `error_message` estén alineados. |
| Falla el plan por defecto | Comprueba que `default = "pruebas"` y `default = "portal-demo"` siguen siendo válidos. |
| No falla el ensayo con `produccion` | Abre la ejecución de ese commit y el **segundo** plan; confirma el contenido publicado del `.tfvars`. |
| El PR compara con `b-regina` | Cambia base y compare para que ambos apunten a **tu repositorio personal**. |
| `Files changed` muestra el error temporal | Comprueba que publicaste el commit de corrección en la misma rama y actualiza la página. |

## Entrega y preguntas de comprensión

Entrega los enlaces a **tu repositorio**, **tu pull request**, **la ejecución roja** y **la ejecución verde**. Explica en cuatro frases qué reglas añadiste, qué paso detectó el entorno incorrecto, qué comprobó la IA y qué decisión tomaste tú como revisor.

¿Por qué una ejecución de `validate` verde no demuestra que todos los valores del `.tfvars` sean aceptables? ¿Qué diferencia hay entre una regla automática y la revisión humana? ¿Puede `.gitignore` borrar una clave ya publicada? ¿Qué parte del workflow demuestra el principio de mínimos privilegios?

Conserva tu `main` con las validaciones: el siguiente ejercicio ampliará la automatización de **este mismo proyecto**.
