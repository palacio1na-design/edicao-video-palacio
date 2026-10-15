# PALÁCIO VÍDEOS — EVOLUÇÃO DO MOTOR DE MONTAGEM INTELIGENTE
## Integração AutoBroll, Auto-Editor, WhisperX e Remotion com Direção Narrativa Palácio Acolhimento
**Documento Técnico e Dossiê de Engenharia Audiovisual — Palácio AI | Palácio.pro**

---

## 1. ETAPA 1: DIAGNÓSTICO DA ARQUITETURA ANTERIOR

### 1.1. Inspecção dos Motores Existentes
Antes desta evolução, o ecossistema do Palácio Vídeos era composto por:
- **Motor de Edição:** `SmartEditor` e `RetentionDirector`, focados em cortes por VAD e cálculo de curvas de câmera virtual.
- **Sistema de Legendas:** `DynamicCaptions.tsx`, com animação de palavras em destaque dourado (`#E5A93C`) no Remotion.
- **Processamento de Áudio:** `Spotify Pedalboard` com equalizador de presença, compressor de voz e `FFmpeg loudnorm` (-14.0 LUFS).
- **Sistema de B-roll:** Banco de vídeos em `remotion/public/broll/` (com alguns arquivos sintéticos descartados por marcas d'água de IA).
- **Renderização:** Remotion v4 em React 19, exportando 1080x1920 @ 30fps via Chromium headless no Apple Silicon.
- **Integração Gemini:** Estruturação de ganchos e geração de prompts no ecossistema do Antigravity.

### 1.2. Motivo Real pelo qual a Edição Anterior Apresentava Poucas Diferenças
Uma auditoria cirúrgica sobre os renders anteriores (`corte-2-creative-master`) revelou o problema de montagem:
1. **Talking-Head Contínuo e Ininterrupto:** O vídeo bruto original de Marcelo Palácio (28.37s) era colocado na timeline do Remotion do segundo 0 ao segundo 28.37 como uma **faixa contínua de imagem**.
2. **Efeitos sobre a Mesma Imagem:** As melhorias anteriores adicionaram uma moldura flutuante 2.5D, um fundo com *ambient blur* e pequenos zooms virtuais (punch-ins). No entanto, aos olhos do espectador, **o vídeo de fundo nunca mudava**. Parecia o mesmo vídeo original com uma "moldura e zoom".
3. **Ausência de B-roll Cutaway Real:** O B-roll não substituía visualmente o locutor. Na montagem tradicional de cinema e nas referências modernas como AutoBroll, quando o locutor diz algo dramático (*"perdi amigos pra droga"*), a imagem do locutor é **cortada** e substituída por uma cena de impacto (B-roll), enquanto a **voz dele continua contínua por baixo como voiceover**.
4. **Falta de Reordenação Semântica de Cenas:** Não havia divisão clara em cenas narrativas distintas (Gancho $\rightarrow$ Dor/Perda $\rightarrow$ Retorno Íntimo $\rightarrow$ Esperança/Acolhimento $\rightarrow$ Encerramento).

---

## 2. ETAPA 2: AVALIAÇÃO TÉCNICA DOS REPOSITÓRIOS DO GITHUB

### 2.1. `andriidrok1/autobroll` (Referência Principal)
- **Licença:** MIT (Permissiva e compatível com uso comercial).
- **Tecnologia:** TypeScript, React e Remotion.
- **Compatibilidade Apple Silicon (M-Series):** 100% nativa (Node.js arm64 + Chromium).
- **Conceito Chave Adotado:** **Multi-track A/B-roll Cross-Cutting**. A trilha de áudio principal permanece soberana e ininterrupta, mas a trilha visual chaveia entre:
  - `Trilha A (A-Roll):` Locutor (Marcelo Palácio) em planos específicos.
  - `Trilha B (B-Roll):` Cenas contextuais cinematográficas de apoio dramático cobrindo a tela inteira com transições suaves (fade/slide) enquanto a fala corre em voiceover.

### 2.2. `WyattBlue/auto-editor` (Referência de Ritmo e Respiros)
- **Licença:** CC-BY-SA 4.0 / Open Source.
- **Conceito Chave Adotado:** **Acoustic Margin Padding (Respiro Humano)**. A remoção de silêncios em conteúdos sensíveis (saúde mental e dependência química) não pode ser mecânica como em vídeos de humor rápido. O algoritmo precisa manter `0.15s` a `0.25s` de margem antes e após cada oração para preservar o peso dramático das pausas de reflexão.

### 2.3. `m-bain/whisperX` (Referência de Alinhamento Forçado)
- **Conceito Chave Adotado:** Alinhamento fonético determinístico via wav2vec2. Garante que o corte no milissegundo 0.00 coincida exatamente com o primeiro fonema da palavra *"Ontem"*, eliminando o clique ou respiração morta inicial.

---

## 3. ETAPA 3: IMPLEMENTAÇÃO DA MONTAGEM INTELIGENTE

Implementamos o motor definitivo em:
- **Core Python:** `core/intelligent_montage_engine.py`
- **Composição Remotion:** `remotion/src/creative-engine/IntelligentMontageComposition.tsx`
- **Registro do Root:** `corte-2-intelligent-montage` em `remotion/src/Root.tsx`

### Arquitetura das 5 Cenas Narrativas (Timeline Segundo a Segundo):

| Cena | Início | Fim | Tipo Visual | Conteúdo e Decisão Editorial | Áudio e Voiceover |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Cena 1** | `0.00s` | `7.29s` | **A-Roll (Locutor)** | **O Gancho Fatal:** Marcelo abre com corte no primeiro fonema (*"Ontem na palestra..."*). No segundo `2.0s`, ocorre um **punch-in cinético de 1.22x** cravado na palavra *"morreu!"* acompanhado de impacto grave (sub-boom). | Áudio de Marcelo normalizado + impacto de gancho. |
| **Cena 2** | `7.29s` | `13.00s` | **B-Roll Cutaway 1 (Dor)** | **A Dor Real da Perda:** Transição de corte seco para vídeo cinematográfico autêntico (`homem_solidao_quarto.mp4`, sem marcas de IA) mostrando um jovem em desespero na cama. | A voz de Marcelo continua como **Voiceover contínuo**: *"E eu perdi amigos pra droga..."* |
| **Cena 3** | `13.00s` | `24.00s` | **A-Roll (Locutor)** | **O Retorno Íntimo (Olho no Olho):** Corte de retorno para Marcelo em **enquadramento fechado e íntimo (1.14x)** com foco absoluto nos olhos: *"E eu não quero que seja você. Não quero perder você pra droga."* | Fala com máxima clareza acústica, sem música agressiva, apenas ambiência de reflexão. |
| **Cena 4** | `24.00s` | `26.50s` | **B-Roll Cutaway 2 (Acolhimento)** | **A Conexão Familiar:** Transição para B-Roll de acolhimento (`pai_filho_acolhimento.mp4`), onde um pai abraça o filho adulto com alívio e amor. | Voiceover de Marcelo: *"Tem uma família chorando por trás esperando você."* |
| **Cena 5** | `26.50s` | `28.37s` | **A-Roll + Outro Oficial** | **A Chave da Esperança:** Retorno a Marcelo com encerramento caloroso (*"Vem pro acolhimento!"*), subindo o **Monograma 'P' Dourado Oficial de Palácio Acolhimento** com `@palacioacolhimento`. | Transição suave com quem (whoosh) e fechamento institucional. |

---

## 4. AUDITORIA DETERMINÍSTICA DO QUALITY DIRECTOR

O vídeo final masterizado foi submetido à inspeção rigorosa do `PalácioQualityDirector`:
- **Arquivo Exportado:** `/Users/palacio.pro/Downloads/Corte_02_Vida_Serena_Palacio_Acolhimento_MONTAGEM_INTELIGENTE.mp4`
- **Tamanho:** `15.06 MB`
- **Resolução:** `1080x1920` (Vertical 9:16 nativo) @ 30fps
- **Duração:** `28.43s`

### Métricas Acústicas EBU R128:
- **Loudness Integrado:** `-14.0 LUFS` (Alvo perfeito para Reels/TikTok/Shorts: -14 LUFS)
- **True Peak:** `-1.3 dBFS` (Abaixo do limite de segurança de -0.9 dBFS, zero distorção/clipping)
- **Loudness Range (LRA):** `4.1 LU` (Faixa dinâmica cinematográfica ideal para voz humana)
- **Score de Clareza Vocal:** `10.0 / 10.0` (Nota máxima)

### Auditoria de Marca e Zonas Seguras:
- **Marca Configurada:** `palacio-acolhimento`
- **Violações de Marca Encontradas:** `0` (Zero menções a Palácio.pro, cumprimento de 100%)
- **Ancoragem da Legenda:** $Y = 1380\text{px}$ (`bottom: 540px` no frame 1080x1920)
- **Conformidade de Interface:** Legenda 100% desobstruída das barras do Instagram Reels, botões laterais do TikTok e títulos do YouTube Shorts.
- **Status da Auditoria:** `PASSED = TRUE` (**Aprovado com louvor**).

---

## 5. STORYBOARD COMPARATIVO (ORIGINAL VS EDITADO)

Foram extraídos pares de frames idênticos em `scratch/storyboard_comparison/` para verificação visual das mudanças:

```
+--------------------------------------------------------------------------------------------------+
| Segundo | Cena               | Frame Original (Talking-Head) | Frame Montagem Inteligente       |
+---------+--------------------+-------------------------------+----------------------------------+
| 2.0s    | Cena 1 (Gancho)    | Plano médio estático          | Punch-in 1.22x + Legenda Dourada |
| 9.5s    | Cena 2 (B-Roll 1)  | Mesmo plano estático          | B-Roll Dramático (Jovem na cama) |
| 18.0s   | Cena 3 (A-Roll)    | Mesmo plano estático          | Retorno em Close Íntimo (Olhos)  |
| 25.5s   | Cena 4 (B-Roll 2)  | Mesmo plano estático          | B-Roll Emocional (Abraço Pai)    |
| 27.2s   | Cena 5 (Outro)     | Fim abrupto no mesmo enquadr. | Monograma 'P' Dourado + CTA      |
+--------------------------------------------------------------------------------------------------+
```

---

## 6. COMANDOS OPERACIONAIS DE REPRODUÇÃO

Para renderizar novas variações com esta composição no futuro:
```bash
# Renderizar via Remotion
cd ~/.gemini/config/skills/edicao-video-palacio/remotion
npx remotion render corte-2-intelligent-montage \
  ~/Downloads/Corte_02_Vida_Serena_Palacio_Acolhimento_MONTAGEM_INTELIGENTE.mp4 \
  --concurrency=7

# Executar Auditoria Técnica Completa e Geração de Storyboard
/Users/palacio.pro/.gemini/antigravity/scratch/.venv/bin/python \
  /Users/palacio.pro/.gemini/antigravity/scratch/audit_and_compare_montage.py
```
