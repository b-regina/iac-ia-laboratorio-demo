# Ejercicio 8 · Taller final de IaC gobernada con apoyo de IA

**Punto de partida:** tu copia personal con el ejercicio 7 terminado y los dos escenarios en verde. **Entorno:** GitHub.com, github.dev y una segunda pestaña de Copilot o ChatGPT. No hacen falta instalaciones, terminal, credenciales cloud ni tarjeta bancaria.

## Sigue trabajando en tu copia

Esta guía se publica en la plantilla del curso para que puedas leerla desde el navegador. **Tu repositorio personal no recibe automáticamente los archivos añadidos después de crear la copia.** Abre este enlace en una pestaña y sigue trabajando en la misma copia donde terminaste el 7. No crees otro repositorio ni clones de nuevo. Si ya usas VS Code local, abre tu carpeta actual y comprueba con `git remote -v` que `origin` es tu repositorio personal; si apunta a `b-regina/iac-ia-laboratorio-demo`, detente antes de publicar.

## La necesidad y lo que aprenderás

En la empresa ficticia Nexo Portal, el catálogo del ejercicio 7 contiene dos fichas: `portal` y `ayuda`. Ya existe una política que admite exactamente esas dos fichas. Antes de dar por revisado el proyecto, el equipo quiere que cada ficha indique **a qué proyecto, entorno y equipo responsable pertenece**. El equipo de integración será distinto del equipo del escenario de pruebas. La política debe detectar una asignación equivocada aunque OpenTofu pueda planificarla.

Al terminar tendrás el mismo proyecto, el mismo módulo, los mismos dos escenarios y la misma automatización. Añadirás tres etiquetas *didácticas* a las entradas de `terraform_data`; no son etiquetas de un servicio cloud. Conseguirás una ejecución verde, provocarás un rechazo controlado en integración y restaurarás el verde. Por último explicarás una decisión de diseño y entregarás la trazabilidad del cambio.

**Resultado esperado:** dos recursos ficticios en cada escenario; en pruebas, responsable `equipo-lab`; en integración, `equipo-integracion`; la política aprobará ambas configuraciones. Si asignas `equipo-lab` a integración, `tofu validate` y los dos planes seguirán siendo válidos, pero la política del plan de integración deberá fallar.

## Preparación

1. Entra en **tu copia personal** de GitHub. Selecciona la rama donde terminaste el ejercicio 7; comprueba que `main.tf` contiene `module "fichas"` con `for_each`, y que existen `modulo_ficha/`, `politica_plan.py` y `escenario-integracion.tfvars`. La rama `main` de la plantilla docente no equivale necesariamente a tu ejercicio 7 terminado.
2. En GitHub.com pulsa el selector de ramas, escribe `taller-final-ejercicio-8` y elige **Create branch from** tu rama del ejercicio 7. Confirma en la parte superior que la rama nueva está seleccionada. Todos los cambios pertenecen a tu copia.
3. En la URL de **tu repositorio**, sustituye `github.com` por `github.dev` y pulsa Intro. Puede redirigir a `vscode.dev`. Abre el explorador de archivos. Si el editor solicita acceso al repositorio, revisa la cuenta y los permisos antes de autorizar.
4. En una segunda pestaña abre Copilot en GitHub.com o ChatGPT. Usa exclusivamente el caso ficticio. Antes de cambiar el código, anota tu predicción: ¿qué archivos necesitarán conocer el responsable?, ¿qué control debe detectar la asignación incorrecta? Pregunta a la IA: «Dibuja en texto el recorrido de un responsable ficticio desde un `.tfvars` hasta el `input` de `terraform_data` y la política Python. Señala qué pasos son validación técnica y cuáles son reglas de gobierno. No escribas código todavía». Contrasta el recorrido con tus archivos del ejercicio 7.

**Punto de control:** no crees otro repositorio, otra carpeta ni otro workflow. Trabajarás en seis archivos ya existentes: `variables.tf`, `escenario-integracion.tfvars`, `main.tf`, `modulo_ficha/variables.tf`, `modulo_ficha/main.tf` y `politica_plan.py`. El workflow y `outputs.tf` se mantienen.

## Paso 1  Parametriza el responsable

En el `variables.tf` de la **raíz**, después de `nombre_aplicacion`, añade:

```hcl
variable "responsable" {
  description = "Equipo ficticio responsable de las fichas"
  type        = string
  default     = "equipo-lab"
}
```

