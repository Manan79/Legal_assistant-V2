/**
 * LexAI Assistant V2 - Frontend Application Logic
 */

let chatHistory = [];
let API_URL = localStorage.getItem('lexai_api_url') || 'https://legal-ai-backend-5ze6.onrender.com/legal_assistant';
let HEALTH_URL = localStorage.getItem('lexai_health_url') || 'https://legal-ai-backend-5ze6.onrender.com/health';

// Generate a unique thread ID for each conversation session
let currentThreadId = (typeof crypto !== 'undefined' && crypto.randomUUID) ? crypto.randomUUID() : 'thread_' + Math.random().toString(36).substring(2, 15);

document.addEventListener('DOMContentLoaded', () => {
    const apiUrlInput = document.getElementById('apiUrlInput');
    const apiHealthInput = document.getElementById('apiHealthInput');
    const endpointDisplay = document.getElementById('endpointDisplay');

    if (apiUrlInput) apiUrlInput.value = API_URL;
    if (apiHealthInput) apiHealthInput.value = HEALTH_URL;
    if (endpointDisplay) endpointDisplay.textContent = `API: ${API_URL}`;

    // Initialize Theme
    if (localStorage.getItem('theme') === 'dark') {
        document.documentElement.classList.add('dark');
        const icon = document.getElementById('themeIcon');
        if (icon) icon.className = 'fa-solid fa-moon';
    } else {
        document.documentElement.classList.remove('dark');
        const icon = document.getElementById('themeIcon');
        if (icon) icon.className = 'fa-solid fa-sun';
    }

    // Check Health
    checkApiHealth();
});

async function checkApiHealth() {
    const statusText = document.getElementById('apiStatusText');
    if (!statusText) return;

    try {
        const res = await fetch(HEALTH_URL);
        if (res.ok) {
            statusText.textContent = "FastAPI Connected";
            statusText.className = "truncate font-medium text-emerald-500";
        } else {
            statusText.textContent = "API Degraded";
            statusText.className = "truncate font-medium text-amber-500";
        }
    } catch (e) {
        statusText.textContent = "Backend Offline";
        statusText.className = "truncate font-medium text-rose-500";
    }
}

function toggleDarkMode() {
    const html = document.documentElement;
    const icon = document.getElementById('themeIcon');
    if (html.classList.contains('dark')) {
        html.classList.remove('dark');
        if (icon) icon.className = 'fa-solid fa-sun';
        localStorage.setItem('theme', 'light');
    } else {
        html.classList.add('dark');
        if (icon) icon.className = 'fa-solid fa-moon';
        localStorage.setItem('theme', 'dark');
    }
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const backdrop = document.getElementById('sidebarBackdrop');
    if (sidebar) sidebar.classList.toggle('-translate-x-full');
    if (backdrop) backdrop.classList.toggle('hidden');
}

function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 160) + 'px';
}

function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        const form = document.getElementById('chatForm');
        if (form) form.requestSubmit();
    }
}

function usePreset(btn) {
    const prompt = btn.getAttribute('data-prompt');
    const input = document.getElementById('queryInput');
    if (input) {
        input.value = prompt;
        autoResize(input);
        input.focus();
    }
}

