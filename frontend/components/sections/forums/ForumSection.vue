<!-- components/ForumSection.vue -->
<template>
  <div class="forum-container">
    <!-- Header du Forum -->
    <div class="forum-header">
      <div class="header-info">
        <h2 class="forum-title">
          <Icon name="mdi:forum" class="forum-icon" />
          Forum {{ currentCommune ? currentCommune.nom : 'Communautaire' }}
        </h2>
        <div class="online-status">
          <span class="online-dot"></span>
          {{ onlineUsers.length }} en ligne
        </div>
      </div>

      <!-- Boutons d'action -->
      <div class="header-actions">
        <button @click="toggleSearch" class="action-btn" :class="{ active: showSearch }">
          <Icon name="mdi:magnify" />
        </button>
        <button @click="loadMessages" class="action-btn">
          <Icon name="mdi:refresh" />
        </button>
      </div>
    </div>

    <!-- Barre de recherche -->
    <div v-if="showSearch" class="search-bar">
      <div class="search-input-container">
        <Icon name="mdi:magnify" class="search-icon" />
        <input v-model="searchQuery" @input="searchMessages" type="text" placeholder="Rechercher dans les messages..."
          class="search-input" />
        <button v-if="searchQuery" @click="clearSearch" class="clear-search">
          <Icon name="mdi:close" />
        </button>
      </div>
    </div>

    <!-- Liste des utilisateurs en ligne -->
    <div v-if="onlineUsers.length > 0" class="online-users-bar">
      <div class="online-users-scroll">
        <div v-for="user in onlineUsers" :key="user.user.id" class="online-user" @click="mentionUser(user.user)">
          <div class="user-avatar">
            {{ getUserInitials(user.user) }}
          </div>
          <span class="user-name">{{ user.user.first_name || user.user.username }}</span>
        </div>
      </div>
    </div>

    <!-- Zone des messages -->
    <div ref="messagesContainer" class="messages-container" @scroll="handleScroll">
      <div v-if="loading" class="loading-spinner">
        <Icon name="mdi:loading" class="spinning" />
        <span>Chargement des messages...</span>
      </div>

      <div v-else-if="messages.length === 0" class="empty-state">
        <Icon name="mdi:message-text-outline" class="empty-icon" />
        <h3>Aucun message</h3>
        <p>Soyez le premier à démarrer la conversation !</p>
      </div>

      <div v-else class="messages-list">
        <div v-for="message in allMessages" :key="message.id" class="message-item"
          :class="{ 'own-message': message.author.id === props.currentUser?.id }">
          <!-- Message de réponse -->
          <div v-if="message.reply_to" class="reply-reference">
            <div class="reply-line"></div>
            <div class="reply-content">
              <span class="reply-author">{{ message.reply_to.author }}</span>
              <span class="reply-text">{{ message.reply_to.content }}</span>
            </div>
          </div>

          <!-- Contenu principal du message -->
          <div class="message-bubble">
            <div class="message-header">
              <div class="author-info">
                <div class="author-avatar">
                  {{ getUserInitials(message.author) }}
                </div>
                <span class="author-name">{{ message.author.first_name || message.author.username }}</span>
                <span v-if="message.author.is_online" class="online-indicator"></span>
              </div>
              <div class="message-actions">
                <button @click="replyToMessage(message)" class="action-btn small">
                  <Icon name="mdi:reply" />
                </button>
                <button v-if="message.author.id === currentUser?.id" @click="editMessage(message)"
                  class="action-btn small">
                  <Icon name="mdi:pencil" />
                </button>
                <button v-if="message.author.id === currentUser?.id" @click="deleteMessage(message)"
                  class="action-btn small danger">
                  <Icon name="mdi:delete" />
                </button>
              </div>
            </div>

            <div class="message-content">
              <p v-if="!message.isEditing">{{ message.content }}</p>
              <div v-else class="edit-form">
                <textarea v-model="message.editContent" @keydown.enter.prevent="saveEdit(message)"
                  @keydown.esc="cancelEdit(message)" class="edit-textarea" rows="3"></textarea>
                <div class="edit-actions">
                  <button @click="saveEdit(message)" class="save-btn">
                    <Icon name="mdi:check" />
                  </button>
                  <button @click="cancelEdit(message)" class="cancel-btn">
                    <Icon name="mdi:close" />
                  </button>
                </div>
              </div>
            </div>

            <!-- Message Footer -->
            <div class="message-footer">
              <div class="message-time">
                {{ formatTime(message.created_at) }}
                <span v-if="message.is_edited" class="edited-indicator">(modifié)</span>
                <span v-if="message.author.id === currentUser?.id" class="message-status">
                  <Icon v-if="getMessageStatus(message) === 'sending'" name="mdi:clock-outline" class="animate-spin" />
                  <Icon v-else-if="getMessageStatus(message) === 'sent'" name="mdi:check" />
                  <Icon v-else-if="getMessageStatus(message) === 'error'" name="mdi:alert" class="text-red-500" />
                  <Icon v-if="message.read_by && message.read_by.length > 0" name="mdi:check-all"
                    :class="{ 'text-green-500': message.read_by.length === onlineUsers.length }" />
                </span>
              </div>

              <!-- Réactions -->
              <div class="reactions-container">
                <div v-if="Object.keys(message.reactions_count || {}).length > 0" class="reactions-display">
                  <template v-for="(count, reaction) in message.reactions_count" :key="reaction">
                    <button @click="toggleReaction(message, reaction)" class="reaction-btn"
                      :class="{ active: hasUserReacted(message, reaction) }">
                      {{ reaction }} {{ count }}
                    </button>
                  </template>
                </div>

                <div class="reaction-picker" :class="{ show: message.showReactions }">
                  <button v-for="emoji in reactionEmojis" :key="emoji" @click="addReaction(message, emoji)"
                    class="emoji-btn">
                    {{ emoji }}
                  </button>
                </div>

                <button @click="toggleReactionPicker(message)" class="add-reaction-btn">
                  <Icon name="mdi:emoticon-outline" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Indicateur de frappe -->
      <div v-if="typingUsers.length > 0" class="typing-indicator">
        <div class="typing-dots">
          <span></span>
          <span></span>
          <span></span>
        </div>
        <span>{{ getTypingText() }}</span>
      </div>
    </div>

    <!-- Zone de saisie de message -->
    <div class="message-input-container">
      <!-- Réponse en cours -->
      <div v-if="replyingTo" class="reply-preview">
        <div class="reply-info">
          <Icon name="mdi:reply" />
          <span>Réponse à {{ replyingTo.author.username }}</span>
        </div>
        <div class="reply-content-preview">{{ replyingTo.content }}</div>
        <button @click="cancelReply" class="cancel-reply">
          <Icon name="mdi:close" />
        </button>
      </div>

      <div class="input-row">
        <!-- Zone de saisie -->
        <div class="text-input-container">
          <textarea ref="messageInput" v-model="newMessage" @keydown="handleKeyDown" @input="handleTyping"
            @paste="handlePaste" placeholder="Écrivez votre message..." class="message-textarea" rows="1"></textarea>

          <!-- Suggestions de mentions -->
          <div v-if="showMentions" class="mentions-dropdown">
            <div v-for="user in mentionSuggestions" :key="user.id" @click="insertMention(user)" class="mention-item">
              <div class="mention-avatar">{{ getUserInitials(user) }}</div>
              <span>{{ user.first_name || user.username }}</span>
            </div>
          </div>
        </div>

        <!-- Boutons d'action -->
        <div class="input-actions">
          <button @click="openEmojiPicker" class="action-btn" :class="{ active: showEmojiPicker }">
            <Icon name="mdi:emoticon-outline" />
          </button>

          <button @click="sendMessage" :disabled="!canSend" class="send-btn" :class="{ active: canSend }">
            <Icon name="mdi:send" />
          </button>
        </div>
      </div>

      <!-- Sélecteur d'emoji -->
      <div v-if="showEmojiPicker" class="emoji-picker">
        <div class="emoji-categories">
          <button v-for="category in emojiCategories" :key="category.name" @click="activeEmojiCategory = category.name"
            class="emoji-category-btn" :class="{ active: activeEmojiCategory === category.name }">
            {{ category.icon }}
          </button>
        </div>
        <div class="emoji-grid">
          <button v-for="emoji in getCurrentEmojis()" :key="emoji" @click="insertEmoji(emoji)" class="emoji-btn">
            {{ emoji }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useCommuneStore } from '~/stores/communes'
