<!-- MapSection.vue - Template modifié -->
<template>
  <div class="map-container">
    <!-- Indicateur de géolocalisation -->
    <div v-if="locationStatus" class="location-status" :class="locationStatus.type">
      <span>{{ locationStatus.message }}</span>
      <button v-if="locationStatus.type === 'error'" @click="getUserLocation" class="retry-btn">
        Réessayer
      </button>
    </div>

    <!-- Statistiques des signalements -->
    <div class="stats-container">
      <div class="stat-card pollution">
        <div class="stat-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2a7.008 7.008 0 0 0-7 7c0 5.353 6.036 11.45 6.293 11.707l.707.707.707-.707C12.964 20.45 19 14.353 19 9a7.008 7.008 0 0 0-7-7zm0 16.533C10.471 16.825 7 12.553 7 9a5 5 0 0 1 10 0c0 3.546-3.473 7.823-5 9.533z"/>
            <path d="M12 6a3 3 0 1 0 3 3 3 3 0 0 0-3-3zm0 4a1 1 0 1 1 1-1 1 1 0 0 1-1 1z"/>
          </svg>
        </div>
        <div class="stat-number">{{ getCountByType('pollution') }}</div>
        <div class="stat-label">Pollution</div>
      </div>
      <div class="stat-card dechets">
        <div class="stat-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2a7.008 7.008 0 0 0-7 7c0 5.353 6.036 11.45 6.293 11.707l.707.707.707-.707C12.964 20.45 19 14.353 19 9a7.008 7.008 0 0 0-7-7zm0 16.533C10.471 16.825 7 12.553 7 9a5 5 0 0 1 10 0c0 3.546-3.473 7.823-5 9.533z"/>
            <path d="M12 6a3 3 0 1 0 3 3 3 3 0 0 0-3-3zm0 4a1 1 0 1 1 1-1 1 1 0 0 1-1 1z"/>
          </svg>
        </div>
        <div class="stat-number">{{ getCountByType('dechets') }}</div>
        <div class="stat-label">Déchets</div>
      </div>
      <div class="stat-card climat">
        <div class="stat-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2a7.008 7.008 0 0 0-7 7c0 5.353 6.036 11.45 6.293 11.707l.707.707.707-.707C12.964 20.45 19 14.353 19 9a7.008 7.008 0 0 0-7-7zm0 16.533C10.471 16.825 7 12.553 7 9a5 5 0 0 1 10 0c0 3.546-3.473 7.823-5 9.533z"/>
            <path d="M12 6a3 3 0 1 0 3 3 3 3 0 0 0-3-3zm0 4a1 1 0 1 1 1-1 1 1 0 0 1-1 1z"/>
          </svg>
        </div>
        <div class="stat-number">{{ getCountByType('climat') }}</div>
        <div class="stat-label">Climat</div>
      </div>
    </div>

    <!-- Filtres -->
    <div class="filters-container">
      <div class="filter-group">
        <label>Type</label>
        <select v-model="selectedType" @change="filterSignalements" class="filter-select">
          <option value="">Tous les types</option>
          <option v-for="type in typeChoices" :key="type.value" :value="type.value">
            {{ type.label }}
          </option>
        </select>
      </div>
      <div class="filter-group">
        <label>Statut</label>
        <select v-model="selectedStatus" @change="filterSignalements" class="filter-select">
          <option value="">Tous les statuts</option>
          <option v-for="statut in statutChoices" :key="statut.value" :value="statut.value">
            {{ statut.label }}
          </option>
        </select>
      </div>
    </div>

    <!-- Boutons d'action -->
    <div class="action-buttons">
      <button class="action-btn secondary" @click="resetFilters">
        <i class="reset-icon">⟲</i>
        Réinitialiser
      </button>
      <button class="action-btn primary" @click="centerOnUser" :disabled="!userLocation">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 2a7.008 7.008 0 0 0-7 7c0 5.353 6.036 11.45 6.293 11.707l.707.707.707-.707C12.964 20.45 19 14.353 19 9a7.008 7.008 0 0 0-7-7zm0 16.533C10.471 16.825 7 12.553 7 9a5 5 0 0 1 10 0c0 3.546-3.473 7.823-5 9.533z"/>
          <path d="M12 6a3 3 0 1 0 3 3 3 3 0 0 0-3-3zm0 4a1 1 0 1 1 1-1 1 1 0 0 1-1 1z"/>
        </svg>
        {{ userLocation ? 'Ma position' : 'Position indisponible' }}
      </button>
    </div>

    <!-- Message de chargement -->
    <div v-if="loading" class="loading-message">
      <div class="loading-spinner"></div>
      <span>Chargement des signalements...</span>
    </div>

    <!-- Carte -->
    <div id="map" class="map"></div>

    <!-- Panneau de filtres latéral (version desktop) -->
    <div class="filter-panel" v-if="!isMobile">
      <h3>Filtrer par type</h3>
      <div v-for="(type, index) in signalementTypes" :key="index" class="filter-item">
        <input 
          type="checkbox" 
          :id="type.name" 
          v-model="type.active" 
          @change="filterSignalements"
        >
        <label :for="type.name">{{ type.label }}</label>
        <div class="map-icon-indicator" :style="{ color: type.color }">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2a7.008 7.008 0 0 0-7 7c0 5.353 6.036 11.45 6.293 11.707l.707.707.707-.707C12.964 20.45 19 14.353 19 9a7.008 7.008 0 0 0-7-7zm0 16.533C10.471 16.825 7 12.553 7 9a5 5 0 0 1 10 0c0 3.546-3.473 7.823-5 9.533z"/>
            <path d="M12 6a3 3 0 1 0 3 3 3 3 0 0 0-3-3zm0 4a1 1 0 1 1 1-1 1 1 0 0 1-1 1z"/>
          </svg>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { onMounted, ref, computed, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'MapSection',
  setup() {
    const router = useRouter();
    const map = ref(null);
    const userMarker = ref(null);
    const userLocation = ref(null);
    const signalements = ref([]);
    const signalementMarkers = ref([]);
    const selectedType = ref('');
    const selectedStatus = ref('');
    const isMobile = ref(window.innerWidth <= 768);
    const loading = ref(false);
    const locationStatus = ref(null);
    const token = localStorage.getItem('authToken');
    
    // Choix disponibles (correspondent à votre API)
    const typeChoices = ref([
      { value: 'pollution', label: 'Pollution' },
      { value: 'dechets', label: 'Déchets' },
      { value: 'climat', label: 'Climat' }
    ]);

    const statutChoices = ref([
      { value: 'en_attente', label: 'En attente' },
      { value: 'en_cours', label: 'En cours' },
      { value: 'traite', label: 'Traité' }
    ]);
    
    const signalementTypes = ref([
      { name: 'pollution', label: 'Pollution', color: '#FF6B6B', active: true },
      { name: 'dechets', label: 'Déchets', color: '#FFD93D', active: true },
      { name: 'climat', label: 'Climat', color: '#6BCF7F', active: true }
    ]);

    const getCountByType = (type) => {
      return signalements.value.filter(s => s.type_signalement === type).length;
    };

    const initMap = () => {
      // Centre sur Yaoundé, Cameroun
      const yaoundeCenter = [3.8480, 11.5021];

      map.value = L.map('map', {
        center: yaoundeCenter,
        zoom: 12,
        zoomControl: true,
        attributionControl: true
      });

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18,
        minZoom: 8
      }).addTo(map.value);

      // Limite de la vue à la zone du Cameroun
      const cameroonBounds = L.latLngBounds(
        L.latLng(1.6546, 8.4948), // Sud-Ouest
        L.latLng(13.0856, 16.1921) // Nord-Est
      );
      map.value.setMaxBounds(cameroonBounds);

      // Obtenir la position de l'utilisateur automatiquement
      setTimeout(() => {
        getUserLocation();
      }, 1000);
    };

    const getUserLocation = () => {
      console.log('Tentative de géolocalisation...');
      locationStatus.value = { type: 'info', message: 'Recherche de votre position...' };

      if (!navigator.geolocation) {
        console.error('Géolocalisation non supportée');
        locationStatus.value = { 
          type: 'error', 
          message: 'Géolocalisation non supportée par ce navigateur' 
        };
        return;
      }

      const options = {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 300000 // 5 minutes
      };

      navigator.geolocation.getCurrentPosition(
        (position) => {
          console.log('Position obtenue:', position.coords);
          const { latitude, longitude, accuracy } = position.coords;
          const userPosition = [latitude, longitude];
          
          userLocation.value = { latitude, longitude, accuracy };

          // Supprimer l'ancien marqueur s'il existe
          if (userMarker.value) {
            map.value.removeLayer(userMarker.value);
          }

          // Créer le marqueur utilisateur avec le SVG bleu
          const userIcon = L.divIcon({
            className: 'user-location-marker',
            html: `
              <div class="user-marker-svg">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="#2196F3">
                  <path d="M12 2a7.008 7.008 0 0 0-7 7c0 5.353 6.036 11.45 6.293 11.707l.707.707.707-.707C12.964 20.45 19 14.353 19 9a7.008 7.008 0 0 0-7-7zm0 16.533C10.471 16.825 7 12.553 7 9a5 5 0 0 1 10 0c0 3.546-3.473 7.823-5 9.533z"/>
                  <path d="M12 6a3 3 0 1 0 3 3 3 3 0 0 0-3-3zm0 4a1 1 0 1 1 1-1 1 1 0 0 1-1 1z"/>
                </svg>
              </div>
            `,
            iconSize: [32, 32],
            iconAnchor: [16, 30] // Point d'ancrage en bas du marqueur
          });

          userMarker.value = L.marker(userPosition, { 
            icon: userIcon,
            zIndexOffset: 1000 // S'assurer que le marqueur utilisateur est au-dessus
          }).addTo(map.value);

          userMarker.value.bindPopup(`
            <div class="user-popup">
              <strong>Ma position</strong><br>
              <small>Précision: ±${Math.round(accuracy)}m</small><br>
              <small>Lat: ${latitude.toFixed(6)}</small><br>
              <small>Lng: ${longitude.toFixed(6)}</small>
            </div>
          `);

          locationStatus.value = { 
            type: 'success', 
            message: `Position trouvée (±${Math.round(accuracy)}m)` 
          };

          // Masquer le message après 3 secondes
          setTimeout(() => {
            locationStatus.value = null;
          }, 3000);

          console.log('Marqueur utilisateur ajouté à la carte');
        },
        (error) => {
          console.error('Erreur de géolocalisation:', error);
          let errorMessage = 'Impossible d\'obtenir votre position';
          
          switch(error.code) {
            case error.PERMISSION_DENIED:
              errorMessage = 'Accès à la géolocalisation refusé';
              break;
            case error.POSITION_UNAVAILABLE:
              errorMessage = 'Position indisponible';
              break;
            case error.TIMEOUT:
              errorMessage = 'Délai de géolocalisation dépassé';
              break;
          }
          
          locationStatus.value = { type: 'error', message: errorMessage };
        },
        options
      );
    };

    // Fonction pour extraire latitude et longitude de la localisation
    const parseLocation = (localisation) => {
      if (!localisation) return null;
      
      try {
        // Format: "lat,lng"
        if (localisation.includes(',')) {
          const [lat, lng] = localisation.split(',').map(coord => parseFloat(coord.trim()));
          if (!isNaN(lat) && !isNaN(lng)) {
            return { latitude: lat, longitude: lng };
          }
        }
        
        // Format JSON: {"lat": x, "lng": y} ou {"latitude": x, "longitude": y}
        if (localisation.startsWith('{')) {
          const parsed = JSON.parse(localisation);
          if (parsed.lat && parsed.lng) {
            return { latitude: parsed.lat, longitude: parsed.lng };
          }
          if (parsed.latitude && parsed.longitude) {
            return { latitude: parsed.latitude, longitude: parsed.longitude };
          }
        }
        
        // Si c'est juste du texte, générer des coordonnées aléatoires autour de Yaoundé
        const baseLatitude = 3.8480;
        const baseLongitude = 11.5021;
        const randomOffset = 0.05;
        
        return {
          latitude: baseLatitude + (Math.random() - 0.5) * randomOffset,
          longitude: baseLongitude + (Math.random() - 0.5) * randomOffset
        };
      } catch (error) {
        console.error('Erreur parsing localisation:', error);
        return null;
      }
    };

  // Correction de l'URL de l'API et amélioration de la fonction loadSignalements
