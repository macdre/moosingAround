<template>
  <div class="word-item" v-bind:class="{'is-complete':word.operation}">
    <p>
      <!--<input type="checkbox" v-on:change="toggleOperation">-->
      <a v-on:click="toggleOperation"> 
        <!--<i :icon="[this.word.operation ? 'minus-square' : 'plus-square']" v-on:change="toggleOperation"/>-->
        <font-awesome-icon :icon="this.word.operation ? 'minus-square' : 'plus-square'" size="2x" />
      </a>    
      {{word.content}}
      <button @click="$emit('del-word', word.id)" class="del">x</button>
    </p>
  </div>
</template>

<script>
export default {
  name: "WordItem",
  props: ["word"],
  methods: {
    toggleOperation() {
      this.word.operation = !this.word.operation;
    }
  }
}
</script>

<style scoped>
  .word-item {
    background: #f4f4f4;
    padding: 10px;
    border-bottom: 1px #ccc dotted;
  }

  .is-complete {
    text-decoration: line-through;
  }

  .del {
    background: #ff0000;
    color: #fff;
    border: none;
    padding: 5px 9px;
    border-radius: 50%;
    cursor: pointer;
    float: right;
  }
</style>

