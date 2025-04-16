<template>
    <div id="app" class="container">
      <h2>Wheel Spin</h2>
      <div class="slot-machine">
        <div class="slot-container">
          <div
            v-for="(item, index) in elements"
            :key="item.id"
            class="slot-item"
            :style="{ backgroundColor: item.bgColor, color: item.color }"
            :class="{ active: index === activeIndex }"
          >
            {{ item.name }}
          </div>
        </div>
        <button @click="spin" :disabled="spinning">Spin</button>
      </div>
  
      <h2>Result</h2>
      <p v-if="selectedItem">Today's food : {{ selectedItem.name }}</p>
  
      <h2>Manage Elements</h2>
      <textarea v-model="elementInput" placeholder="Enter each element on a new line"></textarea>
      <button @click="updateElements">Update</button>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  
  interface SlotItem {
    id: number
    name: string
    bgColor: string
    color: string
  }
  
  // Generate random color function
  function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }
  
  // Calculate luminance of a color
  function getLuminance(hex: string) {
    const rgb = parseInt(hex.slice(1), 16); 
    const r = (rgb >> 16) & 0xff;
    const g = (rgb >>  8) & 0xff;
    const b = (rgb >>  0) & 0xff;
  
    const luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b;
    return luminance;
  }
  
  // Get contrasting color (black or white) based on background color luminance
  function getContrastingColor(bgColor: string) {
    const luminance = getLuminance(bgColor);
    return luminance > 128 ? '#000000' : '#FFFFFF';
  }
  
  // Change the initial value of elementInput to new default elements
  const elementInput = ref('Taco\nChinese Food\nPizza\nMaccas\nKFC\nBurger\nSushi\nPasta\nSalad')
  const elements = ref<SlotItem[]>([])
  const activeIndex = ref(-1)
  const spinning = ref(false)
  const selectedItem = ref<SlotItem | null>(null)
  
  function updateElements() {
    const lines = elementInput.value.split('\n').filter(line => line.trim() !== '');
    elements.value = lines.map((line, index) => {
      const bgColor = getRandomColor();
      const color = getContrastingColor(bgColor);
      return {
        id: index + 1,
        name: line,
        bgColor,
        color,
      };
    });
    selectedItem.value = null; // Reset selected item
  }
  
  function spin() {
    if (elements.value.length === 0) return;
    
    spinning.value = true;
    selectedItem.value = null; // Reset selected item
    let totalSpins = 20; // Total number of highlights
    let delay = 100; // Initial delay
  
    function highlightNext() {
      if (totalSpins > 0) {
        activeIndex.value = (activeIndex.value + 1) % elements.value.length;
        totalSpins--;
        setTimeout(highlightNext, delay);
      } else {
        spinning.value = false;
        selectedItem.value = elements.value[activeIndex.value]; // Set selected item
      }
    }
  
    highlightNext();
  }
  
  updateElements(); // Initialize elements list
  </script>
  
  <style scoped>
  .container {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    text-align: center;
  }
  
  .slot-machine {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .slot-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    width: 300px;
    border: 1px solid #ccc;
    margin-bottom: 10px;
  }
  
  .slot-item {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100px;
    height: 50px;
    margin: 5px;
    border-radius: 5px;
    transition: background-color 0.2s;
  }
  
  .slot-item.active {
    background-color: yellow !important;
    color: black !important;
  }
  
  textarea {
    width: 100%;
    height: 150px;
    margin-top: 10px;
    margin-bottom: 10px;
  }
  
  button {
    display: block;
    margin-top: 10px;
  }
  </style>
  