La variable raíz representa el responsable del escenario. Su valor predeterminado corresponde a `pruebas`. En `escenario-integracion.tfvars` añade la tercera línea; conserva las otras dos:

```hcl
entorno           = "integracion"
nombre_aplicacion = "portal-interno"
responsable       = "equipo-integracion"
```

**Comprueba antes de continuar:** la raíz tiene una sola declaración `variable "responsable"`; el fichero `.tfvars` contiene tres asignaciones y ninguna contraseña. `responsable` es un nombre ficticio de equipo, no un usuario de GitHub ni una identidad real.

## Paso 2  Pasa el dato al módulo

En el `main.tf` de la raíz, **dentro del bloque existente** `module "fichas"`, añade `responsable = var.responsable`. El bloque completo debe quedar:

```hcl
module "fichas" {
  for_each    = local.catalogo
  source      = "./modulo_ficha"
  nombre      = each.value
  entorno     = var.entorno
  responsable = var.responsable
}
```

No cambies las dos entradas del `local.catalogo`. En `modulo_ficha/variables.tf` agrega al final:

```hcl
variable "responsable" {
  description = "Equipo ficticio responsable de la ficha"
  type        = string
}
```

**La relación:** la variable de la raíz alimenta la entrada de cada instancia del módulo. El módulo declara por separado qué entradas acepta. Si omites el nuevo bloque del módulo, OpenTofu mostrará `Unsupported argument` al recibir `responsable`.

## Paso 3  Describe las etiquetas ficticias

En `modulo_ficha/main.tf`, reemplaza el contenido completo por este bloque. La alineación de `nombre` y `entorno` es deliberada; el formato de OpenTofu comprobará exactamente cómo deben aparecer:

```hcl
resource "terraform_data" "ficha" {
  input = {
    nombre  = var.nombre
    entorno = var.entorno
    etiquetas = {
      proyecto    = "nexo-portal"
      entorno     = var.entorno
      responsable = var.responsable
    }
  }
}
```

`proyecto` identifica el caso ficticio, `entorno` repite el entorno de la ficha para poder revisar coherencia y `responsable` identifica el equipo del escenario. La salida `resumen` del módulo ya utiliza `terraform_data.ficha.input`, por lo que mostrará también `etiquetas` **sin modificar `outputs.tf`**. El plan puede marcar algunas salidas como conocidas después de `apply`; en este laboratorio solo inspeccionamos los valores de `input` previstos y no se ejecuta `apply`.

## Paso 4  Amplía tu política sin perder los controles anteriores

Abre el `politica_plan.py` que **tú desarrollaste** en los ejercicios 6 y 7. Es posible que tus funciones y variables no se llamen igual que las de un compañero: busca las comprobaciones por su **comportamiento**. No sustituyas el archivo completo.

1. Declara el criterio de responsables por entorno: `desarrollo → equipo-lab`, `pruebas → equipo-lab`, `integracion → equipo-integracion`. Puedes representarlo con un diccionario. Solo consúltalo después de comprobar que el entorno está permitido.
2. Localiza dónde tu política rechaza valores desconocidos y sensibles de `change.after_unknown.input` y `change.after_sensitive.input`. Al añadir `etiquetas`, OpenTofu puede representar esas marcas como mapas anidados con valores `false`. Un diccionario que existe pero contiene solo `false` **no equivale** a una entrada desconocida. Si tu código hace simplemente `if marcas:`, adáptalo para recorrer diccionarios y listas y rechazar cuando aparezca un booleano `true`. Pide a la IA una función recursiva pequeña; comprueba conceptualmente que un JSON como `{"etiquetas": {"responsable": false}}` no se rechaza, mientras `true` sí se rechaza. En Python los booleanos equivalentes se escriben `False` y `True`.
3. Localiza la condición que antes aceptaba las claves `nombre` y `entorno` en `change.after.input`. Debe aceptar ahora exactamente `nombre`, `entorno` y `etiquetas`. Comprueba que `etiquetas` sea un mapa con las claves exactas `proyecto`, `entorno` y `responsable`, sin extras.
4. Exige `proyecto = "nexo-portal"`, `etiquetas.entorno` igual al entorno principal de la ficha y `etiquetas.responsable` igual al equipo permitido para ese entorno. Conserva las reglas anteriores: solo dos direcciones de `module.fichas`, recursos `terraform_data`, acción `create`, nombres admitidos y entornos iguales.
5. Haz que el mensaje final de éxito sea `POLÍTICA APROBADA: dos fichas con etiquetas y responsable ficticios correctos`. Cada rechazo debe explicar **qué** regla falló y devolver código distinto de cero.

