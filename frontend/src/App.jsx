import { useEffect, useMemo, useRef, useState } from 'react'
import './App.css'

function createEmptyConversation(id) {
  return {
    id,
    title: 'New chat',
    messages: [],
    createdAt: new Date().toISOString(),
  }
}

function App() {
  const [conversations, setConversations] = useState(() => {
    const firstId = crypto.randomUUID()
    return [createEmptyConversation(firstId)]
  })
  const [activeId, setActiveId] = useState(() => conversations[0]?.id ?? null)
  const [input, setInput] = useState('')
  const [attachedFile, setAttachedFile] = useState(null)
  const [isRecording, setIsRecording] = useState(false)
  const recognitionRef = useRef(null)
  const messagesEndRef = useRef(null)

  const activeConversation = useMemo(
    () => conversations.find((c) => c.id === activeId) ?? conversations[0],
    [activeId, conversations],
  )

  const supportsVoice = typeof window !== 'undefined' &&
    ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window)

  useEffect(() => {
    if (!supportsVoice || recognitionRef.current) return

    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SpeechRecognition) return

    const recognition = new SpeechRecognition()
    recognition.lang = 'en-US'
    recognition.continuous = false
    recognition.interimResults = true

    recognition.onresult = (event) => {
      let transcript = ''
      for (let i = 0; i < event.results.length; i += 1) {
        transcript += event.results[i][0].transcript
      }
      setInput(transcript)
    }

    recognition.onend = () => {
      setIsRecording(false)
    }

    recognitionRef.current = recognition
  }, [supportsVoice])

  useEffect(() => {
    if (!messagesEndRef.current) return
    messagesEndRef.current.scrollIntoView({ behavior: 'smooth' })
  }, [activeConversation?.messages.length])

  const handleNewChat = () => {
    const id = crypto.randomUUID()
    const next = createEmptyConversation(id)
    setConversations((prev) => [next, ...prev])
    setActiveId(id)
    setInput('')
    setAttachedFile(null)
  }

  const updateConversation = (id, updater) => {
    setConversations((prev) =>
      prev.map((c) => (c.id === id ? updater(c) : c)),
    )
  }

  const handleSubmit = (event) => {
    event.preventDefault()
    const trimmed = input.trim()
    if (!trimmed && !attachedFile) return
    if (!activeConversation) return

    const userMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content: trimmed || (attachedFile ? attachedFile.name : ''),
      fileName: attachedFile?.name ?? null,
      createdAt: new Date().toISOString(),
    }

    const mockReply = {
      id: crypto.randomUUID(),
      role: 'assistant',
      content:
        'This is a placeholder response. Wire this UI to your backend when ready.',
      createdAt: new Date().toISOString(),
    }

    updateConversation(activeConversation.id, (c) => {
      const nextMessages = [...c.messages, userMessage, mockReply]
      const firstUser = nextMessages.find((m) => m.role === 'user')
      const title = firstUser?.content?.slice(0, 40) || 'New chat'
      return {
        ...c,
        messages: nextMessages,
        title,
      }
    })

    setInput('')
    setAttachedFile(null)
  }

  const handleFileChange = (event) => {
    const file = event.target.files?.[0]
    if (!file) {
      setAttachedFile(null)
      return
    }
    setAttachedFile(file)
  }

  const toggleRecording = () => {
    if (!supportsVoice || !recognitionRef.current) return
    const recognition = recognitionRef.current

    if (isRecording) {
      recognition.stop()
      setIsRecording(false)
    } else {
      setInput('')
      recognition.start()
      setIsRecording(true)
    }
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="sidebar-header">
          <button className="new-chat-button" type="button" onClick={handleNewChat}>
            <span className="new-chat-icon">＋</span>
            <span>New chat</span>
          </button>
        </div>
        <div className="sidebar-section-label">History</div>
        <nav className="sidebar-list">
          {conversations.map((conversation) => (
            <button
              key={conversation.id}
              type="button"
              className={
                conversation.id === activeConversation?.id
                  ? 'sidebar-item sidebar-item-active'
                  : 'sidebar-item'
              }
              onClick={() => {
                setActiveId(conversation.id)
                setInput('')
                setAttachedFile(null)
              }}
            >
              <span className="sidebar-item-title">
                {conversation.title || 'New chat'}
              </span>
            </button>
          ))}
        </nav>
      </aside>

      <main className="chat-main">
        <header className="chat-header">
          <div className="chat-header-title">
            <span className="chat-brand-dot" />
            <span className="chat-brand-name">Find Assist</span>
          </div>
          <div className="chat-header-subtitle">
            Ask anything about your project. Voice, files, and history are all in one place.
          </div>
        </header>

        <section className="chat-messages">
          {activeConversation?.messages.length ? (
            activeConversation.messages.map((message) => (
              <div
                key={message.id}
                className={
                  message.role === 'user'
                    ? 'message message-user'
                    : 'message message-assistant'
                }
              >
                <div className="message-avatar">
                  {message.role === 'user' ? 'You' : 'AI'}
                </div>
                <div className="message-body">
                  <div className="message-text">{message.content}</div>
                  {message.fileName ? (
                    <div className="message-file-pill">
                      <span className="message-file-icon">📎</span>
                      <span className="message-file-name">{message.fileName}</span>
                    </div>
                  ) : null}
                </div>
              </div>
            ))
          ) : (
            <div className="chat-empty-state">
              <div className="chat-empty-pill">Inspired by gemini.google.com</div>
              <h1 className="chat-empty-title">
                Hello there,
                <br />
                what can I help you find?
              </h1>
              <p className="chat-empty-subtitle">
                Start with a question, attach a file, or hold the mic to speak.
              </p>
            </div>
          )}
          <div ref={messagesEndRef} />
        </section>

        <form className="chat-input-container" onSubmit={handleSubmit}>
          {attachedFile ? (
            <div className="attached-file-pill">
              <span className="attached-file-icon">📎</span>
              <span className="attached-file-name">{attachedFile.name}</span>
              <button
                type="button"
                className="attached-file-remove"
                onClick={() => setAttachedFile(null)}
              >
                ✕
              </button>
            </div>
          ) : null}

          <div className="chat-input-row">
            <label className="icon-button" htmlFor="file-upload">
              <span className="icon">📎</span>
              <input
                id="file-upload"
                type="file"
                className="file-input-hidden"
                onChange={handleFileChange}
              />
            </label>

            <div className="chat-input-wrapper">
              <input
                className="chat-input"
                placeholder="Ask a question about your code, data, or files..."
                value={input}
                onChange={(event) => setInput(event.target.value)}
              />
            </div>

            <button
              type="button"
              className={`icon-button ${isRecording ? 'icon-button-active' : ''}`}
              onClick={toggleRecording}
              disabled={!supportsVoice}
              title={
                supportsVoice
                  ? isRecording
                    ? 'Stop voice input'
                    : 'Start voice input'
                  : 'Voice input is not available in this browser'
              }
            >
              <span className="icon">
                {isRecording ? '■' : '🎤'}
              </span>
            </button>

            <button
              type="submit"
              className="send-button"
              disabled={!input.trim() && !attachedFile}
            >
              Send
            </button>
          </div>
        </form>

        <div className="chat-footer-hint">
          <span>Built with Vite + React. Connect this UI to your API when ready.</span>
        </div>
      </main>
    </div>
  )
}

export default App
