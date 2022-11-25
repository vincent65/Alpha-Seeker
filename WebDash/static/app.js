var app = new Vue({
  el: "#app",
  data: {
    message: "Hello Trader!",
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
    },
    applyOnOffClass: function(val) {
        if (val === 0 || val === false){
            return "";
        }
        else{
            return 'alert_green';
        }
    },
    applyDirectionClass : function(val) {
        if(val === 0) {
            return "";
        }
        else if (val === 1){
            return 'alert_green';
        }
        else if (val == -1){
            return 'alert_red';
        }
    }
  }
});
