<template>
    <aside class="w-64 bg-green-700 text-white min-h-screen p-4 space-y-4">
        <NuxtLink to="/" class="flex-shrink-0 flex items-center">
                <span class="text-xl font-bold">Redevabilité Verte</span>
              </NuxtLink>
      <ul>
        <!-- <li><NuxtLink to="/communes" class="block py-2 hover:bg-green-600 rounded">Communes</NuxtLink></li> -->
        <li><NuxtLink to="/dashboard/dashboard" class="flex items-center gap-2 py-2 px-3 rounded hover:bg-green-600"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M1 21h22L12 2zm12-3h-2v-2h2zm0-4h-2v-4h2z"/></svg>Signalements</NuxtLink></li>

        <li><NuxtLink to="/dashboard/forum" class="flex items-center gap-2 py-2 px-3 rounded hover:bg-green-600"><svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor"><path  d="M20 6h-1v8c0 .55-.45 1-1 1H6v1c0 1.1.9 2 2 2h10l4 4V8c0-1.1-.9-2-2-2m-3 5V4c0-1.1-.9-2-2-2H4c-1.1 0-2 .9-2 2v13l4-4h9c1.1 0 2-.9 2-2"/></svg>Forum</NuxtLink></li>

        <li><NuxtLink to="/dashboard/projets" class="flex items-center gap-2 py-2 px-3 rounded hover:bg-green-600"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M3 6H1v13c0 1.1.9 2 2 2h17v-2H3z"/><path fill="currentColor" d="M21 4h-7l-2-2H7c-1.1 0-1.99.9-1.99 2L5 15c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2"/></svg>Projets</NuxtLink></li>

        <li><NuxtLink to="/dashboard/meteo" class="flex items-center gap-2 py-2 px-3 rounded hover:bg-green-600"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M18.16 17.98c-2.76 1.76-4.67.77-5.61.08a.96.96 0 0 0-1.12.01c-.97.7-2.83 1.65-5.55-.06c-.33-.21-.75-.23-1.07-.01c-.91.61-1.53.85-2 .94s-.81.5-.81.97c0 .6.54 1.09 1.13.98c.77-.14 1.51-.42 2.2-.83a6.58 6.58 0 0 0 6.67 0a6.54 6.54 0 0 0 6.67 0c.69.41 1.44.69 2.21.83c.59.11 1.13-.38 1.13-.98v-.01c0-.47-.33-.88-.8-.97c-.49-.1-1.11-.34-2.02-.94a.96.96 0 0 0-1.03-.01M19.33 12H21c.55 0 1-.45 1-1s-.45-1-1-1h-1.61c-1.86 0-3.4-1.5-3.39-3.36c0-.37.06-.7.16-1.05c.37-1.29-.56-2.56-1.89-2.59H14C7.36 3 2.15 8.03 2.01 14.5v.03c-.04 1.13 1.07 1.98 2.14 1.6c.4-.14.78-.32 1.15-.54c2.08 1.2 4.64 1.22 6.7-.02a6.54 6.54 0 0 0 6.67 0c.68.41 1.42.68 2.18.82a.99.99 0 0 0 1.16-.98v-.01c0-.46-.32-.88-.78-.97c-.49-.09-1.12-.33-2.03-.94a.95.95 0 0 0-1.05-.01c-2.73 1.74-4.63.77-5.58.09a.99.99 0 0 0-1.16-.01c-.15.11-.09.06-.32.2c-.7-.94-1.09-2.06-1.09-3.26c0-2.58 1.77-4.74 4.21-5.33c-.13.51-.21 1.02-.21 1.5C14 9.61 16.39 12 19.33 12"/></svg>Meteo</NuxtLink></li>

        <li><NuxtLink to="/dashboard/cartographie" class="flex items-center gap-2 py-2 px-3 rounded hover:bg-green-600"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="m20.5 3l-.16.03L15 5.1L9 3L3.36 4.9c-.21.07-.36.25-.36.48V20.5c0 .28.22.5.5.5l.16-.03L9 18.9l6 2.1l5.64-1.9c.21-.07.36-.25.36-.48V3.5c0-.28-.22-.5-.5-.5M15 19l-6-2.11V5l6 2.11z"/></svg>cartographie</NuxtLink></li>
        <li>

    <NuxtLink to="/dashboard/notifications" class="flex items-center gap-2 py-2 px-3 rounded hover:bg-green-600"><svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor"><path d="M7.58 4.08L6.15 2.65C3.75 4.48 2.17 7.3 2.03 10.5h2a8.45 8.45 0 0 1 3.55-6.42m12.39 6.42h2c-.15-3.2-1.73-6.02-4.12-7.85l-1.42 1.43a8.5 8.5 0 0 1 3.54 6.42M18 11c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2zm-6 11c.14 0 .27-.01.4-.04c.65-.14 1.18-.58 1.44-1.18q.15-.36.15-.78h-4c.01 1.1.9 2 2.01 2"/></svg>Notifications</NuxtLink></li>

    <li><NuxtLink to="/dashboard/chatbot" class="flex items-center gap-2 py-2 px-3 rounded hover:bg-green-600"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M15.85 8.14c.39 0 .77.03 1.14.08C16.31 5.25 13.19 3 9.44 3c-4.25 0-7.7 2.88-7.7 6.43c0 2.05 1.15 3.86 2.94 5.04L3.67 16.5l2.76-1.19c.59.21 1.21.38 1.87.47c-.09-.39-.14-.79-.14-1.21c-.01-3.54 3.44-6.43 7.69-6.43M12 5.89a.96.96 0 1 1 0 1.92a.96.96 0 0 1 0-1.92M6.87 7.82a.96.96 0 1 1 0-1.92a.96.96 0 0 1 0 1.92"/><path fill="currentColor" d="M22.26 14.57c0-2.84-2.87-5.14-6.41-5.14s-6.41 2.3-6.41 5.14s2.87 5.14 6.41 5.14c.58 0 1.14-.08 1.67-.2L20.98 21l-1.2-2.4c1.5-.94 2.48-2.38 2.48-4.03m-8.34-.32a.96.96 0 1 1 .96-.96c.01.53-.43.96-.96.96m3.85 0a.96.96 0 1 1 0-1.92a.96.96 0 0 1 0 1.92"/></svg>Chatbot</NuxtLink></li>
      </ul>
    </aside>
  </template>
  