# Exercício Prático — Sistema de Cálculo de Frete

Desenvolva, em **Python**, uma função responsável por calcular o valor do frete de uma entrega.

## Função a implementar

```python
calcular_frete(peso, distancia, tipo="normal")
```

## Regras

O valor do frete deverá ser calculado considerando:

- Taxa fixa de **R$ 10,00**;
- **R$ 2,00 por kg** transportado;
- **R$ 0,50 por km** percorrido;
- Para entregas do tipo `"expresso"`, deverá ser aplicado um acréscimo de **50%** sobre o valor total;
- O tipo de entrega padrão deverá ser `"normal"`.

A fórmula base será:

`frete = 10 + (peso × 2) + (distancia × 0.5)`

## Validações

A função deverá gerar `ValueError` quando:

- O peso for menor ou igual a `0`;
- A distância for menor ou igual a `0`;
- O tipo de entrega for diferente de `"normal"` ou `"expresso"`.

## Testes com Pytest

Após implementar a função, crie testes automatizados utilizando **Pytest** para verificar:

- Cálculo de frete normal;
- Cálculo de frete expresso;
- Diferentes valores de peso e distância;
- Peso igual a `0`;
- Peso negativo;
- Distância igual a `0`;
- Distância negativa;
- Tipo de entrega inválido.

Utilize também testes de exceção com:

```python
with pytest.raises(ValueError):
    ...
```

Implemente pelo menos um conjunto de testes utilizando:

```python
@pytest.mark.parametrize(...)
```

## Cobertura de Testes

Ao final, utilize o **pytest-cov** para verificar o percentual de cobertura dos testes.

Execute:

```bash
pytest -v --cov=frete --cov-report=term-missing
```

Analise o relatório gerado e verifique quais linhas do código não foram executadas pelos testes.

## Objetivo

Praticar a implementação de funções, validação de entradas, tratamento de exceções, criação de testes automatizados, testes parametrizados e análise de cobertura de código utilizando **Pytest**.
