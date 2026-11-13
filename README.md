# Laboratorio de IaC e IA

Proyecto ficticio `portal-demo` para practicar Infraestructura como Código. OpenTofu usa el recurso incorporado `terraform_data`; GitHub Actions ejecuta comprobaciones y calcula un plan. No hay `apply`, credenciales ni infraestructura cloud comercial.

## Ejercicio 1: mi primer cambio de infraestructura como código

**Meta:** cambiar el entorno de `desarrollo` a `pruebas` y explicar qué propone OpenTofu. El alumno necesita solo GitHub.com en el navegador y su propia copia pública de esta plantilla.

1. En tu copia, abre `variables.tf`. Comprueba que pone `default = "desarrollo"`.
2. Pulsa el lápiz **Edit this file**. Sustituye únicamente `desarrollo` por `pruebas`.
3. Pulsa **Commit changes...**, escribe `Ejercicio 1: cambiar entorno a pruebas` y confirma el cambio en tu copia.
4. En la pestaña **Actions**, abre la ejecución de **Validacion IaC** que corresponde a ese commit. Entra en el trabajo **comprobar** y observa **Inicializar**, **Comprobar formato**, **Validar** y **Mostrar plan**.
5. Comprueba que el plan muestra `entorno = "pruebas"` y `Plan: 1 to add, 0 to change, 0 to destroy`. El runner comienza sin estado anterior en cada ejecución; el plan no aplica cambios.

**IA en el primer ejercicio:** la docente muestra en directo cómo preguntar a Copilot Chat o ChatGPT qué relación tienen `variables.tf`, `main.tf` y `outputs.tf`. Los participantes comparan la respuesta con los archivos y el plan. La IA no necesita modificar el repositorio; el primer objetivo es entender y comprobar el cambio. En una práctica posterior se incorporará su uso autónomo.

**Editor opcional:** quien quiera practicar con `github.dev` puede abrir su copia allí, guardar `variables.tf` y usar **Source Control → Commit & Push**. El editor web no tiene terminal. El modo Agente integrado y la ejecución local de OpenTofu no forman parte de este ejercicio; OpenTofu se ejecuta en Actions.

Si Actions falla, abre el paso marcado en rojo y lee la línea del error antes de corregir y confirmar un nuevo commit. No introduzcas errores deliberados en la rama principal de la plantilla docente.
