provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "ml_api_server" {
  ami                         = "ami-0c02fb55956c7d316"
  instance_type               = "t3.micro"
  monitoring                  = true
  associate_public_ip_address = false

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required"
  }

  root_block_device {
    encrypted   = true
    volume_type = "gp3"
  }

  tags = {
    Name        = "ML-Docker-Orchestrator-Server"
    Environment = "production"
  }
}
