const palavrasChaveSuspeitas = [
  /pix/i, /cart[aã]o/i, /senha/i, /urgente/i, /b[oô]nus/i,
  /confirma/i, /brinde/i, /expira/i, /criptomoeda/i,
  /transfer[êe]ncia/i, /premi[oô]/i, /ganhador/i,
  /login/i, /verifica/i, /validar/i, /boleto/i, /pagamento/i,
  /recarga/i, /dep[oó]sito/i, /s[aã]o seguro/i, /clique aqui/i,
  /atualizar/i, /cart[aã]o de cr[eé]dito/i, /senha banc[aá]ria/i
];

const whitelist = [
  // Computador Pessoal – Redes sociais e comunicação
  "www.facebook.com", "facebook.com",
  "www.instagram.com", "instagram.com",
  "web.whatsapp.com",
  "twitter.com", "www.twitter.com",
  "discord.com", "www.discord.com",
  "web.telegram.org", "telegram.org",

  // Computador Pessoal – Entretenimento
  "www.youtube.com", "youtube.com",
  "www.netflix.com", "netflix.com",
  "open.spotify.com", "spotify.com",
  "www.twitch.tv", "twitch.tv",
  "www.tiktok.com", "tiktok.com",

  // Computador Pessoal – Compras e e-commerce
  "www.amazon.com", "amazon.com",
  "www.mercadolivre.com.br", "mercadolivre.com.br",
  "www.americanas.com.br", "americanas.com.br",
  "shopee.com.br", "www.shopee.com.br",
  "www.aliexpress.com", "aliexpress.com",

  // Computador Pessoal – Notícias e portais
  "www.globo.com", "globo.com",
  "www.uol.com.br", "uol.com.br",
  "g1.globo.com",
  "www.r7.com", "r7.com",
  "www.cnnbrasil.com.br", "cnnbrasil.com.br",

  // Computador Pessoal – Bancos e finanças
  "www.nubank.com.br", "nubank.com.br",
  "www.itau.com.br", "itau.com.br",
  "www.bradesco.com.br", "bradesco.com.br",
  "www.bb.com.br", "bb.com.br",
  "www.picpay.com", "picpay.com",

  // Computador Pessoal – Serviços e utilitários
  "drive.google.com", "docs.google.com", "photos.google.com",
  "www.icloud.com", "icloud.com",
  "outlook.live.com", "outlook.com",

  // Computador Pessoal – Downloads e jogos
  "store.steampowered.com", "steampowered.com",
  "www.epicgames.com", "epicgames.com",
  "www.origin.com", "origin.com",
  "www.mediafire.com", "mediafire.com",
  "mega.nz",

  // Computador Escolar – Plataformas educacionais
  "classroom.google.com",
  "teams.microsoft.com",
  "moodle.org",
  "pt.khanacademy.org",
  "escoladigital.sp.gov.br",

  // Computador Escolar – Ferramentas de pesquisa e produtividade
  "www.google.com", "google.com",
  "docs.google.com", "sheets.google.com", "slides.google.com",
  "www.wikipedia.org", "wikipedia.org",
  "www.grammarly.com", "grammarly.com",
  "www.canva.com", "canva.com",

  // Computador Escolar – Portais de educação e governo
  "enem.inep.gov.br",
  "portal.mec.gov.br",
  "www.brasilescola.uol.com.br", "brasilescola.uol.com.br",
  "educamaisbrasil.com.br",

  // Computador Escolar – Simulados e conteúdos acadêmicos
  "www.descomplica.com.br", "descomplica.com.br",
  "www.stoodi.com.br", "stoodi.com.br",
  "www.geekie.com.br", "geekie.com.br",
  "novaescola.org.br",
  "www.passeidireto.com", "passeidireto.com",

  // Computador Escolar – Bibliotecas e repositórios científicos
  "www.scielo.br", "scielo.br",
  "scholar.google.com",
  "www.capes.gov.br", "capes.gov.br",
  "www.wdl.org", "wdl.org",

  // Computador Escolar – Email e armazenamento
  "mail.google.com", "gmail.com",
  "outlook.office365.com", "outlook.com",
  "drive.google.com", "docs.google.com"
];

