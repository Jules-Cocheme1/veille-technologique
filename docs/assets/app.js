(() => {
  const root = document.querySelector("[data-veille]");
  if (!root) return;

  const grid = root.querySelector("#article-grid");
  const search = root.querySelector("#veille-search");
  const resultCount = root.querySelector("#result-count");
  const status = root.querySelector("#collection-status");
  const liveBadge = document.querySelector(".dashboard-live");
  const filterButtons = [...root.querySelectorAll("[data-axis]")];
  const axisNames = {
    security: "Sécurité",
    systems: "IA & systèmes",
    "ai-cyber": "IA & cyber"
  };
  const dateFormatter = new Intl.DateTimeFormat("fr-FR", {
    dateStyle: "medium"
  });
  const timeFormatter = new Intl.DateTimeFormat("fr-FR", {
    timeStyle: "short"
  });
  const timestampFormatter = new Intl.DateTimeFormat("fr-FR", {
    dateStyle: "medium",
    timeStyle: "short"
  });
  let articles = [];
  let activeAxis = "all";

  function safeArticleUrl(value) {
    try {
      const url = new URL(value);
      return url.protocol === "https:" || url.protocol === "http:" ? url.href : null;
    } catch {
      return null;
    }
  }

  function formatDate(value, formatter = dateFormatter) {
    if (!value) return "Date non précisée";
    const date = new Date(value);
    return Number.isNaN(date.getTime()) ? "Date non précisée" : formatter.format(date);
  }

  function cleanSummary(value) {
    return (value || "")
      .replace(/\s*(?:the post|le post)\s+.+$/i, "")
      .replace(/\s+/g, " ")
      .trim();
  }

  function updateStats(data) {
    const sources = new Set(articles.map((article) => article.source).filter(Boolean));
    const axes = new Set(articles.map((article) => article.axis).filter((axis) => axisNames[axis]));
    const lastUpdated = document.querySelector("#stat-updated");
    document.querySelector("#stat-publications").textContent = String(articles.length).padStart(2, "0");
    document.querySelector("#stat-sources").textContent = String(sources.size).padStart(2, "0");
    document.querySelector("#stat-axes").textContent = String(axes.size).padStart(2, "0");
    lastUpdated.textContent = formatDate(data.updatedAt);

    const timestamp = new Date(data.updatedAt);
    document.querySelector(".stat-card--updated .stat-note").textContent =
      Number.isNaN(timestamp.getTime())
        ? "date de collecte indisponible"
        : `Sources RSS · ${timeFormatter.format(timestamp)}`;
  }

  function setLiveStatus(message, isError = false) {
    const dot = document.createElement("span");
    dot.className = `status-dot${isError ? " status-dot--error" : ""}`;
    dot.setAttribute("aria-hidden", "true");
    liveBadge.replaceChildren(dot, document.createTextNode(` ${message}`));
    liveBadge.setAttribute("aria-label", message);
  }

  function createArticleCard(article) {
    const href = safeArticleUrl(article.url);
    if (!href) return null;

    const card = document.createElement("article");
    card.className = "article-card";

    const meta = document.createElement("div");
    meta.className = "article-card__meta";

    const badge = document.createElement("span");
    badge.className = `article-badge article-badge--${article.axis}`;
    badge.textContent = axisNames[article.axis] || "Veille";
    meta.append(badge);

    const date = document.createElement("time");
    date.textContent = formatDate(article.publishedAt);
    if (article.publishedAt && !Number.isNaN(new Date(article.publishedAt).getTime())) {
      date.dateTime = new Date(article.publishedAt).toISOString();
    }
    meta.append(date);

    const title = document.createElement("h3");
    title.textContent = article.title || "Publication sans titre";

    const summary = document.createElement("p");
    summary.textContent = cleanSummary(article.summary) || "Ouvrir la source pour consulter la publication.";

    const footer = document.createElement("div");
    footer.className = "article-card__footer";

    const source = document.createElement("span");
    source.className = "article-source";
    source.textContent = article.source || "Source";

    const link = document.createElement("a");
    link.href = href;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.setAttribute("aria-label", `Lire « ${article.title || "la publication"} » sur ${article.source || "le site source"}`);
    link.textContent = "Lire la source";
    const arrow = document.createElement("span");
    arrow.setAttribute("aria-hidden", "true");
    arrow.textContent = " ↗";
    link.append(arrow);

    footer.append(source, link);
    card.append(meta, title, summary, footer);
    return card;
  }

  function render() {
    const query = search.value.trim().toLocaleLowerCase("fr");
    const visibleArticles = articles
      .filter((article) => activeAxis === "all" || article.axis === activeAxis)
      .filter((article) => {
        const searchableText = [
          article.title,
          cleanSummary(article.summary),
          article.source,
          axisNames[article.axis]
        ].join(" ").toLocaleLowerCase("fr");
        return searchableText.includes(query);
      })
      .sort((first, second) => {
        const firstDate = Date.parse(first.publishedAt || "") || 0;
        const secondDate = Date.parse(second.publishedAt || "") || 0;
        return secondDate - firstDate;
      });

    grid.replaceChildren();
    resultCount.textContent = `${visibleArticles.length} publication${visibleArticles.length > 1 ? "s" : ""}`;

    if (visibleArticles.length === 0) {
      const empty = document.createElement("p");
      empty.className = "empty-state";
      if (articles.length === 0) {
        empty.textContent = "Aucune publication n'est disponible pour le moment. Les flux seront actualisés lors de la prochaine collecte.";
      } else if (query) {
        empty.textContent = "Aucune publication ne correspond à cette recherche.";
      } else {
        empty.textContent = `Aucune publication disponible pour l'axe ${axisNames[activeAxis] || "sélectionné"}.`;
      }
      grid.append(empty);
      return;
    }

    for (const article of visibleArticles) {
      const card = createArticleCard(article);
      if (card) grid.append(card);
    }
  }

  for (const button of filterButtons) {
    button.addEventListener("click", () => {
      activeAxis = button.dataset.axis;
      for (const item of filterButtons) {
        const isActive = item === button;
        item.classList.toggle("is-active", isActive);
        item.setAttribute("aria-pressed", String(isActive));
      }
      render();
    });
  }

  search.addEventListener("input", render);

  document.addEventListener("keydown", (event) => {
    const isTyping = event.target instanceof HTMLElement &&
      (event.target.isContentEditable || ["INPUT", "TEXTAREA", "SELECT"].includes(event.target.tagName));
    if ((event.key === "/" && !isTyping && !event.metaKey && !event.ctrlKey && !event.altKey) ||
        ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k")) {
      event.preventDefault();
      search.focus();
    }
  });

  fetch(new URL("data/articles.json", document.baseURI), { cache: "no-cache" })
    .then((response) => {
      if (!response.ok) throw new Error(`Chargement des publications impossible (${response.status}).`);
      return response.json();
    })
    .then((data) => {
      if (!data || !Array.isArray(data.articles)) {
        throw new Error("Le fichier des publications ne respecte pas le format attendu.");
      }
      articles = data.articles;
      updateStats(data);
      status.textContent = data.updatedAt
        ? `Collecte : ${formatDate(data.updatedAt, timestampFormatter)} · sources RSS`
        : "Sources RSS · date de collecte indisponible";
      setLiveStatus("Flux RSS actif");
      render();
    })
    .catch((error) => {
      status.textContent = "Les publications n'ont pas pu être chargées.";
      setLiveStatus("Flux RSS indisponible", true);
      const message = document.createElement("p");
      message.className = "empty-state empty-state--error";
      message.setAttribute("role", "alert");
      message.textContent = error.message;
      grid.replaceChildren(message);
      resultCount.textContent = "Erreur de chargement";
      console.error(error);
    });
})();
