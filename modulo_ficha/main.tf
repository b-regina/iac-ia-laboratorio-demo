resource "terraform_data" "ficha" {
  input = {
    nombre  = var.nombre
    entorno = var.entorno
  }
}
