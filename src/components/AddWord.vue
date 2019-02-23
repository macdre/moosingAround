<template>
  <div>
    <form @submit="addWord">
      <input type="text" v-model="content" name="content" placeholder="Add Word...">
      <input type="submit" value="Submit" class="btn">
    </form>
  </div>
</template>

<script>

import uuid from 'uuid';

export default {
  name: "AddWord",
  data() {
    return {
      content: ''
    }
  },
  methods: {
    addWord(e) {
      e.preventDefault();
      const newWord = {
        id: uuid(),
        content: this.content,
        operation: false
      }
      // Send up to parent
      this.$emit('add-word', newWord);

      this.content = '';
    }
  }
}
</script>

<style scoped>
  form {
    display: flex;
  }

  input[type="text"] {
    flex: 10;
    padding: 5px;
  }

  input[type="submit"] {
    flex: 2;
  }
</style>
