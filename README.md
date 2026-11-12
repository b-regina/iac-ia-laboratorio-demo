# Laboratorio de IaC e IA

Proyecto ficticio `portal-demo` para practicar Infraestructura como Código. El código registra un nombre y un entorno mediante `terraform_data`, un recurso integrado en OpenTofu. El workflow calcula un plan y muestra lo que se registraría. No aplica cambios ni crea infraestructura en la nube.

## Primera práctica desde el navegador

1. En tu copia del repositorio, cambia `github.com` por `github.dev` en la URL. Puede abrirse en `vscode.dev`. Abre `variables.tf`.
2. Lee `default = "desarrollo"` y predice qué mostrará el plan. Cambia el valor a `pruebas` y guarda con `Ctrl+S`.
3. Abre Control de código fuente, escribe el mensaje `Ejercicio 1: cambiar entorno a pruebas` y confirma el cambio con **Commit & Push**. Si el editor presenta los pasos por separado, confirma primero y después publica o sincroniza los cambios.
4. En la página de tu repositorio en `github.com`, entra en **Actions** y abre la ejecución de **Validacion IaC** correspondiente a tu commit. Abre el trabajo **comprobar** y consulta las etapas Inicializar, Comprobar formato, Validar y Mostrar plan.
5. En el plan, busca `terraform_data.aplicacion`, `entorno = "pruebas"` y `Plan: 1 to add, 0 to change, 0 to destroy`. En cada ejecución se usa un runner nuevo, así que no conserva el estado de ejecuciones anteriores.

Si no tienes GitHub Copilot disponible, pega el código ficticio en ChatGPT Free y solicita que identifique variable, recurso y salida. Comprueba las afirmaciones mirando los archivos y el resultado del workflow.

Si el editor de `github.dev` pide una autorización que tu cuenta o navegador no permite, puedes hacer el mismo cambio desde `github.com`: abre `variables.tf`, pulsa **Edit this file** (icono del lápiz), modifica el valor y elige **Commit changes**. Después consulta **Actions** como en el paso 4.

Para volver a intentarlo, modifica solo el valor de `entorno`, guarda y confirma un nuevo commit. La guía del ejercicio explica los puntos de control, las incidencias y las preguntas finales.