// Example suspicious domain pattern list
const suspiciousDomainPatterns = [
  /.*-secure-login\.com$/,  // example suspicious domain pattern
  /.*-verify-account\.net$/,
  /.*-payment-info\.xyz$/,
  /(^|\.)login-facebook\.com$/,
  /(^|\.)micros0ft-security\.com$/,
  /(^|\.)bradescoseguroonline\.info$/,
  /(^|\.)update-flashplayer\.xyz$/,
  /(^|\.)premio-whatsapp\.com$/,
  /(^|\.)abc123xyz\.top$/,
  /(^|\.)mining-service\.online$/,
  /(^|\.)g00gle\.com$/,
  /(^|\.)bbseguroclientes\.com$/,
  /(^|\.)apple-id-login\.net$/,
  /(^|\.)paypal-verification\.info$/,
  /(^|\.)caixa-atualizacao\.xyz$/,
  /(^|\.)icloud-security\.click$/,
  /(^|\.)support-amazon\.top$/,
  /(^|\.)netflix-user-access\.ml$/,
  /(^|\.)seguranca-itau\.cf$/,
  /(^|\.)whatsapp-premio\.tk$/,
  /(^|\.)gov-brasil\.support$/,
  /(^|\.)win10-update\.online$/,
  /(^|\.)malware-checker\.xyz$/
];

// Additional functions for phishing visual detection and ML integration

// Function to check domain similarity (basic Levenshtein distance)
function levenshteinDistance(a, b) {
  const matrix = [];
  for (let i = 0; i <= b.length; i++) {
    matrix[i] = [i];
  }
  for (let j = 0; j <= a.length; j++) {
    matrix[0][j] = j;
  }
  for (let i = 1; i <= b.length; i++) {
    for (let j = 1; j <= a.length; j++) {
      if (b.charAt(i - 1) === a.charAt(j - 1)) {
        matrix[i][j] = matrix[i - 1][j - 1];
      } else {
        matrix[i][j] = Math.min(
          matrix[i - 1][j - 1] + 1,
          Math.min(matrix[i][j - 1] + 1, matrix[i - 1][j] + 1)
        );
      }
    }
  }
  return matrix[b.length][a.length];
}

// Function to check if domain is similar to known official domains
function isDomainSimilar(domain, officialDomains, threshold = 2) {
  return officialDomains.some(officialDomain => levenshteinDistance(domain, officialDomain) <= threshold);
}

// Function to detect psychological manipulation phrases
const manipulationPhrases = [
  /sua conta será bloqueada/i,
  /clique agora/i,
  /você ganhou um prêmio/i,
  /ação imediata necessária/i,
  /atualize seus dados/i,
  /confira seu prêmio/i,
  /última chance/i
];

// Function to detect manipulation phrases in page text
function detectManipulationPhrases(text) {
  return manipulationPhrases.some(rx => rx.test(text));
}