import type { User, Message, Commune, WebSocketMessage, CommuneStore, ReactionType } from '~/types'
import { reactionToString } from '~/types'

// Définition des props
const props = defineProps<{
  currentUser: User
}>()

// --- États réactifs ---
const messages = ref<Message[]>([])
const pendingMessages = ref<Message[]>([])
const newMessage = ref('')
const loading = ref(false)
const currentCommune = ref<Commune | null>(null)
const onlineUsers = ref<{ user: User }[]>([])
const typingUsers = ref<string[]>([])
const searchQuery = ref('')
const showSearch = ref(false)
const showEmojiPicker = ref(false)
const showMentions = ref(false)
const mentionSuggestions = ref<User[]>([])
const replyingTo = ref<Message | null>(null)
const activeEmojiCategory = ref('smileys')
const page = ref(1)
const hasMoreMessages = ref(true)
const isLoadingMore = ref(false)
const socket = ref<WebSocket | null>(null)
const messageStatus = ref<{ [key: string]: 'sending' | 'sent' | 'error' }>({})

// Références DOM
const messagesContainer = ref<HTMLElement | null>(null)
const messageInput = ref<HTMLTextAreaElement | null>(null)

// Config emojis
const reactionEmojis: ReactionType[] = ['👍', '❤️', '😂', '😮', '😢', '😡']
const emojiCategories = [
  { name: 'smileys', icon: '😀', emojis: ['😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚', '😋', '😛', '😝', '😜', '🤪', '🤨', '🧐', '🤓', '😎', '🤩', '🥳'] },
  { name: 'gestures', icon: '👍', emojis: ['👍', '👎', '👌', '🤌', '🤏', '✌️', '🤞', '🤟', '🤘', '🤙', '👈', '👉', '👆', '🖕', '👇', '☝️', '👋', '🤚', '🖐️', '✋', '🖖', '👏', '🙌', '🤝', '🙏'] },
  { name: 'hearts', icon: '❤️', emojis: ['❤️', '🧡', '💛', '💚', '💙', '💜', '🖤', '🤍', '🤎', '💔', '❣️', '💕', '💞', '💓', '💗', '💖', '💘', '💝'] }
]

