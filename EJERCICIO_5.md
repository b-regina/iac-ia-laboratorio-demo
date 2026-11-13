# Ejercicio 5  Un módulo reutilizable y revisión final

**Duración orientativa:** 120 a 150 minutos. **Punto de partida:** tu propia copia del laboratorio al terminar el ejercicio 4. **Herramientas:** navegador, cuenta GitHub, github.dev y una segunda pestaña de IA si está permitida. No necesitas instalar programas. No usaremos credenciales, proveedores cloud ni `tofu apply`.

## Para qué sirve esta práctica

Trabajas en la empresa ficticia Nexo Portal. Ya has definido una ficha de aplicación con OpenTofu, has comparado desarrollo e integración y has automatizado las comprobaciones. Ahora el equipo necesita representar también una segunda aplicación de ayuda sin copiar la misma definición del recurso. Vas a construir **una plantilla interna de código**, llamada módulo local, y a llamarla dos veces desde el proyecto que ya tienes.

Al final tendrás dos fichas ficticias en cada plan, un error detectado y corregido, una revisión con IA y una propuesta de cambios revisable. La actividad representa la modularidad del temario y cierra el ciclo completo: necesidad, diseño, código, revisión, validación y entrega.

**Qué significa módulo.** Es un conjunto pequeño de archivos OpenTofu que acepta entradas y ofrece salidas. `source = "./modulo_ficha"` indica una carpeta del mismo repositorio. Las dos llamadas comparten la definición, pero reciben valores distintos. El recurso `terraform_data` forma parte de OpenTofu; aquí solo se calcula el plan, no se aplica ni se despliega nada.

## Antes de empezar y mapa del proyecto

1. Abre **tu copia** en `github.com`, no el repositorio de la docente. Comprueba que en ella aparecen `main.tf`, `variables.tf`, `outputs.tf`, `escenario-integracion.tfvars` y `.github/workflows/validacion.yml`. Tu ejercicio 4 debe estar ya integrado en la rama con la que vas a trabajar.
2. En el selector de ramas, crea `arquitectura-ejercicio-5` **desde la rama que contiene tu ejercicio 4**. Si hiciste el ejercicio 4 en una rama sin fusionarla, selecciónala primero y crea la nueva desde allí. Así conservas todos tus pasos previos.
3. Abre la rama nueva en github.dev cambiando `github.com` por `github.dev` en su URL. Si se abre `vscode.dev`, sigue allí. En el Explorador comprobarás la rama abajo a la izquierda. Si aparece una solicitud de autorización, revisa la cuenta y los permisos mostrados antes de continuar.
4. Abre otra pestaña para GitHub Copilot en la web o ChatGPT, si tu organización lo permite. El editor web puede no ofrecer el agente integrado: la segunda pestaña basta para solicitar explicaciones y revisar fragmentos ficticios.

Solo añadiremos **una carpeta**. La raíz sigue siendo la del mismo laboratorio:

```text
tu-copia-del-laboratorio/
  main.tf                     llamadas al módulo
  variables.tf                entradas del proyecto, ya existentes
  outputs.tf                  resumen de las dos fichas
  escenario-integracion.tfvars segundo escenario, ya existente
  modulo_ficha/               única carpeta nueva
    main.tf                   recurso ficticio compartido
    variables.tf              entradas requeridas del módulo
    outputs.tf                salida del módulo
  .github/workflows/validacion.yml
```

**Punto de control:** si `escenario-integracion.tfvars` no existe en tu copia, detente y recupera el trabajo del ejercicio 3 antes de continuar. No pegues todo en `main.tf`: raíz y módulo tienen funciones diferentes.

## Paso 1  Diseña las dos fichas antes de escribir

El portal principal conservará el nombre de `var.nombre_aplicacion`. La ficha de ayuda tendrá siempre `portal-ayuda`. Ambas usarán `var.entorno`. Con los valores predeterminados del ejercicio anterior deberían aparecer `portal-demo` y `portal-ayuda`, ambas en `pruebas`. En integración, `portal-interno` y `portal-ayuda`, ambas en `integracion`.

Escribe en una frase por qué no conviene duplicar el bloque `resource "terraform_data"` en la raíz. Identifica qué dos entradas necesita la ficha y qué datos debe devolver. Comprueba tus respuestas con las tablas de resultados más abajo.

