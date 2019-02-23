<template>
  <div>
    <div v-bind:key="word.id" v-for="word in words">
      <WordItem v-bind:word="word" v-on:del-word="$emit('del-word', word.id)" />
    </div>
  </div>
</template>

<script>
import WordItem from './WordItem.vue';

export default {
  name: "Words",
  components: {
    WordItem
  },
  props: ["words"]
}
</script>

<style scoped>

</style>

