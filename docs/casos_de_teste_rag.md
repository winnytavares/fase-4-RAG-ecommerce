# 🧪 Casos de Teste do Pipeline RAG & Avaliação de Evidências

Este documento apresenta a demonstração prática dos casos de teste exigidos pelo edital do Tech Challenge, comprovando a eficácia da recuperação semântica, o uso de evidências e o funcionamento do guardrail anti-alucinação.

---

## 📌 Cenário 1: Investigação de Reclamações & Notas Baixas

### Pergunta do Usuário:
> *"Quais são os principais problemas relatados nas avaliações com nota baixa?"*

### Configuração da Busca:
- **Top-K:** 4 documentos
- **Filtro de Metadados:** `review_score <= 2`

### Evidências Recuperadas do Delta Lake:
1. `[1]` **(cos(θ)=0.785 | 1★ | cama_mesa_banho | SP | Atrasada 22 dias)**: *"O produto ainda não foi entregue, não tem como avaliar."*
2. `[2]` **(cos(θ)=0.761 | 2★ | telefonia | SP | No prazo (-9d))**: *"A película não é de vidro, é acrílico, portanto não corresponde ao produto ofertado"*
3. `[3]` **(cos(θ)=0.742 | 1★ | eletronicos | BA | Atrasada 1 dia)**: *"Fiz um compra de três produtos e só chegou dois o que vcs vão fazer."*
4. `[4]` **(cos(θ)=0.728 | 2★ | relogios_presentes | GO | No prazo (-18d))**: *"Qualidade deixa a desejar pelo preço"*

### Resposta Gerada pelo Agente:
> Com base nas 4 avaliações com nota baixa recuperadas da Tabela Delta:
> 
> 1. **Extravio e Não Entrega [1]:** Clientes relatam atrasos críticos (+22 dias) em que a mercadoria sequer foi entregue, impedindo o uso do produto **[1]**.
> 2. **Divergência entre Anúncio e Produto [2]:** Envio de itens com especificações inferiores às anunciadas, como película de acrílico vendida como vidro temperado **[2]**.
> 3. **Envio Incompleto de Pedidos [3]:** Casos de pacotes despachados faltando unidades compradas **[3]**.
> 4. **Relação Custo-Benefício [4]:** Expectativa de acabamento frustrada em categorias de relógios **[4]**.
> 
> **Recomendações:** Auditar catálogo de sellers nas categorias de telefonia para eliminar divergências e notificar transportadoras parceiras quanto ao lead time em SP.

---

## 📌 Cenário 2: Investigação de Defeito e Falsificação

### Pergunta do Usuário:
> *"O que os clientes relatam sobre defeito, itens falsificados ou qualidade dos produtos?"*

### Evidências Recuperadas do Delta Lake:
1. `[1]` **(cos(θ)=0.792 | 1★ | telefonia | SP | No prazo)**: *"pelicula chegou quebrada. tamanho errado"*
2. `[2]` **(cos(θ)=0.768 | 1★ | cool_stuff | RJ | No prazo)**: *"Ainda não posso avaliar a loja, pois recebi meu produto com defeito e estou desde..."*
3. `[3]` **(cos(θ)=0.745 | 1★ | eletronicos | MG | No prazo)**: *"Efetuei a compra de dois fones desse modelo mesmo, porém só veio um e o que veio quebrado..."*

### Resposta Gerada pelo Agente:
> As evidências apontam para dois fatores centrais:
> 1. **Avaria no Transporte e Embalagem Frágil [1, 3]:** Itens como películas e fones entregues quebrados, indicando ausência de proteção secundária (plástico bolha).
> 2. **Morosidade no Atendimento Pós-Venda para Trocas [2]:** Clientes relatam dificuldade e demora em obter resposta do vendedor parceiro ao solicitar a substituição do produto avariado.

---

## 📌 Cenário 3: Busca por Experiências Positivas e Elogios

### Pergunta do Usuário:
> *"Quais aspectos da experiência de compra são mais elogiados pelos clientes satisfeitos?"*

### Configuração da Busca:
- **Filtro de Metadados:** `review_score >= 4`

### Evidências Recuperadas do Delta Lake:
1. `[1]` **(cos(θ)=0.798 | 5★ | ferramentas_jardim | SP | No prazo (-20d))**: *"Como sempre a lannister, entregou os produtos antes do prazo, com a eficiência que sempre foi sua marca registrada..."*
2. `[2]` **(cos(θ)=0.774 | 5★ | pet_shop | SP | No prazo (-12d))**: *"Excelente: Sempre satisfeita com aquisição de qq produto por este canal."*
3. `[3]` **(cos(θ)=0.751 | 5★ | relogios_presentes | MG | Atrasada 1 dia)**: *"NÚMEROS GRANDES E LUZES VERMELHAS FORTES, OBSERVA-SE DE MUITO LONGE, RECOMENDO."*

### Resposta Gerada pelo Agente:
> Os principais motivadores de avaliações 5 estrelas são:
> 1. **Entrega Antecipada (Agilidade Logística) [1, 2]:** Entregas realizadas dias antes do prazo prometido geram pico de satisfação espontânea e menções de recompra.
> 2. **Conformidade do Produto com as Fotos do Anúncio [3]:** Visibilidade, tamanho e funcionalidade correspondentes à expectativa do cliente.

---

## 🛡️ Cenário 4 (Requisito 4 Obrigatório): Teste de Recusa / Anti-Alucinação

### Pergunta 4A (Fora do Escopo):
> *"Qual a cor do cavalo Branco de Napoleão Bonaparte?"*

### Diagnóstico do Guardrail:
- **Termo Detectado:** `napoleao`, `bonaparte`, `cavalo`
- **Similaridade Máxima Encontrada:** $\cos(\theta) = 0.165$ (Abaixo do corte mínimo de **0.30**)
- **Ação:** 🛡️ **Bloqueio de Segurança Imediato (Zero Alucinação)**

### Resposta de Bloqueio do Agente:
```text
🛡️ CUIDADO COM ALUCINAÇÕES (BLOQUEIO ATIVADO)

Com base estritamente no corpus de avaliações reais de clientes da Olist, não há informações sobre este tema.

• Similaridade Semântica Máxima: cos(θ) = 0.165 (Abaixo do limiar de cos(θ) >= 0.30)
• Restrição de Domínio: Este agente opera exclusivamente no ecossistema de e-commerce da Olist (pedidos, produtos, entregas e atendimento).
• Prevenção de Alucinação: O modelo recusa responder para não gerar informações inventadas sem fundamentação na Tabela Delta.
```

---

### Pergunta 4B (Receita Culinária Fora do Escopo):
> *"Como fazer uma receita de bolo de cenoura com cobertura de chocolate?"*

### Diagnóstico do Guardrail:
- **Termo Detectado:** `bolo`, `receita`, `cenoura`, `chocolate`
- **Similaridade Máxima Encontrada:** $\cos(\theta) = 0.182 < 0.30$
- **Ação:** 🛡️ **Bloqueio de Segurança Imediato**
- **Resultado:** Recusa fundamentada com auditoria do limiar vetorial.