Prompt de apoyo, con solo datos inventados:

> Este es mi `politica_plan.py` del ejercicio anterior. Señala exactamente dónde cambiarías la validación de marcas anidadas, las claves permitidas y el responsable por entorno. Conserva todas las reglas existentes, modifica lo mínimo y explica cada diferencia. Para las marcas, no confundas un diccionario con valores false con un valor desconocido. No añadas proveedores, credenciales ni apply.

Revisa línea a línea el código sugerido. La IA podría quitar una regla que ya funcionaba o consultar un entorno inexistente y provocar `KeyError`. Revisa que el archivo siga rechazando las direcciones antiguas y la tercera ficha del ejercicio 7.

**Punto de control:** tu política sigue siendo un control didáctico versionado en la misma rama. Una ejecución verde aquí no equivale a aprobación independiente para producción.

## Paso 5  Pide una revisión crítica a la IA

En la segunda pestaña usa este prompt; no incluyas información corporativa ni planes JSON completos:

> Estoy realizando un laboratorio ficticio de OpenTofu sin proveedores cloud ni `apply`. Tengo dos instancias de un módulo `terraform_data` (`portal` y `ayuda`), dos escenarios (`pruebas` e `integracion`) y una política Python que lee `tofu show -json`. He añadido un mapa `etiquetas` con `proyecto`, `entorno` y `responsable`. Revisa conceptualmente el recorrido variable raíz → argumento del módulo → variable del módulo → `input` → plan → política. El responsable admitido en pruebas es `equipo-lab` y en integración `equipo-integracion`. ¿Qué podría fallar aunque `tofu validate` pase? Propón tres comprobaciones concretas en los logs y una limitación de esta simulación. No propongas servicios cloud, credenciales, `apply` ni cambios ajenos al ejercicio.

Escribe una afirmación que la IA haya hecho y cómo la comprobarás. No copies a ciegas cambios sugeridos: contrástalos con el plan y con el primer paso rojo si aparece un fallo.

## Paso 6  Guarda, confirma y verifica

1. Pulsa `Ctrl+S` en cada archivo. En **Source Control** revisa que solo cambian los seis archivos indicados. Escribe el mensaje `Ejercicio 8: etiquetas y responsables gobernados`; selecciona **Commit & Push**. Si aparecen como acciones separadas, realiza primero **Commit** y luego **Push/Sync**. Espera a que GitHub muestre el commit en tu rama.
2. En otra pestaña visita **GitHub.com → tu copia → Actions → Validacion IaC**. Abre la ejecución correspondiente al mensaje y SHA nuevos. Entra en el trabajo **comprobar**. No confundas una ejecución anterior con la de este commit.
3. Verifica en este orden `Inicializar`, `Comprobar formato`, `Validar`, `Plan con valores por defecto`, `Politica del plan predeterminado`, `Plan del escenario integracion` y `Politica del plan de integracion`. Los dos planes deben indicar `Plan: 2 to add, 0 to change, 0 to destroy` y las dos políticas deben escribir `POLÍTICA APROBADA`.
4. En el primer plan localiza `etiquetas`, `proyecto = "nexo-portal"`, `entorno = "pruebas"`, `responsable = "equipo-lab"`. En el de integración busca `portal-interno`, `integracion` y `equipo-integracion`. `Summary` muestra los seis resultados y `evidencia.txt` se conserva siete días. Copia la URL verde.

**Si el formato falla:** abre `Comprobar formato` y usa su diff para corregir espacios; si falla `Validar`, revisa argumentos y variables; si falla un plan, consulta el mensaje de OpenTofu; si falla una política, lee su mensaje de rechazo. Los pasos omitidos después de un fallo no prueban nada sobre el código que no llegaron a ejecutar.

## Paso 7  Prueba un cambio no aprobado

En **tu misma rama**, cambia *solo* la última línea de `escenario-integracion.tfvars` a `responsable = "equipo-lab"`. Es un valor válido de tipo `string`, pero es el equipo equivocado para integración. Antes del commit, predice el resultado de cada uno de los dos planes y políticas. Publica `Prueba: responsable de integracion incorrecto` y abre **esa** ejecución.

**Resultado que debes encontrar:** formato, validación, plan y política predeterminados verdes; plan de integración verde con dos fichas y la etiqueta `responsable = "equipo-lab"`; **Política del plan de integración roja** con `POLÍTICA RECHAZADA: responsable no aprobado para integracion`. El trabajo completo debe quedar rojo. Copia su URL. Si falló antes otro paso, corrige primero ese error: aún no has demostrado el control deseado.

