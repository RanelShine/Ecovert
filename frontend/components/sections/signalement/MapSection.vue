<template>
  <div class="map-container">
    <div id="map"></div>
    <div class="filter-container">
      <h3>Filtrer par type de signalement</h3>
      <div v-for="(type, index) in signalementTypes" :key="index" class="filter-item">
        <input type="checkbox" :id="type.name" v-model="type.active" @change="filterSignalements">
        <label :for="type.name">{{ type.name }}</label>
        <span class="color-indicator" :style="{ backgroundColor: type.color }"></span>
      </div>
    </div>
  </div>
</template>

<script>
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { onMounted, ref } from 'vue';
import { getFirestore, collection, getDocs } from 'firebase/firestore';

export default {
  name: 'MapSection',
  setup() {
    const map = ref(null);
    const userMarker = ref(null);
    const signalements = ref([]);
    const signalementMarkers = ref([]);
    const signalementTypes = ref([
      { name: 'Accident', color: '#FF0000', active: true },
      { name: 'Embouteillage', color: '#FFA500', active: true },
      { name: 'Route endommagée', color: '#8B4513', active: true },
      { name: 'Inondation', color: '#0000FF', active: true },
      { name: 'Autre', color: '#800080', active: true }
    ]);

    const initMap = () => {
      // Coordonnées du centre du Cameroun
      const cameroonCenter = [7.3697, 12.3547];

      map.value = L.map('map').setView(cameroonCenter, 7);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18
      }).addTo(map.value);

      // Limite de la vue à la zone du Cameroun (approximative)
      const cameroonBounds = L.latLngBounds(
        L.latLng(1.6546, 8.4948), // Sud-Ouest
        L.latLng(13.0856, 16.1921) // Nord-Est
      );
      map.value.setMaxBounds(cameroonBounds);

      // Obtenir la position de l'utilisateur
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const { latitude, longitude } = position.coords;
            const userPosition = [latitude, longitude];

            // Vérifier si la position est dans les limites du Cameroun
            if (cameroonBounds.contains(userPosition)) {
              // Créer un marqueur pour la position de l'utilisateur
              const userIcon = L.divIcon({
                className: 'user-location-icon',
                html: '<div style="background-color: blue; width: 12px; height: 12px; border-radius: 50%; border: 2px solid white;"></div>',
                iconSize: [16, 16],
                iconAnchor: [8, 8]
              });

              userMarker.value = L.marker(userPosition, { icon: userIcon }).addTo(map.value);
              userMarker.value.bindPopup('Votre position actuelle').openPopup();

              // Zoomer sur la position de l'utilisateur
              map.value.setView(userPosition, 12);
            }
          },
          (error) => {
            console.error('Erreur de géolocalisation:', error);
          }
        );
      }
    };

    const loadSignalements = async () => {
      try {
        const db = getFirestore();
        const signalementsCollection = collection(db, 'signalements');
        const signalementsSnapshot = await getDocs(signalementsCollection);

        signalements.value = signalementsSnapshot.docs.map(doc => {
          return { id: doc.id, ...doc.data() };
        });

        displaySignalements();
      } catch (error) {
        console.error('Erreur lors du chargement des signalements:', error);
      }
    };

    const displaySignalements = () => {
      // Supprimer les marqueurs existants
      if (signalementMarkers.value.length > 0) {
        signalementMarkers.value.forEach(marker => {
          map.value.removeLayer(marker);
        });
        signalementMarkers.value = [];
      }

      // Filtrer les signalements actifs
      const activeTypes = signalementTypes.value
        .filter(type => type.active)
        .map(type => type.name);

      // Ajouter les nouveaux marqueurs
      signalements.value.forEach(signalement => {
        if (activeTypes.includes(signalement.type) && signalement.latitude && signalement.longitude) {
          const typeInfo = signalementTypes.value.find(t => t.name === signalement.type);
          const color = typeInfo ? typeInfo.color : '#000000';

          const signalementIcon = L.divIcon({
            className: 'signalement-icon',
            html: `<div style="background-color: ${color}; width: 10px; height: 10px; border-radius: 50%; border: 2px solid white;"></div>`,
            iconSize: [14, 14],
            iconAnchor: [7, 7]
          });

          const marker = L.marker([signalement.latitude, signalement.longitude], { icon: signalementIcon }).addTo(map.value);
          marker.bindPopup(`
            <strong>${signalement.type}</strong><br>
            ${signalement.description || 'Aucune description'}<br>
            ${new Date(signalement.date.toDate()).toLocaleString()}
          `);

          signalementMarkers.value.push(marker);
        }
      });
    };

    const filterSignalements = () => {
      displaySignalements();
    };

    onMounted(() => {
      initMap();
      loadSignalements();
    });

    return {
      signalementTypes,
      filterSignalements
    };
  }
}
</script>

<style scoped>
.map-container {
  display: flex;
  height: 100%;
  position: relative;
}

#map {
  height: 600px;
  width: 80%;
}

.filter-container {
  width: 20%;
  padding: 15px;
  background-color: rgba(255, 255, 255, 0.9);
  border-left: 1px solid #ddd;
}

.filter-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.filter-item label {
  margin: 0 10px;
}

.color-indicator {
  width: 15px;
  height: 15px;
  border-radius: 50%;
  display: inline-block;
  margin-left: auto;
}

@media (max-width: 768px) {
  .map-container {
    flex-direction: column;
  }

  #map {
    width: 100%;
    height: 400px;
  }

  .filter-container {
    width: 100%;
  }
}
</style>