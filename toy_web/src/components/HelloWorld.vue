<template>
  <div>
    <input type="text" v-model="devicekey">
    <button @click="start">开机</button>
  </div>
</template>

<script>
  var ws = null;
export default {
  name: 'HelloWorld',
  data () {
    return {
      devicekey: ''
    }
  },
  methods:{
    createws:function(){
      // ws = new webSocket('ws/127.0.0.1:8000/ws/'++'/')
    },
    start:function(){
      if (this.devicekey == null){
        return
      }else{
        
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
