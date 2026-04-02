import { useEffect, useMemo, useRef, useState } from 'react'
import './App.css'
import Sidebar from './components/Sidebar.jsx'
import ChatHeader from './components/ChatHeader.jsx'
import MessageList from './components/MessageList.jsx'
import ChatInput from './components/ChatInput.jsx'

// Small helper to keep the "shape" of a conversation in one place.
// App owns the data, but other components just receive what they need as props.
function createEmptyConversation(id) {
  return {
    id,
    title: 'New Chat',
    messages: [],
    createdAt: new Date().toISOString(),
  }
}

// App is now a "page‑level" component: it owns state and behavior,
// and delegates rendering details to smaller, focused components.
function App() {
  // List of all chats in the left sidebar
  const [conversations, setConversations] = useState(() => {
    const firstId = crypto.randomUUID()
    return [createEmptyConversation(firstId)]
  })

  // Which conversation is currently selected
  const [activeId, setActiveId] = useState(() => conversations[0]?.id ?? null)

  // Text input + attached file for the message being composed
  const [input, setInput] = useState('')
  const [attachedFile, setAttachedFile] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  // Voice input state + browser SpeechRecognition instance
  const [isRecording, setIsRecording] = useState(false)
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const recognitionRef = useRef(null)

  // Used to auto‑scroll the messages list when a new message arrives
  const messagesEndRef = useRef(null)

  // Compute the active conversation from the list + active id
  const activeConversation = useMemo(
    () => conversations.find((c) => c.id === activeId) ?? conversations[0],
    [activeId, conversations],
  )

  // Feature‑detection for browser voice support so we can disable the mic button
  const supportsVoice = typeof window !== 'undefined' &&
    ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window)

  // One‑time setup of the SpeechRecognition instance (if the browser supports it).
  useEffect(() => {
    if (!supportsVoice || recognitionRef.current) return

    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition
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

    recognition.onend = () => {
      setIsRecording(false)
    }

    recognitionRef.current = recognition
  }, [supportsVoice])

  // When messages change, scroll the messages container to the bottom.
  useEffect(() => {
    if (!messagesEndRef.current) return
    messagesEndRef.current.scrollIntoView({ behavior: 'smooth' })
  }, [activeConversation?.messages.length])

  // Create a brand‑new empty chat and make it active.
  const handleNewChat = () => {
    const id = crypto.randomUUID()
    const next = createEmptyConversation(id)
    setConversations((prev) => [next, ...prev])
    setActiveId(id)
    setInput('')
    setAttachedFile(null)
  }

  // Helper to update a single conversation by id in an immutable way.
  const updateConversation = (id, updater) => {
    setConversations((prev) =>
      prev.map((c) => (c.id === id ? updater(c) : c)),
    )
  }

  // Handle the form submit from ChatInput.
  // For now this just generates a mock AI reply;
  // you can later replace this with a real API call.
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

    const formData = new FormData()

    formData.append("id", userMessage.id)
    formData.append("role", userMessage.role)
    
    // For the backend, ask for a summary if the user didn't type anything.
    const backendPrompt = trimmed || (attachedFile ? "Please summarize the attached document." : '')
    formData.append("message", backendPrompt)
    
    if (attachedFile) {
      formData.append("file", attachedFile)
    }
    formData.append("created_at", userMessage.createdAt)

    updateConversation(activeConversation.id, (c) => {
      const nextMessage = [...c.messages, userMessage]
      // const firstUser = nextMessage.find((m) => m.role === 'user')
      // const title = c.title || firstUser?.content?.slice(0, 40) || 'New Chat'
      const title = c.messages.length === 0
        ? userMessage.content.slice(0, 40)
        : c.title
      return {
        ...c,
        messages: nextMessage,
        title,
      }
    })

    try {
      setIsLoading(true)
      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        body: formData,
      })

      const data = await response.json()

      const aiReply = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: data.reply ?? 'Sorry, I could not generate a response.',
        createdAt: new Date().toISOString(),
      }

      updateConversation(activeConversation.id, (c) => {
        const nextMessage = [...c.messages, aiReply]
        return {
          ...c,
          messages: nextMessage,
        }
      })
    } catch (error) {
      console.error("Chat error:", error)
    } finally {
      setIsLoading(false)
    }
      
    setInput('')
    setAttachedFile(null)
  }

  // Keep App in charge of the file object, and let ChatInput tell us
  // when the user picked or cleared a file.
  const handleFileChange = (event) => {
    const file = event.target.files?.[0]
    if (!file) {
      setAttachedFile(null)
      return
    }
    setAttachedFile(file)
  }

  // Start/stop the SpeechRecognition instance when the mic button is clicked.
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

  const toggleSidebar = () => {
    setIsSidebarOpen((prev) => !prev)
  }

  return (
    <div className={`app ${!isSidebarOpen ? 'sidebar-open' : 'sidebar-collapsed'}`}>
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
      />

      <main className="chat-main">
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

        <div className="chat-footer-hint">
          <span>2026</span>
        </div>
      </main>
    </div>
  )
}

export default App
