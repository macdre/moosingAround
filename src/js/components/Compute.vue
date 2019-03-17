<template>
  <div class='compute'>
    <form @submit="compute">
      <input type="submit" value="Compute" class="btn">
    </form>
    <div>
      Computed Result: {{result}}
    </div>
  </div>
</template>

<script>

export default {
  name: "Compute",
  props: ["result"],
  methods: {
    compute(e) {
      e.preventDefault();
      // Send up to parent
      this.$emit('compute');
    }
  }
}
</script>

<style scoped>
  form {
    display: flex;
  }

  input[type="submit"] {
    flex: 2;
  }

  .compute {
    background: #333;
    color: #fff;
    text-align: center;
    padding: 10px;
  }

  .compute a {
    color: #fff;
    padding-right: 5px;
    text-decoration: none;
  }
</style>