const loadSignalements = async () => {
  if (!token) {
    console.error('Token d\'authentification manquant');
    await loadDemoData();
    return;
  }
  
  loading.value = true;
  console.log('🔍 Début du chargement des signalements...');
  
  try {
    // 1. D'abord, récupérer les signalements
    let url = 'http://localhost:8000/api/signalements/liste/';
    const params = new URLSearchParams();
    if (selectedStatus.value) params.append('statut', selectedStatus.value);
    if (selectedType.value) params.append('type', selectedType.value);
    if (params.toString()) {
      url += '?' + params.toString();
    }
    
    console.log('📡 Requête API signalements vers:', url);
    const signalementResponse = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (!signalementResponse.ok) {
      console.error('❌ Erreur HTTP:', signalementResponse.status, signalementResponse.statusText);
      throw new Error('Erreur lors du chargement des signalements');
    }
    
    const signalementData = await signalementResponse.json();
    console.log('✅ Données des signalements reçues:', signalementData);
    
    // Déterminer l'array de signalements selon la structure de réponse
    let signalementsArray = [];
    if (signalementData.signalements) {
      signalementsArray = signalementData.signalements;
    } else if (Array.isArray(signalementData)) {
      signalementsArray = signalementData;
    } else if (signalementData.results) {
      signalementsArray = signalementData.results;
    }
    
    console.log(`📊 Nombre de signalements récupérés: ${signalementsArray.length}`);
    
    // Afficher les informations sur les photo_id des signalements
    const photoIds = signalementsArray
      .filter(s => s.photo_id)
      .map(s => s.photo_id);
    
    console.log(`🖼️ Signalements avec photo_id: ${photoIds.length}/${signalementsArray.length}`);
    
    // 2. Récupérer les coordonnées des photos - CORRIGER L'URL ICI
    console.log('🔍 Récupération des coordonnées de photos...');
    const photoLocationsResponse = await fetch('http://localhost:8000/api/photos/locations/', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (!photoLocationsResponse.ok) {
      console.error('❌ Erreur lors de la récupération des coordonnées de photos:', 
        photoLocationsResponse.status, photoLocationsResponse.statusText);
      throw new Error('Erreur lors du chargement des coordonnées');
    }
    
    const photoLocationsData = await photoLocationsResponse.json();
    console.log('✅ Données des coordonnées reçues:', photoLocationsData);
    
    // Créer un map des coordonnées par ID de photo
    const photoCoordinatesMap = {};
    
    // Adapter en fonction de la structure de votre API
    if (Array.isArray(photoLocationsData)) {
      photoLocationsData.forEach(photo => {
        if (photo.id && (photo.latitude !== undefined && photo.longitude !== undefined)) {
          photoCoordinatesMap[photo.id] = {
            latitude: parseFloat(photo.latitude),
            longitude: parseFloat(photo.longitude)
          };
        }
      });
    } else if (photoLocationsData.photos) {
      photoLocationsData.photos.forEach(photo => {
        if (photo.id && (photo.latitude !== undefined && photo.longitude !== undefined)) {
          photoCoordinatesMap[photo.id] = {
            latitude: parseFloat(photo.latitude),
            longitude: parseFloat(photo.longitude)
          };
        }
      });
    } else {
      // Explorer la structure pour trouver les coordonnées
      console.log('⚠️ Structure inconnue, exploration des données...');
      
      // Essayer de parcourir toutes les propriétés pour trouver des coordonnées
      Object.entries(photoLocationsData).forEach(([key, value]) => {
        if (Array.isArray(value)) {
          console.log(`📑 Trouvé un tableau dans la propriété "${key}" avec ${value.length} éléments`);
          value.forEach((item, index) => {
            if (item.id && (item.latitude !== undefined && item.longitude !== undefined)) {
              photoCoordinatesMap[item.id] = {
                latitude: parseFloat(item.latitude),
                longitude: parseFloat(item.longitude)
              };
              console.log(`  ✅ Item #${index} a des coordonnées valides`);
            }
          });
        }
      });
    }
    
    console.log('🗺️ Map des coordonnées par ID de photo:', photoCoordinatesMap);
    console.log(`📊 Nombre d'entrées dans le map: ${Object.keys(photoCoordinatesMap).length}`);
    
    // 3. Associer les coordonnées aux signalements
    const processedSignalements = signalementsArray.map(signalement => {
      console.log(`\n📝 Traitement du signalement ID ${signalement.id}:`);
      console.log(`  - Type: ${signalement.type_signalement}`);
      console.log(`  - Photo ID: ${signalement.photo_id || 'Aucun'}`);
      
      // D'abord vérifier si le signalement a un photo_id et si on a des coordonnées pour cette photo
      let coords = null;
      
      if (signalement.photo_id && photoCoordinatesMap[signalement.photo_id]) {
        coords = photoCoordinatesMap[signalement.photo_id];
        console.log(`  ✅ Coordonnées trouvées via photo_id ${signalement.photo_id}:`, coords);
      } else {
        if (signalement.photo_id) {
          console.log(`  ⚠️ Photo ID ${signalement.photo_id} présent mais pas de coordonnées correspondantes`);
        }
        
        // Essayer d'extraire les coordonnées de la localisation
        coords = parseLocation(signalement.localisation);
        console.log(`  🔄 Utilisation du fallback parseLocation: ${signalement.localisation} -> `, coords);
      }
      
      // Vérifier que les coordonnées sont dans des plages valides
      if (coords && coords.latitude && coords.longitude) {
        // Vérifier que les coordonnées sont numériques et dans des plages valides
        const lat = parseFloat(coords.latitude);
        const lng = parseFloat(coords.longitude);
        
        if (isNaN(lat) || isNaN(lng) || lat < -90 || lat > 90 || lng < -180 || lng > 180) {
          console.error(`  ❌ Coordonnées invalides: ${lat}, ${lng}`);
          coords = null;
        } else {
          coords.latitude = lat;
          coords.longitude = lng;
          console.log(`  ✅ Coordonnées validées: ${lat}, ${lng}`);
        }
      }
      
      return {
        ...signalement,
        latitude: coords?.latitude,
        longitude: coords?.longitude,
        type: signalement.type_signalement,
        status: signalement.statut,
        description: signalement.description || signalement.objet
      };
    });
    console.log('Coordonnées des signalements traités:', processedSignalements.map(s => ({
  id: s.id,
  latitude: s.latitude,
  longitude: s.longitude
  })));
    
    // Filtrer les signalements sans coordonnées valides
    signalements.value = processedSignalements.filter(s => {
      if (!s.latitude || !s.longitude) {
        console.log(`❌ Signalement ID ${s.id} sans coordonnées valides, filtré`);
        return false;
      }
      return true;
    });
    
    console.log(`\n📊 Résultat final: ${signalements.value.length}/${processedSignalements.length} signalements avec coordonnées valides`);
    console.log('Signalements chargés:', signalements.value);
    // 4. Afficher les signalements sur la carte
    console.log('🗺️ Affichage des signalements sur la carte...');
    
    // Assurez-vous que la carte est initialisée avant d'afficher les signalements
    if (!map.value) {
      console.error('❌ La carte n\'est pas initialisée!');
      await initMap();
    }
    
    // Afficher les signalements
    displaySignalements();
    
    // Ajuster la vue pour voir tous les signalements
    if (signalements.value.length > 0) {
      fitMapToSignalements();
    }
    
  } catch (error) {
    console.error('❌ Erreur lors du chargement des données:', error);
    await loadDemoData(); // Utiliser les données de démo en cas d'erreur
  } finally {
    loading.value = false;
  }

};

// Fonction pour ajuster la vue de la carte pour voir tous les signalements
const fitMapToSignalements = () => {
  if (!map.value || signalements.value.length === 0) return;
  
  try {
    console.log('📏 Ajustement de la vue pour voir tous les signalements...');
    
    // Créer des bounds qui incluent tous les signalements
    const bounds = L.latLngBounds([]);
    
    signalements.value.forEach(s => {
      if (s.latitude && s.longitude) {
        bounds.extend([s.latitude, s.longitude]);
      }
    });
    
    // Ajouter la position de l'utilisateur si disponible
    if (userLocation.value) {
      bounds.extend([userLocation.value.latitude, userLocation.value.longitude]);
    }
    
    // Vérifier que les bounds sont valides
    if (bounds.isValid()) {
      map.value.fitBounds(bounds, {
        padding: [50, 50], // Ajouter un peu d'espace autour
        maxZoom: 15,       // Ne pas zoomer trop près
        animate: true
      });
      console.log('✅ Vue ajustée pour voir tous les signalements');
    } else {
      console.warn('⚠️ Impossible d\'ajuster la vue, bounds invalides');
      centerOnDefaultLocation();
    }
  } catch (error) {
    console.error('❌ Erreur lors de l\'ajustement de la vue:', error);
    centerOnDefaultLocation();
  }
};

// Améliorer la fonction displaySignalements
const displaySignalements = () => {
  console.log('🔄 Affichage des signalements sur la carte...');
  
  if (!map.value) {
    console.error('❌ La carte n\'est pas initialisée, impossible d\'afficher les signalements');
    return;
  }
  
  // Supprimer les marqueurs existants (sauf l'utilisateur)
  signalementMarkers.value.forEach(marker => {
    map.value.removeLayer(marker);
  });
  signalementMarkers.value = [];
  
  // Filtrer les signalements
  let filteredSignalements = signalements.value.filter(signalement => {
    const typeMatch = !selectedType.value || signalement.type_signalement === selectedType.value;
    const statusMatch = !selectedStatus.value || signalement.statut === selectedStatus.value;
    const typeActive = signalementTypes.value.find(t => t.name === signalement.type_signalement)?.active !== false;
    
    return typeMatch && statusMatch && typeActive && signalement.latitude && signalement.longitude;
  });
  
  console.log(`📍 Affichage de ${filteredSignalements.length} signalements sur la carte`);
  
  // Ajouter les nouveaux marqueurs avec des icônes personnalisées
  filteredSignalements.forEach(signalement => {
    try {
      const typeInfo = signalementTypes.value.find(t => t.name === signalement.type_signalement);
      const color = typeInfo ? typeInfo.color : '#9775FA';
      
      // Créer un marqueur avec une icône personnalisée selon le type
      let markerHtml = '';
      
      // Utiliser des icônes différentes selon le type
      switch (signalement.type_signalement) {
        case 'pollution':
          markerHtml = `<div class="custom-marker pollution-marker" style="background-color: ${color}"></div>`;
          break;
        case 'dechets':
          markerHtml = `<div class="custom-marker dechets-marker" style="background-color: ${color}"></div>`;
          break;
        case 'climat':
          markerHtml = `<div class="custom-marker climat-marker" style="background-color: ${color}"></div>`;
          break;
        default:
          markerHtml = `<div class="custom-marker" style="background-color: ${color}"></div>`;
      }
      
      const signalementIcon = L.divIcon({
        className: `signalement-marker-${signalement.type_signalement}`,
        html: markerHtml,
        iconSize: [30, 30],
        iconAnchor: [15, 30]
      });
      
      // Créer le marqueur à la position du signalement
      const markerPosition = [signalement.latitude, signalement.longitude];
      console.log(`  📍 Marqueur à: ${markerPosition[0]}, ${markerPosition[1]}`);
      
      const marker = L.marker(markerPosition, {
        icon: signalementIcon
      }).addTo(map.value);
      
      // Textes pour les statuts et types
      const statusText = {
        'en_attente': 'En attente',
        'en_cours': 'En cours',
        'traite': 'Traité'
      };
      
      const typeText = {
        'pollution': 'Pollution',
        'dechets': 'Déchets',
        'climat': 'Climat'
      };
      
      // Créer un popup informatif
      marker.bindPopup(`
        <div class="popup-content">
          <div class="popup-header">
            <strong>${typeText[signalement.type_signalement] || signalement.type_signalement}</strong>
            <span class="popup-status status-${signalement.statut}">${statusText[signalement.statut] || 'En attente'}</span>
          </div>
          <div class="popup-title"><strong>${signalement.objet || 'Sans titre'}</strong></div>
          <div class="popup-description">${signalement.description || 'Aucune description'}</div>
          <div class="popup-user">Signalé par: ${signalement.utilisateur_nom || 'Utilisateur'}</div>
          <div class="popup-date">${signalement.date_signalement ? new Date(signalement.date_signalement).toLocaleString('fr-FR') : 'Date inconnue'}</div>
        </div>
      `);
      
      // Ajouter le marqueur à la liste
      signalementMarkers.value.push(marker);
      
    } catch (error) {
      console.error(`❌ Erreur lors de l'affichage du signalement ${signalement.id}:`, error);
    }
  });
  
  console.log(`✅ ${signalementMarkers.value.length} marqueurs ajoutés à la carte`);
};

    const filterSignalements = () => {
      displaySignalements();
    };

    const resetFilters = () => {
      selectedType.value = '';
      selectedStatus.value = '';
      signalementTypes.value.forEach(type => type.active = true);
      filterSignalements();
    };

    const centerOnUser = () => {
      if (userLocation.value && map.value) {
        map.value.setView([userLocation.value.latitude, userLocation.value.longitude], 16);
        if (userMarker.value) {
          userMarker.value.openPopup();
        }
      } else {
        getUserLocation();
      }
    };

    const goBack = () => {
      router.push('/dashboard/ctd');
    };

    // Responsive handling
    const handleResize = () => {
      isMobile.value = window.innerWidth <= 768;
      if (map.value) {
        map.value.invalidateSize();
      }
    };

    onMounted(() => {
      console.log('Initialisation de la carte...');
      initMap();
      loadSignalements();
      window.addEventListener('resize', handleResize);
    });

    onUnmounted(() => {
      window.removeEventListener('resize', handleResize);
    });

    return {
      signalementTypes,
      typeChoices,
      statutChoices,
      selectedType,
      selectedStatus,
      isMobile,
      loading,
      locationStatus,
      userLocation,
      getCountByType,
      filterSignalements,
      resetFilters,
      centerOnUser,
      goBack,
      loadSignalements,
      getUserLocation
    };
  }
}
</script>

