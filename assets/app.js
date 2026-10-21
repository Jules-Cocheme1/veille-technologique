(() => {
  const root = document.querySelector("[data-veille]");
  if (!root) return;

  const grid = document.querySelector("#article-grid");
  const search = document.querySelector("#veille-search");
  const resultCount = document.querySelector("#result-count");
  const status = document.querySelector("#collection-status");
  const stats = {
    articles: document.querySelector("#stat-articles"),
    sources: document.querySelector("#stat-sources"),
    axes: document.querySelector("#stat-axes"),
    updated: document.querySelector("#stat-updated")
  };
  const filterButtons = [...document.querySelectorAll("[data-axis]")];
  const axisNames = {
    security: "Sécurité",
    systems: "IA & systèmes",
    "ai-cyber": "IA & cyber"
  };
  const dateFormatter = new Intl.DateTimeFormat("fr-FR", {
    dateStyle: "medium"
  });
  const dateTimeFormatter = new Intl.DateTimeFormat("fr-FR", {
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

  function formatDate(value) {
    if (!value) return "Date non précisée";
    const date = new Date(value);
    return Number.isNaN(date.getTime()) ? "Date non précisée" : dateFormatter.format(date);
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
    summary.textContent = article.summary || "Ouvrir la source pour consulter la publication.";

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
          article.summary,
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
      const sources = new Set(articles.map((article) => article.source).filter(Boolean));
      const representedAxes = new Set(articles.map((article) => article.axis).filter((axis) => axisNames[axis]));
      const updatedAt = data.updatedAt ? new Date(data.updatedAt) : null;

      stats.articles.textContent = String(articles.length);
      stats.sources.textContent = String(sources.size);
      stats.axes.textContent = `${representedAxes.size} / ${Object.keys(axisNames).length}`;
      stats.updated.textContent = updatedAt && !Number.isNaN(updatedAt.getTime())
        ? dateTimeFormatter.format(updatedAt)
        : "Non disponible";
      status.textContent = updatedAt && !Number.isNaN(updatedAt.getTime())
        ? `Collecte du ${dateTimeFormatter.format(updatedAt)} · flux RSS`
        : "Date de collecte indisponible · flux RSS";
      render();
    })
    .catch((error) => {
      status.textContent = "Les publications n'ont pas pu être chargées.";
      const message = document.createElement("p");
      message.className = "empty-state empty-state--error";
      message.setAttribute("role", "alert");
      message.textContent = error.message;
      grid.replaceChildren(message);
      resultCount.textContent = "Erreur de chargement";
      console.error(error);
    });
})();