// --- Computed ---
const canSend = computed(() => newMessage.value.trim().length > 0)

const allMessages = computed(() => {
  return [...pendingMessages.value, ...messages.value].sort((a, b) =>
    new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
  )
})

// --- WebSocket Setup ---
const setupWebSocket = () => {
  const token = localStorage.getItem('authToken')
  const wsUrl = `ws://localhost:8000/ws/forum/${currentCommune.value?.id}/?token=${token}`

  console.log('Tentative de connexion WebSocket:', wsUrl)

  socket.value = new WebSocket(wsUrl)

  socket.value.onopen = () => {
    console.log('WebSocket connecté avec succès')
    // Renvoyer les messages en attente
    pendingMessages.value.forEach(msg => {
      sendMessageToServer(msg)
    })
  }

  socket.value.onerror = (error: Event) => {
    console.error('Erreur WebSocket:', error)
    // Marquer les messages en attente comme en erreur
    pendingMessages.value.forEach(msg => {
      messageStatus.value[msg.id] = 'error'
    })
  }

  socket.value.onmessage = (event: MessageEvent) => {
    const data: WebSocketMessage = JSON.parse(event.data)
    console.log('Message WebSocket reçu:', data)
    handleWebSocketMessage(data)
  }

  socket.value.onclose = () => {
    console.log('WebSocket connection closed')
    setTimeout(setupWebSocket, 1000) // Tentative de reconnexion
  }
}

