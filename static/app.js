// Tab Switching
function switchTab(tabName) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    event.currentTarget.classList.add('active');
    document.getElementById(`${tabName}-tab`).classList.add('active');

    if (tabName === 'files' && currentPath === '') {
        loadFiles('f:/bn');
    }
}

// Auto-resize textarea
const promptInput = document.getElementById('prompt-input');
promptInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

promptInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Chat Functionality
const messagesContainer = document.getElementById('chat-messages');
let waitingForResponse = false;
let pollingInterval = null;

function appendMessage(text, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'msg-content';
    contentDiv.textContent = text;
    
    msgDiv.appendChild(contentDiv);
    messagesContainer.appendChild(msgDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

async function sendMessage() {
    if (waitingForResponse) return;
    
    const text = promptInput.value.trim();
    if (!text) return;
    
    promptInput.value = '';
    promptInput.style.height = 'auto';
    
    appendMessage(text, 'user');
    waitingForResponse = true;
    
    // Disable input while waiting
    document.getElementById('send-btn').style.opacity = '0.5';
    promptInput.placeholder = "Waiting for AI...";
    promptInput.disabled = true;

    try {
        await fetch('/api/chat/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        
        // Start polling for response
        pollForResponse();
    } catch (e) {
        appendMessage("Error sending message to server.", 'system');
        resetInput();
    }
}

function pollForResponse() {
    if (pollingInterval) clearInterval(pollingInterval);
    
    pollingInterval = setInterval(async () => {
        try {
            const res = await fetch('/api/chat/receive');
            const data = await res.json();
            
            if (data.status === 'success' && data.message) {
                clearInterval(pollingInterval);
                appendMessage(data.message, 'ai');
                resetInput();
            }
        } catch (e) {
            console.error("Polling error", e);
        }
    }, 2000); // check every 2 seconds
}

function resetInput() {
    waitingForResponse = false;
    document.getElementById('send-btn').style.opacity = '1';
    promptInput.placeholder = "Message AI assistant...";
    promptInput.disabled = false;
    promptInput.focus();
}

// File Explorer Functionality
let currentPath = '';

async function loadFiles(path) {
    try {
        const res = await fetch(`/api/fs/list?path=${encodeURIComponent(path)}`);
        const data = await res.json();
        
        if (res.ok) {
            currentPath = path;
            document.getElementById('current-path').textContent = path;
            renderFiles(data.items);
        } else {
            alert(data.error);
        }
    } catch (e) {
        alert("Failed to load directory.");
    }
}

function renderFiles(items) {
    const list = document.getElementById('file-list');
    list.innerHTML = '';
    
    items.forEach(item => {
        const div = document.createElement('div');
        div.className = 'file-item';
        
        const icon = document.createElement('i');
        icon.className = item.is_dir ? 'fa-solid fa-folder dir-icon file-icon' : 'fa-solid fa-file file-icon-text file-icon';
        
        const name = document.createElement('div');
        name.className = 'file-name';
        name.textContent = item.name;
        
        div.appendChild(icon);
        div.appendChild(name);
        
        div.onclick = () => {
            if (item.is_dir) {
                loadFiles(item.path);
            } else {
                openFile(item.path, item.name);
            }
        };
        
        list.appendChild(div);
    });
}

function goUp() {
    if (!currentPath) return;
    const parts = currentPath.split('/');
    if (parts.length > 1) {
        parts.pop();
        let newPath = parts.join('/');
        if (newPath.endsWith(':')) newPath += '/';
        loadFiles(newPath);
    }
}

function refreshFiles() {
    if (currentPath) loadFiles(currentPath);
}

// Editor functionality
const modal = document.getElementById('editor-modal');
let currentEditingPath = '';

async function openFile(path, name) {
    try {
        const res = await fetch(`/api/fs/read?path=${encodeURIComponent(path)}`);
        const data = await res.json();
        
        if (res.ok) {
            currentEditingPath = path;
            document.getElementById('editor-filename').textContent = name;
            document.getElementById('editor-textarea').value = data.content;
            modal.classList.add('open');
        } else {
            alert(data.error || "Cannot read this file.");
        }
    } catch (e) {
        alert("Error opening file.");
    }
}

async function saveFile() {
    if (!currentEditingPath) return;
    const content = document.getElementById('editor-textarea').value;
    try {
        const res = await fetch('/api/fs/write', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ path: currentEditingPath, content: content })
        });
        const data = await res.json();
        if (res.ok) {
            // Provide simple visual feedback
            const btn = document.querySelector('.save-btn');
            const oldColor = btn.style.color;
            btn.style.color = '#fff';
            setTimeout(() => btn.style.color = oldColor, 1000);
        } else {
            alert(data.error || 'Cannot save this file.');
        }
    } catch (e) {
        alert('Error saving file.');
    }
}

function closeEditor() {
    modal.classList.remove('open');
}

// Terminal Functionality
const termInput = document.getElementById('terminal-input');
const termOutput = document.getElementById('terminal-output');

termInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        sendTerminalCommand();
    }
});

async function sendTerminalCommand() {
    const cmd = termInput.value.trim();
    if (!cmd) return;
    
    termInput.value = '';
    
    const cmdDiv = document.createElement('div');
    cmdDiv.style.color = 'white';
    cmdDiv.textContent = `$ ${cmd}`;
    termOutput.appendChild(cmdDiv);
    
    try {
        const res = await fetch('/api/terminal/run', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command: cmd, cwd: currentPath || 'f:/bn' })
        });
        const data = await res.json();
        
        if (data.stdout) {
            const outDiv = document.createElement('div');
            outDiv.textContent = data.stdout;
            termOutput.appendChild(outDiv);
        }
        if (data.stderr) {
            const errDiv = document.createElement('div');
            errDiv.style.color = '#ef5350';
            errDiv.textContent = data.stderr;
            termOutput.appendChild(errDiv);
        }
        if (data.error) {
            const errDiv = document.createElement('div');
            errDiv.style.color = '#ef5350';
            errDiv.textContent = data.error;
            termOutput.appendChild(errDiv);
        }
        termOutput.scrollTop = termOutput.scrollHeight;
    } catch (e) {
        const errDiv = document.createElement('div');
        errDiv.style.color = '#ef5350';
        errDiv.textContent = "Error executing command.";
        termOutput.appendChild(errDiv);
    }
}