## Paso 2  Crea la carpeta compartida

1. En el Explorador de github.dev, haz clic con el botón derecho sobre la raíz del proyecto y elige **New Folder**. Escribe exactamente `modulo_ficha`.
2. Dentro de ella crea **New File** llamado `main.tf`. Escribe lo siguiente y guarda con `Ctrl+S`:

```hcl
resource "terraform_data" "ficha" {
  input = {
    nombre  = var.nombre
    entorno = var.entorno
  }
}
```

Este recurso define la ficha una sola vez. Los valores `var.nombre` y `var.entorno` llegarán de cada llamada al módulo. No hay conexión con servicios externos.

3. En la **misma carpeta**, crea `variables.tf`. Copia las dos entradas y sus condiciones:

```hcl
variable "nombre" {
  description = "Nombre ficticio de la ficha"
  type        = string

  validation {
    condition     = startswith(var.nombre, "portal-")
    error_message = "El nombre debe empezar por portal-."
  }
}

variable "entorno" {
  description = "Entorno ficticio de la ficha"
  type        = string

  validation {
    condition     = contains(["desarrollo", "pruebas", "integracion"], var.entorno)
    error_message = "Usa desarrollo, pruebas o integracion."
  }
}
```

Al no tener `default`, ambas entradas son obligatorias para **cada** llamada. La condición de nombre repite la regla de la raíz también para la ficha de ayuda. Los mensajes explican cómo corregir un valor.

4. Crea `modulo_ficha/outputs.tf` y guarda:

```hcl
output "resumen" {
  description = "Valores previstos de la ficha, sin aplicar recursos"
  value       = terraform_data.ficha.input
}
```

**Punto de control:** `main.tf`, `variables.tf` y `outputs.tf` deben estar dentro de `modulo_ficha`; los tres archivos con esos mismos nombres que ya existen en la raíz siguen allí. No hay dos proyectos: el módulo es una pieza del proyecto.

## Paso 3  Usa el mismo módulo dos veces

Abre el `main.tf` de la **raíz**. Sustituye el bloque anterior `resource "terraform_data" "aplicacion"` por estas dos llamadas. Guarda:

```hcl
module "portal" {
  source  = "./modulo_ficha"
  nombre  = var.nombre_aplicacion
  entorno = var.entorno
}

module "ayuda" {
  source  = "./modulo_ficha"
  nombre  = "portal-ayuda"
  entorno = var.entorno
}
```

`source` señala el código que se reutiliza. `portal` y `ayuda` son los identificadores de las dos instancias; `nombre` y `entorno` son argumentos exigidos por el módulo. No cambies el `variables.tf` de la raíz: ya proporciona `var.nombre_aplicacion` y `var.entorno` desde los ejercicios anteriores.

## Paso 4  Reúne las dos salidas

Abre el `outputs.tf` de la **raíz**. La antigua referencia `terraform_data.aplicacion.output` dejará de existir al mover el recurso al módulo. Sustituye el bloque completo por:

```hcl
output "resumen" {
  description = "Fichas previstas para el caso ficticio"
  value = {
    portal = module.portal.resumen
    ayuda  = module.ayuda.resumen
  }
}
```

La salida raíz reúne ambas fichas; cada salida interna corresponde a su instancia. Antes de ejecutar, señala en el código de dónde procede `module.ayuda.resumen`.

## Paso 5  Comprueba el formato de la carpeta nueva

Abre `.github/workflows/validacion.yml`. En el paso **Comprobar formato**, cambia **solo** la línea de ejecución anterior por:

```yaml
        run: tofu fmt -check -diff -recursive
```

`-recursive` permite revisar los archivos `.tf` dentro de `modulo_ficha`. Conserva los otros pasos del ejercicio 4: `init`, `validate`, dos planes, resumen y artefacto. Comprueba la indentación YAML antes de guardar. `tofu init` cargará el módulo local en el runner y los planes seguirán ejecutándose en el servicio gratuito de GitHub Actions del repositorio público.

**Punto de control:** en Control de código fuente deben aparecer la carpeta nueva y solo tres archivos modificados en la raíz: `main.tf`, `outputs.tf` y el workflow. `variables.tf` y el escenario anterior permanecen igual.