const handleWebSocketMessage = (data: WebSocketMessage) => {
  switch (data.type) {
    case 'message':
      if (data.message) {
        // Supprimer le message en attente correspondant s'il existe
        const tempId = data.message.temp_id
        if (tempId) {
          pendingMessages.value = pendingMessages.value.filter(m => m.temp_id !== tempId)
          delete messageStatus.value[tempId]
        }
        messages.value.unshift(data.message)
        scrollToBottom()
      }
      break
    case 'message_ack':
      if (data.temp_id && data.message_id) {
        // Mettre à jour le statut du message
        messageStatus.value[data.temp_id] = 'sent'
        // Supprimer le message en attente et ajouter le message confirmé
        pendingMessages.value = pendingMessages.value.filter(m => m.temp_id !== data.temp_id)
        if (data.message) {
          messages.value.unshift(data.message)
        }
      }
      break
    case 'typing':
      if (data.user && typeof data.is_typing === 'boolean') {
        updateTypingUsers(data.user.username || data.user.email, data.is_typing)
      }
      break
    case 'online':
      if (data.users) {
        updateOnlineUsers(data.users)
      }
      break
    case 'read':
      if (data.message_id && data.user_id) {
        updateMessageReadStatus(data.message_id, data.user_id)
      }
      break
  }
}

// --- Utilitaires ---
const getUserInitials = (user: User): string => {
  const firstName = user.prenom || user.first_name || ''
  const lastName = user.nom || ''
  if (firstName && lastName) {
    return `${firstName[0]}${lastName[0]}`.toUpperCase()
  }
  return user.email.substring(0, 2).toUpperCase()
}

const formatTime = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now.getTime() - date.getTime()

  if (diff < 60000) return 'À l\'instant'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}min`
  if (diff < 86400000) return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
  return date.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' })
}

const getCurrentEmojis = () => {
  return emojiCategories.find(cat => cat.name === activeEmojiCategory.value)?.emojis || []
}

const getTypingText = () => {
  if (typingUsers.value.length === 1) {
    return `${typingUsers.value[0]} est en train d'écrire...`
  }
  return `${typingUsers.value.length} personnes écrivent...`
}

// Scroll automatique en bas des messages
const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// Gestion du scroll infini
const handleScroll = async () => {
  if (!messagesContainer.value || isLoadingMore.value || !hasMoreMessages.value) return

  const { scrollTop, scrollHeight, clientHeight } = messagesContainer.value
  if (scrollTop <= 100) {
    await loadMoreMessages()
  }
}

// --- Chargement des messages ---
const loadMessages = async () => {
  loading.value = true
  try {
    const url = new URL(`http://localhost:8000/api/forum/messages/${currentCommune.value?.id}`)
    url.searchParams.append('search', searchQuery.value || '')
    url.searchParams.append('page', page.value.toString())

    const response = await fetch(url.toString(), {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
        'Content-Type': 'application/json'
      }
    })

    if (response.ok) {
      const data = await response.json()
      messages.value = data.results || data
      hasMoreMessages.value = data.next !== null
      await nextTick()
      scrollToBottom()
    }
  } catch (error) {
    console.error('Erreur lors du chargement des messages:', error)
  } finally {
    loading.value = false
  }
}

const loadMoreMessages = async () => {
  if (isLoadingMore.value || !hasMoreMessages.value) return

  isLoadingMore.value = true
  page.value++

  try {
    const url = new URL(`http://localhost:8000/api/forum/messages/${currentCommune.value?.id}`)
    url.searchParams.append('page', page.value.toString())
    url.searchParams.append('search', searchQuery.value || '')

    const response = await fetch(url.toString(), {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
        'Content-Type': 'application/json'
      }
    })

    if (response.ok) {
      const data = await response.json()
      messages.value = [...data.results, ...messages.value]
      hasMoreMessages.value = data.next !== null
    }
  } catch (error) {
    console.error('Erreur lors du chargement des messages supplémentaires:', error)
    page.value--
  } finally {
    isLoadingMore.value = false
  }
}

// --- Envoi de messages ---
const generateTempId = () => `temp-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`

const sendMessage = async () => {
  if (!canSend.value) return

  const tempId = generateTempId()
  const tempMessage: Message = {
    id: -1,
    temp_id: tempId,
    content: newMessage.value.trim(),
    author: props.currentUser,
    created_at: new Date().toISOString(),
    is_edited: false,
    reactions_count: {},
    user_reactions: [],
    read_by: [],
    reply_to: replyingTo.value ? {
      id: replyingTo.value.id,
      content: replyingTo.value.content,
      author: replyingTo.value.author.username || replyingTo.value.author.email
    } : undefined
  }

  // Ajouter le message à la liste des messages en attente
  pendingMessages.value.unshift(tempMessage)
  messageStatus.value[tempId] = 'sending'

  // Réinitialiser le formulaire
  newMessage.value = ''
  replyingTo.value = null

  // Envoyer le message au serveur
  await sendMessageToServer(tempMessage)

  // Faire défiler vers le bas
  scrollToBottom()
}

