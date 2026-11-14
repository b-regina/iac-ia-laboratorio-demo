variable "entorno" {
  description = "Entorno del caso ficticio"
  type        = string
  default     = "pruebas"

  validation {
    condition     = contains(["desarrollo", "pruebas", "integracion"], var.entorno)
    error_message = "El entorno debe ser desarrollo, pruebas o integracion."
  }
}

variable "nombre_aplicacion" {
  description = "Nombre ficticio de la aplicacion"
  type        = string
  default     = "portal-demo"

  validation {
    condition     = startswith(var.nombre_aplicacion, "portal-")
    error_message = "El nombre debe comenzar por portal-."
  }
}

variable "responsable" {
  description = "Equipo ficticio responsable de las fichas"
  type        = string
  default     = "equipo-lab"
}
