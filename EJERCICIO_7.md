# Ejercicio 7  Un catálogo reutilizable con control de cambios

**Duración orientativa:** 90 a 120 minutos. **Punto de partida:** tu copia personal con el ejercicio 6 terminado y sus dos escenarios en verde. **Herramientas:** navegador, GitHub, github.dev y una pestaña separada de Copilot o ChatGPT. No necesitas terminal, OpenTofu ni VS Code instalados.

## La historia y la finalidad

En la organización ficticia Nexo Portal, el portal y su ficha de ayuda se describen con el mismo módulo. En el ejercicio 5 escribiste dos llamadas casi iguales; en el 6 añadiste una política que admite exactamente esas dos fichas. Ahora el equipo quiere un **catálogo pequeño** que enumere las fichas por nombre. Una sola llamada al módulo leerá el catálogo y preparará una instancia para cada entrada. El equipo también exige que la política siga comprobando qué fichas están permitidas.

El objetivo es entender el patrón `for_each` y la relación entre **reutilización** y **gobierno**. El resultado visible será un plan con dos fichas, una salida `resumen` ordenada por claves, una ejecución roja al solicitar una tercera ficha no aprobada y una ejecución verde después de retirarla. Solo se calculan planes de `terraform_data`: no hay `apply`, credenciales, suscripciones ni infraestructura cloud.

**Qué significa cada palabra.** Un `local` da nombre a un valor dentro de esta configuración. Un **mapa** asocia claves (`portal`, `ayuda`) con nombres. `for_each` crea una instancia del módulo por cada clave. La clave queda en la dirección del plan; el valor se entrega al módulo como `each.value`. La salida `resumen` reúne las salidas de esas instancias. Esto ilustra una idea de catálogo interno, pero no crea un servicio de autoservicio real.

## Antes de editar

1. Abre **tu propia copia** en GitHub.com. Comprueba que contiene `modulo_ficha/`, `politica_plan.py`, `escenario-integracion.tfvars` y `.github/workflows/validacion.yml`. Si falta alguno, recupera el ejercicio anterior antes de continuar. No trabajes en la plantilla de la docente.
2. Parte de tu rama final del ejercicio 6 o de tu `main` **si ya incorporaste ese ejercicio**. En GitHub.com, abre el selector de ramas y crea `catalogo-ejercicio-7` desde esa rama. Anota de cuál has partido.
3. En la URL de **tu copia**, cambia `github.com` por `github.dev` y pulsa Intro. Si se redirige a `vscode.dev`, continúa. En el explorador verás la raíz, `modulo_ficha/` y `.github/`. El trabajo se hace con el editor, sin terminal.
4. Abre una segunda pestaña con tu IA disponible. Usa solo los nombres ficticios del laboratorio. Si no tienes Copilot, utiliza ChatGPT; no dependes del agente integrado en VS Code Web.

**Punto de control:** lee el `main.tf` actual. Debe tener `module "portal"` y `module "ayuda"` con `source = "./modulo_ficha"`. En el plan del ejercicio 6, esas direcciones eran `module.portal.terraform_data.ficha` y `module.ayuda.terraform_data.ficha`. Predice qué cambiará en el nombre de las direcciones cuando las instancias tengan claves.

## Paso 1  Define el catálogo y reutiliza el módulo

En `main.tf` de la **raíz** reemplaza las dos llamadas al módulo por este contenido completo. No modifiques `modulo_ficha/main.tf`:

```hcl
locals {
  catalogo = {
    portal = var.nombre_aplicacion
    ayuda  = "portal-ayuda"
  }
}

module "fichas" {
  for_each = local.catalogo
  source   = "./modulo_ficha"
  nombre   = each.value
  entorno  = var.entorno
}
```

**Lee línea a línea.** `local.catalogo` contiene exactamente dos claves. `for_each` recorre ambas. Cada instancia usa la misma carpeta `./modulo_ficha`; `each.value` será `portal-demo` para `portal` en el escenario por defecto y `portal-ayuda` para `ayuda`. `var.entorno` llega igual a las dos fichas. En integración, `var.nombre_aplicacion` toma el valor de `escenario-integracion.tfvars`.

**Punto de control:** hay **un bloque module y dos entradas en el mapa**. No crees otra carpeta ni dupliques el módulo. El valor `each.key` sería `portal` o `ayuda`; aquí no hace falta escribirlo porque OpenTofu ya identifica las instancias por esas claves.

## Paso 2  Construye una salida legible

Abre `outputs.tf` de la raíz y reemplaza el bloque `output "resumen"` anterior por:

```hcl
output "resumen" {
  description = "Catalogo de fichas ficticias previsto para este entorno"
  value = {
    for clave, ficha in module.fichas : clave => ficha.resumen
  }
}
```

`module.fichas` es ahora un mapa de instancias. La expresión `for` conserva la clave del catálogo y toma `resumen` de cada módulo. El nombre de salida externa sigue siendo `resumen`, así que sabes dónde encontrarla en el plan. **No confundas este bloque `for` con `for_each`:** el primero construye el valor de salida; el segundo crea instancias del módulo.