## Paso 6  Pregunta a la IA y revisa su respuesta

En la segunda pestaña, pega únicamente el código ficticio de esta práctica. Puedes usar este prompt:

> Actúa como revisor de OpenTofu para una práctica de aprendizaje. Tengo un módulo local `modulo_ficha` con dos entradas obligatorias, `nombre` y `entorno`, y un recurso `terraform_data`. En la raíz lo llamo dos veces, `portal` y `ayuda`. Explica qué papel tienen `source`, cada argumento y `module.portal.resumen`; predice las dos fichas en el escenario predeterminado y en integración. Señala un error que `tofu validate` detectaría y otro que `tofu fmt -check -diff -recursive` detectaría. No propongas `apply`, servicios cloud, credenciales ni nuevos repositorios. Distingue la predicción del resultado comprobado en Actions.

Contrasta la respuesta con los archivos. Si la IA afirma que se desplegó una aplicación, corrígela: aquí solo hay un plan. Escribe una observación útil de la revisión en tu propuesta de cambios.

## Paso 7  Confirma y lee las dos ejecuciones de plan

1. En el panel **Source Control**, revisa los seis cambios de esta práctica. Escribe el mensaje `Ejercicio 5: módulo local reutilizable`. Haz **Commit & Push**; si aparecen por separado, haz primero Commit y después Sync o Push. Comprueba que la rama es `arquitectura-ejercicio-5`.
2. Vuelve a `github.com` en tu copia, pestaña **Actions**. Abre **Validacion IaC** y selecciona la ejecución asociada a ese commit y a tu rama. No confundas una ejecución anterior con la actual.
3. En el trabajo **comprobar**, abre **Inicializar**, **Comprobar formato**, **Validar**, **Plan con valores por defecto** y **Plan del escenario integracion**. Los cinco pasos deben estar verdes.
4. En el primer plan busca `module.portal.terraform_data.ficha` con `portal-demo` y `pruebas`, y `module.ayuda.terraform_data.ficha` con `portal-ayuda` y `pruebas`. En el segundo busca `portal-interno` y `portal-ayuda`, ambas con `integracion`.
5. En ambos debe aparecer `Plan: 2 to add, 0 to change, 0 to destroy`. Lee también **Changes to Outputs**, el resumen del trabajo y el artefacto `evidencia-iac-...` si lo deseas. Ese artefacto caduca después de siete días; conserva el enlace de la ejecución.

| Escenario | Portal principal | Ayuda | Entorno de ambas |
| --- | --- | --- | --- |
| Predeterminado | `portal-demo` | `portal-ayuda` | `pruebas` |
| Integración | `portal-interno` | `portal-ayuda` | `integracion` |

**Interpretación:** el plan dice **dos recursos previstos** porque cada llamada crea una instancia distinta del recurso ficticio. No hay `apply`; `to add` no demuestra que se haya desplegado nada. Los runners no comparten estado entre ejecuciones de esta práctica.

## Paso 8  Provoca un fallo y repáralo

Haz esto solamente en tu rama de ejercicio. Abre `main.tf` de la raíz y elimina la línea `nombre  = "portal-ayuda"` del bloque `module "ayuda"`. Guarda y confirma con el mensaje `Prueba: falta nombre en módulo ayuda`. En Actions abre **el nuevo commit**. Espera un trabajo rojo. En **Validar**, busca el mensaje de argumento requerido ausente para `nombre`; los planes no deben ejecutarse. El resumen y el artefacto de evidencias pueden aparecer en verde, pero el trabajo completo sigue fallando.

Restituye exactamente `nombre  = "portal-ayuda"`, guarda y confirma con `Corrección: restaurar nombre del módulo`. Abre la nueva ejecución y comprueba que formato, validación y ambos planes vuelven a verde. Guarda los enlaces de las ejecuciones roja y verde. Si el error aparece antes en formato, revisa primero llaves, comillas y espacios del bloque.

## Paso 9  Explica el diseño y entrega una revisión

Añade al final de tu `README.md` una sección breve `## Arquitectura ficticia` con tus palabras. Explica: qué necesidad cubren las dos fichas, qué código se comparte, qué cambia entre escenarios, qué comprueba el pipeline y por qué **no** hay gastos de infraestructura ni observabilidad real. Señala una medida de gobernanza: revisar el plan, el cambio de código y la evidencia antes de aprobar una configuración. No inventes un despliegue ni cifras de costes. Confirma el cambio.