<style scoped>
.map-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f5f5f5;
}

.map-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background-color: #4CAF50;
  color: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.back-btn, .refresh-btn, .settings-btn, .location-btn {
  background: none;
  border: none;
  color: white;
  font-size: 18px;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.back-btn:hover, .refresh-btn:hover, .settings-btn:hover, .location-btn:hover {
  background-color: rgba(255,255,255,0.1);
}

.location-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.map-title {
  font-size: 18px;
  font-weight: 500;
  margin: 0;
}

.header-right {
  display: flex;
  gap: 8px;
}

.location-status {
  padding: 8px 16px;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.location-status.info {
  background-color: #E3F2FD;
  color: #1976D2;
  border-left: 4px solid #2196F3;
}

.location-status.success {
  background-color: #E8F5E8;
  color: #2E7D32;
  border-left: 4px solid #4CAF50;
}

.location-status.error {
  background-color: #FFEBEE;
  color: #C62828;
  border-left: 4px solid #F44336;
}

.retry-btn {
  background: none;
  border: 1px solid currentColor;
  color: inherit;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
}

.stats-container {
  display: flex;
  padding: 16px;
  gap: 12px;
  background-color: white;
}

.stat-card {
  flex: 1;
  padding: 16px;
  border-radius: 12px;
  text-align: center;
  color: white;
  font-weight: 500;
}

.stat-card.pollution {
  background-color: #FF6B6B;
}

.stat-card.dechets {
  background-color: #FFD93D;
  color: #333;
}

.stat-card.climat {
  background-color: #6BCF7F;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  opacity: 0.9;
}

.filters-container {
  display: flex;
  padding: 16px;
  gap: 16px;
  background-color: white;
  border-bottom: 1px solid #eee;
}

.filter-group {
  flex: 1;
}

.filter-group label {
  display: block;
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
  font-weight: 500;
}

.filter-select {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  background-color: white;
  color: #333;
}

.action-buttons {
  display: flex;
  padding: 16px;
  gap: 12px;
  background-color: white;
  border-bottom: 1px solid #eee;
}

.map-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f5f5f5;
}

.map-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background-color: #4CAF50;
  color: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.back-btn, .refresh-btn, .settings-btn, .location-btn {
  background: none;
  border: none;
  color: white;
  font-size: 18px;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: background-color 0.2s;
}

/* Styles améliorés pour les marqueurs */
.custom-marker {
  width: 30px;
  height: 30px;
  border-radius: 50% 50% 50% 0;
  background: #00cae9;
  position: absolute;
  transform: rotate(-45deg);
  left: 50%;
  top: 50%;
  margin: -15px 0 0 -15px;
  border: 2px solid #fff;
  box-shadow: 0 2px 5px rgba(0,0,0,0.4);
}

.custom-marker:after {
  content: '';
  width: 14px;
  height: 14px;
  margin: 8px 0 0 8px;
  background: #fff;
  position: absolute;
  border-radius: 50%;
}

.pollution-marker {
  background: #FF6B6B;
}

.dechets-marker {
  background: #FFD93D;
}

.climat-marker {
  background: #6BCF7F;
}

/* Styles améliorés pour les popups */
.leaflet-popup-content-wrapper {
  border-radius: 8px;
  padding: 0;
  overflow: hidden;
  box-shadow: 0 3px 14px rgba(0,0,0,0.2);
}

.leaflet-popup-content {
  margin: 0;
  padding: 0;
}

.popup-content {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  width: 250px;
}

.popup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #eee;
}

