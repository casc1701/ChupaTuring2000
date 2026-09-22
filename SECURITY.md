# Segurança

## Uso pretendido

Didático. Demonstrar permutação posicional, `secrets` e o custo de um pad de papel.

**Não** use este software para proteger dados reais: senhas, prontuários, chaves, conversas que não podem vazar.

## Ameaças que o modelo ignora

- pad fotografado, impresso em nuvem, commitado neste repo
- reuso de linhas
- operador que cifra duas mensagens “só desta vez”
- malware no computador que gerou o pad
- side-channel no `list.index` (acadêmico aqui)
- metadata (tamanho da cifra ≈ tamanho do plaintext em letras)

## Se achar um bug

Abra uma issue descrevendo:

- comando exato
- pad sintético (nunca um pad que você tenha usado de verdade)
- resultado observado vs esperado

Não envie pads reais por issue, e-mail ou gist.