const sendMessageToServer = async (message: Message) => {
  if (!socket.value || socket.value.readyState !== WebSocket.OPEN) {
    console.error('WebSocket non connecté')
    messageStatus.value[message.temp_id!] = 'error'
    return
  }

  try {
    const messageData = {
      type: 'message',
      content: message.content,
      temp_id: message.temp_id,
      reply_to: message.reply_to?.id || null,
      commune_id: currentCommune.value?.id
    }

    socket.value.send(JSON.stringify(messageData))
  } catch (error) {
    console.error('Erreur lors de l\'envoi du message:', error)
    messageStatus.value[message.temp_id!] = 'error'
  }
}

// Modifier le template pour afficher le statut des messages
const getMessageStatus = (message: Message) => {
  if (message.temp_id) {
    return messageStatus.value[message.temp_id] || 'sending'
  }
  return 'sent'
}

// --- Édition d'un message ---
const editMessage = (message: Message) => {
  message.isEditing = true
  message.editContent = message.content
}

const saveEdit = async (message: Message) => {
  if (!message.editContent?.trim()) return

  const messageData = {
    type: 'edit',
    message_id: message.id,
    content: message.editContent.trim()
  }

  socket.value?.send(JSON.stringify(messageData))
  message.isEditing = false
}

const cancelEdit = (message: Message) => {
  message.isEditing = false
}

// --- Suppression d'un message ---
const deleteMessage = async (message: Message) => {
  if (!confirm('Voulez-vous vraiment supprimer ce message ?')) return

  const messageData = {
    type: 'delete',
    message_id: message.id
  }

  socket.value?.send(JSON.stringify(messageData))
}

// --- Recherche ---
const toggleSearch = () => {
  showSearch.value = !showSearch.value
  if (!showSearch.value) {
    searchQuery.value = ''
    loadMessages()
  }
}

const searchMessages = () => {
  page.value = 1
  loadMessages()
}

const clearSearch = () => {
  searchQuery.value = ''
  page.value = 1
  loadMessages()
}

// --- Réactions ---
const hasUserReacted = (message: Message, reaction: ReactionType): boolean => {
  const reactionStr = reactionToString(reaction)
  return message.user_reactions?.includes(reactionStr) || false
}

const toggleReaction = async (message: Message, reaction: ReactionType): Promise<void> => {
  const reactionStr = reactionToString(reaction)
  const reactionData = {
    type: 'reaction' as const,
    message_id: message.id,
    reaction: reactionStr
  }

  socket.value?.send(JSON.stringify(reactionData))
}

const addReaction = async (message: Message, emoji: ReactionType): Promise<void> => {
  await toggleReaction(message, emoji)
  message.showReactions = false
}

const toggleReactionPicker = (message: Message): void => {
  message.showReactions = !message.showReactions
}

// --- Mentions ---
const mentionUser = (user: User) => {
  newMessage.value += `@${user.username} `
  showMentions.value = false
}

const insertMention = (user: User) => {
  newMessage.value += `@${user.username} `
  showMentions.value = false
}

// --- Gestion des entrées clavier ---
const handleKeyDown = (event: KeyboardEvent) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMessage()
  }
}

const handleTyping = () => {
  if (!socket.value) return

  socket.value.send(JSON.stringify({
    type: 'typing',
    is_typing: true
  }))
}

const handlePaste = (event: ClipboardEvent) => {
  // TODO: Gestion du collage d'images
}

// --- Emoji ---
const openEmojiPicker = () => {
  showEmojiPicker.value = !showEmojiPicker.value
}

const insertEmoji = (emoji: string) => {
  newMessage.value += emoji
  showEmojiPicker.value = false
  messageInput.value?.focus()
}

// --- Gestion des utilisateurs ---
const updateTypingUsers = (user: string, isTyping: boolean) => {
  if (isTyping) {
    if (!typingUsers.value.includes(user)) {
      typingUsers.value.push(user)
    }
  } else {
    typingUsers.value = typingUsers.value.filter(u => u !== user)
  }
}

const updateOnlineUsers = (users: { user: User }[]) => {
  onlineUsers.value = users
}