.popup-title {
  padding: 10px 10px 5px 10px;
  font-size: 16px;
}

.popup-description {
  padding: 0 10px 10px 10px;
  color: #666;
  font-size: 14px;
}

.popup-user, .popup-date {
  padding: 0 10px;
  font-size: 12px;
  color: #888;
}

.popup-date {
  padding-bottom: 10px;
}

.back-btn:hover, .refresh-btn:hover, .settings-btn:hover, .location-btn:hover {
  background-color: rgba(255,255,255,0.1);
}

.location-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.map-title {
  font-size: 18px;
  font-weight: 500;
  margin: 0;
}

.header-right {
  display: flex;
  gap: 8px;
}

.location-status {
  padding: 8px 16px;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  animation: slideDown 0.3s ease-out;
}

.location-status.info {
  background-color: #E3F2FD;
  color: #1976D2;
  border-left: 4px solid #2196F3;
}

.location-status.success {
  background-color: #E8F5E8;
  color: #2E7D32;
  border-left: 4px solid #4CAF50;
}

.location-status.error {
  background-color: #FFEBEE;
  color: #C62828;
  border-left: 4px solid #F44336;
}

.retry-btn {
  background: none;
  border: 1px solid currentColor;
  color: inherit;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.retry-btn:hover {
  background-color: rgba(0,0,0,0.1);
}

.stats-container {
  display: flex;
  padding: 16px;
  gap: 12px;
  background-color: white;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.stat-card {
  flex: 1;
  padding: 16px;
  border-radius: 12px;
  text-align: center;
  color: white;
  font-weight: 500;
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.stat-card.pollution {
  background: linear-gradient(135deg, #FF6B6B, #FF5252);
}

.stat-card.dechets {
  background: linear-gradient(135deg, #FFD93D, #FFC107);
  color: #333;
}

.stat-card.climat {
  background: linear-gradient(135deg, #6BCF7F, #4CAF50);
}

.stat-icon {
  margin-bottom: 8px;
  opacity: 0.8;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  opacity: 0.9;
}

.filters-container {
  display: flex;
  padding: 16px;
  gap: 16px;
  background-color: white;
  border-bottom: 1px solid #eee;
}

.filter-group {
  flex: 1;
}

.filter-group label {
  display: block;
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
  font-weight: 500;
}

.filter-select {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  background-color: white;
  color: #333;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.filter-select:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

.action-buttons {
  display: flex;
  padding: 16px;
  gap: 12px;
  background-color: white;
  border-bottom: 1px solid #eee;
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn.primary {
  background-color: #4CAF50;
  color: white;
}

.action-btn.primary:hover:not(:disabled) {
  background-color: #45a049;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.action-btn.primary:disabled {
  background-color: #ccc;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.action-btn.secondary {
  background-color: #f5f5f5;
  color: #666;
  border: 1px solid #ddd;
}

.action-btn.secondary:hover {
  background-color: #e0e0e0;
  transform: translateY(-1px);
}

.reset-icon {
  font-size: 16px;
  display: inline-block;
  transition: transform 0.3s;
}

.action-btn.secondary:hover .reset-icon {
  transform: rotate(180deg);
}

.loading-message {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background-color: white;
  color: #666;
  font-size: 14px;
  gap: 12px;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #e0e0e0;
  border-left-color: #4CAF50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.map {
  flex: 1;
  min-height: 400px;
  z-index: 0;
}

.filter-panel {
  position: absolute;
  top: 120px;
  right: 20px;
  width: 280px;
  background-color: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  z-index: 1000;
}

.filter-panel h3 {
  margin: 0 0 16px 0;
  font-size: 16px;
  color: #333;
  border-bottom: 2px solid #4CAF50;
  padding-bottom: 8px;
}

.filter-item {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  padding: 8px;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.filter-item:hover {
  background-color: #f5f5f5;
}

.filter-item input[type="checkbox"] {
  margin-right: 12px;
  width: 18px;
  height: 18px;
  accent-color: #4CAF50;
  cursor: pointer;
}

.filter-item label {
  flex: 1;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  margin: 0;
}

.map-icon-indicator {
  margin-left: auto;
  display: flex;
  align-items: center;
}

/* Styles pour les marqueurs personnalisés */
.user-location-marker {
  background: none !important;
  border: none !important;
}

.user-marker-svg {
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
  animation: pulse 2s infinite;
}

.signalement-marker {
  background: none !important;
  border: none !important;
}

.signalement-marker-container {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.3);
  border: 2px solid white;
  transition: transform 0.2s;
}

.signalement-marker-container:hover {
  transform: scale(1.2);
}

.signalement-marker-inner {
  width: 8px;
  height: 8px;
  background-color: white;
  border-radius: 50%;
}

/* Styles pour les popups */
.popup-content {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-width: 250px;
}

.popup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;
}

.popup-status {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 12px;
  font-weight: 500;
}

.status-en_attente {
  background-color: #FFF3E0;
  color: #F57C00;
}

.status-en_cours {
  background-color: #E3F2FD;
  color: #1976D2;
}

.status-traite {
  background-color: #E8F5E8;
  color: #388E3C;
}

.popup-title {
  margin-bottom: 8px;
  color: #333;
}

.popup-description {
  color: #666;
  font-size: 14px;
  margin-bottom: 8px;
  line-height: 1.4;
}

.popup-user {
  font-size: 12px;
  color: #888;
  margin-bottom: 4px;
}

.popup-date {
  font-size: 12px;
  color: #888;
}

.user-popup {
  text-align: center;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.user-popup strong {
  color: #2196F3;
}

.user-popup small {
  display: block;
  color: #666;
  margin-top: 4px;
}

/* Animations */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

@keyframes slideDown {
  0% {
    transform: translateY(-100%);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .stats-container {
    flex-direction: column;
    gap: 8px;
  }
  
  .stat-card {
    padding: 12px;
  }
  
  .stat-number {
    font-size: 20px;
  }
  
  .filters-container {
    flex-direction: column;
    gap: 12px;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 8px;
  }
  
  .filter-panel {
    display: none;
  }
  
  .map {
    min-height: 300px;
  }
}

@media (max-width: 480px) {
  .map-container {
    height: 100vh;
  }
  
  .stats-container {
    padding: 12px;
  }
  
  .filters-container {
    padding: 12px;
  }
  
  .action-buttons {
    padding: 12px;
  }
  
  .stat-number {
    font-size: 18px;
  }
  
  .stat-label {
    font-size: 11px;
  }
}
</style>