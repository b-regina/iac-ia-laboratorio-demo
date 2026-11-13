# Ejercicio 2. Una configuración para dos escenarios

## Por qué hacemos esta práctica

En el ejercicio 1 cambiaste el entorno de una aplicación ficticia de `desarrollo` a `pruebas` y comprobaste el resultado en GitHub Actions. Ahora un equipo ficticio quiere usar **la misma configuración** para describir dos escenarios, sin copiar el proyecto ni crear otra carpeta.

Aprenderás a separar los valores del código: `variables.tf` declara parámetros, `main.tf` los utiliza y `escenario-integracion.tfvars` les da valores distintos para un plan concreto. Git guarda dos decisiones en dos commits. OpenTofu solo calcula planes: **no se ejecuta `tofu apply` ni se despliega infraestructura**.

**Duración orientativa:** 75 a 100 minutos. **Requisitos:** tu copia personal del ejercicio 1, navegador y una segunda pestaña de IA. VS Code local y Git son opcionales si tu equipo los permite. Sigue usando tu propia copia: `https://github.com/TU_USUARIO/iac-ia-practica-tuusuario`.

## Antes de editar

1. Abre tu copia en GitHub y confirma que estás en la rama `main`. En `variables.tf`, la línea `default` de `entorno` debe contener `"pruebas"`. Si hiciste el reto opcional del ejercicio 1 y ahora pone `integracion`, vuelve a `pruebas` con un commit antes de empezar.
2. Comprueba que el último workflow **Validacion IaC** de tu rama terminó en verde. Abre `main.tf`, `variables.tf`, `outputs.tf` y `.github/workflows/validacion.yml`. Son los mismos archivos que ya conoces.
3. En otra pestaña, abre GitHub Copilot Chat o ChatGPT. Puedes preguntarle: «En este código ficticio, ¿qué diferencia hay entre declarar una variable, usar `var.nombre_aplicacion` y darle otro valor mediante un archivo `.tfvars`? Indica qué dos planes esperas ver. No propongas recursos cloud ni `tofu apply`.». Verifica la respuesta con el código y los registros.

## Parte A. Convierte el nombre en un parámetro

**Predicción.** En el primer commit el plan deberá conservar `nombre = "portal-demo"` y `entorno = "pruebas"`, aunque el nombre ya no esté escrito directamente en `main.tf`.

1. Abre tu copia con `github.dev` cambiando el dominio en la dirección. Si se abre `vscode.dev`, continúa. En el explorador, abre `variables.tf`.
2. Al final de `variables.tf`, añade este bloque sin modificar la variable `entorno`:

   ```hcl
   variable "nombre_aplicacion" {
     description = "Nombre ficticio de la aplicacion"
     type        = string
     default     = "portal-demo"
   }
   ```

3. En `main.tf`, sustituye únicamente `nombre = "portal-demo"` por `nombre = var.nombre_aplicacion`. Conserva la línea `entorno = var.entorno`.
4. Guarda ambos archivos con `Ctrl+S`. En **Source Control**, revisa que solo cambian `main.tf` y `variables.tf`. Escribe `Ejercicio 2A: parametrizar nombre`, confirma el commit y publica con **Push** o **Sync Changes**.
5. Vuelve a GitHub.com → tu copia → **Actions** → **Validacion IaC** → ejecución de ese commit → trabajo **comprobar**. Las cuatro etapas deben ser verdes. Abre **Mostrar plan** y busca el nombre y el entorno previstos. Si el plan no aparece, lee la primera etapa que falló antes de editar nada más.

**Qué has conseguido.** El nombre se lee desde una variable. El valor predeterminado mantiene el mismo resultado observable, y el cambio queda documentado en Git.

## Parte B. Usa la misma configuración con otros valores

**Predicción.** El plan normal mostrará `portal-demo` y `pruebas`. El plan que lee el archivo de escenario mostrará `portal-interno` e `integracion`. Ninguno crea un servicio real.

1. En la raíz del repositorio, crea un archivo llamado **exactamente** `escenario-integracion.tfvars`. Debe quedar al lado de `main.tf`, no dentro de `.github`. Escribe:

   ```hcl
   entorno           = "integracion"
   nombre_aplicacion = "portal-interno"
   ```

