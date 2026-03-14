resource "aws_ecr_repository" "backend" {
  name                 = "gps-backend"
  image_tag_mutability = "MUTABLE"
  force_delete         = true
}
resource "aws_ecr_repository" "frontend" {
  name                 = "gps-frontend"
  image_tag_mutability = "MUTABLE"
  force_delete         = true
}