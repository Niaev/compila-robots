# Compila Robots

Robôs feitos em Python (Selenium e Requests) que baixam PDF de nota fiscal no site de Belém do Pará de acordo com dados fornecidos.

## Requisitos

Para executar os robôs é necessário ter Python 3.10 ou superior e também instalar as bibliotecas necessárias utilizando o comando abaixo:

```
pip install reqs.txt
```

## Executar robôs

Com os requisitos instalados, basta executar os robôs da seguinte forma:

```
python3 requests_robot.py
python3 selenium_robot.py
```

### No código

É possível ver o código de cada robô abrindo seus respectivos arquivos em um editor de textos.

O robô feito em Selenium, por exemplo, possui dois parâmetros para configuração: `verbose` e `headless`, que são, respectivamente, `False` e `True` por padrão. 

```python
robot = SeleniumRobot(verbose=True, headless=False)

try:
    robot.initialize_browser()
    robot.execute_all()
finally:
    robot.driver.quit()
```

Acima, o robô feito em Selenium irá executar exibindo logs e mostrando a navegação em tempo real.

De forma muito semelhante, o robô feito com Requests possui apenas o parâmetro `verbose`, que por padrão possui valor `False`.

```python
robot = RequestsRobot(verbose=True)

robot.initialize_session()
robot.execute_all()
```