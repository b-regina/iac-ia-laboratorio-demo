# Ejercicio 9 · Demostración docente resuelta

**Ampliación opcional** sobre el taller final de las 25 horas. Esta rama conserva el mismo proyecto y añade una comparación entre el plan de pruebas y el de integración. La [guía de alumnado](EJERCICIO_9.md) se realiza en la copia personal de cada participante.

## Guion para proyectar

1. `criterio-promocion.json`: nombre y responsable esperados en el caso ficticio.
2. `revision_promocion.py`: extrae dos fichas de cada plan y compara los escenarios con el criterio.
3. `.github/workflows/validacion.yml`: tras los dos planes y las dos políticas individuales, genera JSON temporales y ejecuta la revisión conjunta. El resumen muestra su resultado.
4. Actions: compara la [ejecución verde de la solución](https://github.com/b-regina/iac-ia-laboratorio-demo/actions/runs/43623583790), la [rama de ensayo con `portal-ensayo`](https://github.com/b-regina/iac-ia-laboratorio-demo/actions/runs/43623629249) (políticas individuales verdes y revisión conjunta roja) y la [corrección verde](https://github.com/b-regina/iac-ia-laboratorio-demo/actions/runs/43623714152).

La versión sin resolver está en [`ejercicio-9-inicio`](https://github.com/b-regina/iac-ia-laboratorio-demo/tree/ejercicio-9-inicio). `main` continúa como plantilla inicial del ejercicio 1. Cada alumno mantiene **un único repositorio personal** durante los ejercicios; estas ramas docentes son referencias, no copias nuevas que deban importar.

El criterio es editable con el código: su aprobación real requeriría protección y revisión independientes. El pipeline solo calcula planes de `terraform_data`. **No ejecuta `tofu apply` ni despliega infraestructura.**
