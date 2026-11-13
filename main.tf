resource "terraform_data" "aplicacion" {
  input = {
    nombre  = var.nombre_aplicacion
    entorno = var.entorno
  }
}