const updateMessageReadStatus = (messageId: number, userId: number) => {
  const message = messages.value.find(m => m.id === messageId)
  if (message) {
    if (!message.read_by) message.read_by = []
    if (!message.read_by.includes(userId)) {
      message.read_by.push(userId)
    }
  }
}

// --- Gestion de la réponse ---
const replyToMessage = (message: Message) => {
  replyingTo.value = message
  nextTick(() => {
    messageInput.value?.focus()
  })
}

const cancelReply = () => {
  replyingTo.value = null
}

// --- Cycle de vie ---
onMounted(async () => {
  if (!props.currentUser) {
    console.error('Utilisateur non connecté')
    return
  }

  const token = localStorage.getItem('authToken')
  if (!token) {
    console.error('Token d\'authentification non trouvé')
    return
  }

  try {
    console.log('Chargement des informations de la commune...')
    // Utiliser le store des communes
    const communeStore = useCommuneStore() as CommuneStore
    await communeStore.fetchCommunes()

    // Récupérer la commune de l'utilisateur
    if (props.currentUser.commune) {
      currentCommune.value = communeStore.getCommuneById(props.currentUser.commune)
      console.log('Commune chargée:', currentCommune.value)

      if (currentCommune.value) {
        // Initialiser WebSocket et charger les messages
        setupWebSocket()
        await loadMessages()
      } else {
        console.error('Commune non trouvée dans le store')
      }
    } else {
      console.error('Utilisateur sans commune associée')
    }
  } catch (error) {
    console.error('Erreur lors de l\'initialisation:', error)
  }
})

onUnmounted(() => {
  if (socket.value) {
    socket.value.close()
  }
})

// Surveiller les changements de recherche
watch(searchQuery, () => {
  if (searchQuery.value) {
    searchMessages()
  }
})
</script>

<style scoped>
.forum-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-height: 800px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

/* Header */
.forum-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.header-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.forum-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: #2d3748;
  margin: 0;
}

.forum-icon {
  font-size: 1.5rem;
  color: #667eea;
}

.online-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #718096;
}

.online-dot {
  width: 8px;
  height: 8px;
  background: #48bb78;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.header-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  background: rgba(102, 126, 234, 0.1);
  border: none;
  border-radius: 10px;
  padding: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  color: #667eea;
}

.action-btn:hover {
  background: rgba(102, 126, 234, 0.2);
  transform: translateY(-1px);
}

.action-btn.active {
  background: #667eea;
  color: white;
}

.action-btn.small {
  padding: 0.25rem;
  font-size: 1rem;
}

.action-btn.danger {
  color: #e53e3e;
}

.action-btn.danger:hover {
  background: rgba(229, 62, 62, 0.1);
}

