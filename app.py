from flask import Flask
from datetime import datetime
from zoneinfo import ZoneInfo
import socket

app = Flask(__name__)

# horário em que a aplicação subiu, ou seja, o horário do último deploy
DEPLOY_EM = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M")

PAGINA = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Hello World | Atividade TTC III</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
    font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e, #1a1a3e);
    background-size: 400% 400%;
    animation: fundo 18s ease infinite;
    overflow-x: hidden;
  }

  @keyframes fundo {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
  }

  .orbe {
    position: fixed;
    border-radius: 50%;
    filter: blur(90px);
    opacity: 0.45;
    pointer-events: none;
    z-index: 0;
  }
  .orbe1 { width: 380px; height: 380px; background: #7873f5; top: -110px; left: -90px; animation: flutua 14s ease-in-out infinite; }
  .orbe2 { width: 320px; height: 320px; background: #ff6ec4; bottom: -100px; right: -70px; animation: flutua 18s ease-in-out infinite reverse; }
  .orbe3 { width: 260px; height: 260px; background: #38bdf8; top: 55%; left: 8%; animation: flutua 22s ease-in-out infinite; }

  @keyframes flutua {
    0%, 100% { transform: translate(0, 0) scale(1); }
    50%      { transform: translate(40px, -50px) scale(1.15); }
  }

  .card {
    position: relative;
    z-index: 1;
    width: 100%;
    max-width: 620px;
    padding: 52px 44px 38px;
    text-align: center;
    background: rgba(255, 255, 255, 0.07);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 28px;
    backdrop-filter: blur(22px);
    box-shadow: 0 30px 70px rgba(0, 0, 0, 0.5);
    animation: entrada 0.9s cubic-bezier(0.2, 0.8, 0.2, 1);
  }

  @keyframes entrada {
    from { opacity: 0; transform: translateY(36px) scale(0.96); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
  }

  .status {
    display: inline-flex;
    align-items: center;
    gap: 9px;
    margin-bottom: 26px;
    padding: 7px 16px;
    font-size: 12.5px;
    font-weight: 600;
    letter-spacing: 0.5px;
    color: #86efac;
    background: rgba(74, 222, 128, 0.12);
    border: 1px solid rgba(74, 222, 128, 0.3);
    border-radius: 999px;
  }

  .ponto {
    width: 8px; height: 8px;
    background: #4ade80;
    border-radius: 50%;
    animation: pulsa 1.8s ease-in-out infinite;
  }

  @keyframes pulsa {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(74, 222, 128, 0.7); }
    50%      { opacity: 0.7; box-shadow: 0 0 0 9px rgba(74, 222, 128, 0); }
  }

  h1 {
    font-size: clamp(38px, 8vw, 62px);
    font-weight: 800;
    letter-spacing: -1.5px;
    line-height: 1.05;
    background: linear-gradient(120deg, #ff6ec4, #7873f5, #38bdf8);
    background-size: 200% auto;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: brilho 5s linear infinite;
  }

  @keyframes brilho {
    to { background-position: 200% center; }
  }

  .sub {
    margin-top: 14px;
    font-size: 16px;
    line-height: 1.6;
    color: rgba(255, 255, 255, 0.62);
  }

  .stack {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 9px;
    margin: 30px 0 34px;
  }

  .chip {
    padding: 7px 15px;
    font-size: 12.5px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.82);
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.13);
    border-radius: 10px;
    transition: 0.25s;
  }
  .chip:hover {
    transform: translateY(-3px);
    background: rgba(255, 255, 255, 0.16);
    border-color: rgba(255, 255, 255, 0.3);
  }

  .botao {
    position: relative;
    padding: 17px 44px;
    font-family: inherit;
    font-size: 16.5px;
    font-weight: 700;
    color: #fff;
    background: linear-gradient(120deg, #ff6ec4, #7873f5);
    background-size: 200% auto;
    border: none;
    border-radius: 14px;
    cursor: pointer;
    box-shadow: 0 12px 30px rgba(120, 115, 245, 0.45);
    transition: 0.3s;
  }
  .botao:hover {
    background-position: right center;
    transform: translateY(-3px);
    box-shadow: 0 18px 40px rgba(255, 110, 196, 0.5);
  }
  .botao:active { transform: translateY(-1px) scale(0.97); }

  .contador {
    margin-top: 20px;
    font-size: 13.5px;
    color: rgba(255, 255, 255, 0.45);
  }
  .contador b { color: #ff6ec4; font-size: 15px; }

  .rodape {
    margin-top: 34px;
    padding-top: 24px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }

  .autor {
    font-size: 17px;
    font-weight: 700;
    color: #fff;
    letter-spacing: 0.3px;
  }

  .servidor {
    margin-top: 9px;
    font-family: "Consolas", monospace;
    font-size: 11.5px;
    color: rgba(255, 255, 255, 0.35);
  }

  #confete {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 9;
  }

  .toast {
    position: fixed;
    top: 28px;
    left: 50%;
    z-index: 20;
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 16px 26px;
    color: #fff;
    background: rgba(30, 27, 75, 0.92);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 16px;
    backdrop-filter: blur(14px);
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
    transform: translate(-50%, -160px);
    opacity: 0;
    transition: 0.5s cubic-bezier(0.2, 0.9, 0.3, 1.3);
  }
  .toast.show { transform: translate(-50%, 0); opacity: 1; }
  .toast .emoji { font-size: 26px; animation: gira 0.7s ease; }
  .toast .txt { font-size: 15px; font-weight: 600; white-space: nowrap; }

  @keyframes gira {
    0%   { transform: scale(0) rotate(-90deg); }
    70%  { transform: scale(1.35) rotate(12deg); }
    100% { transform: scale(1) rotate(0); }
  }

  @media (max-width: 520px) {
    .card { padding: 40px 26px 30px; }
    .toast .txt { white-space: normal; }
  }
</style>
</head>
<body>

  <div class="orbe orbe1"></div>
  <div class="orbe orbe2"></div>
  <div class="orbe orbe3"></div>

  <canvas id="confete"></canvas>

  <div class="toast" id="toast">
    <span class="emoji" id="emoji">&#127881;</span>
    <span class="txt" id="txt">Presenca confirmada!</span>
  </div>

  <main class="card">
    <div class="status"><span class="ponto"></span>SERVIDOR ONLINE</div>

    <h1>Hello World!</h1>

    <p class="sub">
      Aplicacao Web hospedada na Oracle Cloud Infrastructure<br>
      servida por Nginx como proxy reverso<br>
      publicada automaticamente via GitHub Actions (CI/CD)
    </p>

    <div class="stack">
      <span class="chip">Ubuntu 24.04</span>
      <span class="chip">Nginx</span>
      <span class="chip">Gunicorn</span>
      <span class="chip">Flask</span>
      <span class="chip">systemd</span>
      <span class="chip">GitHub Actions</span>
      <span class="chip">Discord</span>
    </div>

    <button class="botao" id="btn">Passei por aqui</button>

    <p class="contador">Visitas registradas nesta sessao: <b id="num">0</b></p>

    <div class="rodape">
      <p class="autor">Atividade TTC III &bull; Joao Manuel</p>
      <p class="servidor">host: __HOST__</p>
      <p class="servidor">último deploy: __DEPLOY__</p>
    </div>
  </main>

<script>
  var canvas = document.getElementById("confete");
  var ctx = canvas.getContext("2d");
  var pecas = [];

  function ajustar() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  ajustar();
  window.addEventListener("resize", ajustar);

  var cores = ["#ff6ec4", "#7873f5", "#4ade80", "#facc15", "#38bdf8", "#fb7185", "#ffffff"];

  function soltarConfete() {
    var alvo = document.getElementById("btn").getBoundingClientRect();
    var cx = alvo.left + alvo.width / 2;
    var cy = alvo.top + alvo.height / 2;
    for (var i = 0; i < 160; i++) {
      pecas.push({
        x: cx + (Math.random() - 0.5) * 120,
        y: cy,
        vx: (Math.random() - 0.5) * 13,
        vy: Math.random() * -15 - 4,
        w: 5 + Math.random() * 8,
        h: 8 + Math.random() * 10,
        cor: cores[Math.floor(Math.random() * cores.length)],
        rot: Math.random() * 6.28,
        vr: (Math.random() - 0.5) * 0.35,
        vida: 1
      });
    }
  }

  function animar() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (var i = 0; i < pecas.length; i++) {
      var p = pecas[i];
      p.vy += 0.32;
      p.vx *= 0.99;
      p.x += p.vx;
      p.y += p.vy;
      p.rot += p.vr;
      p.vida -= 0.007;
      ctx.save();
      ctx.globalAlpha = p.vida > 0 ? p.vida : 0;
      ctx.translate(p.x, p.y);
      ctx.rotate(p.rot);
      ctx.fillStyle = p.cor;
      ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h);
      ctx.restore();
    }
    pecas = pecas.filter(function (p) {
      return p.vida > 0 && p.y < canvas.height + 80;
    });
    requestAnimationFrame(animar);
  }
  animar();

  var frases = [
    "Presenca confirmada!",
    "Mais um visitante registrado!",
    "Boa, voce passou por aqui!",
    "Que alegria te ver por aqui!",
    "Registrado com sucesso!"
  ];
  var emojis = ["\u{1F389}", "\u{1F38A}", "\u{2728}", "\u{1F973}", "\u{1F680}"];

  var toast = document.getElementById("toast");
  var cliques = 0;
  var tempo;

  document.getElementById("btn").addEventListener("click", function () {
    soltarConfete();
    cliques++;
    document.getElementById("num").textContent = cliques;
    var n = Math.floor(Math.random() * frases.length);
    document.getElementById("txt").textContent = frases[n];
    var e = document.getElementById("emoji");
    e.textContent = emojis[Math.floor(Math.random() * emojis.length)];
    e.style.animation = "none";
    void e.offsetWidth;
    e.style.animation = "gira 0.7s ease";
    toast.classList.add("show");
    clearTimeout(tempo);
    tempo = setTimeout(function () {
      toast.classList.remove("show");
    }, 3500);
  });
</script>
</body>
</html>"""


@app.route("/")
def hello():
    pagina = PAGINA.replace("__HOST__", socket.gethostname())
    pagina = pagina.replace("__DATA__", datetime.now().strftime("%d/%m/%Y %H:%M"))
    pagina = pagina.replace("__DEPLOY__", DEPLOY_EM)
    return pagina


if __name__ == "__main__":
    app.run()
