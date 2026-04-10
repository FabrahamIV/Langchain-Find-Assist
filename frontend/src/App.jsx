import { useEffect, useMemo, useRef, useState, useCallback } from 'react'
import './App.css'
import Sidebar from './components/Sidebar.jsx'
import ChatHeader from './components/ChatHeader.jsx'
import MessageList from './components/MessageList.jsx'
import ChatInput from './components/ChatInput.jsx'

const API_BASE = 'http://localhost:8000/api'

function App() {
  const [conversations, setConversations] = useState([])
  const [activeId, setActiveId] = useState(null)
  const [input, setInput] = useState('')
  const [attachedFile, setAttachedFile] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [isRecording, setIsRecording] = useState(false)
  const [isSidebarOpen, setIsSidebarOpen] = useState(true)
  const [userId, setUserId] = useState(null)

  const recognitionRef = useRef(null)
  const messagesEndRef = useRef(null)

  // The active conversation object
  const activeConversation = useMemo(
    () => conversations.find((c) => c.id === activeId) ?? conversations[0] ?? null,
    [activeId, conversations],
  )

  // Feature‑detection for browser voice support
  const supportsVoice = typeof window !== 'undefined' &&
    ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window)

  // ──────────────── Load conversations from DB on mount ────────────────
  const fetchConversations = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/conversations`)
      if (!res.ok) return
      const data = await res.json()
      const mapped = data.map((c) => ({
        id: c.conversation_id,
        title: c.title || 'New Chat',
        messages: [], // messages loaded on select
        createdAt: c.created_at,
        messageCount: c.message_count,
      }))
      setConversations(mapped)
      // If we have conversations but no active one, select the first
      if (mapped.length > 0 && !activeId) {
        setActiveId(mapped[0].id)
      }
    } catch (err) {
      console.error('Failed to fetch conversations:', err)
    }
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    fetchConversations()
  }, [fetchConversations])

  // ──────────────── Load messages when switching conversations ────────────────
  const loadConversationMessages = useCallback(async (convId) => {
    try {
      const res = await fetch(`${API_BASE}/conversations/${convId}`)
      if (!res.ok) return
      const data = await res.json()
      const messages = data.messages.map((m) => ({
        id: m.message_id,
        role: m.role,
        content: m.content,
        fileName: m.file_name || null,
        createdAt: m.created_at,
      }))
      setConversations((prev) =>
        prev.map((c) => (c.id === convId ? { ...c, messages, title: data.title } : c)),
      )
    } catch (err) {
      console.error('Failed to load messages:', err)
    }
  }, [])

  // Load messages when active conversation changes
  useEffect(() => {
    if (activeId) {
      loadConversationMessages(activeId)
    }
  }, [activeId, loadConversationMessages])

  // ──────────────── Speech Recognition setup ────────────────
  useEffect(() => {
    if (!supportsVoice || recognitionRef.current) return
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SpeechRecognition) return

    const recognition = new SpeechRecognition()
    recognition.lang = 'id-ID'
    recognition.continuous = false
    recognition.interimResults = true

    recognition.onresult = (event) => {
      let transcript = ''
      for (let i = 0; i < event.results.length; i += 1) {
        transcript += event.results[i][0].transcript
      }
      setInput(transcript)
    }
    recognition.onend = () => setIsRecording(false)
    recognitionRef.current = recognition
  }, [supportsVoice])

  // Auto‑scroll messages
  useEffect(() => {
    if (!messagesEndRef.current) return
    messagesEndRef.current.scrollIntoView({ behavior: 'smooth' })
  }, [activeConversation?.messages?.length])

  // ──────────────── Handlers ────────────────

  const handleNewChat = async () => {
    // Optimistic: add a local placeholder immediately
    const tempId = crypto.randomUUID()
    const optimistic = {
      id: tempId,
      title: 'New Chat',
      messages: [],
      createdAt: new Date().toISOString(),
    }
    setConversations((prev) => [optimistic, ...prev])
    setActiveId(tempId)
    setInput('')
    setAttachedFile(null)
  }

  const updateConversation = (id, updater) => {
    setConversations((prev) =>
      prev.map((c) => (c.id === id ? updater(c) : c)),
    )
  }

  const handleSubmit = async (event) => {
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

    // Build form data for backend
    const formData = new FormData()
    const backendPrompt = trimmed || (attachedFile ? 'Please summarize the attached document.' : '')
    formData.append('message', backendPrompt)

    if (attachedFile) {
      formData.append('file', attachedFile)
    }

    // Send IDs if we have them (for existing conversations)
    if (userId) formData.append('user_id', userId)

    // Check if activeConversation is a real DB conversation or an optimistic one
    const isNewConversation = !activeConversation.messageCount && activeConversation.messages.length === 0
    if (!isNewConversation) {
      formData.append('conversation_id', activeConversation.id)
    }

    // Optimistic UI: add user message immediately
    updateConversation(activeConversation.id, (c) => {
      const nextMessages = [...c.messages, userMessage]
      const title = c.messages.length === 0
        ? userMessage.content.slice(0, 40)
        : c.title
      return { ...c, messages: nextMessages, title }
    })

    setInput('')
    setAttachedFile(null)

    try {
      setIsLoading(true)
      const response = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()

      // Store user_id for future requests
      if (data.user_id) setUserId(data.user_id)

      // If this was a new conversation, update the local ID to match the DB ID
      if (isNewConversation && data.conversation_id && data.conversation_id !== activeConversation.id) {
        setConversations((prev) =>
          prev.map((c) =>
            c.id === activeConversation.id
              ? { ...c, id: data.conversation_id }
              : c
          ),
        )
        setActiveId(data.conversation_id)
      }

      const aiReply = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: data.reply ?? 'Sorry, I could not generate a response.',
        createdAt: new Date().toISOString(),
      }

      // Use the potentially updated conversation_id
      const targetId = (isNewConversation && data.conversation_id) ? data.conversation_id : activeConversation.id
      updateConversation(targetId, (c) => ({
        ...c,
        messages: [...c.messages, aiReply],
      }))
    } catch (error) {
      console.error('Chat error:', error)
      updateConversation(activeConversation.id, (c) => ({
        ...c,
        messages: [
          ...c.messages,
          {
            id: crypto.randomUUID(),
            role: 'assistant',
            content: 'Sorry, something went wrong. Please try again.',
            createdAt: new Date().toISOString(),
          },
        ],
      }))
    } finally {
      setIsLoading(false)
    }
  }

  const handleDeleteConversation = async (convId) => {
    try {
      await fetch(`${API_BASE}/conversations/${convId}`, { method: 'DELETE' })
      setConversations((prev) => prev.filter((c) => c.id !== convId))
      if (activeId === convId) {
        const remaining = conversations.filter((c) => c.id !== convId)
        setActiveId(remaining.length > 0 ? remaining[0].id : null)
      }
    } catch (err) {
      console.error('Failed to delete conversation:', err)
    }
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

  const toggleSidebar = () => setIsSidebarOpen((prev) => !prev)

  return (
    <div className="flex h-screen w-full bg-surface dark:bg-slate-950 font-['Inter'] relative overflow-hidden">
      <Sidebar
        isOpen={isSidebarOpen}
        onToggle={toggleSidebar}
        conversations={conversations}
        activeConversationId={activeConversation?.id ?? null}
        onNewChat={handleNewChat}
        onSelectConversation={(id) => {
          setActiveId(id)
          setInput('')
          setAttachedFile(null)
        }}
        onDeleteConversation={handleDeleteConversation}
      />

      <main className={`flex-1 min-h-0 flex flex-col h-full relative transition-all duration-300 ${isSidebarOpen ? 'ml-80' : 'ml-20'}`}>
        <ChatHeader />

        <MessageList
          messages={activeConversation?.messages ?? []}
          messagesEndRef={messagesEndRef}
          isLoading={isLoading}
        />

        <ChatInput
          input={input}
          onInputChange={setInput}
          onSubmit={handleSubmit}
          attachedFile={attachedFile}
          onFileChange={handleFileChange}
          onRemoveFile={() => setAttachedFile(null)}
          supportsVoice={supportsVoice}
          isRecording={isRecording}
          onToggleRecording={toggleRecording}
        />
      </main>
    </div>
  )
}

export default App