## Paso 8  Corrige y cierra el taller

1. Devuelve la línea de `escenario-integracion.tfvars` a `responsable = "equipo-integracion"`. Publica `Correccion: responsable aprobado en integracion`. Abre la ejecución nueva y confirma que los dos planes y las dos políticas vuelven a estar en verde. Copia la URL.
2. En el README **de tu copia**, escribe unas líneas que expliquen el mapa de etiquetas, la regla por entorno, el error detectado y el hecho de que no hubo despliegue. Confirma el README y comprueba su ejecución. No incluyas capturas de datos internos.
3. Crea un pull request **dentro de tu propio repositorio** desde `taller-final-ejercicio-8` hacia tu rama del ejercicio 7. En `Files changed`, revisa los seis archivos de código más el README. Describe la necesidad, decisión de diseño, predicción, control que falló, corrección, afirmación de IA contrastada y enlaces a las tres ejecuciones. Puedes dejar el PR abierto o en borrador para recibir comentarios; no apuntes al repositorio original del curso.

## Cómo diagnosticar incidencias

| Lo que observas | Qué comprobar |
| --- | --- |
| `Unsupported argument` para `responsable` | Falta la variable en `modulo_ficha/variables.tf` o el argumento se insertó en el bloque incorrecto. |
| `Reference to undeclared input variable` | Falta `variable "responsable"` en `variables.tf` de la raíz. |
| `tofu fmt` rechaza `modulo_ficha/main.tf` | Compara la alineación de `nombre` y `entorno` con el diff del runner; no alinees estas claves con `etiquetas` como si fuera el mismo grupo. |
| Plan verde y primera política roja | Revisa que la política ahora admite la clave `etiquetas` y que el `input` del módulo contiene las tres entradas. |
| Política de integración roja en el caso correcto | Contrasta el `responsable` del `.tfvars` con el criterio que definiste para integración y mira el valor real del plan. |
| El fallo deliberado no llega a la política de integración | Busca el primer paso rojo; un paso omitido no es una política que rechaza. |
| No aparece la ejecución | Confirma que hiciste Push/Sync y que el mensaje y SHA en Actions coinciden con tu commit. |
| github.dev no carga el repositorio | Edita los mismos archivos desde GitHub.com con el icono del lápiz, confirmando cada cambio en tu rama; Actions sigue siendo la comprobación. |

**Plan B local autorizado:** si ya tienes VS Code y Git en un ordenador permitido, abre el clon de tu copia personal que ya utilizaste, cambia a la rama del taller, modifica los mismos archivos y publícalos. OpenTofu local no es obligatorio: GitHub Actions sigue realizando las comprobaciones. No instales software en un equipo corporativo sin permiso. Mantén la IA en una segunda pestaña si no hay agente local.

## Revisión final con IA y un compañero

Explica sin mirar el código por qué una configuración puede superar `tofu validate` y aun así asignar un responsable inadecuado. Pide a un compañero que encuentre una regla de gobierno ausente, por ejemplo, quién podría modificar el script de política. Pide a la IA una propuesta para controlar ese riesgo **en un sistema real**, clasifícala como recomendación y no la implementes en este laboratorio sin autorización. Añade la limitación detectada a la descripción de tu PR.

## Entrega y autoevaluación

Entrega los enlaces a tu rama, tu pull request, la ejecución verde inicial, la roja y la verde corregida; incluye tu breve decisión de diseño y la afirmación de IA que contrastaste. Antes de entregar, comprueba que el último commit está verde y que tu PR **no** incluye el valor erróneo de la prueba temporal.

1. ¿Por qué el responsable se declara tanto en la raíz como en el módulo?
2. ¿Por qué `tofu validate` admite `equipo-lab` en integración y la política lo rechaza?
3. ¿Qué significa `Plan: 2 to add` en un runner sin estado? ¿Se han creado recursos?
4. ¿Qué demuestra el README y el PR sobre trazabilidad, y qué no demuestra una política editable en la misma rama?
5. ¿Qué habría que decidir antes de adoptar este patrón para recursos reales: permisos, secretos, costes, observabilidad, estado, aprobación y reversión?

**Límite de la práctica:** `terraform_data` y su mapa `etiquetas` solo simulan metadatos. No demuestran etiquetado nativo, RBAC, control de costes, observabilidad ni despliegue. Los ejemplos son ficticios y el pipeline nunca ejecuta `tofu apply`.
