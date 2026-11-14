# Ejercicio 1 · demostración docente resuelta

Caso ficticio: `portal-demo`. Esta rama muestra el ejercicio ya terminado para proyectarlo en clase. La configuración solo usa `terraform_data`; GitHub Actions calcula un plan, sin ejecutar `tofu apply` ni desplegar infraestructura comercial.

## Abrir y explicar en clase

[Ver esta rama en GitHub](https://github.com/b-regina/iac-ia-laboratorio-demo/tree/ejercicio-1-solucion) · [Abrir en VS Code Online](https://github.dev/b-regina/iac-ia-laboratorio-demo/tree/ejercicio-1-solucion)

| Archivo | Qué conviene señalar |
| --- | --- |
| `variables.tf` | La variable `entorno` tiene ahora `default = "pruebas"`. Este es el cambio que realiza el alumnado. |
| `main.tf` | `terraform_data.aplicacion` recibe el nombre ficticio `portal-demo` y `var.entorno`. |
| `outputs.tf` | `resumen` apunta a la salida del recurso. El plan indica que su valor se conocería tras una aplicación; aquí no se aplica. |
| `.github/workflows/validacion.yml` | En cada commit, el runner instala OpenTofu y ejecuta `init`, `fmt`, `validate` y `plan`. |

## Comparar el punto de partida con la solución

En el [punto de partida del ejercicio 1](https://github.com/b-regina/iac-ia-laboratorio-demo/tree/65474c0ba004aecb5a02bb88f36a4a144f1eb679), `entorno` valía `"desarrollo"`. El [commit de la solución](https://github.com/b-regina/iac-ia-laboratorio-demo/commit/b9a46514f0f2dce8c529e7ada20fbcdb63be3454) cambia únicamente ese valor a `"pruebas"`. Este README pertenece solo a la rama docente; el punto de partida y la rama principal no se modificaron para preparar esta demostración.

## Mostrar la ejecución real

Abre la [ejecución correcta de la solución](https://github.com/b-regina/iac-ia-laboratorio-demo/actions/runs/43618066643) y entra en el trabajo **comprobar**. Las cuatro comprobaciones terminan correctamente. En **Mostrar plan** aparecen `terraform_data.aplicacion`, `entorno = "pruebas"`, `nombre = "portal-demo"` y `Plan: 1 to add, 0 to change, 0 to destroy`.

**Interpretación:** el runner empieza sin estado previo y describe lo que haría una aplicación. El plan no crea recursos reales. Si se quiere enseñar IA, abre GitHub Copilot o ChatGPT en una segunda pestaña y pide que explique la relación entre `var.entorno`, el recurso y el plan; contrasta la respuesta con estos archivos y los registros.

**Para el alumnado:** utiliza la guía de la práctica y su propio punto de partida. Esta rama es la referencia resuelta para la docente.
