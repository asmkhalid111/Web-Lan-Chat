// app.js

document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const toggleAuthBtn = document.getElementById('toggle-auth');
    
    // Check if user is already logged in
    const user = localStorage.getItem('user');
    if (user && window.location.pathname === '/') {
        // Redirect to dashboard if logged in
        window.location.href = '/static/dashboard.html';
        return;
    }

    // Only run auth logic if we are on the login page
    if (loginForm && registerForm) {
        let isLoginMode = true;

        // Toggle Auth Mode
        toggleAuthBtn.addEventListener('click', () => {
            isLoginMode = !isLoginMode;
            if (isLoginMode) {
                loginForm.classList.remove('hidden');
                registerForm.classList.add('hidden');
                toggleAuthBtn.textContent = 'Need an account? Register here';
            } else {
                loginForm.classList.add('hidden');
                registerForm.classList.remove('hidden');
                toggleAuthBtn.textContent = 'Already have an account? Login here';
            }
        });

        // Handle Login
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const student_id = document.getElementById('student_id').value;
            const password = document.getElementById('password').value;
            const errorDiv = document.getElementById('login-error');
            const btn = document.getElementById('btn-login');

            btn.disabled = true;
            btn.innerHTML = 'Signing in...';
            errorDiv.classList.add('hidden');

            try {
                const res = await fetch('/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ student_id, password })
                });

                const data = await res.json();

                if (res.ok) {
                    localStorage.setItem('user', JSON.stringify(data.user));
                    window.location.href = '/static/dashboard.html';
                } else {
                    errorDiv.textContent = data.detail || 'Login failed';
                    errorDiv.classList.remove('hidden');
                }
            } catch (err) {
                errorDiv.textContent = 'Network error. Could not connect to server.';
                errorDiv.classList.remove('hidden');
            } finally {
                btn.disabled = false;
                btn.innerHTML = '<span class="relative z-10">Sign In</span><div class="absolute inset-0 h-full w-full bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:animate-shimmer"></div>';
            }
        });

        // Handle Register
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const student_id = document.getElementById('reg_student_id').value;
            const name = document.getElementById('reg_name').value;
            const password = document.getElementById('reg_password').value;
            const errorDiv = document.getElementById('register-error');
            const successDiv = document.getElementById('register-success');
            const btn = document.getElementById('btn-register');

            btn.disabled = true;
            btn.innerHTML = 'Creating...';
            errorDiv.classList.add('hidden');
            successDiv.classList.add('hidden');

            try {
                const res = await fetch('/api/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ student_id, name, password })
                });

                const data = await res.json();

                if (res.ok) {
                    successDiv.textContent = 'Registration successful! You can now login.';
                    successDiv.classList.remove('hidden');
                    // Automatically switch to login mode after 2 seconds
                    setTimeout(() => {
                        toggleAuthBtn.click();
                        document.getElementById('student_id').value = student_id;
                    }, 2000);
                } else {
                    errorDiv.textContent = data.detail || 'Registration failed';
                    errorDiv.classList.remove('hidden');
                }
            } catch (err) {
                errorDiv.textContent = 'Network error. Could not connect to server.';
                errorDiv.classList.remove('hidden');
            } finally {
                btn.disabled = false;
                btn.innerHTML = '<span class="relative z-10">Create Account</span><div class="absolute inset-0 h-full w-full bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:animate-shimmer"></div>';
            }
        });
    }

    // Dashboard Logic
    const chatForm = document.getElementById('chat-form');
    if (chatForm) {
        if (!user) {
            window.location.href = '/static/index.html';
            return;
        }

        const userData = JSON.parse(user);
        document.getElementById('user-name').textContent = userData.name;

        // Logout
        document.getElementById('btn-logout').addEventListener('click', () => {
            localStorage.removeItem('user');
            window.location.href = '/';
        });

        // Notes Logic
        const btnAddNote = document.getElementById('btn-add-note');
        const noteForm = document.getElementById('note-form');
        const notesList = document.getElementById('notes-list');

        btnAddNote.addEventListener('click', () => {
            noteForm.classList.toggle('hidden');
        });

        async function loadNotes() {
            try {
                const res = await fetch(`/api/notes/${userData.student_id}`);
                if (res.ok) {
                    const notes = await res.json();
                    notesList.innerHTML = '';
                    notes.forEach(n => {
                        const div = document.createElement('div');
                        div.className = 'bg-white/5 p-2 rounded text-xs';
                        div.innerHTML = `<div class="font-bold text-gray-200">${n.title}</div><div class="text-gray-400 mt-1">${n.content}</div>`;
                        notesList.appendChild(div);
                    });
                }
            } catch (err) { console.error("Error loading notes"); }
        }

        noteForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const title = document.getElementById('note-title').value;
            const content = document.getElementById('note-content').value;
            try {
                const res = await fetch(`/api/notes/${userData.student_id}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ title, content })
                });
                if (res.ok) {
                    document.getElementById('note-title').value = '';
                    document.getElementById('note-content').value = '';
                    noteForm.classList.add('hidden');
                    loadNotes();
                }
            } catch (err) { console.error("Error creating note"); }
        });

        // Announcements Logic
        const announcementsList = document.getElementById('announcements-list');

        async function loadAnnouncements() {
            try {
                const res = await fetch('/api/announcements');
                if (res.ok) {
                    const anns = await res.json();
                    announcementsList.innerHTML = '';
                    if (anns.length === 0) {
                        announcementsList.innerHTML = '<div class="text-xs text-gray-500 italic">No announcements</div>';
                    }
                    anns.forEach(a => {
                        const div = document.createElement('div');
                        div.className = 'bg-primary/20 p-2 rounded text-xs border border-primary/30';
                        div.innerHTML = `<div class="font-bold text-indigo-300">${a.title}</div><div class="text-gray-300 mt-1">${a.content}</div><div class="text-right text-[10px] text-gray-500 mt-1">- ${a.author}</div>`;
                        announcementsList.appendChild(div);
                    });
                }
            } catch (err) { console.error("Error loading announcements"); }
        }

        // Initial Load
        loadNotes();
        loadAnnouncements();

        // Initialize WebSocket
        // Using window.location.host to automatically connect to the correct IP/port
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/${userData.student_id}`;
        let ws = new WebSocket(wsUrl);

        const chatBox = document.getElementById('chat-box');
        const onlineUsersList = document.getElementById('online-users-list');

        function appendMessage(msg) {
            const isMe = msg.sender_id === userData.student_id;
            const msgDiv = document.createElement('div');
            msgDiv.className = `flex flex-col ${isMe ? 'items-end' : 'items-start'}`;
            
            const bubble = document.createElement('div');
            bubble.className = `max-w-[70%] rounded-2xl px-4 py-2 mt-1 ${isMe ? 'bg-primary text-white rounded-br-none' : 'bg-white/10 text-gray-100 rounded-bl-none'}`;
            bubble.textContent = msg.message;
            
            const senderName = document.createElement('div');
            senderName.className = 'text-xs text-gray-400 px-1';
            senderName.textContent = isMe ? 'You' : msg.sender_name;

            msgDiv.appendChild(senderName);
            msgDiv.appendChild(bubble);
            chatBox.appendChild(msgDiv);
            
            // Auto scroll to bottom
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'status') {
                // Update online users
                onlineUsersList.innerHTML = '';
                data.online_users.forEach(id => {
                    const li = document.createElement('li');
                    li.className = 'px-2 py-1.5 rounded hover:bg-white/5 text-gray-300 text-sm flex items-center cursor-pointer';
                    li.innerHTML = `<span class="w-2 h-2 rounded-full bg-green-500 mr-2"></span> ${id} ${id === userData.student_id ? '(You)' : ''}`;
                    onlineUsersList.appendChild(li);
                });
            } else if (data.type === 'chat') {
                appendMessage(data);
            } else if (data.type === 'history') {
                // Clear welcome message if there is history
                if (data.messages.length > 0) {
                    chatBox.innerHTML = ''; 
                    data.messages.forEach(msg => appendMessage(msg));
                }
            }
        };

        ws.onclose = () => {
            console.log('WebSocket disconnected');
            const div = document.createElement('div');
            div.className = 'text-center text-sm text-red-500 my-4';
            div.textContent = 'Disconnected from server. Please refresh.';
            chatBox.appendChild(div);
        };

        chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            if (message && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({ target: 'global', message: message }));
                input.value = '';
            }
        });
    }
});
