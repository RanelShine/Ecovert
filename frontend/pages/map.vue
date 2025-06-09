<template>
  <div>
    <h2>Carte des photos</h2>
    <div id="map" style="height: 80vh; width: 100%"></div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
const loadMap = () => {
  return new Promise((resolve) => {
    if (window.google) return resolve(window.google)
    const script = document.createElement('script')
    script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyAazbj-8wVdE5oyRPcYd1BLk8B463YW-i8&callback=initMap'
    script.async = true
    window.initMap = resolve
    document.head.appendChild(script)
  })
}

onMounted(async () => {
  await loadMap()

  const map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 7.3697, lng: 12.3547 }, 
    zoom: 6,
  })

  const res = await fetch('http://localhost:8000/api/photos/locations/')
  const photos = await res.json()

  photos.forEach(photo => {
        const marker = new google.maps.Marker({
    position: { lat: photo.latitude, lng: photo.longitude },
    map,
    icon: {
        url: "http://maps.google.com/mapfiles/ms/icons/red-dot.png", // Icône rouge
    },
    label: {
        text: "ici",
        color: "red",
        fontWeight: "bold",
        fontSize: "14px"
    }
    })


    const infoWindow = new google.maps.InfoWindow({
      content: `
        <div style="max-width: 200px;">
          <p><strong>Date :</strong> ${photo.date_uploaded}</p>
          <img src="${photo.image_url}" alt="photo" style="width: 100%;" />
        </div>
      `
    })

    marker.addListener("click", () => {
        map.panTo(marker.getPosition())
        map.setZoom(10)
      infoWindow.open(map, marker)
    })
  })
})
</script>
