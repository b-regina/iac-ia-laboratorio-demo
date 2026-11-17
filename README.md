# Laboratorio de IaC e IA · empieza por aquí

Este repositorio contiene **un único proyecto ficticio**, `portal-demo`. Vas a trabajar en **una copia propia** del repositorio durante todos los ejercicios. Cada ejercicio amplía lo que hiciste en el anterior. Al principio solo existe el código necesario para el ejercicio 1; los demás archivos aparecerán cuando tú los crees.

## Tu primer paso

1. Descarga y abre la [Guía del ejercicio 1 (Word)](GUIAS/Guia_Alumnado_Ejercicio_1.docx?raw=1). Léela desde el principio: incluye los botones para crear tu copia y comprobarla.
2. En esta página pulsa **Use this template → Create a new repository**. En **Owner** elige tu usuario, deja **Include all branches** desmarcado y crea un repositorio público con otro nombre. **Hazlo una sola vez.**
3. Comprueba que la URL de tu copia empieza por `https://github.com/TU_USUARIO/`. A partir de aquí, todos tus cambios irán a esa copia.
4. Abre **Actions** en tu copia. Si aparece **Validacion IaC → Commit inicial → comprobar** en verde, el laboratorio ya ejecutó OpenTofu en GitHub. La guía explica qué hacer si no aparece.
5. Continúa la guía del ejercicio 1: abre **tu copia** en `github.dev`, cambia `variables.tf`, confirma y publica el cambio, y consulta la nueva ejecución de Actions.

**No necesitas instalar GitHub Actions, OpenTofu, Git ni VS Code en tu equipo para la ruta de navegador.** GitHub Actions es una pestaña de GitHub; el workflow instala OpenTofu en un ejecutor temporal. `github.dev` es el editor web. Abre ChatGPT o Copilot Chat en **otra pestaña** para preguntar, predecir y revisar. Usa solo datos ficticios.

## Guías de ejercicios

| Orden | Guía | Qué harás en la misma copia |
| --- | --- | --- |
| 1 | [Puesta en marcha, IA y primer plan](GUIAS/Guia_Alumnado_Ejercicio_1.docx?raw=1) | Crear la copia, comprender tres archivos, cambiar un entorno y leer el resultado. |
| 2 | [Dos escenarios](GUIAS/Guia_Alumnado_Ejercicio_2.docx?raw=1) | Parametrizar la configuración y comparar dos planes. |
| 3 | [Revisión y gobierno](GUIAS/Guia_Alumnado_Ejercicio_3.docx?raw=1) | Crear una rama, añadir validaciones y revisar un pull request. |
| 4 | [Automatización y evidencias](GUIAS/Guia_Alumnado_Ejercicio_4.docx?raw=1) | Mejorar el workflow y diagnosticar un fallo real de la práctica. |
| 5 | [Módulo reutilizable](GUIAS/Guia_Alumnado_Ejercicio_5.docx?raw=1) | Crear un módulo local y usarlo para dos fichas ficticias. |
| 6 | [Política automática sobre el plan](GUIAS/Ejercicio_6.md) | Revisar con IA y Python dos planes; comprobar un rechazo y su corrección. |
| 7 | [Catálogo reutilizable y control](GUIAS/Ejercicio_7.md) | Convertir dos módulos en un catálogo, adaptar la política y comprobar una tercera ficha rechazada. |
| 8 | [Taller final de IaC gobernada](GUIAS/Ejercicio_8.md) | Añadir etiquetas y equipos responsables ficticios, verificar dos escenarios y corregir un rechazo de política. |
| 9 (ampliación) | [Comparar dos planes antes de promocionar](GUIAS/Ejercicio_9.md) | Comparar pruebas e integración con un criterio versionado; comprobar un rechazo y su corrección. |

**El ejercicio 2 empieza donde dejaste el 1**; no crees otra copia. Sigue el mismo principio para los siguientes. Las guías están en `GUIAS/`; el código que editarás está en la raíz y en `.github/workflows/`.

**Si ya creaste tu copia:** las guías añadidas posteriormente a esta plantilla no se incorporan automáticamente a ella. Abre los enlaces de las guías 6 a 9 desde aquí, continúa en tu copia personal y crea allí solo los archivos y cambios que pide la práctica. No vuelvas a clonar, no borres los ejercicios anteriores y no copies una rama resuelta.

## Qué son los archivos iniciales

| Archivo | Función |
| --- | --- |
| `variables.tf` | Declara el entorno, inicialmente `desarrollo`. |
| `main.tf` | Describe una ficha ficticia con `terraform_data`. |
| `outputs.tf` | Define el resumen del plan. |
| `.github/workflows/validacion.yml` | Instala OpenTofu y ejecuta las comprobaciones en GitHub Actions. |

El workflow calcula un plan, **no ejecuta `tofu apply`** y no crea una web ni infraestructura comercial. Si tu equipo permite VS Code local, puedes usarlo con **esa misma copia**: el código y la comprobación en Actions son los mismos. La ruta principal, explicada paso a paso en las guías de `GUIAS/`, funciona desde el navegador.