2. Abre `.github/workflows/validacion.yml`. Al final, deja las primeras etapas como estaban y sustituye solo el paso **Mostrar plan** por estos dos pasos, respetando los espacios:

   ```yaml
      - name: Plan con valores por defecto
        run: tofu plan -input=false -no-color
      - name: Plan del escenario integracion
        run: tofu plan -input=false -no-color -var-file=escenario-integracion.tfvars
   ```

   Los guiones de los pasos deben quedar alineados con `- name: Validar`. No añadas tabuladores. El nombre después de `-var-file=` debe coincidir exactamente con el archivo que creaste.

3. Guarda, comprueba las diferencias en **Source Control** y confirma `Ejercicio 2B: segundo escenario sin duplicar codigo`. Publica el commit.
4. En **Actions**, abre la ejecución de ese segundo commit. Consulta por separado **Plan con valores por defecto** y **Plan del escenario integracion**. En el primero busca `portal-demo` y `pruebas`; en el segundo busca `portal-interno` e `integracion`. Anota las dos parejas de valores.

**Qué significa el resultado.** `default` aporta un valor cuando el plan no recibe otro. `-var-file` carga los valores del escenario para **esa ejecución del comando**. Los dos pasos usan los mismos archivos `.tf`; no son dos proyectos. GitHub Actions descarga OpenTofu en el runner y ejecuta `init`, `fmt`, `validate` y ambos planes. Como el runner no conserva un estado aplicado y no se llama a `apply`, cada plan puede decir `1 to add` sin que exista una aplicación desplegada.

## Si eliges VS Code local

Abre la **misma copia personal** que clonaste en el ejercicio 1. Antes de editar, pulsa **Pull** o **Sync Changes** para traer tus cambios publicados. Realiza las partes A y B con los mismos archivos, mensajes de commit y comprobaciones. Publica cada commit con **Push**; los commits que solo están en el ordenador no activan Actions. OpenTofu local no es necesario para este ejercicio. Si Git o VS Code no están permitidos en tu equipo, sigue con `github.dev`.

## Errores que puedes resolver

| Lo que ves | Qué comprobar |
| --- | --- |
| `Reference to undeclared input variable` | En `variables.tf` debe existir `variable "nombre_aplicacion"` y en `main.tf` debe escribirse `var.nombre_aplicacion`. |
| `No value for required variable` | La nueva variable debe conservar `default = "portal-demo"` en esta práctica. |
| `Failed to read variables file` | El nombre y la ubicación de `escenario-integracion.tfvars` deben coincidir con `-var-file=...`. |
| Falla `Comprobar formato` | Compara sangrías, guarda el archivo y corrige el espaciado HCL. El editor web no tiene terminal; la etapa muestra el archivo afectado. |
| El workflow no muestra los dos planes | Comprueba que editaste `.github/workflows/validacion.yml` en **tu copia** y publicaste el segundo commit. |
| Falla el YAML | Alinea cada `- name:` con los demás pasos y usa espacios, no tabuladores. |

## Reto y entrega

En tu propia copia, cambia solo `nombre_aplicacion` en `escenario-integracion.tfvars` por `"portal-equipo"`. Predice qué plan cambiará. Confirma el cambio y compruébalo en Actions. No modifiques la plantilla docente.

Entrega a la docente **el enlace a tu repositorio**, los enlaces a los dos commits A y B y el enlace a la ejecución verde del segundo commit. Explica en tres frases: qué valor usa el plan normal, qué valores reemplaza el escenario y por qué no se ha desplegado nada.

**Preguntas finales.** ¿Por qué el primer plan conserva `portal-demo` aunque ya no aparezca como literal en `main.tf`? ¿Qué ocurriría si escribieras otro nombre en el `.tfvars` sin editar `main.tf`? ¿Qué diferencias hay entre guardar, confirmar y publicar? ¿Cuál de los dos planes usaría `integracion` si quitas `-var-file`?

**Continuidad.** Conserva tu repositorio y sus commits: las siguientes prácticas ampliarán este mismo proyecto.
