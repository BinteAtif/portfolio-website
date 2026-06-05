const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const chatApi = {
  async sendMessage(message, history = []) {
    const formattedHistory = history.map(msg => ({
      role: msg.role === 'bot' ? 'assistant' : msg.role,
      content: msg.content || msg.text || '',
    }));

    const response = await fetch(`${API_BASE_URL}/ai/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, history: formattedHistory }),
    });

    if (!response.ok) {
      const err = await response.json().catch(() => null);
      throw new Error(err?.detail || `API error: ${response.status}`);
    }

    const data = await response.json();
    if (!data.status) throw new Error('Invalid response from server');
    return data;
  },

  async checkHealth() {
    try {
      const res = await fetch(`${API_BASE_URL}/`);
      return res.ok;
    } catch {
      return false;
    }
  },
};