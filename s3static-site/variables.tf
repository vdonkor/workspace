variable index_document {
  description = "name of the home page file"
  type = string
  default = "index.html"
}
variable "error_document" {
  description = "name of the error document"
  type = string
  default = "error.html"
}
variable app {
  description = "name of the static website"
  default = ""
  type = string
}
variable "domain" {
  description = "domain name for the website"
  type = string
  default = "example.com"
}
variable "stack_name" {
  description = "name of the project"
  type = string
  default = "echs"
}