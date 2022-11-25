var app = new Vue({
  el: "#app",
  data: {
    message: "Hello Vue!",
    kpiData: undefined
  },
  methods: {
    loadData : async function() {
        console.log("Load Data was clicked");
        const response = await fetch('data.json');
        const data = await response.json()
        console.log(response);
        console.log(data);
        this.kpiData = data;
    }
  }
});