// Function to create and show alert overlay
function showAlert(message) {
  const alerta = document.createElement("div");
  alerta.style = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(255, 0, 0, 0.85);
    z-index: 999999;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: "Segoe UI", sans-serif;
  `;
  alerta.innerHTML = `
    <div style="background: #fff; padding: 30px; border-radius: 10px; text-align: center; max-width: 400px; position: relative; box-shadow: 0 0 15px rgba(0,0,0,0.3);">
      <img src="icon_48.png" style="width: 48px; height: 48px; margin-bottom: 15px;" />
      <h2 style="color: red; font-size: 22px; margin-bottom: 15px;">⚠️ Alerta de Segurança</h2>
      <p style="margin-bottom: 20px; font-size: 16px; color: #333;">${message}</p>
      <button id="continuar" style="margin: 10px; padding: 12px 25px; font-size: 16px; cursor: pointer; border: none; border-radius: 6px; background: #007bff; color: white;">Continuar</button>
      <button id="sair" style="margin: 10px; padding: 12px 25px; font-size: 16px; cursor: pointer; border: none; border-radius: 6px; background: #dc3545; color: white;">Sair do Site</button>
      <p style="color:gray; font-size:12px; margin-top: 20px;">Scam Guard © Todos os direitos reservados</p>
    </div>
  `;
  document.body.appendChild(alerta);

  document.getElementById("sair").onclick = () => {
    window.location.href = "https://www.google.com";
  };
  document.getElementById("continuar").onclick = () => {
    alerta.remove();
  };
}

// Real-time DOM mutation observer
const observer = new MutationObserver(mutations => {
  mutations.forEach(mutation => {
    // Example: detect added nodes that might be pop-ups or suspicious elements
    mutation.addedNodes.forEach(node => {
      if (node.nodeType === Node.ELEMENT_NODE) {
        const el = node;
        const style = window.getComputedStyle(el);
        // Block invisible pop-ups or auto clicks
        if ((style.visibility === 'hidden' || style.display === 'none' || style.opacity === '0') && el.tagName === 'DIV') {
          el.remove();
          console.log('Blocked invisible pop-up or auto click element.');
        }
      }
    });
  });
});
observer.observe(document.body, { childList: true, subtree: true });

// Detect suspicious events
window.addEventListener('beforeunload', event => {
  showAlert('Evento suspeito detectado: tentativa de sair da página.');
  event.preventDefault();
  event.returnValue = '';
});

const originalSetTimeout = window.setTimeout;
window.setTimeout = function (fn, delay, ...args) {
  if (typeof fn === 'string' && /location\.href\s*=/.test(fn)) {
    showAlert('Evento suspeito detectado: redirecionamento via setTimeout.');
    return;
  }
  return originalSetTimeout(fn, delay, ...args);
};

// Enhanced form verification
function monitorForms() {
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    // Detect forms inside iframes
    if (form.closest('iframe')) {
      showAlert('Formulário detectado dentro de iframe, possível risco de segurança.');
    }
    form.addEventListener('submit', event => {
      const action = form.action || '';
      const url = new URL(action, window.location.href);
      if (!whitelist.includes(url.hostname)) {
        showAlert('Envio de dados para domínio não verificado detectado.');
        event.preventDefault();
      }
      // Detect sensitive inputs
      const sensitiveInputs = form.querySelectorAll('input[type="password"], input[name*="card"], input[name*="cpf"], input[name*="senha"]');
      if (sensitiveInputs.length > 0) {
        showAlert('Formulário com dados sensíveis detectado.');
      }
    });
  });
}
monitorForms();

// Phishing visual detection: favicon and layout comparison
function checkFavicon() {
  const link = document.querySelector('link[rel~="icon"]');
  if (link) {
    const faviconUrl = link.href;
    // Compare faviconUrl with known official favicons (example list)
    const officialFavicons = [
      'https://www.nubank.com.br/favicon.ico',
      'https://www.itau.com.br/favicon.ico',
      'https://www.bb.com.br/favicon.ico'
    ];
    if (!officialFavicons.includes(faviconUrl)) {
      showAlert('Favicon não corresponde ao site oficial, possível site clonado.');
    }
  }
}
checkFavicon();

// Check domain similarity with official domains
const officialDomains = [
  'nubank.com.br',
  'itau.com.br',
  'bb.com.br'
];
if (isDomainSimilar(dominio, officialDomains)) {
  showAlert('Domínio semelhante a site oficial detectado, possível phishing.'); 
}

// Detect psychological manipulation phrases
if (detectManipulationPhrases(textoPagina)) {
  showAlert('Frases de manipulação psicológica detectadas na página.');
}

async function loadModel() {
  try {
    // Load a pre-trained model or your custom model here
    // For demonstration, we create a simple model
    const model = tf.sequential();
    model.add(tf.layers.dense({units: 5, inputShape: [10], activation: 'relu'}));
    model.add(tf.layers.dense({units: 2, activation: 'softmax'}));
    model.compile({optimizer: 'adam', loss: 'categoricalCrossentropy', metrics: ['accuracy']});
    console.log('TensorFlow.js model created and compiled.');
    return model;
  } catch (error) {
    console.error('Error loading TensorFlow.js model:', error);
  }
}

async function predict(inputData) {
  const model = await loadModel();
  if (!model) return;
  // Prepare input tensor
  const inputTensor = tf.tensor2d([inputData]);
  // Make prediction
  const prediction = model.predict(inputTensor);
  prediction.print();
  // Process prediction results here
}

// Example usage: dummy input data for prediction
const dummyInput = [0,0,0,0,0,0,0,0,0,0];
predict(dummyInput);

