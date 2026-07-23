// handle form submission
document.getElementById('query-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const queryInput = document.getElementById('query-input');
    const query = queryInput.value.trim();
    if (!query) return;

    // reset ui states
    const traceContainer = document.getElementById('trace-container');
    const codeOutput = document.getElementById('code-output');
    traceContainer.innerHTML = '';
    codeOutput.textContent = 'processing...';
    queryInput.value = '';

    try {
        // initiate streaming post request
        const response = await fetch('/api/v1/query/stream', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        // read the stream chunks sequentially
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });
            
            // parse server-sent events format
            const lines = chunk.split('\n');
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const dataStr = line.replace('data: ', '').trim();
                    if (!dataStr) continue;

                    try {
                        const eventData = JSON.parse(dataStr);
                        updateUI(eventData, traceContainer, codeOutput);
                    } catch (err) {
                        console.error('failed to parse stream chunk:', err);
                    }
                }
            }
        }
    } catch (error) {
        console.error('streaming error:', error);
        codeOutput.textContent = 'Error connecting to Syntex backend.';
    }
});

function updateUI(eventData, traceContainer, codeOutput) {
    // append reasoning trace to sidebar
    const traceEl = document.createElement('div');
    traceEl.className = 'bg-gray-700 p-2 rounded border-l-4 border-blue-500 shadow-sm';
    traceEl.innerHTML = `<span class="font-bold text-blue-400">[${eventData.agent}]</span> processing step...`;
    traceContainer.appendChild(traceEl);
    
    // auto-scroll sidebar
    traceContainer.scrollTop = traceContainer.scrollHeight;

    // update main code window if coder agent emits data
    if (eventData.agent === 'coder' && eventData.data) {
        codeOutput.textContent = eventData.data;
    }
}
