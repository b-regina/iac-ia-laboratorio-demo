resource "terraform_data" "aplicacion" {
  input = {
    nombre  = "portal-demo"
    entorno = var.entorno
  }
}
