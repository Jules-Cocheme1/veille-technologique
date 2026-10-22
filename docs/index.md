<div id="haut-de-page" class="dashboard-nav">
  <a class="dashboard-brand" href="#haut-de-page" aria-label="VTEN CONTINU, accueil">
    <span class="dashboard-brand__mark" aria-hidden="true">V</span>
    <span>VTEN <strong>CONTINU</strong></span>
  </a>
  <nav aria-label="Navigation principale">
    <a href="#haut-de-page" aria-current="page">Accueil</a>
    <a href="#axes-de-veille">Axes de veille</a>
    <a href="#methodologie">Méthodologie</a>
  </nav>
  <a class="dashboard-live" href="#dernieres-publications"><span class="status-dot"></span> Flux RSS actif</a>
</div>

<div class="veille-hero">
  <div class="veille-hero__copy">
    <p class="eyebrow">Veille indépendante · sources identifiées</p>
    <h1>Comprendre les signaux.<br><span>Anticiper les changements.</span></h1>
    <p class="veille-hero__intro">Un regard clair et documenté sur la cybersécurité, l’intelligence artificielle et les infrastructures qui évoluent.</p>
    <div class="hero-actions">
      <a class="hero-link" href="#dernieres-publications">Explorer les publications <span aria-hidden="true">↓</span></a>
      <a class="hero-secondary-link" href="a-propos/">Notre méthodologie <span aria-hidden="true">↗</span></a>
    </div>
  </div>
  <div class="veille-hero__panel" aria-hidden="true">
    <div class="orbit orbit--outer"></div>
    <div class="orbit orbit--inner"></div>
    <div class="hero-core"><span>VT</span><small>EN CONTINU</small></div>
    <span class="orbit-label orbit-label--one">CYBER</span>
    <span class="orbit-label orbit-label--two">IA</span>
    <span class="orbit-label orbit-label--three">SYSTÈMES</span>
  </div>
</div>

<section class="stats-grid" aria-label="La veille en chiffres" data-stats>
  <article class="stat-card stat-card--featured">
    <span class="stat-label">Publications suivies</span>
    <strong class="stat-value" id="stat-publications">—</strong>
    <span class="stat-note">dans le flux actuel</span>
  </article>
  <article class="stat-card">
    <span class="stat-label">Sources représentées</span>
    <strong class="stat-value" id="stat-sources">—</strong>
    <span class="stat-note">éditeurs suivis</span>
  </article>
  <article class="stat-card">
    <span class="stat-label">Axes couverts</span>
    <strong class="stat-value" id="stat-axes">—</strong>
    <span class="stat-note">thèmes complémentaires</span>
  </article>
  <article class="stat-card stat-card--updated">
    <span class="stat-label">Dernière collecte</span>
    <strong class="stat-value" id="stat-updated">—</strong>
    <span class="stat-note">actualisation du flux RSS</span>
  </article>
</section>

<section class="section-block" id="axes-de-veille" aria-labelledby="axes-title">
  <div class="section-heading">
    <div>
      <p class="eyebrow">Trois perspectives complémentaires</p>
      <h2 id="axes-title">Les axes de veille</h2>
    </div>
    <p>Des sources identifiées, une fréquence de lecture adaptée à chaque sujet.</p>
  </div>
  <div class="axis-grid">
    <a class="axis-card axis-card--security" href="axe1-securite/">
      <span class="axis-number">01 / SÉCURITÉ</span>
      <span class="axis-icon" aria-hidden="true">⌁</span>
      <h3>Failles & vulnérabilités</h3>
      <p>Alertes CERT-FR, vulnérabilités critiques et correctifs à suivre.</p>
      <span class="axis-footer"><span>Lecture hebdomadaire</span><span aria-hidden="true">↗</span></span>
    </a>
    <a class="axis-card axis-card--systems" href="axe2-ia-admin/">
      <span class="axis-number">02 / INFRASTRUCTURE</span>
      <span class="axis-icon" aria-hidden="true">⌘</span>
      <h3>IA & administration</h3>
      <p>AIOps, automatisation et nouvelles pratiques des équipes systèmes.</p>
      <span class="axis-footer"><span>Lecture mensuelle</span><span aria-hidden="true">↗</span></span>
    </a>
    <a class="axis-card axis-card--ai" href="axe3-ia-cyber/">
      <span class="axis-number">03 / CONVERGENCE</span>
      <span class="axis-icon" aria-hidden="true">✳</span>
      <h3>L'IA face à la cybersécurité</h3>
      <p>Détection augmentée, menaces émergentes et sécurité des modèles.</p>
      <span class="axis-footer"><span>Lecture trimestrielle</span><span aria-hidden="true">↗</span></span>
    </a>
  </div>
</section>

<section class="section-block publications" id="dernieres-publications" aria-labelledby="publications-title" data-veille>
  <div class="section-heading">
    <div>
      <p class="eyebrow">À lire et à surveiller</p>
      <h2 id="publications-title">Dernières publications</h2>
    </div>
    <p id="collection-status" class="collection-status" role="status">Chargement des publications…</p>
  </div>
  <div class="publication-tools">
    <label class="search-field">
      <span class="search-icon" aria-hidden="true">⌕</span>
      <span class="visually-hidden">Rechercher dans les publications</span>
      <input id="veille-search" type="search" placeholder="Rechercher un sujet, une source…" autocomplete="off" aria-keyshortcuts="Control+K Meta+K /">
      <span class="keyboard-hint" aria-hidden="true"><kbd>Ctrl</kbd><kbd>K</kbd></span>
    </label>
    <div class="filter-list" role="group" aria-label="Filtrer par axe">
      <button class="filter-button is-active" type="button" data-axis="all" aria-pressed="true">Tout</button>
      <button class="filter-button" type="button" data-axis="security" aria-pressed="false">Sécurité</button>
      <button class="filter-button" type="button" data-axis="systems" aria-pressed="false">IA & systèmes</button>
      <button class="filter-button" type="button" data-axis="ai-cyber" aria-pressed="false">IA & cyber</button>
    </div>
  </div>
  <p class="result-count" id="result-count" aria-live="polite"></p>
  <div class="article-grid" id="article-grid" aria-live="polite"></div>
</section>

<section class="method-strip" id="methodologie">
  <span class="method-strip__icon" aria-hidden="true">↗</span>
  <div>
    <p class="eyebrow">Méthode & transparence</p>
    <p>Chaque publication renvoie à sa source. La collecte est automatisée ; la sélection et la mise en perspective restent perfectibles.</p>
  </div>
  <a href="a-propos/">Découvrir la méthode <span aria-hidden="true">→</span></a>
</section>

<noscript>
  <p class="noscript-message">Activez JavaScript pour rechercher et filtrer les publications. Les pages des trois axes restent accessibles depuis la navigation.</p>
</noscript>

<footer class="dashboard-footer">
  <span>VTEN CONTINU <span aria-hidden="true">·</span> Une veille indépendante, des sources identifiées.</span>
  <a href="#haut-de-page">Retour en haut <span aria-hidden="true">↑</span></a>
</footer>
