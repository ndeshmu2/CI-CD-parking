resource "aws_instance" "flask_app" {
  ami           = "ami-07caf09b362be10b8"  # Replace with the AMI ID you want to use
  instance_type = "t2.micro"
  key_name      = "assessment"  # SSH key name

  tags = {
    Name = "FlaskApp"
  }
}