**Predicción antes del commit:** en el escenario por defecto, el plan debería indicar `Plan: 2 to add`, `module.fichas["portal"]`, `module.fichas["ayuda"]`, los nombres `portal-demo` y `portal-ayuda`, y el entorno `pruebas`. En integración, `portal-interno` y `portal-ayuda` usarán `integracion`. Una salida de plan expresa valores **previstos**, no recursos aplicados.

## Paso 3  Adapta la política existente

Si confirmaras ya, la política del ejercicio 6 rechazaría las nuevas direcciones aunque haya dos fichas correctas. En `politica_plan.py` cambia **solo** las direcciones esperadas al principio:

```python
ESPERADOS = {
    'module.fichas["portal"].terraform_data.ficha',
    'module.fichas["ayuda"].terraform_data.ficha',
}
```

En la comprobación del nombre de ayuda, sustituye la clave del diccionario `valores` por la nueva dirección. La condición completa queda:

```python
if valores['module.fichas["ayuda"].terraform_data.ficha']["nombre"] != "portal-ayuda":
    rechazar("la ficha de ayuda debe llamarse portal-ayuda")
```

Conserva el resto: dos recursos `terraform_data`, solo acción `create`, entradas `nombre` y `entorno`, nombres con prefijo `portal-`, ayuda fija y entornos iguales. Las comillas simples externas de Python permiten incluir `"ayuda"` dentro de la dirección. No incluyas datos reales ni planes JSON en una IA.

**Punto de control:** busca `module.portal` y `module.ayuda` dentro de `politica_plan.py`; ya no deben aparecer. En cambio `module.fichas` debe estar en `ESPERADOS` y en la comprobación de ayuda. El workflow del ejercicio 6 **no se modifica**: sigue produciendo dos planes y pasando sus JSON a la política.

## Paso 4  Usa la IA como revisora

En la segunda pestaña, utiliza este prompt:

> Revisa este cambio didáctico de OpenTofu: un mapa local con las claves portal y ayuda alimenta `module "fichas"` mediante `for_each`; la salida `resumen` usa una expresión `for`. La política Python debe permitir exactamente `module.fichas["portal"].terraform_data.ficha` y `module.fichas["ayuda"].terraform_data.ficha`. Explica en lenguaje sencillo qué cambia en las direcciones del plan, si dos fichas mantienen los escenarios pruebas e integracion, y qué sucedería al añadir una tercera clave `informes` sin revisar la política. Señala una limitación del laboratorio. No propongas proveedores cloud, `apply`, permisos adicionales ni datos sensibles. Indica qué afirmaciones hay que comprobar en Actions.

Apunta una afirmación de la IA que después verificarás. La respuesta es una hipótesis; los logs y el plan de tu propia copia son la evidencia.

## Paso 5  Publica y comprueba los dos escenarios

1. Guarda los tres archivos con `Ctrl+S`. En **Source Control**, comprueba que solo cambian `main.tf`, `outputs.tf` y `politica_plan.py`. Escribe el mensaje `Ejercicio 7: catalogo de fichas reutilizable`. Confirma con **Commit & Push**. Si el editor separa Commit de Push/Sync, realiza ambos.
2. En GitHub.com → **tu repositorio** → **Actions** → **Validacion IaC**, abre la ejecución del commit y el trabajo **comprobar**. Espera a que termine. Deben pasar `Inicializar`, `Comprobar formato`, `Validar`, los dos planes, las dos políticas y los pasos de evidencia.
3. Abre `Plan con valores por defecto` y localiza ambas direcciones con `module.fichas["…"]`, `Plan: 2 to add, 0 to change, 0 to destroy` y `Changes to Outputs: resumen`. Compara las claves, nombres y `pruebas`.
4. En `Plan del escenario integracion` verifica `portal-interno`, `portal-ayuda` e `integracion`. Abre los dos pasos de política y busca `POLÍTICA APROBADA`. Si algo falla, lee **el primer paso rojo**; no interpretes un paso omitido como un rechazo de la política.
5. Copia el enlace de la ejecución verde. En `Summary` verás los seis resultados; `evidencia.txt` conserva el resumen durante siete días. Los planes temporales y su JSON no se publican como artefacto.

**Interpretación:** `for_each` hace reutilizable el código para estas dos entradas; la política deja visible que el catálogo aprobado tiene un alcance exacto. El plan muestra lo que OpenTofu haría; el workflow nunca ejecuta `tofu apply`.

## Paso 6  Pide una tercera ficha y observa el control

En **la misma rama de tu copia**, añade temporalmente una entrada al mapa de `main.tf`. Respeta la alineación:

```hcl
  catalogo = {
    portal   = var.nombre_aplicacion
    ayuda    = "portal-ayuda"
    informes = "portal-informes"
  }
```

Antes de confirmar, responde: ¿cuántas instancias se planificarán?, ¿pasará `tofu validate`?, ¿aprobará la política que espera exactamente dos fichas? Publica el commit `Prueba: tercera ficha sin aprobar` y abre **su nueva ejecución** de Actions.

