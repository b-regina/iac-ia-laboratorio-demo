# Ejercicio 8 · Punto de partida

**Estás viendo una rama docente de referencia.** El código técnico corresponde al ejercicio 7 terminado: dos fichas ficticias (`portal` y `ayuda`), dos escenarios, un módulo reutilizable y una política que revisa el plan. Todavía no incluye las etiquetas ni el control de responsables del ejercicio 8.

## Si eres alumno o alumna

1. Abre **tu propio repositorio**, el mismo que usaste en los ejercicios anteriores. Selecciona la rama donde terminaste el ejercicio 7.
2. Crea allí una rama nueva llamada `taller-final-ejercicio-8`. **No crees otra copia ni edites esta rama docente.**
3. Sigue la [guía paso a paso del ejercicio 8](EJERCICIO_8.md) o el Word/PDF entregado en clase. Edita los seis archivos indicados en **tu rama** desde github.dev o, si está permitido, VS Code local.
4. Publica tus commits y consulta **Actions en tu propio repositorio**. La guía te llevará por una ejecución correcta, un fallo deliberado de la política y su corrección.

**Punto de control antes de empezar:** tu `main.tf` ya contiene `module "fichas"` con `for_each`, y existen `modulo_ficha/`, `politica_plan.py` y `escenario-integracion.tfvars`. Si aún no están, termina primero el ejercicio 7.

## Qué vas a conseguir

Cada ficha tendrá tres metadatos didácticos: proyecto, entorno y responsable. El plan de integración utilizará `equipo-integracion`; una asignación incorrecta se podrá planificar, pero la política la rechazará. Los recursos son `terraform_data` ficticios. El workflow calcula planes y **no ejecuta `tofu apply` ni despliega servicios cloud**.

**Para orientarte en este repositorio docente:** `main` conserva la plantilla inicial del ejercicio 1; `ejercicio-8-inicio` es la referencia de entrada de este taller. Tu trabajo y tus commits viven siempre en tu propia copia.
