const loader = document.getElementById('loader');

function showLoader() {
    loader.style.display = 'flex';
}

function hideLoader() {
    loader.style.display = 'none';
}

// Interceptar TODOS los formularios
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', () => {
            showLoader();
        });
    });
});

// Interceptar fetch API globalmente
const originalFetch = window.fetch;
window.fetch = async (...args) => {
    try {
        showLoader();
        const response = await originalFetch(...args);
        // modal error.
        if (!response.ok) {
            const errorText = await response.text();
            showErrorModal(`Error ${response.status}: ${errorText || response.statusText}`);
        }
        return response;
    } catch (err) {
        // modal error.
        showErrorModal("No se pudo conectar con el servidor.");
        throw err;
    } finally {
        hideLoader();
    }
};

// Interceptar XMLHttpRequest (AJAX clásico)
(function() {
    const oldOpen = XMLHttpRequest.prototype.open;
    XMLHttpRequest.prototype.open = function(method, url, async, user, pass) {
        this.addEventListener('loadstart', () => showLoader());
        this.addEventListener('loadend', () => hideLoader());
        this.addEventListener('error', () => showErrorModal("Error en la solicitud."));
        this.addEventListener('abort', () => showErrorModal("Solicitud cancelada."));
        this.addEventListener('load', function () {
            if (this.status >= 400) {
                showErrorModal(`Error ${this.status}: ${this.statusText}`);
            }
        });
        oldOpen.call(this, method, url, async, user, pass);
    };
})();

// modal errors
function showErrorModal(message = "Ha ocurrido un error.") {
    document.getElementById("modal-overlay").style.display = "flex";
    document.getElementById("modal-message").innerText = message;
}

function closeErrorModal() {
    document.getElementById("modal-overlay").style.display = "none";
}