/* Barre de recherche */
.search-bar {
  padding: 1rem 1.5rem;
  background: rgba(255, 255, 255, 0.9);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.search-input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 1rem;
  color: #a0aec0;
  z-index: 1;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 2px solid rgba(102, 126, 234, 0.2);
  border-radius: 25px;
  font-size: 0.875rem;
  background: white;
  transition: all 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.clear-search {
  position: absolute;
  right: 0.5rem;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  color: #a0aec0;
  border-radius: 50%;
}

/* Utilisateurs en ligne */
.online-users-bar {
  background: rgba(255, 255, 255, 0.9);
  padding: 1rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.online-users-scroll {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.online-users-scroll::-webkit-scrollbar {
  display: none;
}

.online-user {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 60px;
}

.online-user:hover {
  transform: translateY(-2px);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
}

.user-name {
  font-size: 0.75rem;
  color: #4a5568;
  text-align: center;
  max-width: 60px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Messages */
.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  height: 200px;
  color: white;
}

.spinning {
  animation: spin 1s linear infinite;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  height: 200px;
  color: white;
  text-align: center;
}

.empty-icon {
  font-size: 3rem;
  opacity: 0.7;
}

.messages-list {
  display: flex;
  flex-direction: column-reverse;
  gap: 1rem;
}

.message-item {
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
}

.message-item.own-message {
  align-items: flex-end;
}

.message-item.own-message .message-bubble {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.reply-reference {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  margin-left: 1rem;
}

.reply-line {
  width: 3px;
  height: 100%;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
  min-height: 20px;
}

.reply-content {
  background: rgba(255, 255, 255, 0.1);
  padding: 0.5rem;
  border-radius: 8px;
  font-size: 0.875rem;
}

.reply-author {
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin-right: 0.5rem;
}

.reply-text {
  color: rgba(255, 255, 255, 0.7);
}

.message-bubble {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 18px;
  padding: 1rem;
  max-width: 70%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  transition: all 0.2s;
}

.message-bubble:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.author-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 0.75rem;
}

.author-name {
  font-weight: 600;
  color: #2d3748;
  font-size: 0.875rem;
}

.own-message .author-name {
  color: rgba(255, 255, 255, 0.9);
}

.online-indicator {
  width: 8px;
  height: 8px;
  background: #48bb78;
  border-radius: 50%;
  border: 2px solid white;
}

.message-actions {
  display: flex;
  gap: 0.25rem;
  opacity: 0;
  transition: opacity 0.2s;
}

.message-bubble:hover .message-actions {
  opacity: 1;
}

.message-content {
  margin-bottom: 0.5rem;
}

.message-content p {
  margin: 0;
  line-height: 1.5;
  color: #2d3748;
  word-wrap: break-word;
}

.own-message .message-content p {
  color: rgba(255, 255, 255, 0.95);
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.edit-textarea {
  width: 100%;
  min-height: 60px;
  padding: 0.5rem;
  border: 2px solid rgba(102, 126, 234, 0.2);
  border-radius: 8px;
  font-family: inherit;
  font-size: 0.875rem;
  resize: vertical;
  background: white;
}

.edit-textarea:focus {
  outline: none;
  border-color: #667eea;
}

.edit-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.save-btn {
  background: #48bb78;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 0.25rem 0.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.875rem;
}

.cancel-btn {
  background: #a0aec0;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 0.25rem 0.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.875rem;
}

.message-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5rem;
}

.message-time {
  font-size: 0.75rem;
  color: #a0aec0;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.own-message .message-time {
  color: rgba(255, 255, 255, 0.7);
}

.edited-indicator {
  font-style: italic;
  opacity: 0.8;
}

/* Réactions */
.reactions-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  position: relative;
}

.reactions-display {
  display: flex;
  gap: 0.25rem;
  flex-wrap: wrap;
}

.reaction-btn {
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.reaction-btn:hover {
  background: rgba(102, 126, 234, 0.2);
  transform: scale(1.05);
}

.reaction-btn.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.reaction-picker {
  position: absolute;
  bottom: 100%;
  right: 0;
  background: white;
  border-radius: 12px;
  padding: 0.5rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  display: none;
  gap: 0.25rem;
  z-index: 10;
}

.reaction-picker.show {
  display: flex;
}

.emoji-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  border-radius: 6px;
  padding: 0.25rem;
  transition: all 0.2s;
}

.emoji-btn:hover {
  background: rgba(102, 126, 234, 0.1);
  transform: scale(1.2);
}

.add-reaction-btn {
  background: none;
  border: none;
  color: #a0aec0;
  cursor: pointer;
  font-size: 1rem;
  padding: 0.25rem;
  border-radius: 50%;
  transition: all 0.2s;
}

.add-reaction-btn:hover {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
}

/* Indicateur de frappe */
.typing-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 18px;
  margin-top: 1rem;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.875rem;
}

.typing-dots {
  display: flex;
  gap: 0.25rem;
}

.typing-dots span {
  width: 6px;
  height: 6px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 50%;
  animation: typing-bounce 1.4s infinite ease-in-out;
}

.typing-dots span:nth-child(1) {
  animation-delay: -0.32s;
}

.typing-dots span:nth-child(2) {
  animation-delay: -0.16s;
}

/* Zone de saisie */
.message-input-container {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 1rem 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.reply-preview {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(102, 126, 234, 0.1);
  padding: 0.75rem;
  border-radius: 12px;
  margin-bottom: 0.75rem;
  border-left: 4px solid #667eea;
}

.reply-info {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #667eea;
}

.reply-content-preview {
  flex: 1;
  font-size: 0.875rem;
  color: #4a5568;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.cancel-reply {
  background: none;
  border: none;
  color: #a0aec0;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 50%;
  transition: all 0.2s;
}

.cancel-reply:hover {
  background: rgba(160, 174, 192, 0.2);
  color: #718096;
}

.input-row {
  display: flex;
  gap: 0.75rem;
  align-items: flex-end;
}

.text-input-container {
  flex: 1;
  position: relative;
}

.message-textarea {
  width: 100%;
  min-height: 44px;
  max-height: 120px;
  padding: 0.75rem 1rem;
  border: 2px solid rgba(102, 126, 234, 0.2);
  border-radius: 22px;
  font-family: inherit;
  font-size: 0.875rem;
  resize: none;
  background: white;
  transition: all 0.2s;
  line-height: 1.4;
}

.message-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.message-textarea::placeholder {
  color: #a0aec0;
}

/* Mentions */
.mentions-dropdown {
  position: absolute;
  bottom: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
  margin-bottom: 0.5rem;
}

.mention-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.mention-item:hover {
  background: rgba(102, 126, 234, 0.1);
}

.mention-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 0.625rem;
}

.input-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.send-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 50%;
  width: 44px;
  height: 44px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  transition: all 0.2s;
  opacity: 0.5;
}