**Resultado que debes observar:** formato y validación verdes, primer plan verde con `Plan: 3 to add` y dirección `module.fichas["informes"].terraform_data.ficha`, pero `Politica del plan predeterminado` roja con `POLÍTICA RECHAZADA: se esperan exactamente las fichas portal y ayuda`. Los pasos posteriores normales se omiten; el resumen y el artefacto pueden completarse por `always()`, pero **el trabajo es rojo**. Guarda el enlace. Si falla `Comprobar formato`, corrige primero la alineación y repite: todavía no habrías probado la política.

**Decisión de gobierno:** una tercera ficha no está aprobada por esta regla docente. En este ejercicio la retiras. En una adopción real, ampliar el catálogo exigiría acordar requisitos, actualizar y proteger la política y revisar su efecto en el estado y las aprobaciones; no basta con cambiar una lista.

## Paso 7  Corrige y documenta

1. Retira solo la línea `informes` y devuelve las dos líneas anteriores al formato del paso 1. Confirma `Correccion: catalogo de dos fichas`. Comprueba que **una tercera ejecución** vuelve a mostrar dos planes y dos políticas verdes. Guarda su enlace.
2. Añade a **tu README** una sección `## Catálogo de fichas`: explica qué claves contiene, para qué sirve `for_each`, qué muestra `resumen`, por qué el tercer elemento falló en la política y que aquí no existe despliegue ni autoservicio real. Confirma ese texto en un commit; comprueba también su ejecución.
3. Crea un **pull request en tu propia copia** desde `catalogo-ejercicio-7` hacia la rama que usaste como punto de partida (o hacia tu `main` ya actualizada). En `Files changed` confirma los tres archivos técnicos y el README. Incluye los enlaces de la primera ejecución verde, la roja y la verde corregida; explica tu predicción, el primer paso que falló y tu revisión de la IA. Puedes dejarlo en borrador para revisión docente. No apuntes el PR a la cuenta de la docente.

## Si algo no coincide

| Síntoma | Revisión concreta |
| --- | --- |
| `Reference to undeclared module` | En `outputs.tf` usa `module.fichas`, no `module.portal` ni `module.ayuda`. |
| Primer plan verde y política roja tras el primer commit | Comprueba las dos direcciones de `ESPERADOS` y la clave `valores` de la ayuda. |
| `SyntaxError` en la política | Usa comillas simples alrededor de la dirección que contiene `"ayuda"`. |
| `tofu fmt` falla al añadir `informes` | Alinea las tres asignaciones como en el ejemplo; mira el diff de formato. |
| Plan de tres fichas, política no ejecutada | Busca el primer paso anterior que falló; un paso omitido no equivale a rechazo. |
| La ejecución parece verde pero era el commit anterior | Comprueba el SHA o el mensaje del commit en Actions. Cada commit tiene su propia ejecución. |
| github.dev no abre en tu equipo | Si GitHub.com permite editar, usa el lápiz y `Commit changes`; sigue consultando Actions. Si la organización bloquea Actions, observa la demo docente y anota que tu ejecución individual queda pendiente. |

**Plan B local autorizado:** si ya tienes VS Code y Git o tu equipo permite instalarlos, abre **la misma copia** en VS Code local, crea la rama, edita los mismos tres archivos, confirma y publica. GitHub Actions sigue siendo la evidencia común; OpenTofu y Python local no son obligatorios. No instales nada en un equipo corporativo sin autorización. La IA permanece en otra pestaña si el agente local no está disponible.

## Entrega y preguntas

Entrega los enlaces a **tu copia**, **tu PR**, **la ejecución verde inicial**, **la roja** y **la verde corregida**. En cinco frases explica la necesidad, el efecto de `for_each`, el papel de `resumen`, por qué un plan válido puede incumplir la política y qué parte verificaste tú frente a la sugerencia de la IA.

1. ¿Qué diferencia hay entre la clave `ayuda` y el valor `portal-ayuda`?
2. ¿Por qué cambió `module.ayuda.terraform_data.ficha` por `module.fichas["ayuda"].terraform_data.ficha`?
3. ¿Qué construye la expresión `for` en `outputs.tf` y qué crea `for_each` en `main.tf`?
4. ¿Por qué `tofu validate` y `tofu plan` aceptaron `informes` mientras la política lo rechazó?
5. ¿Qué habría que revisar antes de cambiar direcciones de recursos en un entorno que ya tiene estado y recursos aplicados?

**Reto opcional:** en otra rama de tu copia, cambia temporalmente el nombre de la ayuda a `portal-asistencia` sin añadir una tercera clave. Predice qué controles pasan y qué texto rechaza el plan; verifica el fallo y restaura el nombre. No mezcles este reto con tu PR principal.

**Límite profesional:** cambiar direcciones de módulos en una infraestructura ya aplicada puede requerir migrar estado. Aquí solo existe un plan efímero, sin `apply` ni estado persistente. Un catálogo, una política editable en la misma rama y un plan aprobado no equivalen a una plataforma interna ni a un control de producción.