En `github.com`, entra en **Pull requests** de tu copia y pulsa **New pull request**. Selecciona como base la rama de tu propio ejercicio 4 (o tu `main` si ya lo habías fusionado) y como compare `arquitectura-ejercicio-5`. Revisa **Files changed**. En la descripción responde:

- ¿Qué necesidad resuelves y qué módulo has creado?
- ¿Qué diferencias muestran los dos planes y qué evidencia consultaste?
- ¿Qué fallo detectó el pipeline y con qué commit lo corregiste?
- ¿Qué consejo de la IA aceptaste o rechazaste y por qué?
- ¿Qué límites tendría este diseño antes de usarlo con infraestructura real?

Puedes dejar el PR en borrador para recibir comentarios. Entrega el enlace del PR y las ejecuciones verde, roja y corregida. No apuntes el PR a la plantilla de la docente. No fusiones hasta haber revisado la comparación con la docente si así se organiza la clase.

## Si algo no sale como esperabas

| Síntoma | Revisión concreta |
| --- | --- |
| `Unclosed configuration block` | Comprueba las llaves de `main.tf` y de `variables.tf` dentro del módulo. |
| `Missing required argument` | Revisa que **cada** bloque `module` tenga `nombre` y `entorno`. |
| `Module not installed` o ruta inválida | Comprueba que la carpeta se llame `modulo_ficha`, que `source` sea `./modulo_ficha` y que `tofu init` se haya ejecutado. |
| Falla el formato | Revisa la ruta exacta y pulsa en **Comprobar formato** para ver el diff. El `-recursive` incluye los `.tf` de la carpeta. |
| `Unsupported attribute` | La salida interna se llama `resumen` y está declarada en `modulo_ficha/outputs.tf`; revisa las referencias `module.portal.resumen` y `module.ayuda.resumen`. |
| No aparece la ejecución | Comprueba que hiciste Push, que miras tu copia y la rama correcta. Una política de GitHub puede requerir habilitar Actions. |
| No se abre github.dev | Usa el lápiz de edición en `github.com` sobre cada archivo y confirma el cambio desde esa web. El pipeline sigue siendo el mismo. |

## Si puedes usar VS Code instalado

Abre **tu copia** del mismo repositorio en VS Code local solo si tu equipo y sus políticas permiten instalarlo o ya lo tienes. Puedes clonar tu copia con Git, crear `arquitectura-ejercicio-5` desde tu rama del ejercicio 4 y editar los **mismos** archivos. Si tienes OpenTofu local, puedes ejecutar `tofu init -backend=false`, `tofu fmt -check -diff -recursive`, `tofu validate` y ambos `tofu plan` por comodidad, pero no es necesario. El criterio de entrega sigue siendo confirmar, publicar la rama y leer GitHub Actions. Si no tienes Git u OpenTofu local, usa el navegador. La IA permanece en una segunda pestaña si no tienes agente integrado autorizado.

## Preguntas finales y reto autónomo

1. ¿Qué línea indica a OpenTofu dónde está el módulo y qué archivo define sus entradas?
2. ¿Por qué aparecen dos recursos previstos aunque hay un solo bloque `resource` en la carpeta?
3. ¿Qué cambia si el escenario de integración usa `portal-interno` y qué se mantiene igual?
4. ¿Por qué la falta de `nombre` impide ejecutar el plan y por qué `to add` no implica despliegue?
5. ¿Qué aportan el PR, los logs y la revisión humana cuando la IA sugiere cambios?

**Reto:** en una rama distinta de tu copia, cambia el nombre del portal principal a otro valor ficticio que empiece por `portal-` en el escenario de integración. Predice el efecto en las dos fichas y ejecuta el pipeline. No alteres la carpeta compartida ni la rama docente. Entrega tu predicción y el enlace del plan para comprobar si coincidieron.

**Nota para entornos reales:** aquí los runners no conservan estado y solo se planifica. Mover un recurso ya aplicado desde la raíz a un módulo cambia su dirección de estado y requiere una migración planificada. Esta práctica no representa ese procedimiento ni acredita costes, seguridad u observabilidad de una nube real.
