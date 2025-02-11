const modal = document.getElementById("modal");
const openModal = document.getElementById("openModal");
const closeModal = document.querySelector(".close");
const openCalendar = document.getElementById('deadline');
const categoryInput = document.getElementById('category');
const suggestionsDiv = document.getElementById('suggestionsDropdown');

openModal.addEventListener("click", () => {
    document.getElementById('description').value = '';
    modal.style.display = "flex";
});

closeModal.addEventListener("click", () => {
    modal.style.display = "none";
});

window.addEventListener("click", (event) => {
    if (event.target === modal) {
        modal.style.display = "none";
    }
});

openCalendar.addEventListener('focus', function() {
    this.showPicker();
});

// Atualiza o dropdown com as categorias existentes ao carregar a página
document.addEventListener("DOMContentLoaded", function () {
    fetch('/buscar-categorias')
        .then(response => response.json())
        .then(data => {
            data.categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category.name;
                option.textContent = category.name;
                categoryInput.appendChild(option);
            });
        })
        .catch(error => console.error('Erro ao buscar categorias:', error));
});

// Mostra sugestões conforme o usuário digita
categoryInput.addEventListener('input', function () {
    const query = this.value.trim();
    suggestionsDiv.innerHTML = ''; // Limpa sugestões anteriores

    if (query.length > 0) {
        fetch(`/buscar-categorias?query=${query}`)
            .then(response => response.json())
            .then(data => {
                if (data.categories.length > 0) {
                    suggestionsDiv.style.display = 'block';
                    data.categories.forEach(category => {
                        const li = document.createElement('li');
                        li.classList.add('suggestion-item');
                        li.textContent = category.name;
                        li.addEventListener('click', function () {
                            categoryInput.value = category.name;
                            suggestionsDiv.style.display = 'none';
                        });
                        suggestionsDiv.appendChild(li);
                    });
                } else {
                    suggestionsDiv.style.display = 'none'; // Esconde caso não haja sugestões
                }
            })
            .catch(error => console.error('Erro ao buscar categorias:', error));
    } else {
        suggestionsDiv.style.display = 'none';
    }
});
