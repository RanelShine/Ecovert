<template>
    <section class="pt-30 md:pt-24 relative">
      <div
      class="w-full px-5 sm:px-8 md:px-12 lg:px-8 max-w-screen-lg lg:max-w-screen-xl mx-auto relative m-8 dark:from-gray-900 dark:to-body-color"
    >
      <!-- Notifications Toast -->
      <div
        v-if="toastMessage"
        :class="[
          'toast fixed top-4 right-4 px-6 py-3 rounded-lg shadow-lg text-white z-50',
          toastClass,
        ]"
        @click="closeToast"
      >
        <p>{{ toastMessage }}</p>
      </div>
  
      <!-- Contenu principal -->
      <div
        class="main-content flex flex-col md:flex-row justify-between gap-12  max-w-screen-xl mt-12 rounded-lg"
      >
        <!-- Section gauche -->
        <div class="left-section flex-1 max-w-lg text-gray-900 dark:text-white">
          <h3
            class="text-gray-800 pt-4 dark:text-white font-bold text-2xl md:text-3xl lg:text-4xl"
          >
            Contactez notre
            <span
              class="text-transparent bg-clip-text bg-gradient-to-br from-primary to-[#8cd66a]"
            >
              équipe d'experts
            </span>
            en comptabilité
          </h3>
          <p class="mb-6 mt-3">
            Collaborez avec notre équipe dévouée de spécialistes en comptabilité
            pour transformer votre vision financière en réalité.
          </p>
          <div
            class="image-section mt-4 bg-gray-100 dark:bg-gray-700 text-black p-1 rounded-md shadow-md text-center"
          >
            <div
              class="flex flex-col lg:flex-row items-center lg:items-start gap-4"
            >
              <div
                class="contact-info flex flex-wrap justify-around text-center gap-4 text-sm text-primary"
              >
                <div
                  class="flex text-black dark:text-white w-full sm:w-auto mb-0"
                >
                  <h2
                    class="flex items-center text-sm font-semibold mb-2 whitespace-nowrap overflow-visible"
                  >
                    <span class="mr-1 text-primary">
                      <Icon icon="line-md:phone-twotone" width="40" height="40" />
                    </span>
                    438-877-1890 / 514-577-5143
                  </h2>
                </div>
                <div class="flex text-black dark:text-white w-full sm:w-auto">
                  <h2 class="flex items-center text-sm mb-2 font-semibold me-3">
                    <span class="mr-1 text-primary">
                      <Icon icon="mi:email" width="40" height="40" />
                    </span>
                    joseph_kamta@yahoo.ca
                  </h2>
                </div>
                <div class="flex text-black dark:text-white w-full sm:w-auto">
                  <h2 class="text-sm font-semibold">
                    <span class="mr-1 text-primary">
                      <Icon icon="mi:location" width="40" height="40" />
                    </span>
                  </h2>
                  <div
                    class="text-left text-xs whitespace-nowrap overflow-visible"
                  >
                    <span class="font-semibold text-sm">RIVE SUD:</span> <br />341
                    RUE RENOIR, ST. CONSTANT <br />
                    <span class="font-semibold text-sm"> RIVE NORD: </span
                    ><br />355 RUE DES ALISMAS, LAVAL <br />
                    <span class="font-semibold text-sm"> MONTREAL:</span>
                    <br />824 BOUL DECARIE, ST LAURENT <br />
                    <span class="font-semibold text-sm"></span> <br />1240 Av
                    Dollard, Lasalle H8N 2P2 <br />
                  </div>
                </div>
              </div>
              <img
                src="/assets/team-member.png"
                alt="Team Member"
                class="w-37 max-h-37 h-auto rounded-lg mb-0 mx-auto"
              />
            </div>
            <p class="text-sm mb-2 dark:text-white">
              Souhaitez-vous rejoindre notre équipe talentueuse ?<br /><a
                href="/job-board"
                class="text-primary hover:underline"
                >Visitez notre tableau d'offres d'emplois</a
              >
            </p>
          </div>
        </div>
  
        <!-- Section formulaire -->
        <form
          class="contact-form flex-1 max-w-lg bg-gray-100 dark:bg-gray-700 p-6 rounded-md shadow-lg text-black mb-0"
          @submit.prevent="submitForm"
        >
          <div class="form-group flex flex-wrap gap-4 mb-4">
            <div class="flex-1">
              <label
                for="fullname"
                class="block text-sm text-gray-800 dark:text-gray-300 font-semibold mb-2"
                >Nom complet *</label
              >
              <input
                type="text"
                placeholder="Nom complet"
                v-model="form.fullname"
                required
                class="w-full p-3 border dark:bg-gray-800 dark:text-white rounded-md"
                :class="{ 'border-red-500': errors.fullname }"
                @input="handleInput('fullname')"
              />
              <label v-if="errors.fullname" class="text-red-500 text-sm mt-1">{{
                errors.fullname
              }}</label>
            </div>
            <div class="flex-1">
              <label
                for="email"
                class="block text-sm text-gray-800 dark:text-gray-300 font-semibold mb-2"
                >Adresse mail *</label
              >
              <input
                type="email"
                placeholder="Adresse mail"
                v-model="form.email"
                required
                class="w-full p-3 border border-gray-400 dark:bg-gray-800 dark:text-white rounded-md"
                :class="{ 'border-red-500': errors.email }"
                @input="handleInput('email')"
              />
              <label v-if="errors.email" class="text-red-500 text-sm mt-1">{{
                errors.email
              }}</label>
            </div>
          </div>
          <div class="form-group flex flex-wrap gap-4 mb-4">
            <div class="flex-1">
              <label
                for="phone"
                class="block text-sm text-gray-800 dark:text-gray-300 font-semibold mb-2"
                >Numéro de téléphone *</label
              >
              <input
                type="text"
                placeholder="Numéro de téléphone"
                v-model="form.phone"
                class="w-full p-3 border border-gray-400 dark:bg-gray-800 dark:text-white rounded-md"
                :class="{ 'border-red-500': errors.phone }"
                @input="handleInput('phone')"
              />
              <label v-if="errors.phone" class="text-red-500 text-sm mt-1">{{
                errors.phone
              }}</label>
            </div>
            <div class="flex-1">
              <label
                for="location"
                class="block text-sm text-gray-800 dark:text-gray-300 font-semibold mb-2"
                >Adresse *</label
              >
              <input
                type="text"
                placeholder="Adresse"
                v-model="form.location"
                class="w-full p-3 border border-gray-400 dark:bg-gray-800 dark:text-white rounded-md"
                :class="{ 'border-red-500': errors.location }"
                @input="handleInput('location')"
              />
              <label v-if="errors.location" class="text-red-500 text-sm mt-1">{{
                errors.location
              }}</label>
            </div>
          </div>
          <div class="form-group mb-4">
            <label
              for="expertise"
              class="block text-sm text-gray-800 dark:text-gray-300 font-semibold mb-2"
              >Quelle expertise vous intéresse ? *</label
            >
            <select
              id="expertise"
              v-model="form.expertise"
              required
              class="w-full p-3 border border-gray-400 dark:bg-gray-800 dark:text-white rounded-md"
              :class="{ 'border-red-500': errors.expertise }"
              @change="handleInput('expertise')"
            >
              <option value="">--Selectionner un service--</option>
              <option value="cabinet">CABINET D'AVOCAT</option>
              <option value="civil">DROIT CIVIL</option>
              <option value="affaires">DROIT DES AFFAIRES</option>
              <option value="penal">DROIT PENAL</option>
              <option value="Comptabilité">COMPTABILITE</option>
              <option value="impotS">IMPOTS</option>
              <option value="formation">FORMATIONS</option>
              <option value="cabinet d'avocat">CABINET D'AVOCAT</option>
            </select>
            <label v-if="errors.expertise" class="text-red-500 text-sm mt-1">{{
              errors.expertise
            }}</label>
          </div>
          <div class="form-group mb-8">
            <label
              for="message"
              class="block text-sm text-gray-800 dark:text-gray-300 font-semibold mb-4"
              >Parlez-nous de votre projet. *</label
            >
            <textarea
              id="message"
              v-model="form.message"
              required
              class="w-full p-3 border border-gray-400 dark:bg-gray-800 dark:text-white rounded-md"
              placeholder="Veuillez entrer une description de votre projet"
              :class="{ 'border-red-500': errors.message }"
              @input="handleInput('message')"
            ></textarea>
            <label v-if="errors.message" class="text-red-500 text-sm mt-1">{{
              errors.message
            }}</label>
          </div>
          <button
            type="submit"
            class="submit-button bg-primary text-white mb-0 w-full py-3 px-6 rounded-md hover:bg-secondary transition-all duration-300 font-semibold"
          >
            Envoyer
          </button>
        </form>
      </div>
    </div>
    </section>
  </template>
  
  <script lang="ts" setup>
  import { ref } from "vue";
  import { Icon } from "@iconify/vue";
  
  const form = ref({
    fullname: "",
    email: "",
    phone: "",
    location: "",
    expertise: "",
    message: "",
  });
  
  const errors = ref({
    fullname: "",
    email: "",
    phone: "",
    location: "",
    expertise: "",
    message: "",
  });
  
  const toastMessage = ref("");
  const toastClass = ref("");
  
  const showToast = (message: string, toastClassValue: string) => {
    toastMessage.value = message;
    toastClass.value = toastClassValue;
  
    setTimeout(() => {
      toastMessage.value = "";
      toastClass.value = "";
    }, 3000);
  };
  
  const validateField = (fieldName: string, value: string) => {
    let isValid = true;
  
    switch (fieldName) {
      case "fullname":
        errors.value.fullname =
          value.trim().length < 3
            ? "Le nom doit comporter au moins 3 caractères."
            : "";
        isValid = !errors.value.fullname;
        break;
      case "email":
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        errors.value.email = !emailRegex.test(value)
          ? "Adresse email invalide."
          : "";
        isValid = !errors.value.email;
        break;
      case "phone":
        errors.value.phone = !/^\d+$/.test(value)
          ? "Le numéro de téléphone doit contenir uniquement des chiffres."
          : "";
        isValid = !errors.value.phone;
        break;
      case "location":
        errors.value.location = !value.trim()
          ? "Veuillez spécifier votre localisation."
          : "";
        isValid = !errors.value.location;
        break;
      case "expertise":
        errors.value.expertise = !value
          ? "Veuillez sélectionner une expertise."
          : "";
        isValid = !errors.value.expertise;
        break;
      case "message":
        errors.value.message =
          value.trim().length < 10
            ? "La description doit comporter au moins 10 caractères."
            : "";
        isValid = !errors.value.message;
        break;
    }
  
    return isValid;
  };
  
  const handleInput = (fieldName: string) => {
    validateField(fieldName, (form.value as any)[fieldName]);
  };
  
  const submitForm = async () => {
    const fieldsToValidate = [
      "fullname",
      "email",
      "expertise",
      "phone",
      "location",
      "message",
    ];
  
    const isValid = fieldsToValidate.every((field) =>
      validateField(field, (form.value as any)[field])
    );
  
    if (!isValid) return;
  
    try {
      const response = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form.value),
      });
  
      if (!response.ok) throw new Error("Erreur lors de l'envoi du formulaire");
  
      showToast("Votre message a été envoyé avec succès !", "bg-green-500");
    } catch (error) {
      showToast(`Une erreur est survenue`, "bg-red-500");
    }
  };
  
  const closeToast = () => {
    toastMessage.value = "";
    toastClass.value = "";
  };
  </script>
  
  <style scoped></style>
  