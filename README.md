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

## Ejercicio 5  Módulo local reutilizable

Esta rama docente continúa `ejercicio-4-solucion`: las dos llamadas de `main.tf` reutilizan `modulo_ficha` para fichas ficticias del portal y de ayuda. `variables.tf` y `escenario-integracion.tfvars` mantienen los dos escenarios anteriores. El workflow comprueba también el formato de la carpeta nueva con `tofu fmt -check -diff -recursive`.

[Guía completa del ejercicio 5](EJERCICIO_5.md). Para el alumnado se recomienda seguirla en su propia copia tras terminar los ejercicios anteriores. El código de esta rama es el solucionario docente. El pipeline solo calcula planes: no ejecuta `apply` ni despliega servicios.

## Ejercicio 6  Política didáctica del plan

Esta rama continúa la solución del ejercicio 5. `politica_plan.py` revisa en cada escenario el plan temporal: solo dos fichas ficticias `terraform_data`, nombres admitidos y el mismo entorno para portal y ayuda. El workflow registra las dos políticas en el resumen. [Guía paso a paso del ejercicio 6](EJERCICIO_6.md).

Los archivos `.tfplan` se crean solo durante la ejecución y ya están excluidos del repositorio. No se sube el JSON ni se ejecuta `apply`. La política es editable junto al código y tiene valor didáctico; una implantación real precisaría reglas protegidas, revisión humana y controles adicionales.

## Ejercicio 7  Catálogo reutilizable

Esta rama docente continúa el ejercicio 6. Un mapa local reúne `portal` y `ayuda`, y una única llamada a `modulo_ficha` usa `for_each` para planificar las dos fichas ficticias. La salida `resumen` conserva las claves del catálogo. La política reconoce las nuevas direcciones de las instancias y sigue permitiendo exactamente dos fichas. [Guía paso a paso del ejercicio 7](EJERCICIO_7.md).

La rama de ensayo añade una tercera entrada y demuestra que el plan puede calcular tres altas mientras la política rechaza el cambio; después se corrige. No se ejecuta `apply`. En un entorno con estado persistente, cambiar direcciones de módulos requeriría planificar la migración del estado.