function startNewChat() {
    chatHistory = [];
    currentThreadId = (typeof crypto !== 'undefined' && crypto.randomUUID) ? crypto.randomUUID() : 'thread_' + Math.random().toString(36).substring(2, 15);
    console.log("New conversation thread:", currentThreadId);
    const container = document.getElementById('chatContainer');
    if (container) {
        container.innerHTML = `
            <div id="welcomeBanner" class="text-center py-16 px-4 max-w-2xl mx-auto my-auto">
                <div class="w-20 h-20 bg-gradient-to-tr from-blue-600 via-indigo-600 to-purple-600 text-white rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-xl shadow-blue-500/10 text-3xl">
                    <i class="fa-solid fa-scale-balanced"></i>
                </div>
                <h2 class="text-2xl sm:text-3xl font-extrabold tracking-tight mb-3">Legal AI Assistant V2</h2>
                <p class="text-sm sm:text-base text-gray-500 dark:text-gray-400 mb-8 leading-relaxed">
                    Advanced constitutional & statutory analysis powered by LangGraph ReAct agents, MMR vector retrieval, and NeMo guardrails.
                </p>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs font-medium">
                    <div class="bg-white dark:bg-legal-900 border border-gray-200 dark:border-gray-800 p-3.5 rounded-2xl shadow-sm flex items-center gap-3">
                        <div class="w-8 h-8 rounded-xl bg-emerald-500/10 text-emerald-500 flex items-center justify-center shrink-0">
                            <i class="fa-solid fa-database"></i>
                        </div>
                        <div class="text-left truncate">
                            <div class="font-bold text-gray-900 dark:text-white">MMR Search</div>
                            <div class="text-gray-400">Contextual retrieval</div>
                        </div>
                    </div>
                    <div class="bg-white dark:bg-legal-900 border border-gray-200 dark:border-gray-800 p-3.5 rounded-2xl shadow-sm flex items-center gap-3">
                        <div class="w-8 h-8 rounded-xl bg-blue-500/10 text-blue-500 flex items-center justify-center shrink-0">
                            <i class="fa-solid fa-shield-halved"></i>
                        </div>
                        <div class="text-left truncate">
                            <div class="font-bold text-gray-900 dark:text-white">Guardrails</div>
                            <div class="text-gray-400">Safe legal reasoning</div>
                        </div>
                    </div>
                    <div class="bg-white dark:bg-legal-900 border border-gray-200 dark:border-gray-800 p-3.5 rounded-2xl shadow-sm flex items-center gap-3">
                        <div class="w-8 h-8 rounded-xl bg-indigo-500/10 text-indigo-500 flex items-center justify-center shrink-0">
                            <i class="fa-solid fa-brain"></i>
                        </div>
                        <div class="text-left truncate">
                            <div class="font-bold text-gray-900 dark:text-white">ReAct Agent</div>
                            <div class="text-gray-400">Multi-step analysis</div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    const historyList = document.getElementById('historyList');
    if (historyList) {
        historyList.innerHTML = `<div class="text-xs text-gray-400 italic px-2 py-3">No recent inquiry sessions yet.</div>`;
    }
}

function clearChat() {
    startNewChat();
}

function openSettingsModal() {
    const modal = document.getElementById('settingsModal');
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
}

function closeSettingsModal() {
    const modal = document.getElementById('settingsModal');
    if (modal) {
        modal.classList.remove('flex');
        modal.classList.add('hidden');
    }
}

function saveSettings() {
    const apiUrlInput = document.getElementById('apiUrlInput');
    const apiHealthInput = document.getElementById('apiHealthInput');
    const endpointDisplay = document.getElementById('endpointDisplay');

    if (apiUrlInput) API_URL = apiUrlInput.value;
    if (apiHealthInput) HEALTH_URL = apiHealthInput.value;

    localStorage.setItem('lexai_api_url', API_URL);
    localStorage.setItem('lexai_health_url', HEALTH_URL);

    if (endpointDisplay) endpointDisplay.textContent = `API: ${API_URL}`;
    closeSettingsModal();
    checkApiHealth();
}

async function handleSendMessage(event) {
    event.preventDefault();
    const input = document.getElementById('queryInput');
    if (!input) return;

    const query = input.value.trim();
    if (!query) return;

    const banner = document.getElementById('welcomeBanner');
    if (banner) banner.remove();

    input.value = '';
    input.style.height = 'auto';

    appendMessage(query, 'user');

    const typing = document.getElementById('typingIndicator');
    if (typing) typing.classList.remove('hidden');

    const container = document.getElementById('chatContainer');
    if (container) container.scrollTop = container.scrollHeight;

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: query, thread_id: currentThreadId })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        if (typing) typing.classList.add('hidden');

        const answer = data.response || data.answer || "No response received.";
        const context = data["retrived context"] || data.context || [];

        appendAssistantMessage(answer, context);
        updateHistory(query);

    } catch (error) {
        if (typing) typing.classList.add('hidden');
        if (error.message.includes('HTTP error') || error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            appendAssistantMessage(`⚠️ **Connection Error**: Failed to reach FastAPI backend at \`${API_URL}\`.\n\nPlease ensure your backend is running (\`python Legal_graph/Backend/main.py\`).\n\nError details: ${error.message}`, []);
        } else {
            appendAssistantMessage(`⚠️ **Application Error**: ${error.message}`, []);
        }
    }
}

