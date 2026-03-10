<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Robleddo Consulting — Diagnóstico de Postagem</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg: #0d0d0d; --surface: #161616; --card: #202020; --border: #2c2c2c;
    --text: #f0f0f0; --muted: #666; --accent: #f5a623;
    --green: #27ae60; --red: #e74c3c; --gray: #7f8c8d;
  }
  body { background: var(--bg); color: var(--text); font-family: 'DM Sans', 'Segoe UI', sans-serif; min-height: 100vh; }
  input, textarea, select { background: var(--card); border: 1px solid var(--border); border-radius: 8px; color: var(--text); font-family: inherit; font-size: 14px; padding: 10px 12px; width: 100%; outline: none; transition: border .2s; }
  input:focus, textarea:focus, select:focus { border-color: var(--accent); }
  textarea { resize: vertical; }
  button { cursor: pointer; font-family: inherit; transition: all .2s; }
  .btn-primary { background: var(--accent); border: none; border-radius: 9px; color: #000; font-size: 15px; font-weight: 800; padding: 13px 24px; }
  .btn-primary:hover { opacity: .9; }
  .btn-primary:disabled { background: var(--border); color: var(--muted); cursor: not-allowed; }
  .btn-ghost { background: transparent; border: 1px solid var(--accent); border-radius: 9px; color: var(--accent); font-size: 13px; font-weight: 700; padding: 9px 18px; }
  .btn-success { background: #1a2e1a; border: 1px solid var(--green); border-radius: 8px; color: var(--green); font-size: 13px; font-weight: 700; padding: 9px 18px; }
  .btn-pdf { background: #1a1a2e; border: 1px solid #6c5ce7; border-radius: 8px; color: #6c5ce7; font-size: 13px; font-weight: 700; padding: 9px 18px; cursor: pointer; transition: all .2s; }
  .btn-pdf:hover { opacity: .85; }
  .label { color: var(--muted); display: block; font-size: 12px; font-weight: 600; letter-spacing: .8px; margin-bottom: 6px; text-transform: uppercase; }
  .section { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; margin-bottom: 16px; overflow: hidden; }
  .section-header { border-bottom: 1px solid var(--border); padding: 14px 20px; }
  .section-title { color: var(--muted); font-size: 12px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; }
  .section-body { padding: 20px; }
  .tag-badge { border-radius: 6px; display: inline-block; font-size: 11px; font-weight: 700; padding: 3px 9px; white-space: nowrap; }
  .header { align-items: center; background: var(--surface); border-bottom: 1px solid var(--border); display: flex; height: 58px; justify-content: space-between; padding: 0 40px; position: sticky; top: 0; z-index: 100; }
  .logo-text { font-size: 18px; font-weight: 900; letter-spacing: -1px; }
  .page { display: none; }
  .page.active { display: block; }
  .upload-zone { border: 2px dashed var(--border); border-radius: 8px; cursor: pointer; padding: 24px; text-align: center; transition: all .2s; }
  .upload-zone:hover { border-color: var(--accent); }
  .upload-zone.has-file { background: rgba(245,166,35,.05); border-color: var(--accent); }
  .tag-item { align-items: center; background: var(--card); border: 1px solid var(--border); border-radius: 8px; display: flex; gap: 10px; margin-bottom: 8px; padding: 10px 12px; }
  .progress-bar-wrap { background: var(--surface); border-radius: 10px; height: 8px; margin: 12px 0; overflow: hidden; }
  .progress-bar-fill { background: var(--accent); border-radius: 10px; height: 100%; transition: width .4s ease; width: 0%; }
  .step-item { align-items: center; background: var(--surface); border: 1px solid var(--border); border-radius: 8px; display: flex; gap: 10px; margin-bottom: 8px; padding: 10px 14px; }
  .stat-card { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; cursor: pointer; padding: 16px; transition: all .2s; }
  .stat-number { font-size: 26px; font-weight: 900; line-height: 1; }
  .theme-card { background: var(--card); border: 1px solid var(--border); border-radius: 8px; cursor: pointer; padding: 12px 14px; transition: all .2s; }
  .theme-bar-bg { background: var(--border); border-radius: 99px; height: 3px; margin-top: 8px; }
  .theme-bar-fill { border-radius: 99px; height: 100%; }
  .table-header { background: #111; border-bottom: 1px solid var(--border); display: grid; font-size: 10px; font-weight: 700; gap: 8px; grid-template-columns: 40px 1fr 150px 160px; letter-spacing: .8px; padding: 10px 20px; text-transform: uppercase; color: var(--muted); }
  .table-row { align-items: start; border-bottom: 1px solid var(--border); display: grid; font-size: 13px; gap: 8px; grid-template-columns: 40px 1fr 150px 160px; padding: 12px 20px; }
  .table-body { max-height: 500px; overflow-y: auto; }
  .table-num { color: var(--muted); font-size: 11px; padding-top: 2px; }
  .table-comment { color: #ccc; line-height: 1.6; }
  .pagination { align-items: center; border-top: 1px solid var(--border); display: flex; gap: 8px; justify-content: center; padding: 12px 20px; }
  .page-btn { background: var(--card); border: 1px solid var(--border); border-radius: 6px; color: var(--text); font-size: 13px; padding: 6px 14px; }
  .api-key-notice { background: #1a1800; border: 1px solid var(--accent)44; border-radius: 8px; font-size: 12px; color: #aaa; padding: 10px 14px; margin-bottom: 16px; line-height: 1.6; }
</style>
</head>
<body>

<div class="header">
  <div class="logo-text">
    <span style="color:#fff;">ROBLEDDO</span><span style="color:var(--accent);"> CONSULTING</span>
  </div>
  <div id="header-actions"></div>
</div>

<!-- ══ SETUP ══ -->
<div class="page active" id="setup-page">
  <div style="max-width:680px; margin:0 auto; padding:40px 20px;">

    <div style="margin-bottom:24px;">
      <h2 style="font-size:20px; font-weight:800;">✨ Diagnóstico de Postagem</h2>
      <p style="color:var(--muted); font-size:13px; margin-top:4px;">Análise estratégica de comentários via IA</p>
    </div>

    <!-- API Key -->
    <div class="section">
      <div class="section-header"><span class="section-title">🔑 Chave da API Anthropic</span></div>
      <div class="section-body">
        <div class="api-key-notice">A chave é usada diretamente no navegador e <strong style="color:var(--accent);">nunca é salva</strong> no servidor. Você precisará inserir a cada sessão.</div>
        <input type="password" id="api-key-input" placeholder="sk-ant-..." oninput="checkCanExecute()">
      </div>
    </div>

    <!-- Postagem -->
    <div class="section">
      <div class="section-header"><span class="section-title">🔗 Postagem</span></div>
      <div class="section-body">
        <div style="margin-bottom:14px;">
          <label class="label">URL do Instagram</label>
          <input type="text" id="url-input" placeholder="https://www.instagram.com/p/...">
        </div>
        <div>
          <label class="label">Contexto</label>
          <input type="text" id="context-input" placeholder="Ex: Prefeitura de Natal, gestão Paulinho Freire 2025">
        </div>
      </div>
    </div>

    <!-- Screenshot -->
    <div class="section">
      <div class="section-header"><span class="section-title">📸 Screenshot da Postagem</span></div>
      <div class="section-body">
        <div class="upload-zone" id="screenshot-zone" onclick="document.getElementById('screenshot-input').click()">
          <div id="screenshot-placeholder">
            <div style="font-size:32px; margin-bottom:8px;">📸</div>
            <div style="font-size:14px; font-weight:700;">Clique para adicionar o print</div>
            <div style="color:var(--muted); font-size:12px; margin-top:4px;">JPG, PNG, WEBP</div>
          </div>
          <div id="screenshot-preview-wrap" style="display:none;">
            <img id="screenshot-preview-img" style="border-radius:6px; display:block; margin:0 auto 8px; max-height:200px; max-width:100%;">
            <div id="screenshot-name" style="color:var(--accent); font-size:12px; font-weight:700;"></div>
            <div style="color:var(--muted); font-size:11px; margin-top:2px;">Clique para trocar</div>
          </div>
        </div>
        <input type="file" id="screenshot-input" accept="image/*" style="display:none;">
        <button id="screenshot-remove" onclick="removeScreenshot()" style="background:none;border:none;color:var(--red);font-size:12px;margin-top:6px;display:none;">× Remover</button>
      </div>
    </div>

    <!-- Excel -->
    <div class="section">
      <div class="section-header"><span class="section-title">📊 Comentários (Excel)</span></div>
      <div class="section-body">
        <div class="upload-zone" id="excel-zone" onclick="document.getElementById('excel-input').click()">
          <div id="excel-placeholder">
            <div style="font-size:32px; margin-bottom:8px;">📁</div>
            <div style="font-size:14px; font-weight:700;">Clique para carregar o Excel</div>
            <div style="color:var(--muted); font-size:12px; margin-top:4px;">.xlsx / .xls</div>
          </div>
          <div id="excel-loaded" style="display:none;">
            <div style="font-size:28px; margin-bottom:6px;">✅</div>
            <div id="excel-filename" style="color:var(--accent); font-size:14px; font-weight:700;"></div>
            <div id="excel-count" style="color:var(--muted); font-size:12px; margin-top:4px;"></div>
          </div>
        </div>
        <input type="file" id="excel-input" accept=".xlsx,.xls,.csv" style="display:none;">
        <div id="col-selector-wrap" style="display:none; margin-top:12px;">
          <label class="label">Coluna dos comentários <span id="col-count" style="color:var(--accent);"></span></label>
          <select id="col-selector"></select>
          <div id="col-preview" style="background:var(--card);border:1px solid var(--border);border-radius:6px;margin-top:8px;padding:8px 10px;display:none;"></div>
        </div>
      </div>
    </div>

    <!-- Critério -->
    <div class="section">
      <div class="section-header"><span class="section-title">🎯 Critério de Análise</span></div>
      <div class="section-body">
        <textarea id="criterion-input" rows="4" placeholder="Ex: Quero entender o sentimento em relação à gestão do prefeito Paulinho Freire..." oninput="checkCanExecute()"></textarea>
        <div id="criterion-counter" style="color:var(--muted);font-size:11px;margin-top:4px;">0 / 30 caracteres mínimos</div>
      </div>
    </div>

    <!-- Tags -->
    <div class="section">
      <div class="section-header"><span class="section-title">🏷 Tags Principais</span></div>
      <div class="section-body">
        <div id="tags-list"></div>
        <div style="background:var(--card);border:1px dashed var(--border);border-radius:8px;padding:14px;margin-top:4px;">
          <input type="text" id="new-tag-name" placeholder="Nome da tag (ex: APOIADOR DE ÁLVARO)" style="margin-bottom:8px;">
          <input type="text" id="new-tag-desc" placeholder="Quando usar esta tag..." style="margin-bottom:10px;">
          <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
            <span style="color:var(--muted);font-size:12px;">Cor:</span>
            <div id="color-picker" style="display:flex;gap:6px;flex-wrap:wrap;"></div>
            <button class="btn-ghost" onclick="addTag()" style="margin-left:auto;padding:6px 16px;font-size:12px;">+ Adicionar</button>
          </div>
        </div>
      </div>
    </div>

    <button class="btn-primary" id="execute-btn" onclick="executeAnalysis()" disabled style="width:100%;padding:16px;font-size:16px;border-radius:10px;">
      ⚡ Executar Diagnóstico
    </button>
  </div>
</div>

<!-- ══ PROCESSING ══ -->
<div class="page" id="processing-page">
  <div style="max-width:480px;margin:100px auto;padding:24px;text-align:center;">
    <div style="font-size:52px;margin-bottom:20px;">🔬</div>
    <h2 style="font-size:20px;font-weight:900;margin-bottom:8px;">Processando diagnóstico</h2>
    <p id="processing-log" style="color:var(--muted);font-size:14px;margin-bottom:28px;">Iniciando...</p>
    <div class="progress-bar-wrap"><div class="progress-bar-fill" id="progress-fill"></div></div>
    <div id="progress-pct" style="color:var(--accent);font-size:13px;font-weight:700;margin-bottom:24px;">0%</div>
    <div id="steps-list" style="text-align:left;"></div>
  </div>
</div>

<!-- ══ REPORT ══ -->
<div class="page" id="report-page">
  <div style="max-width:1080px;margin:0 auto;padding:32px 20px;">

    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:24px;flex-wrap:wrap;gap:12px;">
      <div>
        <div id="report-date" style="color:var(--muted);font-size:12px;"></div>
        <h1 style="font-size:22px;font-weight:900;margin:4px 0 0;">
          <span style="color:#fff;">ROBLEDDO</span><span style="color:var(--accent);"> CONSULTING</span>
        </h1>
        <div id="report-context" style="color:var(--muted);font-size:13px;margin-top:2px;"></div>
      </div>
      <img id="report-screenshot" style="border-radius:8px;border:1px solid var(--border);display:none;max-height:100px;object-fit:cover;">
      <div style="display:flex;gap:10px;">
        <button class="btn-success" onclick="exportExcel()">⬇ Exportar Excel</button>
        <button class="btn-pdf" onclick="exportPDF()" id="btn-pdf">⬇ Exportar PDF</button>
        <button class="btn-ghost" onclick="newAnalysis()">← Nova Análise</button>
      </div>
    </div>

    <div class="section" style="margin-bottom:16px;">
      <div class="section-header"><span class="section-title">📋 Análise Estratégica</span></div>
      <div class="section-body">
        <p id="report-summary" style="color:#ccc;font-size:14px;line-height:1.8;white-space:pre-line;"></p>
      </div>
    </div>

    <div id="stat-cards" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-bottom:16px;"></div>

    <div class="section" style="margin-bottom:16px;">
      <div class="section-header"><span class="section-title">Distribuição por Tag</span></div>
      <div class="section-body"><canvas id="main-chart" height="80"></canvas></div>
    </div>

    <div class="section" style="margin-bottom:16px;">
      <div class="section-header"><span class="section-title">Temas Identificados</span></div>
      <div class="section-body">
        <div id="theme-cards" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;margin-bottom:16px;"></div>
        <canvas id="theme-chart" height="80"></canvas>
      </div>
    </div>

    <div class="section">
      <div style="padding:16px 20px;border-bottom:1px solid var(--border);">
        <div class="section-title" style="margin-bottom:12px;">Comentários (<span id="filtered-count"></span>)</div>
        <input type="text" id="search-input" placeholder="Buscar comentário..." style="margin-bottom:10px;" oninput="applyFilters()">
        <div id="active-filters" style="display:none;gap:8px;margin-bottom:6px;flex-wrap:wrap;align-items:center;"></div>
      </div>
      <div class="table-header"><span>Nº</span><span>Comentário</span><span>Tag</span><span>Tema</span></div>
      <div class="table-body" id="table-body"></div>
      <div class="pagination" id="pagination"></div>
    </div>
  </div>
</div>

<script>
// ─── Constants ────────────────────────────────────────────────────────────────
const POSITIVE_COLORS = ["#2ECC71","#3498DB","#F1C40F","#27AE60","#5DADE2","#1ABC9C","#EB984E","#A8D8A8"];
const NEGATIVE_COLORS = ["#E74C3C","#C0392B","#F39C12","#7F8C8D","#566573","#6E2C00","#6C3483","#2C3E50"];
const PRESET_COLORS   = ["#e74c3c","#27ae60","#3498db","#9b59b6","#f39c12","#1abc9c","#e91e63","#00bcd4","#ff5722","#607d8b"];

// ─── State ────────────────────────────────────────────────────────────────────
const S = {
  comments:[], headers:[], excelRows:[], selectedColIdx:0,
  mainTags:[
    {name:"APOIADOR",  description:"Apoia o prefeito, elogia a gestão, comentários positivos.", color:"#27ae60"},
    {name:"DETRATOR",  description:"Critica o prefeito, desaprova a gestão, comentários negativos.", color:"#e74c3c"},
    {name:"NEUTRO",    description:"Comentário sem posicionamento claro ou ambíguo.", color:"#7f8c8d"},
  ],
  selectedColor: PRESET_COLORS[2],
  screenshot: null,
  themeTags:[], results:[],
  filterMain:"all", filterTheme:"all",
  currentPage:1, perPage:30,
  mainChart:null, themeChart:null,
};

// ─── Helpers ──────────────────────────────────────────────────────────────────
function tagColor(name) {
  const n = name.toUpperCase();
  if (n.includes("APOIADOR")||n.includes("APOIO")||n.includes("POSITIVO")) return "#27ae60";
  if (n.includes("DETRATOR")||n.includes("DETRAT")||n.includes("NEGATIVO")||n.includes("CRITICA")||n.includes("CRÍTICA")) return "#e74c3c";
  if (n.includes("NEUTRO")||n.includes("INDEFINIDO")) return "#7f8c8d";
  let h=0; for(let i=0;i<name.length;i++) h=name.charCodeAt(i)+((h<<5)-h);
  return PRESET_COLORS[Math.abs(h)%PRESET_COLORS.length];
}

function aiTagColor(tag, idx) {
  const n=((tag.name||"")+" "+(tag.description||"")).toLowerCase();
  const neg=["critica","crítica","detrat","negat","reclamaç","denúncia","abandono","falta","buraco","protest","contra","insatisf","problema","falha"];
  const pos=["apoio","elogio","positiv","suport","feliz","satisf","bom","ótimo","excelente","parabéns","melhoria","obra"];
  const isNeg=neg.some(w=>n.includes(w)), isPos=pos.some(w=>n.includes(w));
  if (tag.sentiment==="negative"||(isNeg&&!isPos)) return NEGATIVE_COLORS[idx%NEGATIVE_COLORS.length];
  return POSITIVE_COLORS[idx%POSITIVE_COLORS.length];
}

function makeBadge(label, color) {
  return `<span class="tag-badge" style="background:${color}22;color:${color};border:1px solid ${color}44;">${label}</span>`;
}

function showPage(id) {
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.getElementById(id).classList.add('active');
}

function getCsrf() {
  return document.cookie.split(';').map(c=>c.trim()).find(c=>c.startsWith('csrftoken='))?.split('=')[1]||'';
}

// ─── Claude API — routed through Django proxy ─────────────────────────────────
async function callClaude(prompt, jsonMode=false) {
  const apiKey = document.getElementById('api-key-input').value.trim();
  const res = await fetch("/api/claude/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCsrf(),
    },
    body: JSON.stringify({ prompt, jsonMode, apiKey }),
  });
  const data = await res.json();
  if (data.error) throw new Error(data.error);
  return data.text || "";
}

function parseJSON(text) {
  const clean = text.replace(/```json|```/g,"").trim();
  const match = clean.match(/(\{[\s\S]*\}|\[[\s\S]*\])/);
  return JSON.parse(match ? match[0] : clean);
}

async function generateThematicTags(sample, criterion) {
  const prompt = `Você é um analista político especializado em redes sociais brasileiras.
Analise os comentários abaixo e gere EXATAMENTE 8 tags temáticas DISTINTAS, BEM DISTRIBUÍDAS e com SENTIDO POLÍTICO EXPLÍCITO.

REGRAS OBRIGATÓRIAS:
- As 8 tags devem ser DIFERENTES entre si, sem sobreposição de assuntos
- Cada tag deve ter um assunto claramente distinto das outras 7
- CADA NOME DE TAG deve deixar EXPLÍCITO o sentido político — nunca use nomes neutros ou vagos
- ERRADO: "Comparação Carlos Eduardo" | CERTO: "Nostalgia de Carlos Eduardo vs gestão atual" ou "Comparação favorável a Paulinho vs CE"
- ERRADO: "Críticas a Festas" | CERTO: "Rejeição ao Carnaval como prioridade"
- ERRADO: "Saúde" | CERTO: "Denúncia de colapso na saúde pública"
- ERRADO: "Apoio ao prefeito" | CERTO: "Elogios à gestão e reeleição de Paulinho"
- O nome deve deixar claro SE É A FAVOR ou CONTRA, e em relação A QUEM ou A QUÊ
- Cada tag: 3 a 7 palavras, nome direto com posicionamento político claro
- A descrição deve reforçar o critério de uso
- Inclua o campo sentiment: positive ou negative

Critério de análise: ${criterion}

Comentários (amostra de ${sample.length}):
${sample.map((c,i)=>`${i+1}. ${c}`).join("\n")}

Retorne SOMENTE este JSON sem nenhum texto extra:
{"tags": [{"name": "nome com sentido político explícito", "description": "quando usar esta tag especificamente", "sentiment": "positive ou negative"}]}`;

  const raw = await callClaude(prompt, true);
  return (parseJSON(raw).tags || []).slice(0, 8);
}

async function classifyBatch(batch, mainTags, themeTags) {
  const prompt = `Você é um classificador preciso de comentários políticos em português. Classifique cada comentário abaixo.

REGRAS CRÍTICAS PARA OS TEMAS:
1. Leia o comentário com atenção antes de classificar
2. Escolha o tema que MELHOR descreve o ASSUNTO PRINCIPAL do comentário
3. NÃO use sempre o mesmo tema — distribua entre todos os temas disponíveis conforme o conteúdo
4. Se o comentário for curto ou ambíguo, escolha o tema mais próximo do contexto
5. Nunca repita o mesmo tema para comentários com assuntos claramente diferentes

TAGS PRINCIPAIS (escolha UMA):
${mainTags.map(t=>`- "${t.name}": ${t.description}`).join("\n")}

TAGS TEMÁTICAS DISPONÍVEIS (escolha a que MELHOR encaixa o assunto do comentário):
${themeTags.map((t,i)=>`${i+1}. "${t.name}": ${t.description}`).join("\n")}

FORMATO DE RESPOSTA — retorne SOMENTE este JSON sem nenhum texto extra:
{"results": [{"main": "nome exato da tag principal", "theme": "nome exato do tema"}]}

COMENTÁRIOS PARA CLASSIFICAR (${batch.length} itens):
${batch.map((c,i)=>`${i+1}. ${c}`).join("\n")}`;

  for (let attempt=0; attempt<3; attempt++) {
    try {
      const raw = await callClaude(prompt, true);
      const results = parseJSON(raw).results || [];
      const mainNames = mainTags.map(t=>t.name);
      const themeNames = themeTags.map(t=>t.name);
      return batch.map((_,i) => {
        const r = results[i] || {};
        return {
          main:  mainNames.includes(r.main)  ? r.main  : mainNames[0],
          theme: themeNames.includes(r.theme) ? r.theme : themeNames[0],
        };
      });
    } catch(e) {
      if (attempt===2) throw e;
      await new Promise(r=>setTimeout(r, 1000*(attempt+1)));
    }
  }
}

async function generateSummary(mainCounts, total, criterion, context) {
  const dist = Object.entries(mainCounts)
    .map(([k,v])=>`${k}: ${v} (${total?Math.round(v/total*100):0}%)`)
    .join(", ");

  const prompt = `Você é um analista político estratégico. Escreva uma análise de 4-5 linhas e liste 3 recomendações estratégicas numeradas.

REGRA FUNDAMENTAL: Nunca generalize como representativo da população total. Use sempre "com base nesta postagem", "os usuários que comentaram nesta postagem", "nesta publicação os comentários indicam". Jamais diga "a população sente" ou qualquer frase que extrapole os dados desta postagem.

Contexto: ${context}
Critério: ${criterion}
Total de comentários nesta postagem: ${total}
Distribuição: ${dist}

Seja direto, objetivo e estratégico.`;

  return await callClaude(prompt);
}

// ─── Screenshot ───────────────────────────────────────────────────────────────
document.getElementById('screenshot-input').addEventListener('change', function(e) {
  const file = e.target.files[0];
  if (!file) return;
  S.screenshot = file;
  const reader = new FileReader();
  reader.onload = ev => {
    document.getElementById('screenshot-placeholder').style.display='none';
    document.getElementById('screenshot-preview-wrap').style.display='block';
    document.getElementById('screenshot-preview-img').src=ev.target.result;
    document.getElementById('screenshot-name').textContent=file.name;
    document.getElementById('screenshot-remove').style.display='inline';
    document.getElementById('screenshot-zone').classList.add('has-file');
  };
  reader.readAsDataURL(file);
});

function removeScreenshot() {
  S.screenshot=null;
  document.getElementById('screenshot-placeholder').style.display='block';
  document.getElementById('screenshot-preview-wrap').style.display='none';
  document.getElementById('screenshot-remove').style.display='none';
  document.getElementById('screenshot-zone').classList.remove('has-file');
  document.getElementById('screenshot-input').value='';
}

// ─── Excel ────────────────────────────────────────────────────────────────────
document.getElementById('excel-input').addEventListener('change', function(e) {
  const file = e.target.files[0];
  if (!file) return;
  document.getElementById('excel-filename').textContent=file.name;
  const reader = new FileReader();
  reader.onload = ev => {
    const wb = XLSX.read(ev.target.result, {type:'array'});
    const ws = wb.Sheets[wb.SheetNames[0]];
    const raw = XLSX.utils.sheet_to_json(ws, {header:1});
    if (!raw||raw.length<2) return;
    const headers = raw[0].map(h=>String(h||""));
    const dataRows = raw.slice(1);
    S.headers=headers; S.excelRows=dataRows;

    const known=["text","texto","comment","comentario","comentário","body","message"];
    let best=-1;
    for (const name of known) {
      const idx=headers.findIndex(h=>h.toLowerCase().trim()===name);
      if (idx!==-1){best=idx;break;}
    }
    if (best===-1) {
      let bestScore=-1;
      headers.forEach((_,ci)=>{
        const vals=dataRows.map(r=>String(r[ci]||"")).filter(v=>v.length>3);
        if(!vals.length) return;
        if(vals.filter(v=>v.startsWith("http")).length/vals.length>0.5) return;
        const avg=vals.reduce((a,v)=>a+v.length,0)/vals.length;
        if(avg>bestScore){bestScore=avg;best=ci;}
      });
    }
    if(best===-1) best=0;
    S.selectedColIdx=best;
    loadComments();

    const sel=document.getElementById('col-selector');
    sel.innerHTML=headers.map((h,i)=>`<option value="${i}"${i===best?' selected':''}>${h}</option>`).join('');
    document.getElementById('col-selector-wrap').style.display='block';
    updateColPreview();
    document.getElementById('excel-zone').classList.add('has-file');
  };
  reader.readAsArrayBuffer(file);
});

document.getElementById('col-selector').addEventListener('change', function(){
  S.selectedColIdx=parseInt(this.value);
  loadComments(); updateColPreview();
});

function loadComments() {
  const ci=S.selectedColIdx;
  S.comments=S.excelRows.map(r=>String(r[ci]||"").trim()).filter(s=>s.length>3&&!s.startsWith("http"));
  document.getElementById('excel-placeholder').style.display='none';
  document.getElementById('excel-loaded').style.display='block';
  document.getElementById('excel-count').textContent=`${S.comments.length} comentários encontrados`;
  document.getElementById('col-count').textContent=`(${S.comments.length} itens)`;
  checkCanExecute();
}

function updateColPreview() {
  const ci=S.selectedColIdx;
  const preview=S.excelRows.slice(0,2).map(r=>String(r[ci]||"")).filter(Boolean);
  const el=document.getElementById('col-preview');
  if(!preview.length){el.style.display='none';return;}
  el.style.display='block';
  el.innerHTML=`<div style="color:var(--muted);font-size:10px;margin-bottom:4px;text-transform:uppercase;letter-spacing:1px;">Prévia:</div>`+
    preview.map(v=>v.startsWith("http")
      ?`<div style="color:var(--red);font-size:12px;">⚠ URL — selecione outra coluna</div>`
      :`<div style="color:#ccc;font-size:12px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">"${v.slice(0,90)}${v.length>90?'…':''}"</div>`
    ).join('');
}

// ─── Criterion counter ────────────────────────────────────────────────────────
document.getElementById('criterion-input').addEventListener('input', function(){
  const el=document.getElementById('criterion-counter');
  el.textContent=`${this.value.length} / 30 caracteres mínimos`;
  el.style.color=this.value.length>=30?'var(--green)':'var(--muted)';
  checkCanExecute();
});

// ─── Tags ─────────────────────────────────────────────────────────────────────
function renderTags() {
  document.getElementById('tags-list').innerHTML=S.mainTags.map((t,i)=>`
    <div class="tag-item">
      <div style="width:10px;height:10px;border-radius:50%;background:${t.color};flex-shrink:0;"></div>
      <div style="flex:1;min-width:0;">
        <div style="font-weight:700;font-size:13px;">${t.name}</div>
        <div style="color:var(--muted);font-size:11px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${t.description}</div>
      </div>
      <button onclick="removeTag(${i})" style="background:none;border:none;color:var(--red);font-size:16px;padding:0 4px;">×</button>
    </div>`).join('');
}

function addTag() {
  const name=document.getElementById('new-tag-name').value.trim().toUpperCase();
  const desc=document.getElementById('new-tag-desc').value.trim();
  if (!name) return;
  S.mainTags.push({name,description:desc,color:S.selectedColor});
  document.getElementById('new-tag-name').value='';
  document.getElementById('new-tag-desc').value='';
  renderTags(); checkCanExecute();
}

function removeTag(i){S.mainTags.splice(i,1);renderTags();checkCanExecute();}

function renderColorPicker() {
  document.getElementById('color-picker').innerHTML=PRESET_COLORS.map(c=>`
    <div onclick="selectColor('${c}')" style="width:20px;height:20px;border-radius:50%;background:${c};cursor:pointer;
      border:2px solid ${c===S.selectedColor?'#fff':'transparent'};transition:border .15s;"></div>`).join('');
}
function selectColor(c){S.selectedColor=c;renderColorPicker();}

function checkCanExecute() {
  const apiKey=document.getElementById('api-key-input').value.trim();
  const criterion=document.getElementById('criterion-input').value;
  document.getElementById('execute-btn').disabled=!(apiKey&&S.comments.length>0&&criterion.length>=30&&S.mainTags.length>=1);
}

// ─── Execute ──────────────────────────────────────────────────────────────────
const STEPS=[
  {id:'tags',    label:'Gerando temas identificados'},
  {id:'classify',label:'Classificando comentários'},
  {id:'summary', label:'Análise estratégica'},
];

function setProgress(pct, log, stepId) {
  document.getElementById('progress-fill').style.width=pct+'%';
  document.getElementById('progress-pct').textContent=pct+'%';
  document.getElementById('processing-log').textContent=log;
  document.getElementById('steps-list').innerHTML=STEPS.map(s=>{
    const si=STEPS.findIndex(x=>x.id===stepId), ii=STEPS.findIndex(x=>x.id===s.id);
    const done=ii<si||pct===100, active=s.id===stepId&&pct<100;
    return `<div class="step-item" style="border-color:${active?'var(--accent)':'var(--border)'};">
      <span>${done?'✅':active?'⏳':'⬜'}</span>
      <span style="font-size:13px;color:${active?'var(--accent)':done?'var(--green)':'var(--muted)'};font-weight:${active||done?700:400};">${s.label}</span>
    </div>`;
  }).join('');
}

async function executeAnalysis() {
  const criterion=document.getElementById('criterion-input').value;
  const context=document.getElementById('context-input').value;
  showPage('processing-page');

  try {
    // Step 1: generate 8 thematic tags
    setProgress(5,"Analisando comentários e gerando temas...","tags");
    const sample=S.comments.length>100
      ?S.comments.filter((_,i)=>i%Math.ceil(S.comments.length/100)===0).slice(0,100)
      :S.comments;
    S.themeTags = await generateThematicTags(sample, criterion);

    // Step 2: classify in batches
    const BATCH=10;
    S.results=[];
    for (let i=0;i<S.comments.length;i+=BATCH) {
      const batch=S.comments.slice(i,i+BATCH);
      const pct=Math.round(10+(i/S.comments.length)*75);
      setProgress(pct,`Classificando ${i+1}–${Math.min(i+BATCH,S.comments.length)} de ${S.comments.length}...`,"classify");
      const classified=await classifyBatch(batch,S.mainTags,S.themeTags);
      batch.forEach((comment,j)=>S.results.push({comment,...(classified[j]||{main:S.mainTags[0].name,theme:S.themeTags[0]?.name||"—"})}));
    }

    // Step 3: summary
    setProgress(90,"Gerando análise estratégica...","summary");
    const mainCounts={};
    S.mainTags.forEach(t=>mainCounts[t.name]=0);
    S.results.forEach(r=>{mainCounts[r.main]=(mainCounts[r.main]||0)+1;});
    const summary=await generateSummary(mainCounts,S.results.length,criterion,context);

    setProgress(100,"Concluído!","summary");
    await new Promise(r=>setTimeout(r,500));
    buildReport(summary,context,mainCounts);

  } catch(e) {
    alert("Erro: "+e.message);
    showPage('setup-page');
  }
}

// ─── Report ───────────────────────────────────────────────────────────────────
function buildReport(summary, context, mainCounts) {
  document.getElementById('report-date').textContent="Diagnóstico gerado em "+new Date().toLocaleDateString('pt-BR');
  document.getElementById('report-context').textContent=context||'';
  document.getElementById('report-summary').textContent=summary;

  if (S.screenshot) {
    const reader=new FileReader();
    reader.onload=ev=>{const img=document.getElementById('report-screenshot');img.src=ev.target.result;img.style.display='block';};
    reader.readAsDataURL(S.screenshot);
  }

  // Stat cards
  const cards=document.getElementById('stat-cards');
  cards.innerHTML='';
  S.mainTags.forEach(t=>{
    const c=mainCounts[t.name]||0, pct=S.results.length?Math.round(c/S.results.length*100):0;
    const color=tagColor(t.name);
    const div=document.createElement('div');
    div.className='stat-card';
    div.style.borderColor=color+'33';
    div.innerHTML=`
      <div style="width:8px;height:8px;border-radius:50%;background:${color};margin-bottom:8px;"></div>
      <div style="font-weight:700;font-size:12px;margin-bottom:4px;">${t.name}</div>
      <div class="stat-number" style="color:${color};">${c}</div>
      <div style="font-size:11px;color:var(--muted);margin-top:2px;">${pct}%</div>`;
    div.onclick=()=>{
      S.filterMain=S.filterMain===t.name?'all':t.name;
      applyFilters();
      document.querySelectorAll('.stat-card').forEach(el=>el.style.borderColor='var(--border)');
      if(S.filterMain!=='all') div.style.borderColor=color;
    };
    cards.appendChild(div);
  });
  const tot=document.createElement('div');
  tot.className='stat-card';
  tot.innerHTML=`<div style="width:8px;height:8px;border-radius:50%;background:var(--muted);margin-bottom:8px;"></div>
    <div style="font-weight:700;font-size:12px;margin-bottom:4px;">TOTAL</div>
    <div class="stat-number">${S.results.length}</div>
    <div style="font-size:11px;color:var(--muted);margin-top:2px;">comentários</div>`;
  cards.appendChild(tot);

  // Main chart
  if (S.mainChart) S.mainChart.destroy();
  S.mainChart=new Chart(document.getElementById('main-chart').getContext('2d'),{
    type:'bar',
    data:{labels:S.mainTags.map(t=>t.name),datasets:[{data:S.mainTags.map(t=>mainCounts[t.name]||0),backgroundColor:S.mainTags.map(t=>tagColor(t.name)),borderRadius:4,borderSkipped:false}]},
    options:{indexAxis:'y',plugins:{legend:{display:false}},scales:{x:{display:false,grid:{display:false}},y:{ticks:{color:'#666',font:{size:11}},grid:{color:'#222'}}}}
  });

  // Theme cards
  const themeCounts={};
  S.themeTags.forEach(t=>themeCounts[t.name]=0);
  S.results.forEach(r=>{themeCounts[r.theme]=(themeCounts[r.theme]||0)+1;});

  const themeCards=document.getElementById('theme-cards');
  themeCards.innerHTML='';
  S.themeTags.forEach((t,i)=>{
    const count=themeCounts[t.name]||0, pct=S.results.length?Math.round(count/S.results.length*100):0;
    const color=aiTagColor(t,i);
    const div=document.createElement('div');
    div.className='theme-card';
    div.innerHTML=`
      <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
        <span style="font-weight:700;font-size:12px;color:${color};">${t.name}</span>
        <span style="font-weight:900;font-size:14px;color:${color};">${count}</span>
      </div>
      <div style="font-size:11px;color:var(--muted);line-height:1.4;margin-bottom:8px;">${t.description}</div>
      <div class="theme-bar-bg"><div class="theme-bar-fill" style="width:${pct}%;background:${color};"></div></div>
      <div style="font-size:10px;color:var(--muted);margin-top:3px;">${pct}% dos comentários</div>`;
    div.onclick=()=>{
      S.filterTheme=S.filterTheme===t.name?'all':t.name;
      applyFilters();
      document.querySelectorAll('.theme-card').forEach(el=>{el.style.background='var(--card)';el.style.borderColor='var(--border)';});
      if(S.filterTheme!=='all'){div.style.background=color+'15';div.style.borderColor=color;}
    };
    themeCards.appendChild(div);
  });

  // Theme chart
  const sorted=[...S.themeTags].sort((a,b)=>(themeCounts[b.name]||0)-(themeCounts[a.name]||0));
  if(S.themeChart) S.themeChart.destroy();
  S.themeChart=new Chart(document.getElementById('theme-chart').getContext('2d'),{
    type:'bar',
    data:{labels:sorted.map(t=>t.name),datasets:[{data:sorted.map(t=>themeCounts[t.name]||0),backgroundColor:sorted.map((t,i)=>aiTagColor(t,i)),borderRadius:4,borderSkipped:false}]},
    options:{indexAxis:'y',plugins:{legend:{display:false}},scales:{x:{display:false,grid:{display:false}},y:{ticks:{color:'#666',font:{size:10}},grid:{color:'#222'}}}}
  });

  S.filterMain='all';S.filterTheme='all';S.currentPage=1;
  applyFilters();
  showPage('report-page');
  document.getElementById('header-actions').innerHTML=`<button class="btn-ghost" onclick="newAnalysis()">← Nova Análise</button>`;
  saveState();
}

function applyFilters() {
  const search=document.getElementById('search-input').value.toLowerCase();
  const filtered=S.results.filter(r=>{
    if(S.filterMain!=='all'&&r.main!==S.filterMain) return false;
    if(S.filterTheme!=='all'&&r.theme!==S.filterTheme) return false;
    if(search&&!r.comment.toLowerCase().includes(search)) return false;
    return true;
  });
  document.getElementById('filtered-count').textContent=filtered.length;

  const af=document.getElementById('active-filters');
  if(S.filterMain!=='all'||S.filterTheme!=='all'){
    af.style.display='flex';
    af.innerHTML=
      (S.filterMain!=='all'?`<span class="tag-badge" style="background:${tagColor(S.filterMain)}22;color:${tagColor(S.filterMain)};border:1px solid ${tagColor(S.filterMain)}44;cursor:pointer;" onclick="S.filterMain='all';applyFilters()">✕ ${S.filterMain}</span>`:'')
      +(S.filterTheme!=='all'?`<span class="tag-badge" style="background:#aaa2;color:#aaa;border:1px solid #aaa4;cursor:pointer;" onclick="S.filterTheme='all';applyFilters()">✕ ${S.filterTheme}</span>`:'')
      +`<button onclick="S.filterMain='all';S.filterTheme='all';applyFilters();" style="background:none;border:none;color:var(--muted);font-size:11px;cursor:pointer;">Limpar filtros</button>`;
  } else { af.style.display='none'; }

  const totalPages=Math.ceil(filtered.length/S.perPage);
  if(S.currentPage>totalPages) S.currentPage=1;
  const paginated=filtered.slice((S.currentPage-1)*S.perPage,S.currentPage*S.perPage);

  document.getElementById('table-body').innerHTML=paginated.map((r,i)=>{
    const num=(S.currentPage-1)*S.perPage+i+1;
    const mc=tagColor(r.main);
    const ti=S.themeTags.findIndex(t=>t.name===r.theme);
    const tc=aiTagColor(S.themeTags[ti]||{name:r.theme},ti);
    const comment=r.comment.length>160?r.comment.slice(0,160)+'…':r.comment;
    return `<div class="table-row">
      <span class="table-num">${num}</span>
      <span class="table-comment">${comment}</span>
      ${makeBadge(r.main,mc)}
      ${makeBadge(r.theme,tc)}
    </div>`;
  }).join('')||'<div style="padding:40px;text-align:center;color:var(--muted);">Nenhum comentário encontrado.</div>';

  const pag=document.getElementById('pagination');
  pag.innerHTML=totalPages>1?`
    <button class="page-btn" onclick="changePage(${S.currentPage-1})" ${S.currentPage===1?'disabled':''}>‹</button>
    <span style="font-size:13px;color:var(--muted);">Página ${S.currentPage} de ${totalPages}</span>
    <button class="page-btn" onclick="changePage(${S.currentPage+1})" ${S.currentPage===totalPages?'disabled':''}>›</button>`:'';
}

function changePage(p){S.currentPage=p;applyFilters();}

function exportExcel() {
  const rows=S.results.map((r,i)=>({"#":i+1,"Comentário":r.comment,"Tag Principal":r.main,"Tema":r.theme}));
  const ws=XLSX.utils.json_to_sheet(rows);
  const wb=XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb,ws,"Diagnóstico");
  XLSX.writeFile(wb,`diagnostico-${new Date().toLocaleDateString('pt-BR').replace(/\//g,'-')}.xlsx`);
}

function newAnalysis(){
  S.filterMain='all';S.filterTheme='all';
  localStorage.removeItem('diagnostico_state');
  showPage('setup-page');
  document.getElementById('header-actions').innerHTML='';
}

function saveState() {
  try {
    const snapshot = {
      results: S.results,
      mainTags: S.mainTags,
      themeTags: S.themeTags,
      summary: document.getElementById('report-summary').textContent,
      context: document.getElementById('report-context').textContent,
      date: document.getElementById('report-date').textContent,
      screenshot: document.getElementById('report-screenshot').src || '',
    };
    localStorage.setItem('diagnostico_state', JSON.stringify(snapshot));
  } catch(e) { console.warn('Não foi possível salvar estado:', e); }
}

function restoreState() {
  try {
    const raw = localStorage.getItem('diagnostico_state');
    if (!raw) return;
    const snap = JSON.parse(raw);
    if (!snap.results || !snap.results.length) return;
    S.results   = snap.results;
    S.mainTags  = snap.mainTags;
    S.themeTags = snap.themeTags;
    document.getElementById('report-summary').textContent = snap.summary || '';
    document.getElementById('report-context').textContent = snap.context || '';
    document.getElementById('report-date').textContent    = snap.date || '';
    if (snap.screenshot && snap.screenshot.startsWith('data:')) {
      const img = document.getElementById('report-screenshot');
      img.src = snap.screenshot;
      img.style.display = 'block';
    }
    buildReport(S.results, S.mainTags, S.themeTags);
  } catch(e) { console.warn('Não foi possível restaurar estado:', e); }
}

async function exportPDF() {
  const btn = document.getElementById('btn-pdf');
  const orig = btn.textContent;
  btn.textContent = 'Gerando PDF...';
  btn.disabled = true;

  try {
    const { jsPDF } = window.jspdf;
    const reportEl = document.getElementById('report-page');

    const canvas = await html2canvas(reportEl, {
      backgroundColor: '#0d0d0d',
      scale: 1.5,
      useCORS: true,
      logging: false,
    });

    const imgData = canvas.toDataURL('image/jpeg', 0.92);
    const pdf = new jsPDF({ orientation: 'p', unit: 'mm', format: 'a4' });
    const pageW = pdf.internal.pageSize.getWidth();
    const pageH = pdf.internal.pageSize.getHeight();
    const imgW  = pageW;
    const imgH  = (canvas.height * imgW) / canvas.width;

    let y = 0;
    while (y < imgH) {
      if (y > 0) pdf.addPage();
      pdf.addImage(imgData, 'JPEG', 0, -y, imgW, imgH);
      y += pageH;
    }

    const date = new Date().toLocaleDateString('pt-BR').replace(/\//g, '-');
    pdf.save(`relatorio-diagnostico-${date}.pdf`);
  } catch(e) {
    alert('Erro ao gerar PDF: ' + e.message);
  } finally {
    btn.textContent = orig;
    btn.disabled = false;
  }
}

renderTags();
restoreState();
renderColorPicker();
</script>
</body>
</html>
