const $ = (s) => document.querySelector(s);
let plugins = [], cat = "All", term = "", sort = "stars";

const fmt = (n) => (n >= 1000 ? (n / 1000).toFixed(n >= 10000 ? 0 : 1) + "k" : String(n));

fetch("plugins.json")
  .then((r) => r.json())
  .then((j) => {
    plugins = j.plugins;
    $("#updated").textContent = new Date(j.updated).toLocaleDateString("en", { dateStyle: "medium" });
    render();
  })
  .catch(() => ($("#count").textContent = "Could not load plugins.json"));

function chips() {
  const counts = {};
  plugins.forEach((p) => (counts[p.category] = (counts[p.category] || 0) + 1));
  const box = $("#chips");
  box.innerHTML = "";
  [["All", plugins.length], ...Object.entries(counts)].forEach(([c, n]) => {
    const b = document.createElement("button");
    b.className = "chip" + (c === cat ? " on" : "");
    b.textContent = `${c} (${n})`;
    b.onclick = () => { cat = c; render(); };
    box.appendChild(b);
  });
}

function render() {
  chips();
  const t = term.toLowerCase();
  const list = plugins
    .filter((p) => (cat === "All" || p.category === cat) &&
      `${p.name} ${p.desc} ${p.author} ${p.category}`.toLowerCase().includes(t))
    .sort((a, b) => sort === "name"
      ? a.name.localeCompare(b.name)
      : (b.stars ?? -1) - (a.stars ?? -1) || a.name.localeCompare(b.name));
  $("#count").textContent = `${list.length} plugin${list.length === 1 ? "" : "s"}`;
  const grid = $("#grid");
  grid.innerHTML = "";
  for (const p of list) {
    const a = document.createElement("a");
    a.className = "card";
    a.href = p.url;
    a.target = "_blank";
    a.rel = "noopener";
    a.innerHTML = '<div class="top"><span class="nm"></span><span class="st"></span></div><div class="ds"></div><div class="mt"><span class="au"></span><span class="tg"></span></div>';
    a.querySelector(".nm").textContent = p.name;
    const st = a.querySelector(".st");
    if (p.stars == null) st.remove(); else st.textContent = "★ " + fmt(p.stars);
    a.querySelector(".ds").textContent = p.desc;
    a.querySelector(".au").textContent = p.repo ? "@" + p.author : p.author;
    a.querySelector(".tg").textContent = p.category;
    grid.appendChild(a);
  }
}

$("#q").oninput = (e) => { term = e.target.value; render(); };
$("#sort").onchange = (e) => { sort = e.target.value; render(); };
