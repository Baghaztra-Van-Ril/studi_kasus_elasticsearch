function toggleModal(show) {
  document.getElementById("modal").classList.toggle("hidden", !show);
  if (show) {
    document.getElementById("term").value = "";
    document.getElementById("definition").value = "";
  }
}

function loadAll() {
  fetch("/glossary")
    .then((res) => res.json())
    .then((data) => {
      const list = document.getElementById("data-list");
      list.innerHTML = "";
      if (data.length === 0) {
        list.innerHTML = `
          <li class="p-4 bg-gray-100 rounded-lg text-center shadow-sm">
        <p class="text-gray-600">Tidak ada data ditemukan.</p>
          </li>
        `;
      } else {
        data.forEach((item) => {
          list.innerHTML += `
        <li class="p-4 bg-gray-100 rounded-lg flex justify-between items-start shadow-sm">
          <div>
            <p class="font-semibold text-gray-800">${item.term}</p>
            <p class="text-gray-600 text-sm">${item.definition}</p>
          </div>
          <button onclick="deleteGlossary(${item.id})" class="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded-md text-sm">Hapus</button>
        </li>
          `;
        });
      }
    });
}

async function createGlossary() {
  const term = document.getElementById("term").value;
  const definition = document.getElementById("definition").value;

  const res = await fetch("/glossary", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ term, definition }),
  });

  const data = await res.json();
  toggleModal(false);
  loadAll();
}

function searchData() {
  const keyword = document.getElementById("search-input").value;
  if (!keyword) {
    loadAll();
    return;
  }
  fetch(`/search?q=${keyword}`)
    .then((res) => res.json())
    .then((data) => {
      const list = document.getElementById("data-list");
      list.innerHTML = "";
      if (data.results.length === 0) {
        list.innerHTML = `
          <li class="p-4 bg-gray-100 rounded-lg text-center shadow-sm">
        <p class="text-gray-600">Tidak ada data ditemukan.</p>
          </li>
        `;
      } else {
        data.results.forEach((item) => {
        list.innerHTML += `
            <li class="p-4 bg-gray-100 rounded-lg flex justify-between items-start shadow-sm">
              <div>
                <p class="font-semibold text-gray-800">${item.term}</p>
                <p class="text-gray-600 text-sm">${item.definition}</p>
              </div>
              <button onclick="deleteGlossary(${item.id})" class="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded-md text-sm">Hapus</button>
            </li>
          `;
        });
      }
    });
}

function resetSearch() {
  document.getElementById("search-input").value = "";
  loadAll();
}

async function deleteGlossary(id) {
  const res = await fetch(`/glossary/${id}`, { method: "DELETE" });
  const data = await res.json();
  loadAll();
}

document.getElementById("search-input").addEventListener("input", function() {
  const keyword = this.value;

  if (keyword.length > 2) { // Mulai cari setelah lebih dari 2 karakter
    fetch(`/autocomplete?q=${encodeURIComponent(keyword)}`)
      .then((res) => res.json())
      .then((data) => {
        const suggestionBox = document.getElementById("suggestion-box");
        suggestionBox.innerHTML = ""; // Kosongkan saran yang lama

        if (data.suggestions.length === 0) {
          // suggestionBox.innerHTML = "<p class='text-gray-600 p-2'>Tidak ada saran ditemukan.</p>";
        } else {
          data.suggestions.forEach(suggestion => {
            suggestionBox.innerHTML += `
              <div class="p-2 cursor-pointer hover:bg-gray-200" onclick="selectSuggestion('${suggestion}')">
                ${suggestion}
              </div>
            `;
          });
        }
      });
  }
});

function selectSuggestion(term) {
  document.getElementById("search-input").value = term;
  document.getElementById("suggestion-box").innerHTML = "";
  searchData();
}


loadAll();