function renderMarkdown(content) {
    try {
        let str = "";
        if (typeof content === "string") {
            str = content;
        } else if (typeof content === "number" || typeof content === "boolean") {
            str = String(content);
        } else if (Array.isArray(content)) {
            str = content.map(item => {
                if (typeof item === "string") return item;
                if (item && typeof item === "object") return item.text || item.content || JSON.stringify(item, null, 2);
                return String(item);
            }).join("\n");
        } else if (content && typeof content === "object") {
            str = content.answer || content.response || content.text || content.content || JSON.stringify(content, null, 2);
        } else {
            str = String(content || "");
        }
        return marked.parse(str);
    } catch (err) {
        console.error("Markdown rendering error:", err, content);
        return `<p>${escapeHtml(typeof content === 'string' ? content : JSON.stringify(content))}</p>`;
    }
}

function appendMessage(text, sender) {
    const container = document.getElementById('chatContainer');
    if (!container) return;

    const div = document.createElement('div');
    div.className = `flex ${sender === 'user' ? 'justify-end' : 'justify-start'} mb-6`;

    if (sender === 'user') {
        div.innerHTML = `
            <div class="flex items-start space-x-3 max-w-2xl flex-row-reverse space-x-reverse">
                <div class="w-9 h-9 rounded-2xl bg-gradient-to-tr from-gray-700 to-gray-900 text-white flex items-center justify-center text-xs shadow-md shrink-0">
                    <i class="fa-solid fa-user"></i>
                </div>
                <div class="bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-3xl rounded-tr-sm px-5 py-3.5 text-sm shadow-md leading-relaxed">
                    <p class="whitespace-pre-wrap">${escapeHtml(text)}</p>
                </div>
            </div>
        `;
    }
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

function appendAssistantMessage(answerMarkdown, contextList) {
    const container = document.getElementById('chatContainer');
    if (!container) return;

    const div = document.createElement('div');
    div.className = 'flex justify-start mb-6 w-full';

    const htmlContent = renderMarkdown(answerMarkdown);
    const contextId = 'ctx_' + Math.random().toString(36).substr(2, 9);

    let contextHtml = '';
    const safeContextList = Array.isArray(contextList) ? contextList : [];
    if (safeContextList.length > 0) {
        const sourcesCount = safeContextList.length;
        let contextItemsHtml = '';
        safeContextList.forEach((ctx, idx) => {
            const ctxText = typeof ctx === 'string' ? ctx : (ctx.page_content || JSON.stringify(ctx, null, 2));
            contextItemsHtml += `
                <div class="bg-gray-50 dark:bg-legal-950 border border-gray-200 dark:border-gray-800 rounded-2xl p-4 text-xs font-mono text-gray-700 dark:text-gray-300 overflow-x-auto shadow-inner">
                    <div class="font-semibold text-blue-500 mb-2 flex items-center justify-between">
                        <span class="flex items-center gap-1.5"><i class="fa-solid fa-file-lines"></i> Source Precedent Chunk #${idx + 1}</span>
                        <span class="text-[10px] bg-blue-100 dark:bg-blue-900/50 text-blue-600 dark:text-blue-300 px-2.5 py-0.5 rounded-full">Vector MMR</span>
                    </div>
                    <pre class="whitespace-pre-wrap font-sans text-xs leading-relaxed text-gray-600 dark:text-gray-300">${escapeHtml(ctxText)}</pre>
                </div>
            `;
        });

        contextHtml = `
            <div class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-800">
                <button onclick="toggleContext('${contextId}')" class="flex items-center justify-between w-full text-xs font-semibold text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-950/40 hover:bg-blue-100 dark:hover:bg-blue-900/40 p-3 rounded-2xl transition">
                    <span class="flex items-center gap-2">
                        <i class="fa-solid fa-magnifying-glass-chart"></i> Retrieved Legal Context & Sources (${sourcesCount} chunks)
                    </span>
                    <i id="${contextId}_icon" class="fa-solid fa-chevron-down transition-transform"></i>
                </button>
                <div id="${contextId}" class="hidden mt-3 space-y-3">
                    ${contextItemsHtml}
                </div>
            </div>
        `;
    } else {
        contextHtml = `
            <div class="mt-4 pt-3 border-t border-gray-200 dark:border-gray-800 text-xs text-gray-400 italic flex items-center gap-1.5">
                <i class="fa-solid fa-circle-info"></i> No explicit retrieval context recorded for this turn.
            </div>
        `;
    }

    div.innerHTML = `
        <div class="flex items-start space-x-3 w-full max-w-4xl">
            <div class="w-9 h-9 rounded-2xl bg-gradient-to-tr from-blue-600 to-indigo-600 text-white flex items-center justify-center text-xs shadow-md shrink-0 mt-1">
                <i class="fa-solid fa-scale-balanced"></i>
            </div>
            <div class="flex-1 bg-white dark:bg-legal-900 border border-gray-200 dark:border-gray-800 rounded-3xl rounded-tl-sm p-6 shadow-sm text-sm">
                <div class="markdown-body dark:text-gray-200">${htmlContent}</div>
                ${contextHtml}
                <div class="mt-5 flex items-center justify-between text-xs text-gray-400 pt-3 border-t border-gray-100 dark:border-legal-800">
                    <span class="flex items-center gap-1.5 font-medium text-emerald-500"><i class="fa-solid fa-shield-check"></i> LangGraph ReAct Verified</span>
                    <button onclick="copyResponse(this)" class="hover:text-blue-500 transition flex items-center gap-1.5 bg-gray-50 dark:bg-legal-800 px-3 py-1.5 rounded-xl border border-gray-200 dark:border-gray-700">
                        <i class="fa-regular fa-copy"></i> Copy Answer
                    </button>
                </div>
            </div>
        </div>
    `;

    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

function toggleContext(id) {
    const el = document.getElementById(id);
    const icon = document.getElementById(id + '_icon');
    if (!el || !icon) return;

    if (el.classList.contains('hidden')) {
        el.classList.remove('hidden');
        icon.style.transform = 'rotate(180deg)';
    } else {
        el.classList.add('hidden');
        icon.style.transform = 'rotate(0deg)';
    }
}

function copyResponse(btn) {
    const card = btn.closest('.flex-1');
    if (!card) return;
    const markdownBody = card.querySelector('.markdown-body').innerText;
    navigator.clipboard.writeText(markdownBody).then(() => {
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fa-solid fa-check text-emerald-500"></i> Copied!';
        setTimeout(() => {
            btn.innerHTML = originalText;
        }, 2000);
    });
}

function updateHistory(query) {
    chatHistory.unshift(query);
    const historyList = document.getElementById('historyList');
    if (!historyList) return;

    historyList.innerHTML = '';
    chatHistory.slice(0, 10).forEach(q => {
        const item = document.createElement('button');
        item.className = 'w-full text-left text-xs text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-legal-800 p-2.5 rounded-xl truncate transition flex items-center gap-2.5 font-medium';
        item.innerHTML = `<i class="fa-regular fa-message text-gray-400 shrink-0"></i> <span class="truncate">${escapeHtml(q)}</span>`;
        item.onclick = () => {
            const input = document.getElementById('queryInput');
            if (input) {
                input.value = q;
                autoResize(input);
                input.focus();
            }
        };
        historyList.appendChild(item);
    });
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}
