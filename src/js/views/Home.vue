<template>
  <div id="app">
    <AddWord v-on:add-word="addWord" />
    <Words v-bind:words="words" v-on:del-word="deleteWord" />
    <Compute v-bind:result="result" v-on:compute="compute" />
  </div>
</template>

<script>
import Words from '../components/Words';
import AddWord from '../components/AddWord';
import Compute from '../components/Compute';
import axios from 'axios';

export default {
  name: 'Home',
  components: {
    Words,
    AddWord,
    Compute
  },
  data() {
    return {
      words: [],
      result: 'Nothing'
    }
  },
  methods: {
    deleteWord(id) {
      // axios.delete(`https://my-json-server.typicode.com/macdre/moosingaround/words/${id}`)
      //   .then(res => this.words = this.words.filter(word => word.id !== id))
      //   .catch(err => console.log(err));
      this.words = this.words.filter(word => word.id !== id)
    },
    addWord(newWord) {
      const { content, operation } = newWord;

      // axios.post('https://my-json-server.typicode.com/macdre/moosingaround/words', {
      //   content,
      //   operation
      // })
      //   .then(res => this.words = [...this.words, res.data])
      //   .catch(err => console.log(err));
      this.words = [...this.words, newWord]
    },
    compute() {
    axios.post('https://moosingaroundapi.herokuapp.com/compute', this.words)
      .then(res => this.result = res.data)
      .catch(err => console.log(err));
    }
  },
  created() {
    axios.get('https://my-json-server.typicode.com/macdre/moosingaround/words?_limit=5')
      .then(res => this.words = res.data)
      .catch(err => console.log(err));

  }
}
</script>

<style>
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    font-family: Arial, Helvetica, sans-serif;
    line-height: 1.4;
  }

  .btn {
    display: inline-block;
    border: none;
    background: #555;
    color: #fff;
    padding: 7px 20px;
    cursor: pointer;
  }

  .btn:hover {
    background: #666;
  }
</style>
