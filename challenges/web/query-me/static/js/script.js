document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('query-input');
    const output = document.getElementById('output');
    const runBtn = document.getElementById('run-btn');

    function addLine(text, className = '') {
        const div = document.createElement('div');
        div.className = 'line ' + className;
        div.textContent = text;
        output.appendChild(div);
        output.scrollTop = output.scrollHeight;
    }

    function addResult(data) {
        if (data === null) {
            addLine('No data returned.', 'error');
            return;
        }

        const div = document.createElement('div');
        div.className = 'line result-row';

        // Format JSON nicely
        const pre = document.createElement('pre');
        pre.textContent = JSON.stringify(data, null, 2);
        div.appendChild(pre);

        output.appendChild(div);
        output.scrollTop = output.scrollHeight;
    }

    async function executeQuery() {
        const query = input.value.trim();
        if (!query) return;

        addLine(`sqlite> ${query}`);
        input.value = '';

        try {
            const response = await fetch('/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: query })
            });

            const data = await response.json();

            if (response.ok) {
                if (data.result) {
                    addResult(data.result);
                } else {
                    addLine(data.message || 'No results.', 'error');
                }
            } else {
                addLine(`Error: ${data.error}`, 'error');
            }

        } catch (error) {
            addLine(`Network Error: ${error.message}`, 'error');
        }
    }

    runBtn.addEventListener('click', executeQuery);

    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            executeQuery();
        }
    });

    // Focus input on load
    input.focus();
});
