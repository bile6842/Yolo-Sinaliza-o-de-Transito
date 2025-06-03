## Configuração do ambiente para treinamento YOLO

Na configuração do ambiente, será utilizado um notebook com processador i7-12700H, GPU GTX 3060 6G, 32GB de memória RAM, armazenamento SSD de 1TB e sistema operacional Ubuntu 22.04. 
No ambiente virtual configurado, serão instalados o framework ULTRALYTICS e demais dependências necessárias para o desenvolvimento do projeto. O HAILO DATAFLOW COMPILER será implementado por meio de uma imagem Docker.

A instalação do framework ULTRALYTICS é realizada por meio do comando apresentado no Quadro. 

```bash
pip install ultralytics
```

A utilização da versão em Docker para o framework HAILO DATAFLOW COMPILER é recomendada para garantir maior compatibilidade. 
Para isso, a imagem do contêiner Docker é obtida no site oficial na versão 2025-04, e os comandos necessários para sua execução estão descritos no Quadro.

1. Adicionar a chave GPG oficial do Docker: 
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg 
```
2. Adicionar o repositório Docker: 
```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null 
```
3. Atualizar a lista de pacotes: 
```bash
sudo apt update 
```
4. Instalar o Docker: 
```bash
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin 
```
5. Adicionando o Container Hailo: 
```bash
docker run --runtime=nvidia --gpus all -it hailo_ai_sw_suite_2025-04:1 /bin/bash 
```

## Treinamento da rede neural

- [Treinamento da rede neural](./docs/Treinamento_da_rede_neural.md)

