# E-commerce simulation project

## Arquitetura

O sistema segue os seguintes paradigmas:
- DDD = Domain-Driven Design
- EDA = Event-Driven Architecture
- OOP = Object-Oriented Programming
- SOLID = S.O.L.I.D principles
- Microservices
- Docker containers


## Fluxo do pedido

Cliente -> Carteira -> Carrinho -> Pedido -> Pagamento -> Ligística -> Entrega

## Como rodar




## Decisões técnicas

E-commerces são sistemas de alto fluxo de acesso com uma exigente responsabilidade com a segurança em dados, pensando nisso, microsserviços, são a melhor forma de conseguir escalar o serviço no futuro, principalmente horizontalmente. Com microsserviços tambem se ganha o isolamento adequado e controle fina nas comunicações de dados entre serviços, aqui chegando na proxima decisão que seria usar EDA.
Com Event-Driven Architecture, arquitetura orientada a eventos, o isolamento de cada camada da aplicação é mantido, com contratos simples e rígidos a comunicação entre serviços é segura e eficiente.


## Melhorias futuras