.send-btn:disabled {
  cursor: not-allowed;
  opacity: 0.3;
}

.send-btn.active {
  opacity: 1;
  transform: scale(1.05);
}

.send-btn:hover:not(:disabled) {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

/* Sélecteur d'emoji */
.emoji-picker {
  position: absolute;
  bottom: 100%;
  right: 0;
  background: white;
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 16px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
  width: 320px;
  max-height: 300px;
  z-index: 20;
  margin-bottom: 0.5rem;
}

.emoji-categories {
  display: flex;
  border-bottom: 1px solid rgba(102, 126, 234, 0.1);
  padding: 0.5rem;
  gap: 0.25rem;
}

.emoji-category-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  border-radius: 8px;
  padding: 0.5rem;
  transition: all 0.2s;
}

.emoji-category-btn:hover {
  background: rgba(102, 126, 234, 0.1);
}

.emoji-category-btn.active {
  background: #667eea;
  transform: scale(1.1);
}

.emoji-grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 0.25rem;
  padding: 0.75rem;
  max-height: 200px;
  overflow-y: auto;
}

.emoji-grid .emoji-btn {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

/* Animations */
@keyframes pulse {

  0%,
  100% {
    opacity: 1;
  }

  50% {
    opacity: 0.5;
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

@keyframes typing-bounce {

  0%,
  80%,
  100% {
    transform: scale(0);
    opacity: 0.5;
  }

  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* Responsive */
@media (max-width: 768px) {
  .forum-container {
    border-radius: 0;
    height: 100vh;
    max-height: none;
  }

  .forum-header {
    padding: 1rem;
  }

  .messages-container {
    padding: 0.75rem;
  }

  .message-bubble {
    max-width: 85%;
  }

  .message-input-container {
    padding: 1rem;
  }

  .emoji-picker {
    width: 280px;
    right: -20px;
  }

  .online-users-bar {
    padding: 0.75rem 1rem;
  }

  .search-bar {
    padding: 0.75rem 1rem;
  }
}

@media (max-width: 480px) {
  .header-info {
    gap: 0;
  }

  .forum-title {
    font-size: 1.1rem;
  }

  .online-status {
    font-size: 0.75rem;
  }

  .message-bubble {
    max-width: 90%;
    padding: 0.75rem;
  }

  .emoji-picker {
    width: calc(100vw - 2rem);
    right: -1rem;
  }

  .input-row {
    gap: 0.5rem;
  }
}

/* Scrollbar personnalisée */
.messages-container::-webkit-scrollbar,
.emoji-grid::-webkit-scrollbar,
.mentions-dropdown::-webkit-scrollbar {
  width: 6px;
}

.messages-container::-webkit-scrollbar-track,
.emoji-grid::-webkit-scrollbar-track,
.mentions-dropdown::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb,
.emoji-grid::-webkit-scrollbar-thumb,
.mentions-dropdown::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb:hover,
.emoji-grid::-webkit-scrollbar-thumb:hover,
.mentions-dropdown::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

.message-status {
  display: inline-flex;
  align-items: center;
  margin-left: 0.5rem;
  font-size: 0.875rem;
}

.message-status .icon {
  width: 1rem;
  height: 1rem;
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>