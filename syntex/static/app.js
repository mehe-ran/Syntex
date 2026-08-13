// generate a persistent thread id for the session memory
const sessionId = crypto.randomUUID();

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
            body: JSON.stringify({ query: query, thread_id: sessionId })
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

    // parse markdown and update main code window
    if (eventData.agent === 'coder' && eventData.data) {
        // override container innerhtml instead of textcontent for markdown rendering
        const container = document.getElementById('code-container');
        container.innerHTML = marked.parse(eventData.data);
        
        // style the injected pre/code blocks dynamically
        const codeBlocks = container.querySelectorAll('pre');
        codeBlocks.forEach(block => {
            block.className = 'bg-gray-800 p-4 rounded-lg text-gray-300 shadow-inner overflow-x-auto';
        });
    }
}
