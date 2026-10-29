FROM jenkins/jenkins:lts-jdk17

USER root

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    sudo \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://get.docker.com | sh

RUN usermod -aG docker jenkins

RUN echo "jenkins ALL=(ALL) NOPASSWD: /bin/chmod" >> /etc/sudoers

USER jenkins