<template><v-alert v-if="message" :type="type" variant="tonal" class="mb-4" closable @click:close="$emit('clear')">{{ message }}</v-alert></template>
<script setup>defineProps({ message:String, type:{type:String,default:'error'} }); defineEmits(['clear'])</script>
