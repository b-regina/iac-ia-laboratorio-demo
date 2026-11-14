# Ejercicio 8 · Demostración docente resuelta

**Esta rama contiene la solución completa del taller final.** Se ha construido sobre el código del ejercicio 7. Úsala para proyectar los archivos y los resultados; el alumnado trabaja en su propio repositorio siguiendo la [guía del ejercicio 8](EJERCICIO_8.md).

## Recorrido para proyectar

1. `variables.tf` y `escenario-integracion.tfvars`: el responsable es `equipo-lab` en pruebas y `equipo-integracion` en integración.
2. `main.tf` y `modulo_ficha/variables.tf`: la raíz pasa el responsable a cada instancia del módulo.
3. `modulo_ficha/main.tf`: cada ficha ficticia incluye `etiquetas` con proyecto, entorno y responsable.
4. `politica_plan.py`: el plan se acepta solo si ambas fichas tienen metadatos coherentes y el responsable corresponde al escenario.
5. **Actions**: compara una [ejecución correcta](https://github.com/b-regina/iac-ia-laboratorio-demo/actions/runs/43619445025), un [rechazo deliberado del responsable en integración](https://github.com/b-regina/iac-ia-laboratorio-demo/actions/runs/43619239686) y la [ejecución corregida](https://github.com/b-regina/iac-ia-laboratorio-demo/actions/runs/43619295702). El fallo y la corrección se hicieron en una rama de ensayo, sin contaminar esta solución.

## Separación de versiones

- [`main`](https://github.com/b-regina/iac-ia-laboratorio-demo/tree/main): plantilla inicial del ejercicio 1.
- [`ejercicio-8-inicio`](https://github.com/b-regina/iac-ia-laboratorio-demo/tree/ejercicio-8-inicio): código del ejercicio 7 terminado, sin resolver el 8.
- **`ejercicio-8-solucion` (esta rama):** resultado docente del ejercicio 8.

Hay **un solo proyecto que evoluciona**. Cada participante usa una copia personal y conserva sus propios cambios entre ejercicios; no necesita copiar una rama docente nueva en cada sesión. Los documentos Word/PDF son instrucciones separadas por ejercicio. Este laboratorio solo planifica recursos `terraform_data`; las etiquetas son metadatos ficticios y **no hay `apply`, credenciales ni despliegue cloud**.
