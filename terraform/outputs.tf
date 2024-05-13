output "instance_id" {
  value = aws_instance.flask_app.id
}

output "public_ip" {
  value = aws_instance.flask_app.public_ip
}
